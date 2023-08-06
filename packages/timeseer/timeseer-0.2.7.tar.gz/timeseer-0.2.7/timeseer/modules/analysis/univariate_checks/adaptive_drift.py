"""Identify tags that drift continuously on average over a calculated frequency and calculated time.

<p>A common indication of sensor issues is sensor drift. This is where a measurement of
a sensor starts to slowly deviate from the real measurement. This can be identified in
reduntant sensor cases where for instance the difference between two identical sensors slowly
increases over time. A drift in a measurement can also have process causes
(e.g. fouling, catalyst degradation)</p>
<p><img src='../static/images/reporting/daily_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing positive and negative slopes. E.g. assume a total period being analyzed of 100 days and
2 event-frames, one no drift and one positive, of 25 days and 75 days respectively.
The score of this check will then be 25% = 1 - 75 / 100. Which means that in 25% of time no drift is detected.</p>
<div class="ts-check-impact">
<p>
Sensor drift can lead to increased costs and variability in the process.
Typically drift is detected manually after a long period of time, which can cause slow deterioration
of product quality.
The longer drift goes unnoticed, the higher the cost and often also the higher the consequences.
Early drift detection can turn a maintenance action into a cleaning action.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

import logging

from datetime import datetime, timedelta
from typing import List, Optional

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


META = {
    "checks": [
        {
            "name": "Adaptive drift (upwards)",
            "kpi": "Validity",
            "event_frames": ["Adaptive positive slopes"],
        },
        {
            "name": "Adaptive drift (downwards)",
            "kpi": "Validity",
            "event_frames": ["Adaptive negative slopes"],
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

logger = logging.getLogger(__name__)


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


def _get_global_outliers(df):
    q25, q75 = np.quantile(df, [0.25, 0.75])
    iqr = q75 - q25
    upper = q75 + 3 * iqr
    lower = q25 - 3 * iqr
    return lower, upper


def _apply_mk(df, lower, upper):
    values = df.values
    q25, q75 = np.quantile(values, [0.25, 0.75])
    iqr = q75 - q25
    values[(values > q75 + 1.5 * iqr) | (values < q25 - 1.5 * iqr)] = np.nan
    values[values > upper] = np.nan
    values[values < lower] = np.nan
    values = values[~np.isnan(values)]
    if len(values) < 20:
        return 0
    values = values[np.insert(np.diff(values).astype(bool), 0, True)]
    if len(values) < 20:
        return 0

    try:
        result = mk.original_test(values, alpha=1e-6)
    except Exception as err:  # pylint: disable=broad-except
        logger.error("Error in adaptive drift: %s", err)
        return 0

    if result.trend == "no trend":
        return 0
    if result.trend == "increasing":
        return 1
    return -1


def _get_intervals(
    df: pd.DataFrame, anomalies: pd.Series, interval_type: str, f_and_p: dict
):
    anomalies = pd.Series(data=anomalies, index=df.index).fillna(False)
    anomaly_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(anomaly_grp=anomaly_grp)[anomalies]
        .reset_index()
        .groupby(["anomaly_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["start_date"] = intervals["start_date"] - timedelta(
        seconds=f_and_p["period_s"]
    )
    intervals["type"] = interval_type
    return intervals


def _handle_open_intervals(df: pd.DataFrame, intervals: pd.Series):
    intervals["open"] = intervals["end_date"] >= df.index[-1]
    return intervals


def _get_last_analyzed_point(
    df: pd.DataFrame, freq: float, rolling_size: int
) -> datetime:
    points_before_last_analysis = df.index[
        df.index <= df.index[-1] - timedelta(seconds=freq * rolling_size)
    ]
    if len(df.index) == 0:
        return df.index[0]
    return points_before_last_analysis[-1]


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_drift_check(  # pylint: disable=too-many-locals
    analysis_input: AnalysisInput,
    f_and_p: dict,
    open_event_frames: list[EventFrame],
) -> tuple[list[EventFrame], datetime]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    df_frequency = df.resample(f_and_p["frequency"]).median().interpolate("time")
    lower, upper = _get_global_outliers(df_frequency)
    rolling_size = int(f_and_p["period_s"] / f_and_p["freq_s"])
    slopes = df_frequency.rolling(rolling_size).apply(
        lambda x: _apply_mk(x, lower, upper)
    )
    pos_slopes = slopes["value"] == 1
    neg_slopes = slopes["value"] == -1

    pos_intervals = _get_intervals(
        df_frequency, pos_slopes, "Adaptive positive slopes", f_and_p
    )
    neg_intervals = _get_intervals(
        df_frequency, neg_slopes, "Adaptive negative slopes", f_and_p
    )
    pos_intervals = _handle_open_intervals(df, pos_intervals)
    neg_intervals = _handle_open_intervals(df, neg_intervals)

    mpos = _merge_frames(pos_intervals)
    mneg = _merge_frames(neg_intervals)

    all_intervals = pd.concat((mpos, mneg))

    all_intervals = merge_intervals_and_open_event_frames(
        analysis_start, all_intervals, open_event_frames
    )

    all_frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = _get_last_analyzed_point(df, f_and_p["freq_s"], rolling_size)

    return list(all_frames), last_analyzed_point


def _get_frequency_and_period_values(median_archival_step: float) -> Optional[dict]:
    if median_archival_step <= 1:
        return {"frequency": "1min", "freq_s": 60, "period": "1H", "period_s": 3600}
    if median_archival_step <= 60:
        return {"frequency": "1H", "freq_s": 3600, "period": "1D", "period_s": 86400}
    if median_archival_step <= 300:
        return {
            "frequency": "12H",
            "freq_s": 43200,
            "period": "15D",
            "period_s": 1296000,
        }
    if median_archival_step <= 3600:
        return {"frequency": "1D", "freq_s": 86400, "period": "4W", "period_s": 2419200}
    if median_archival_step <= 86400:
        return {"frequency": "1D", "freq_s": 86400, "period": "4W", "period_s": 2419200}
    return None


def _is_valid_input(
    analysis_input: AnalysisInput, f_and_p: Optional[dict]
) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if len(analysis_input.data["value"].unique()) <= 3:
        return "Not enough unique values", False
    if f_and_p is None:
        return "No frequency and period value", False
    if (analysis_input.data.index[-1] - analysis_input.data.index[0]) < timedelta(
        seconds=f_and_p["period_s"]
    ):
        return "Time range is smaller than the period value", False
    return "OK", True


def _is_relevant_open_event_frame(event_frame: EventFrame) -> bool:
    return event_frame.end_date is None and (
        (event_frame.type in META["checks"][0]["event_frames"])
        or (event_frame.type in META["checks"][1]["event_frames"])
    )


def _get_open_event_frames(analysis_input: AnalysisInput) -> List[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    # Validating input and parameters
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    if median_archival_step is None or len(median_archival_step) == 0:
        return AnalysisResult(condition_message="No median archival step")
    frequency_and_period = _get_frequency_and_period_values(
        float(median_archival_step[0])
    )
    message, is_ok = _is_valid_input(analysis_input, frequency_and_period)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    open_event_frames = _get_open_event_frames(analysis_input)

    # Performing the actual check
    frames, last_analyzed_point = _run_drift_check(
        analysis_input, frequency_and_period, open_event_frames
    )

    # Returning results
    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
