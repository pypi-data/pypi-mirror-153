"""Anomaly based on persist.

<p>Anomaly detection based on a significant difference in a value compared to a
previous window.</p>
<p><img src='../static/images/reporting/persist.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where a persist anomaly occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 10 persist anomalies. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no persist anomaly occurs.</p>
<div class="ts-check-impact">
<p>
Outliers in series can cloud downstream analytics and put the burden of removing these without
background knowledge on the algorithms instead of those in the know.
Several calculations are sensitive to these type of sudden changes and process decision chains
based on such an outlier can propagate through the system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

import logging

from datetime import datetime
from typing import List

import pandas as pd
import numpy as np

from adtk.detector import PersistAD
from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    InterpolationType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Persist Anomaly"

META: dict = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "event_frames": ["Persist Anomaly"],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
            "interpolation_type": [None, InterpolationType.LINEAR],
        }
    ],
    "signature": "univariate",
}

logger = logging.getLogger(__name__)


def _get_intervals(active_points, df: pd.DataFrame, event_type: str):
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


def _get_last_analyzed_point(df: pd.DataFrame, window_size: int) -> datetime:
    if len(df) < window_size:
        return df.index[0]
    last_index = -2 * window_size
    return df.index[last_index]


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _handle_open_intervals(df: pd.DataFrame, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _run_persist_ad(
    analysis_input: AnalysisInput,
    open_event_frames: List[EventFrame],
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)
    window_size = 10
    if len(df["value"]) <= window_size:
        return [], df.index[0]

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    persist_ad = PersistAD(window=10)
    try:
        active_points = persist_ad.fit_detect(df["value"])
    except (ValueError, RuntimeError) as err:
        logger.error("Error in persist anomaly: %s", err)
        return [], df.index[0]

    intervals = _get_intervals(active_points, df, "Persist Anomaly")
    intervals = _handle_open_intervals(df, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = _get_last_analyzed_point(df, window_size)

    return list(frames), last_analyzed_point


def _is_relevant_open_event_frame(event_frame: EventFrame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(analysis_input: AnalysisInput) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
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

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_persist_ad(analysis_input, open_event_frames)

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
