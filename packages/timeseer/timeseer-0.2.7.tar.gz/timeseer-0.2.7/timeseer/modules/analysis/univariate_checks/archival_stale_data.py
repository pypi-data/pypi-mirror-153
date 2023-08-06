"""There is no change in the data for a period longer than expected based on history.

<p> This check identifies periods time where the
exact same value has been consistently recorded for a sensor. These could be indications of issues with
connectivity or offline sensors.</p>
<p><img src='../static/images/reporting/stale_data.svg'></p>
<p class="scoring-explanation">The score for this check is based on the total amount of time
where there seems to be staleness relative to the total time range of the analysis.</p>
<div class="ts-check-impact">
<p>
A series that does not put out any new measurements might be faulty or could indicate a network failure.
Failing to detect this could lead to wrong process operation when attempting to obtain a particular
interval of operation.
</p>
</div>
"""

from datetime import datetime, timedelta

import jsonpickle
import numpy as np
import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Stale data (distribution)"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Timeliness",
            "event_frames": ["Stale data (distribution)"],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 3,
            "min_data_points": 2,
        }
    ],
    "signature": "univariate",
}


def _get_last_analyzed_point(df, intervals):
    if len(intervals) == 0:
        return df.index[-1]

    if intervals.iloc[-1]["end_date"] < df.index[-1]:
        return df.index[-1]

    points_before_last_analysis = df.index[df.index <= intervals.iloc[-1]["start_date"]]
    return points_before_last_analysis[-1]


def _get_cutoff_for_staleness(sketch):
    if sketch.count <= 30:
        return 0

    if sketch.max == sketch.min:
        return sketch.max

    q25, q75 = [sketch.get_quantile_value(q) for q in [0.25, 0.75]]
    iqr = q75 - q25
    return q75 + 1.5 * iqr


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


def _run_stale_data_check(
    analysis_input, median_archival_step, open_event_frames, stale_sketch
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    active_points = df["value"].eq(df["value"].shift().bfill()).astype(bool)

    intervals = _get_intervals(active_points, df, _CHECK_NAME)
    intervals = _handle_open_intervals(df, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    delta = max(_get_cutoff_for_staleness(stale_sketch), 2 * median_archival_step)

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
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
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
    json_stale_sketch = _get_relevant_statistic(analysis_input, "Stale Sketch")
    if median_archival_step is None:
        return AnalysisResult(condition_message="No median archival step")
    if json_stale_sketch is None:
        return AnalysisResult(condition_message="No archival sketch")
    stale_sketch = jsonpickle.decode(json_stale_sketch)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_stale_data_check(
        analysis_input, median_archival_step, open_event_frames, stale_sketch
    )

    return AnalysisResult(
        event_frames=list(frames), last_analyzed_point=last_analyzed_point
    )
