"""Identification of correlation outliers between each combination of two series.

<p>This check identifies periods of behavior in which the correlation between two series
is significantly different from the baseline.</p>
<p><img src='../static/images/reporting/bivariate_correlation_outlier.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing bivariate correlation outliers. E.g. assume a total period being analyzed of 1 year and
2 event-frames, of 1 month and 2 months respectively.
The score of this check will then be 75% = 1 - 3 / 12.
Which means that in 75% of time no bivariate correlation outliers occur.</p>
<div class="ts-check-impact">
<p>A change in the relation between multiple series might indicate potential process upsets,
as well as instrumentation issues.</p>
</div>
"""

from typing import Union
from datetime import timedelta

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import event_frames_from_dataframe


_CHECK_NAME = "Bivariate correlation outlier"
_EVENT_FRAME_NAME = "Bivariate correlation outlier"
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
            "data_type": [
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.DICTIONARY,
                DataType.CATEGORICAL,
            ],
        }
    ],
    "signature": "bivariate",
}


def _get_anomalies(lower, upper, arr):
    a_lower = arr < lower
    a_upper = arr > upper
    return a_lower | a_upper


def _find_anomalous_days(correlations):
    q25, q75 = np.nanquantile(np.array(correlations, dtype=float), [0.25, 0.75], axis=0)
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return [
        _get_anomalies(lower, upper, x) for x in np.array(correlations, dtype=float)
    ]


def _get_intervals(series_anomaly, days):
    anomalies = pd.Series(data=series_anomaly["correlations"], index=days.index)
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()

    intervals = (
        days.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["end_date"] = intervals["end_date"] + timedelta(
        hours=23, minutes=59, seconds=59
    )
    intervals["type"] = _EVENT_FRAME_NAME
    return intervals


def _get_results_per_series(series_anomaly, days) -> BivariateCheckResult:
    intervals = _get_intervals(series_anomaly, days)

    return BivariateCheckResult(
        _CHECK_NAME,
        series_anomaly["series_x"],
        series_anomaly["series_y"],
        event_frames=list(event_frames_from_dataframe(intervals)),
    )


def _anomalous_days_per_series(anomalous_days_matrix, series):
    results = []
    for i in range(len(series) - 1):
        for j in range(i + 1, len(series)):
            results.append(
                {
                    "series_x": series[i],
                    "series_y": series[j],
                    "correlations": [day[i, j] for day in anomalous_days_matrix],
                }
            )
    return results


def _clean_input(inputs) -> pd.DataFrame:
    return (
        pd.concat(
            [
                series.data[~series.data.index.duplicated(keep="first")]["value"]
                for series in inputs
            ],
            axis=1,
            sort=False,
        )
        .interpolate("linear")
        .dropna()
        .sort_index()
    )


def _run_correlation_outlier_detection(
    inputs: list[AnalysisInput],
) -> Union[list[BivariateCheckResult], None]:
    concatenated_df = _clean_input(inputs)
    if len(concatenated_df) == 0:
        return None
    concatenated_df = concatenated_df[(concatenated_df != 0).all(1)]

    daily_correlations = np.array(
        [x[1].corr() for x in concatenated_df.resample("D")], dtype=object
    )

    if len(daily_correlations) == 0:
        return None

    anomalous_days_matrix = _find_anomalous_days(daily_correlations)

    series = [series.metadata.series for series in inputs]
    anomalous_days_per_series = _anomalous_days_per_series(
        anomalous_days_matrix, series
    )

    days = concatenated_df.resample("D").mean()

    return [
        _get_results_per_series(series_anomaly, days)
        for series_anomaly in anomalous_days_per_series
    ]


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def run(  # pylint: disable=missing-function-docstring
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    results = _run_correlation_outlier_detection(inputs)
    if results is None:
        return AnalysisResult()

    return AnalysisResult(bivariate_check_results=results)
