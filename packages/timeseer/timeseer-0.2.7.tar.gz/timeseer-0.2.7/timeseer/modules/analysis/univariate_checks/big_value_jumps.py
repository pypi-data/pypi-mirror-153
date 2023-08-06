"""Identification of big jumps in consecutive values.

<p>This check identifies how many times over the time-frame of the analysis a sudden spike occurs.
A sudden spike is defined as an outlier wrt historical differences in consecutive values.</p>
<p><img src='../static/images/reporting/big_jumps.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where a positive or negative jump occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 2 positive and 1 negative jumps. The score for this check in that case would be
97% = 1 - 3 / 100. Which means that for 90% of all points no jump is present.</p>
<div class="ts-check-impact">
<p>
Big sudden jumps in data often correspond to faults in the data captation chain.
Several calculations are sensitive to these type of sudden changes and process decision chains
based on such an outlier can propagate through the system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""


from datetime import datetime
import jsonpickle
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
            "name": "Jumps (upwards)",
            "kpi": "Validity",
            "event_frames": ["Jump outlier (upwards)"],
        },
        {
            "name": "Jumps (downwards)",
            "kpi": "Validity",
            "event_frames": ["Jump outlier (downwards)"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _get_quantiles(sketch):
    if sketch.max == sketch.min:
        return sketch.max, sketch.max, 0

    q25, q75 = [sketch.get_quantile_value(q) for q in [0.25, 0.75]]
    iqr = q75 - q25
    return q25, q75, iqr


def _get_relevant_jumps(values, jump_up_sketch, jump_down_sketch, strictness):
    ups = values[values > 0]
    down = values[values < 0]

    down_jumps = [False] * len(values)
    up_jumps = [False] * len(values)

    if len(ups) >= 30:
        _, up_q3, up_iqr = _get_quantiles(jump_up_sketch)
        up_jumps = values > (up_q3 + strictness * up_iqr)
        up_jumps = up_jumps | shift(up_jumps, -1, cval=False)

    if len(down) >= 30:
        down_q1, _, down_iqr = _get_quantiles(jump_down_sketch)
        down_jumps = values < (down_q1 - strictness * down_iqr)
        down_jumps = down_jumps | shift(down_jumps, -1, cval=False)

    if len(ups) < 30 and len(down) < 30:
        return None, None

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
    jump_up_sketch,
    jump_down_sketch,
    open_event_frames: list[EventFrame],
    strictness=3,
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    value_diff = df["value"].diff()

    active_points_upwards, active_points_downwards = _get_relevant_jumps(
        value_diff, jump_up_sketch, jump_down_sketch, strictness
    )

    intervals_downwards = _get_intervals(
        active_points_downwards, df, "Jump outlier (downwards)"
    )
    intervals_downwards = _handle_open_intervals(df, intervals_downwards)
    intervals_downwards = merge_intervals_and_open_event_frames(
        analysis_start,
        intervals_downwards,
        list(filter(lambda x: x.type == "Jump outlier (downwards)", open_event_frames)),
    )

    intervals_upwards = _get_intervals(
        active_points_upwards, df, "Jump outlier (upwards)"
    )
    intervals_upwards = _handle_open_intervals(df, intervals_upwards)
    intervals_upwards = merge_intervals_and_open_event_frames(
        analysis_start,
        intervals_upwards,
        list(filter(lambda x: x.type == "Jump outlier (upwards)", open_event_frames)),
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


def _is_valid_input(analysis_input) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    median_archival_step = _get_relevant_statistic(
        analysis_input, "Archival time median"
    )
    json_jump_up_sketch = _get_relevant_statistic(analysis_input, "Jump Up Sketch")
    json_jump_down_sketch = _get_relevant_statistic(analysis_input, "Jump Down Sketch")

    if median_archival_step is None:
        return AnalysisResult(condition_message="No median archival step")
    if json_jump_up_sketch is None:
        return AnalysisResult(condition_message="No jump up sketch")
    if json_jump_down_sketch is None:
        return AnalysisResult(condition_message="No jump down sketch")

    jump_up_sketch = jsonpickle.decode(json_jump_up_sketch)
    jump_down_sketch = jsonpickle.decode(json_jump_down_sketch)

    open_event_frames = _get_open_event_frames(analysis_input)

    event_frames, last_analyzed_point = _run_jump_check(
        analysis_input,
        jump_up_sketch,
        jump_down_sketch,
        open_event_frames,
    )

    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=last_analyzed_point,
    )
