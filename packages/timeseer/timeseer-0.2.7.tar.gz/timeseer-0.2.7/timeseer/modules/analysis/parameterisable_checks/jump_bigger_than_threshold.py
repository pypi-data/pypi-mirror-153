"""Identification of a difference in consecutive measurements bigger than a given threshold.
"""


from datetime import datetime
import pandas as pd

from scipy.ndimage.interpolation import shift

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer import DataType
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)


META = {
    "checks": [
        {
            "name": "Jump up bigger than threshold",
            "kpi": "Validity",
            "event_frames": ["Jump up bigger than threshold"],
        },
        {
            "name": "Jump down bigger than threshold",
            "kpi": "Validity",
            "event_frames": ["Jump down bigger than threshold"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _get_relevant_jumps(values, threshold):
    down_jumps = [False] * len(values)
    up_jumps = [False] * len(values)

    up_jumps = values > threshold
    up_jumps = up_jumps | shift(up_jumps, -1, cval=False)

    down_jumps = values < -threshold
    down_jumps = down_jumps | shift(down_jumps, -1, cval=False)

    return up_jumps, down_jumps


def _handle_open_intervals(df, intervals):
    if len(intervals) == 0:
        return intervals
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _get_intervals(outliers, df, event_type):
    if outliers is None:
        return pd.DataFrame()
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


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_jump_check(
    analysis_input: AnalysisInput,
    open_event_frames: list[EventFrame],
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)
    threshold = analysis_input.parameters["threshold"]

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    value_diff = df["value"].diff()

    active_points_upwards, active_points_downwards = _get_relevant_jumps(
        value_diff, threshold
    )

    intervals_downwards = _get_intervals(
        active_points_downwards, df, "Jump down bigger than threshold"
    )
    intervals_downwards = _handle_open_intervals(df, intervals_downwards)
    intervals_downwards = merge_intervals_and_open_event_frames(
        analysis_start,
        intervals_downwards,
        list(
            filter(
                lambda x: x.type == "Jump down bigger than threshold", open_event_frames
            )
        ),
    )

    intervals_upwards = _get_intervals(
        active_points_upwards, df, "Jump up bigger than threshold"
    )
    intervals_upwards = _handle_open_intervals(df, intervals_upwards)
    intervals_upwards = merge_intervals_and_open_event_frames(
        analysis_start,
        intervals_upwards,
        list(
            filter(
                lambda x: x.type == "Jump up bigger than threshold", open_event_frames
            )
        ),
    )

    all_intervals = pd.concat([intervals_downwards, intervals_upwards])

    frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = df.index[-2]

    return list(frames), last_analyzed_point


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
        or event_frame.type in META["checks"][1]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
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


def _is_valid_input(analysis_input, median_archival_step: float) -> tuple[str, bool]:
    if median_archival_step is None:
        return "No median archival step", False
    if "threshold" not in analysis_input.parameters:
        return "No threshold parameter provided", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
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

    event_frames, last_analyzed_point = _run_jump_check(
        analysis_input,
        open_event_frames,
    )

    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=last_analyzed_point,
    )
