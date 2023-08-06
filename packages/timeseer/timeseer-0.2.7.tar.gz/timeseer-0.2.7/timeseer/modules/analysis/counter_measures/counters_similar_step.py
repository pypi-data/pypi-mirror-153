"""Counters are often expected to increase with a similar step.

<p>
This check identifies when a counter step differs significantly from the mode.
</p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
time where there is an abnormal step.
</p>
<div class="ts-check-impact">
<p>
Could impact downstream dashboards, reports or automated analytics.
</p>
</div>
"""

from datetime import datetime
import pandas as pd
import numpy as np

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Counter step stability"
_EVENT_FRAME_NAME = "Counter step abnormal"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
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


def _get_active_points(df: pd.DataFrame):
    values = df["value"].diff()
    median = np.nanquantile(values, 0.5)
    return (values > 1.1 * median) | (values < 0.9 * median)


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _run_similar_step(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    active_points = _get_active_points(df)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = _handle_open_intervals(df, intervals)

    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df.index[-1]

    return list(frames), last_analyzed_point


def _is_valid_input(
    analysis_input: AnalysisInput, median_archival_step: list[float]
) -> tuple[str, bool]:
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival step", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


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

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_similar_step(analysis_input, open_event_frames)
    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
