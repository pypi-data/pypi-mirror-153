"""
Saturation
"""

from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Saturation"
_EVENT_FRAME_NAME = "Saturation"


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
        return "No median archival step", False
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


def _get_saturation_cutoff(df: pd.DataFrame, cutoff_ratio=0.99):
    if df.max().value > 100:
        return cutoff_ratio * df.max().value
    if df.max().value <= 1:
        return cutoff_ratio
    return 100 * cutoff_ratio


def _get_active_points(df: pd.DataFrame):
    cutoff = _get_saturation_cutoff(df)
    return df["value"] > cutoff


def _get_intervals(outliers, df, event_type):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _merge_close_intervals(intervals, max_gap_minutes=10):
    if len(intervals) == 0:
        return intervals
    max_gap_merge = timedelta(minutes=max_gap_minutes)
    start_datetimes = intervals["start_date"].values
    end_datetimes = intervals["end_date"].values
    gap = np.delete(start_datetimes, 0) - np.delete(end_datetimes, -1)
    gap = np.insert(gap, 0, max_gap_merge)
    ext_intervals = intervals.copy()
    ext_intervals["gap"] = gap
    ext_intervals.reset_index(inplace=True)

    mergers = ext_intervals.index[ext_intervals["gap"] < max_gap_merge]

    for i in mergers:
        if i == 0:
            continue
        ext_intervals.loc[i, "start_date"] = ext_intervals.loc[i - 1, "start_date"]
        ext_intervals = ext_intervals.drop(i - 1)

    return ext_intervals.drop(columns=["gap"])


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _run_saturation(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    active_points = _get_active_points(df)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = _merge_close_intervals(intervals)
    intervals = _handle_open_intervals(df, intervals)

    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df.index[-1]

    return list(frames), last_analyzed_point


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

    frames, last_analyzed_point = _run_saturation(analysis_input, open_event_frames)
    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
