"""Anomaly based on level shift.

<p>Anomaly detection based on a significant difference in the means of
two consecutive sliding windows.</p>
<p><img src='../static/images/reporting/level_shift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where a level shift anomaly occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 10 level shift anomalies. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no level shift anomaly occurs.</p>
<div class="ts-check-impact">
<p>
Level shifts could be indications of physical altercations to a sensor (e.g. camera being bumped) or
other types of issues within the sensor.
Several calculations are sensitive to these type of sudden changes and process decision chains
based on such an outlier can propagate through the system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

from datetime import datetime
import logging

import numpy as np
import pandas as pd

from adtk.detector import LevelShiftAD
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


_CHECK_NAME = "Level Shift Anomaly"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "event_frames": ["Level Shift Anomaly"],
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


def _get_last_analyzed_point(df, window_size):
    if len(df) < window_size:
        return df.index[0]
    last_index = -2 * window_size
    return df.index[last_index]


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_level_shift_ad(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    window_size = 10
    if len(df["value"]) <= window_size:
        return [], df.index[0]

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    level_ad = LevelShiftAD(window=10)
    try:
        active_points = level_ad.fit_detect(df["value"])
    except (ValueError, RuntimeError) as err:
        logger.error("Error in level shift anomaly: %s", err)
        return [], _get_last_analyzed_point(df, window_size)

    intervals = _get_intervals(active_points, df, _CHECK_NAME)
    intervals = _handle_open_intervals(df, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = _get_last_analyzed_point(df, window_size)

    return list(frames), last_analyzed_point


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


def _get_relevant_statistic(analysis_input: AnalysisInput, requested_statistic: str):
    stat = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == requested_statistic
    ]
    if len(stat) == 0:
        return None
    return stat


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    median_archival_step = _get_relevant_statistic(
        analysis_input, "Archival time median"
    )
    if median_archival_step is None:
        return AnalysisResult(condition_message="No median archival step")

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_level_shift_ad(analysis_input, open_event_frames)

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
