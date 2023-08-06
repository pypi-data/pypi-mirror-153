"""
Stiction
"""

from datetime import datetime
import pandas as pd
import numpy as np

from scipy.signal import find_peaks
from scipy.optimize import curve_fit

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    merge_intervals_and_open_event_frames,
)

from timeseer.analysis.utils.oscillations import control_loop_oscillation

_CHECK_NAME = "Stiction"
_EVENT_FRAME_NAME = "Stiction"


META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
            "data_type": [
                DataType.FLOAT64,
                DataType.FLOAT32,
            ],
        }
    ],
    "signature": "univariate",
}


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _is_valid_input(
    analysis_input: AnalysisInput, median_archival_step: list[float]
) -> tuple[str, bool]:
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


def _is_correct_series(analysis_input: AnalysisInput) -> tuple[str, bool]:
    position = analysis_input.metadata.get_field_by_name("control loop")
    if position == "OP":
        return "OK", True
    return "Only applicable to OP", False


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _peaks_finder(df):
    peaks, _ = find_peaks(df["value"], height=0)
    peak_ts = df.index[peaks]
    peaks_df = pd.DataFrame(data={"start": peak_ts[:-1], "end": peak_ts[1:]})
    peaks_df["length"] = peaks_df["end"] - peaks_df["start"]
    peaks_df["seconds"] = [
        length.total_seconds() for length in list(peaks_df["length"])
    ]
    return peaks_df


def _get_segments(df, peaks_df):
    segments = []
    for _, row in peaks_df.iterrows():
        ptop = df.loc[row["start"] : row["end"]]
        segments.append(ptop)
    return segments


def _sine_shape(X, amplitude, phase, intercept, angular_frq):
    y = (amplitude * np.sin(angular_frq * X + phase)) + intercept
    return np.array(y)


def _tri_shape(X, tri_edge_x, tri_edge_y, slope_1, slope_2):
    y = []
    for point in X:
        if point < tri_edge_x:
            height = slope_1 * point + tri_edge_y - slope_1 * tri_edge_x
        if point >= tri_edge_x:
            height = slope_2 * point + tri_edge_y - slope_2 * tri_edge_x
        y.append(height)
    return np.array(y)


# pylint: disable=unbalanced-tuple-unpacking
def _check_stiction(curve):
    start_time = curve.index[0].timestamp()
    if len(curve) < 5:
        return float("nan")
    X = curve.index.to_series().apply(lambda X: X.timestamp() - start_time)
    w_segment = 2 * np.pi / (X[-1])
    try:
        sin_p, _ = curve_fit(
            _sine_shape,
            X.values,
            curve["value"],
            bounds=(
                [0, 2 * np.pi / 5, -np.Inf, 0.95 * w_segment],
                [np.Inf, 3 * np.pi / 5, np.Inf, 1.05 * w_segment],
            ),
        )
    except RuntimeError:
        return float("nan")
    mse_sin = np.sum((curve["value"] - _sine_shape(X.values, *sin_p)) ** 2)
    try:
        tri_p, _ = curve_fit(
            _tri_shape,
            X.values,
            curve["value"],
            bounds=([0, -np.Inf, -np.Inf, 0], [X[-1], np.min(curve.values), 0, np.Inf]),
        )
    except RuntimeError:
        return float("nan")
    mse_tri = np.sum((curve["value"] - _tri_shape(X.values, *tri_p)) ** 2)
    p_stiction = mse_sin / (mse_sin + mse_tri)
    return p_stiction


def _get_oscillation_eventframes(analysis_input):
    oscillation_results = control_loop_oscillation.run(analysis_input)
    frames = oscillation_results.event_frames
    return frames


def _eventframes_to_intervals(df, event_frames):
    starts = [frame.start_date for frame in event_frames]
    ends = [frame.end_date for frame in event_frames]
    names = [frame.type for frame in event_frames]
    intervals = pd.DataFrame(
        data={"type": names, "start_date": starts, "end_date": ends}
    )
    if len(intervals) > 0:
        if intervals.iloc[-1, -1] is None:
            intervals.iloc[-1, -1] = df.index[-1]
    if len(intervals) > 0:
        if intervals.iloc[-1, -1] is pd.NaT:
            intervals.iloc[-1, -1] = df.index[-1]
    return intervals


# pylint: disable=too-many-locals
def _run_stiction(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    oscillation_eventframes = _get_oscillation_eventframes(analysis_input)
    df = analysis_input.data
    df = _clean_dataframe(df)
    last_analyzed_point = df.index[-1]
    if len(oscillation_eventframes) == 0:
        return [], last_analyzed_point
    intervals = _eventframes_to_intervals(df, oscillation_eventframes)

    result_frames = []

    for index, row in intervals.iterrows():
        signal = df.loc[row["start_date"] : row["end_date"]]
        peaks_df = _peaks_finder(signal)
        if len(peaks_df) < 3:
            continue
        segments = _get_segments(signal, peaks_df)
        stiction_probs = [_check_stiction(segment) for segment in segments]
        if np.all(np.isnan(stiction_probs)):
            continue
        if np.nanmean(stiction_probs) >= 0.6:
            frame = oscillation_eventframes[index]
            frame.type = _EVENT_FRAME_NAME
            result_frames.append(frame)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    result_intervals = _eventframes_to_intervals(df, result_frames)

    result_intervals = _handle_open_intervals(df, result_intervals)
    result_intervals = merge_intervals_and_open_event_frames(
        analysis_start, result_intervals, open_event_frames
    )

    return result_frames, last_analyzed_point


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    message, is_ok = _is_valid_input(analysis_input, median_archival_step)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    message, is_ok = _is_correct_series(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_stiction(analysis_input, open_event_frames)

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
