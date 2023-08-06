"""Approximation of uncertainty for a tag based on historical data.

<p>Each sensor or equipment for lab measurements has an inherent uncertainty
(e.g. given on the sensor specification sheet).
Traditional historians using lossy compression also might allow for a deadband in consecutive measurements.
Both of these provide a level of uncertainty about the actual value of the measurement.
The <b>calculated accuracy</b> approximates this uncertainty as a percentage of the historically measured range.
This mimicks typical compression setting behavior for traditional historians.
</p>
<div class="ts-check-impact">
<p>This calculation is done to obtain an approximation on the preciseness of the measurements of a serie.
A high value for accuracy wrt the typical values of the series
is an indication of compression issues. Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

import math
from typing import Optional

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType, InterpolationType
from timeseer.metadata import fields


META = {
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "interpolation_type": [None, InterpolationType.LINEAR],
        }
    ],
    "signature": "univariate",
}


def _find_recommended_upper_limit(df: pd.DataFrame):
    if len(df["value"]) < 100:
        max_value = np.nanmax(df["value"])
    else:
        q25, q75 = np.nanquantile(df["value"], [0.25, 0.75])
        iqr = q75 - q25
        outliers = df["value"][df["value"] <= q75 + 1.5 * iqr]
        if len(outliers) == 0:
            return None
        max_value = np.nanmax(outliers)

    rec_high = 0
    if max_value != 0:
        log_value = np.log10(abs(max_value))
        rec_high = np.ceil(max_value / np.power(10, np.floor(log_value))) * np.power(
            10, np.floor(log_value)
        )
    return rec_high


def _find_recommended_lower_limit(df: pd.DataFrame):
    if len(df["value"]) < 100:
        min_value = np.nanmin(df["value"])
    else:
        q25, q75 = np.nanquantile(df["value"], [0.25, 0.75])
        iqr = q75 - q25
        outliers = df["value"][df["value"] >= q25 - 1.5 * iqr]
        if len(outliers) == 0:
            return None
        min_value = np.nanmin(outliers)

    rec_low = 0
    if min_value != 0:
        log_value = np.log10(abs(min_value))
        rec_low = np.floor(min_value / np.power(10, np.floor(log_value))) * np.power(
            10, np.floor(log_value)
        )
    return rec_low


def _calculate_range(df: pd.DataFrame) -> Optional[float]:
    rec_upper = _find_recommended_upper_limit(df)
    rec_lower = _find_recommended_lower_limit(df)
    if rec_lower is None or rec_upper is None:
        return None
    return rec_upper - rec_lower


def _calculated_accuracy(calculated_range: float):
    if calculated_range < 1000:
        return calculated_range / 200
    if calculated_range >= 1000:
        return calculated_range / 100
    return 0


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    data_type = analysis_input.metadata.get_field(fields.DataType)
    interpolation_type = analysis_input.metadata.get_field(fields.InterpolationType)

    if data_type is not None:
        if data_type not in [DataType.FLOAT32, DataType.FLOAT64]:
            return timeseer.AnalysisResult(condition_message="No data of type float")
    if interpolation_type is not None:
        if interpolation_type != InterpolationType.LINEAR:
            return timeseer.AnalysisResult(
                condition_message="Interpolation type is not linear"
            )
    if is_string_dtype(analysis_input.data["value"]):
        return timeseer.AnalysisResult(condition_message="Can not be a string")

    calculated_range = _calculate_range(analysis_input.data)
    if calculated_range is None or calculated_range == 0:
        return timeseer.AnalysisResult(condition_message="No calculated range")

    calculated_accuracy = _calculated_accuracy(calculated_range)
    if math.isnan(calculated_accuracy):
        return timeseer.AnalysisResult(
            condition_message="Calculated accuracy is not a number"
        )
    calculated_metadata = [timeseer.CalculatedMetadata("accuracy", calculated_accuracy)]
    return timeseer.AnalysisResult(calculated_metadata=calculated_metadata)
