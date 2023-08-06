"""There is a period between data being recorded longer than a user-specified number of seconds.
"""

from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Archival gap longer than threshold"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["Archival gap longer than threshold"],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
        }
    ],
    "signature": "univariate",
}


def _get_last_analyzed_point(df: pd.DataFrame, intervals: pd.Series):
    if len(intervals) == 0:
        return df.index[-1]

    if intervals.iloc[-1]["end_date"] < df.index[-1]:
        return df.index[-1]

    points_before_last_analysis = df.index[df.index <= intervals.iloc[-1]["start_date"]]
    return points_before_last_analysis[-1]


def _is_frame_long_enough(frame, df, delta):
    end_date = frame.end_date
    if frame.end_date is None:
        end_date = df.index[-1]

    return (
        end_date.replace(tzinfo=None) - frame.start_date.replace(tzinfo=None)
    ) >= timedelta(seconds=delta)


def _filter_stale_event_frames(all_frames, df, delta):
    filter_iterator = filter(lambda x: _is_frame_long_enough(x, df, delta), all_frames)
    return filter_iterator


def _get_intervals(active_points, df, event_type):
    interval_grp = (active_points != active_points.shift().bfill()).cumsum()
    active_points[active_points.isna()] = 0
    active_points = np.array(active_points, dtype=bool)
    intervals = (
        df.assign(interval_grp=interval_grp)[active_points]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = event_type
    return intervals


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_archival_gap_longer_than_threshold(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    delta = analysis_input.parameters["threshold"]
    active_points = pd.DataFrame(
        {"value": ((df.index.to_series().diff()).dt.total_seconds() > delta)}
    )
    active_points = active_points | active_points.shift(-1).bfill()

    intervals = _get_intervals(active_points, df, _CHECK_NAME)
    intervals = _handle_open_intervals(df, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = _filter_stale_event_frames(
        event_frames_from_dataframe(process_open_intervals(intervals)), df, delta
    )

    last_analyzed_point = _get_last_analyzed_point(df, intervals)

    return frames, last_analyzed_point


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> List[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _get_relevant_statistic(analysis_input, stat_name):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _is_valid_input(
    analysis_input: AnalysisInput, median_archival_step: float
) -> tuple[str, bool]:
    if median_archival_step is None:
        return "No median archival step", False
    if len(analysis_input.data) == 0:
        return "No data", False
    if "threshold" not in analysis_input.parameters:
        return "No threshold parameter provided", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    median_archival_step = _get_relevant_statistic(
        analysis_input, "Archival time median"
    )
    message, is_ok = _is_valid_input(analysis_input, median_archival_step)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_archival_gap_longer_than_threshold(
        analysis_input, open_event_frames
    )

    return AnalysisResult(
        event_frames=list(frames),
        last_analyzed_point=last_analyzed_point,
    )
