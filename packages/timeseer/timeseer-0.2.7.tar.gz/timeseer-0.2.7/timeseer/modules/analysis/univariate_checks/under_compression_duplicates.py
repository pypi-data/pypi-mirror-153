"""There should be no consecutively recorded repeated values close to each other.

<p>This is a simple check for undercompression. If there are repeated
consecutive values recorded closer together than the maximum allowed time frame
by the compression settings, this could indicate that the exception setting is too strict.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Undercompression can lead to too high storage requirements.
</p>
</div>
"""

from datetime import datetime
from typing import List

import jsonpickle
import numpy as np
import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "No repeated values"
_EVENT_FRAME_NAME = "Repeated values"


META: dict = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Consistency",
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.DICTIONARY,
                DataType.CATEGORICAL,
            ],
        }
    ],
    "signature": "univariate",
}


def _get_active_points(df, cut_off):
    short_intervals = (df.index.to_series().diff()).dt.total_seconds() < cut_off
    same_value = df["value"].diff() == 0
    return short_intervals & same_value


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


def _are_consecutive_duplicates_present(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame], stale_sketch
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    cut_off = stale_sketch.get_quantile_value(0.1)

    active_points = _get_active_points(df, cut_off)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = _handle_open_intervals(df, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df.index[-1]

    return list(frames), last_analyzed_point


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


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    median_archival_step = _get_relevant_statistic(
        analysis_input, "Archival time median"
    )
    json_stale_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")
    if median_archival_step is None:
        return AnalysisResult(condition_message="No median archival step")
    if json_stale_sketch is None:
        return AnalysisResult(condition_message="No archival sketch")
    stale_sketch = jsonpickle.decode(json_stale_sketch)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _are_consecutive_duplicates_present(
        analysis_input, open_event_frames, stale_sketch
    )

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
