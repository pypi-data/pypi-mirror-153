"""Identification of downtime

<p>This check tries to automatically detect periods of downtime for a series set within a specified time-frame.
</p>
<p><img src='../static/images/reporting/downtime.svg'></p>
<div class="ts-check-impact">
<p>Automated analysis flows typically have difficulties during periods in which they
are not intended to run. Automatically flaggin periods of downtime can build in conditional
execution of these flows.</p>
</div>
"""

from datetime import timedelta
from typing import Optional

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import event_frames_from_dataframe
from timeseer.metadata import fields


_CHECK_NAME = "Downtime"
_EVENT_FRAME_NAME = "Downtime"
_MIN_SERIES = 2

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Consistency",
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": _MIN_SERIES,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "multivariate",
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


def _identify_long_gaps_in_data(df, analysis_input):
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    if median_archival_step is None or len(median_archival_step) == 0:
        return pd.Series([False] * len(df))

    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()

    gaps = diff_times >= 3 * timedelta(seconds=median_archival_step[0])
    return gaps


def _is_dense(values):
    return sum(values) / len(values) > 0.5


def _get_extreme_cutoffs(
    analysis_input: timeseer.AnalysisInput,
) -> tuple[Optional[float], Optional[float]]:
    lower = analysis_input.metadata.get_field(fields.LimitLowFunctional)
    upper = analysis_input.metadata.get_field(fields.LimitHighFunctional)

    if analysis_input.calculated_metadata is not None:
        calculated_lower = analysis_input.calculated_metadata.get_field(
            fields.LimitLowFunctional
        )
        calculated_upper = analysis_input.calculated_metadata.get_field(
            fields.LimitHighFunctional
        )

        if calculated_lower is not None:
            lower = calculated_lower
        if calculated_upper is not None:
            upper = calculated_upper

    return lower, upper


def _identify_high_density_of_extremes(
    df: pd.DataFrame, analysis_input: timeseer.AnalysisInput
):
    lower, upper = _get_extreme_cutoffs(analysis_input)
    if lower is None or upper is None:
        return pd.Series([False] * len(df))
    value_range = upper - lower

    anomalies = (df <= lower - value_range) | (df >= upper + value_range)
    sums = anomalies.rolling("1H").sum().fillna(0)
    counts = anomalies.rolling("1H").count().fillna(1)
    return (sums / counts) >= 0.5


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

    low_values = df.to_numpy() <= (low + low / 100)
    return low_values


def _run_single_downtime_detection(
    clean_df: pd.DataFrame, analysis_input: timeseer.AnalysisInput
):
    lows = _identify_close_to_low(clean_df, analysis_input)
    extremes = _identify_high_density_of_extremes(clean_df, analysis_input)
    gaps = _identify_long_gaps_in_data(clean_df, analysis_input)

    return _combine_downtime_indicators([lows, extremes, gaps])


def _significant_downtime(all_anomalies):
    arr_anomalies = np.array(all_anomalies)
    nb_series = arr_anomalies.shape[0]
    return np.sum(arr_anomalies, axis=0) >= 0.25 * nb_series


def _run_downtime_detection(
    inputs: list[timeseer.AnalysisInput],
) -> list[timeseer.EventFrame]:
    concatenated_df = (
        pd.concat(
            [
                series.data[~series.data.index.duplicated(keep="first")]
                for series in inputs
            ],
            axis=1,
            sort=False,
        )
        .interpolate("linear")
        .dropna()
    )
    all_anomalies = [
        _run_single_downtime_detection(concatenated_df.iloc[:, i], analysis)
        for i, analysis in enumerate(inputs)
    ]

    combined_anomalies = _significant_downtime(all_anomalies)

    return list(
        _filter_event_frames(_get_event_frames(concatenated_df, combined_anomalies))
    )


def _filter_invalid_inputs(
    inputs: list[timeseer.AnalysisInput],
) -> list[timeseer.AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def run(
    analysis_input: timeseer.MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return timeseer.AnalysisResult()

    event_frames = _run_downtime_detection(inputs)

    return timeseer.AnalysisResult(event_frames=event_frames)
