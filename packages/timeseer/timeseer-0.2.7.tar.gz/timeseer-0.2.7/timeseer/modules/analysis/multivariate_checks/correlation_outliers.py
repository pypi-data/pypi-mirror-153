"""Identification of correlation outliers between two series.

<p>This check identifies periods of behavior in which the correlations between any 2 series
is significantly different from the baseline.</p>
<p><img src='../static/images/reporting/bivariate_correlation_outlier.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing correlation outliers. E.g. assume a total period being analyzed of 1 year and
2 event-frames, of 1 month and 2 months respectively.
The score of this check will then be 75% = 1 - 3 / 12.
Which means that in 75% of time no correlation outliers occur.</p>
<div class="ts-check-impact">
<p>A change in the relation between multiple series might indicate potential process upsets,
as well as instrumentation issues.</p>
</div>
"""

from datetime import timedelta

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import event_frames_from_dataframe


_CHECK_NAME = "Correlation outlier"
_EVENT_FRAME_NAME = "Correlation outlier"
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
    "signature": "multivariate",
}


def _is_anomaly(lower, upper, arr):
    a_lower = np.any(arr < lower)
    a_upper = np.any(arr > upper)
    return a_lower or a_upper


def _get_active_days(correlations):
    q25, q75 = np.nanquantile(np.array(correlations, dtype=float), [0.25, 0.75], axis=0)
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return [_is_anomaly(lower, upper, x) for x in np.array(correlations, dtype=float)]


def _get_intervals(active_days, days):
    anomalies = pd.Series(data=active_days, index=days.index)
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


def _clean_input(inputs):
    concatenated_df = (
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
    return concatenated_df[(concatenated_df != 0).all(1)]


def _run_correlation_outlier_detection(inputs: list[AnalysisInput]) -> list[EventFrame]:
    concatenated_df = _clean_input(inputs)
    if len(concatenated_df) < 30:
        return []
    daily_correlations = np.array(
        [x[1].corr() for x in concatenated_df.resample("D")], dtype=object
    )

    active_days = _get_active_days(daily_correlations)
    days = concatenated_df.resample("D").mean()
    intervals = _get_intervals(active_days, days)
    frames = event_frames_from_dataframe(intervals)

    return list(frames)


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def run(
    analysis_input: MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    event_frames = _run_correlation_outlier_detection(inputs)

    return AnalysisResult(event_frames=event_frames)
