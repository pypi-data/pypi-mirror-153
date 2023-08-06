"""Regime detection event frames.

<p></p>"""

from datetime import timedelta
from typing import Optional

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import event_frames_from_dataframe
from timeseer.metadata import fields

_EVENT_FRAME_NAME = "Downtime"

META = {
    "event_frames": [_EVENT_FRAME_NAME],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _is_frame_long_enough(frame):
    return (frame.end_date - frame.start_date) >= timedelta(hours=2)


def _filter_event_frames(all_frames):
    filter_iterator = filter(_is_frame_long_enough, all_frames)
    return filter_iterator


def _get_event_frames(df, anomalies):
    anomalies = pd.Series(data=anomalies, index=df.index)
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()

    intervals = (
        df.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _EVENT_FRAME_NAME

    return event_frames_from_dataframe(intervals)


def _combine_downtime_indicators(anomalies):
    arr_anomalies = np.array(anomalies)
    return np.sum(arr_anomalies, axis=0, dtype=bool)


def _identify_long_gaps_in_data(
    df: pd.DataFrame, analysis_input: timeseer.AnalysisInput
):
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]

    if (
        median_archival_step is None
        or len(median_archival_step) == 0
        or all(np.isnan(median_archival_step))
    ):
        return pd.Series([False] * len(df))

    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    gaps = diff_times >= 3 * timedelta(seconds=median_archival_step[0])
    return gaps


def _get_low_value(analysis_input: timeseer.AnalysisInput) -> Optional[float]:
    limit_low = analysis_input.metadata.get_field(fields.LimitLowFunctional)
    if limit_low is not None:
        return limit_low
    if analysis_input.calculated_metadata is not None:
        calculated_limit_low = analysis_input.calculated_metadata.get_field(
            fields.LimitLowFunctional
        )
        if calculated_limit_low is not None:
            return calculated_limit_low
    return None


def _identify_close_to_low(df: pd.DataFrame, analysis_input: timeseer.AnalysisInput):
    low = _get_low_value(analysis_input)
    if low is None:
        return pd.Series([False] * len(df))

    low_values = df["value"] <= low + low / 100
    return low_values


def _get_clean_df(analysis_input: timeseer.AnalysisInput) -> Optional[pd.DataFrame]:
    df = analysis_input.data
    df = df[~df.index.duplicated(keep="first")].dropna().sort_index()
    if len(df) == 0:
        return None
    return df


def _run_downtime_detection(
    analysis_input: timeseer.AnalysisInput,
) -> Optional[list[timeseer.EventFrame]]:
    clean_df = _get_clean_df(analysis_input)
    if clean_df is None:
        return None

    lows = _identify_close_to_low(clean_df, analysis_input)
    gaps = _identify_long_gaps_in_data(clean_df, analysis_input)

    combined_anomalies = _combine_downtime_indicators([lows, gaps])

    return list(_filter_event_frames(_get_event_frames(clean_df, combined_anomalies)))


def _is_input_valid(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_input_valid(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    frames = _run_downtime_detection(analysis_input)
    if frames is None:
        return timeseer.AnalysisResult()
    return timeseer.AnalysisResult(event_frames=frames)
