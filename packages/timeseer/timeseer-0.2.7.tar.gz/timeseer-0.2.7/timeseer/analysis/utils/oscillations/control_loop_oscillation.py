"""
Find oscillation eventframes for use in Control loop checks
"""

import logging

from datetime import datetime

import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype
from scipy import signal, stats
from scipy.signal import butter

from timeseer import AnalysisInput, AnalysisResult, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)
from timeseer.metadata import fields


_CHECK_NAME = "Control Loop Oscillation"
_EVENT_FRAME_NAME = "Control Loop Oscillation"

logger = logging.getLogger(__name__)


def _close_open_event_frames(open_event_frames, analysis_start):
    for item in open_event_frames:
        item.end_date = analysis_start
    return open_event_frames


def _get_last_analyzed_point(df, window_size):
    if len(df) < window_size:
        return df.index[0]
    return df.index[-window_size]


def _get_intervals(df, anomalies):
    anomalies = pd.Series(data=anomalies, index=df.index).fillna(False)
    anomaly_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(anomaly_grp=anomaly_grp)[anomalies]
        .reset_index()
        .groupby(["anomaly_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _CHECK_NAME
    return intervals


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _compute_bandpass_filter(lowcut=1 / 512, highcut=100 / 1024, order=5):
    sos = butter(order, [2 * lowcut, 2 * highcut], btype="band", output="sos")
    w_filter, filter_gain = signal.sosfreqz(sos, worN=20000)
    filter_frequencies = (0.5 / np.pi) * w_filter
    return sos, filter_frequencies, filter_gain


def _compute_non_distorted_frequencies(filter_frequencies, filter_gain):
    non_dist_frequency = filter_frequencies[abs(filter_gain) > 0.99]
    return min(non_dist_frequency), max(non_dist_frequency)


def _compute_median_absolute_deviations(amplitudes):
    my_median = np.median(amplitudes, axis=0)
    mad = stats.median_abs_deviation(amplitudes, axis=0)
    return np.divide(
        abs(amplitudes - my_median),
        mad,
        out=np.zeros_like(abs(amplitudes - my_median)),
        where=mad != 0,
    )


# pylint: disable=too-many-locals
def _compute_window_median_absolute_deviations(resampled, w_size):
    f, _, z_xx = signal.stft(
        resampled,
        fs=1,
        window="hann",
        nperseg=w_size,
        boundary=None,
        detrend="constant",
    )
    amplitudes = np.array(np.abs(z_xx), dtype=float)
    _, filter_frequencies, filter_gain = _compute_bandpass_filter()
    min_non_dist_frequency, max_non_dist_frequency = _compute_non_distorted_frequencies(
        filter_frequencies, filter_gain
    )
    non_dist_frequency_index = (f > min_non_dist_frequency) & (
        f < max_non_dist_frequency
    )
    non_dist_amplitudes = amplitudes[non_dist_frequency_index, :]

    sum_non_dist = np.sum(non_dist_amplitudes, axis=0)
    sum_amplitudes = np.sum(amplitudes, axis=0)
    bandpass_energy_ratio = np.divide(
        sum_non_dist,
        sum_amplitudes,
        out=np.zeros_like(sum_non_dist),
        where=sum_amplitudes != 0,
    )
    window_median_absolute_deviations = _compute_median_absolute_deviations(
        non_dist_amplitudes
    )
    return window_median_absolute_deviations, bandpass_energy_ratio


def _run_oscillation_check(
    analysis_input: AnalysisInput,
    mas: float,
    open_event_frames: list[EventFrame],
    strictness=10,  # Strictness on MAD
) -> tuple[list[EventFrame], datetime]:  # pylint: disable=too-many-locals
    # Set params for window size
    w_size = 1024
    overlap_size = 512
    # Clean up the data
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    # Resample at median archival rate
    old_index = df.index
    frequency = max(1, round(mas))
    new_index = pd.date_range(
        old_index.min(), old_index.max(), freq=str(frequency) + "S"
    )
    resampled = (
        df.reindex(old_index.union(new_index)).interpolate("linear").reindex(new_index)
    )
    resampled.index = resampled.index.set_names("ts")
    if len(resampled) < w_size:
        closed_event_frames = _close_open_event_frames(
            open_event_frames, analysis_start
        )
        return closed_event_frames, analysis_start

    resampled = resampled.iloc[0 : (len(resampled) // w_size) * w_size]
    (
        window_median_absolute_deviations,
        banpass_energy_ratio,
    ) = _compute_window_median_absolute_deviations(
        resampled.values.flatten(), w_size=w_size
    )
    window_median_absolute_deviations_max = np.max(
        window_median_absolute_deviations, axis=0
    )  # Maximum median absolute deviation per window, in MAD units. Probably redundant.
    window_anomalies = (window_median_absolute_deviations_max > strictness) & (
        banpass_energy_ratio > 0.5
    )  # Thresholds on MAD and energy ratio.

    # Transform anomalies in windows to anomalies in resampled
    idx = [
        [np.arange(index * overlap_size, index * overlap_size + w_size)]
        for index, window in enumerate(window_anomalies)
        if window
    ]

    if len(idx) == 0:
        closed_event_frames = _close_open_event_frames(
            open_event_frames, analysis_start
        )
        return closed_event_frames, _get_last_analyzed_point(resampled, w_size)

    anomalies = np.array([False] * len(resampled))
    anomalies[np.array(idx).flatten()] = True
    intervals = _get_intervals(resampled, anomalies)
    intervals = _handle_open_intervals(resampled, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = _get_last_analyzed_point(resampled, w_size)

    return list(frames), last_analyzed_point


def _get_interpolation_type(analysis_input: AnalysisInput) -> str:
    interpolation_type = analysis_input.metadata.get_field(fields.InterpolationType)
    if interpolation_type is not None and interpolation_type == "STEPPED":
        return "pad"
    return "linear"


def _is_relevant_open_event_frame(event_frame):
    return event_frame.end_date is None and event_frame.type == _EVENT_FRAME_NAME


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


# pylint: disable=missing-function-docstring,unreachable
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    if median_archival_step is None or len(median_archival_step) == 0:
        return AnalysisResult(condition_message="No median archival step")

    interpolation_type = _get_interpolation_type(analysis_input)
    if interpolation_type == "pad":
        return AnalysisResult(condition_message="Interpolation type can not be pad")

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_oscillation_check(
        analysis_input, float(median_archival_step[0]), open_event_frames
    )

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
