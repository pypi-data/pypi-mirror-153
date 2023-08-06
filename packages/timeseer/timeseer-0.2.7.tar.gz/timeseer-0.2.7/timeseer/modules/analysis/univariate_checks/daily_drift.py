"""Identify tags that drift continuously on daily average for at least a month.

<p>A common indication of sensor issues is sensor drift. This is where a measurement of
a sensor starts to slowly deviate from the real measurement. This can be identified in
reduntant sensor cases where for instance the difference between two identical sensors slowly
increases over time. A drift in a measurement can also have process causes
(e.g. fouling, catalyst degradation)</p>
<p><img src='../static/images/reporting/daily_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing positive and negative slopes. E.g. assume a total period being analyzed of 1 year and
2 event-frames, one negative and one positive, of 1 month and 2 months respectively.
The score of this check will then be 75% = 1 - 3 / 12. Which means that in 75% of time no drift is detected.</p>
<div class="ts-check-impact">
<p>
Sensor drift can lead to increased costs and variability in the process.
Typically drift is detected manually after a long period of time, which can cause slow deterioration
of product quality.
The longer drift goes unnoticed, the higher the cost and often also the higher the consequences.
Early drift detection can turn a maintenance action into a cleaning action.
Any type of anomaly detection based on normal behavior of the phyiscal ensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pymannkendall as mk

from pandas.api.types import is_string_dtype

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Daily drift"


META = {
    "checks": [
        {
            "name": "Daily drift (upwards)",
            "kpi": "Validity",
            "event_frames": ["Positive slopes"],
        },
        {
            "name": "Daily drift (downwards)",
            "kpi": "Validity",
            "event_frames": ["Negative slopes"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 4,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _merge_frames(frames: pd.DataFrame) -> pd.DataFrame:
    if len(frames) == 0:
        return frames

    merged_frame = pd.DataFrame(
        {
            "start_date": pd.Series(dtype="datetime64[ns, UTC]"),
            "end_date": pd.Series(dtype="datetime64[ns, UTC]"),
            "type": [],
            "open": [],
        }
    )

    frames = frames.sort_values(by=["start_date"])

    current_start = frames.iloc[0]["start_date"]
    current_end = frames.iloc[0]["end_date"]
    current_type = frames.iloc[0]["type"]
    current_open = frames.iloc[0]["open"]
    for index, row in frames.reset_index(drop=True).iterrows():
        if current_end < row["start_date"]:
            merged_frame = pd.concat(
                [
                    merged_frame,
                    pd.DataFrame(
                        {
                            "start_date": [current_start],
                            "end_date": [current_end],
                            "type": [current_type],
                            "open": [current_open],
                        }
                    ),
                ]
            )
            current_start = row["start_date"]
        if index == len(frames) - 1:
            if current_end < row["start_date"]:
                merged_frame = pd.concat(
                    [
                        merged_frame,
                        pd.DataFrame(
                            {
                                "start_date": [row["start_date"]],
                                "end_date": [row["end_date"]],
                                "type": [row["type"]],
                                "open": [row["open"]],
                            }
                        ),
                    ]
                )
            else:
                merged_frame = pd.concat(
                    [
                        merged_frame,
                        pd.DataFrame(
                            {
                                "start_date": [current_start],
                                "end_date": [row["end_date"]],
                                "type": [current_type],
                                "open": row["open"],
                            }
                        ),
                    ]
                )

        current_end = row["end_date"]
        current_type = row["type"]
        current_open = row["open"]
    merged_frame["open"] = merged_frame["open"].astype("bool")
    return merged_frame


def _get_intervals(df, anomalies, interval_type):
    anomaly_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(anomaly_grp=anomaly_grp)[anomalies]
        .reset_index()
        .groupby(["anomaly_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = interval_type
    intervals["start_date"] = intervals["start_date"] - timedelta(days=27)
    return intervals


def _get_global_outliers(df):
    q25, q75 = np.quantile(df, [0.25, 0.75])
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return lower, upper


def _apply_mk(df, lower, upper):
    if any(df > upper) or any(df < lower):
        return 0

    values = df.values
    q25, q75 = np.quantile(values, [0.25, 0.75])
    iqr = q75 - q25
    values[(values > q75 + 1.5 * iqr) | (values < q25 - 1.5 * iqr)] = np.nan
    values = values[~np.isnan(values)]
    values = values[np.insert(np.diff(values).astype(bool), 0, True)]

    if len(values) <= 20:
        return 0
    result = mk.original_test(values, alpha=0.001)
    if result.trend == "no trend":
        return 0
    if result.trend == "increasing":
        return 1
    return -1


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _get_last_analyzed_point(df):
    points_before_last_analysis = df.index[
        df.index <= df.index[-1] - timedelta(weeks=4)
    ]
    if len(points_before_last_analysis) == 0:
        return df.index[0]
    return points_before_last_analysis[-1]


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_drift_check(  # pylint: disable=too-many-locals
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    df_daily = df.resample("1D").median().interpolate("time")
    lower, upper = _get_global_outliers(df_daily)
    slopes = df_daily.rolling(28).apply(lambda x: _apply_mk(x, lower, upper))
    pos_slopes = slopes["value"] == 1
    neg_slopes = slopes["value"] == -1

    pos_intervals = _get_intervals(df_daily, pos_slopes, "Positive slopes")
    neg_intervals = _get_intervals(df_daily, neg_slopes, "Negative slopes")
    pos_intervals = _handle_open_intervals(df_daily, pos_intervals)
    neg_intervals = _handle_open_intervals(df_daily, neg_intervals)

    mpos = _merge_frames(pos_intervals)
    mneg = _merge_frames(neg_intervals)

    all_intervals = pd.concat((mpos, mneg))

    all_intervals = merge_intervals_and_open_event_frames(
        analysis_start, all_intervals, open_event_frames
    )

    all_frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = _get_last_analyzed_point(df)

    return list(all_frames), last_analyzed_point


def _is_relevant_open_event_frame(event_frame):
    return event_frame.end_date is None and (
        event_frame.type in META["checks"][0]["event_frames"]
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


def _is_valid_input(data: pd.DataFrame) -> tuple[str, bool]:
    df = _clean_dataframe(data)
    if len(df) == 0:
        return "Not enough data", False
    if len(df["value"].unique()) <= 3:
        return "Not enough unique values", False
    if is_string_dtype(df["value"]):
        return "Can not be a string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    open_event_frames = _get_open_event_frames(analysis_input)

    message, is_ok = _is_valid_input(analysis_input.data)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames, last_analyzed_point = _run_drift_check(analysis_input, open_event_frames)
    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
