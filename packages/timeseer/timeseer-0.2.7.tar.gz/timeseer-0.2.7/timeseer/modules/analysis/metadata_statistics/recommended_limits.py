"""Recommendation for low and high limits based on historical data.

<p>Each sensor or lab measuring equipment has an inherent measurement range. Outside of this range
the readings from the sensor can't be relied on. This information is typically present in
the sensor specification sheet.
Traditional historians also allow setting limits (often Low-Low, Low, High and High-High limits).
These limits are often based on process safety concerns or indeed taken from the normal operating range.
In all cases having access to these limits is essential for interpreting readings from the equipment.
The <b>recommended limits</> are based upon historical measurements and rounded to a human friendly number
similar as in most charting.</p>
<div class="ts-check-impact">
<p>Missing or badly configured limits can cause missing warning signs of abnormal situations both
in the process as well as with the instrumentation.
</p>
</div>
"""

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

from pint import UndefinedUnitError

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import get_unit_registry
from timeseer.metadata import fields


META = {
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 12,
            "min_data_points": 300,
        }
    ],
    "signature": "univariate",
}


def _get_dimensionality(unit):
    ureg = get_unit_registry()
    try:
        return ureg.get_dimensionality(unit)
    except (UndefinedUnitError, AttributeError, ValueError, KeyError):
        return "Unknown"


def _make_units_dir():
    ureg = get_unit_registry()
    units_zero_min = [
        "meter",
        "second",
        "ampere",
        "candela",
        "gram",
        "mole",
        "kelvin",
        "unit",
        "pH",
        "m2",
        "liter",
        "hertz",
        "kph",
        "galileo",
        "newton",
        "joule",
        "watt",
        "water",
        "pascal",
        "foot_pound",
        "poise",
        "stokes",
        "rhe",
        "particle",
        "molar",
        "katal",
        "clausius",
        "entropy_unit",
        "curie",
        "langley",
        "nit",
        "lumen",
        "lux",
        "a_u_intensity",
        "volt",
        "ohm",
        "siemens",
        "henry",
        "weber",
        "tesla",
        "bohr_magneton",
    ]
    dimensions_zero_min = []
    for unit in units_zero_min:
        dimension = ureg.get_dimensionality(unit)
        dimensions_zero_min.append(dimension)
    return dimensions_zero_min


def _unit_dir(analysis_input: timeseer.AnalysisInput):
    input_dimension = _get_dimensionality(
        analysis_input.metadata.get_field(fields.Unit)
    )
    return input_dimension


def _deconstruct(value):
    if value == 0:
        return [0, 0, 0, 0]
    abs_value = abs(value)
    sign = np.sign(value)
    magnitude = np.floor(np.log10(abs_value))
    scale = np.floor(abs_value // np.power(10, magnitude))
    remainder = abs_value - scale * np.power(10, magnitude)
    smsr = [sign, magnitude, scale, remainder]
    return smsr


def _max_limit(max_value):
    smsr = _deconstruct(max_value)
    sign = smsr[0]
    magnitude = smsr[1]
    scale = smsr[2]
    remainder = smsr[3]
    if magnitude < 0:
        if sign < 0:
            return 0
        lim = np.power(10, magnitude + 1)
        return lim
    lim = np.power(10, magnitude) * (scale)
    if remainder > 0:
        if sign > 0:
            smsr_remainder = _deconstruct(remainder)
            small_mag = max((smsr_remainder[1] + 1), np.floor(magnitude / 2))
            small = np.power(10, np.sign(magnitude) * small_mag)
            lim += small
        if sign < 0:
            smsr_remainder = _deconstruct(remainder)
            if smsr_remainder[1] >= (magnitude / 2):
                small = np.power(10, smsr_remainder[1]) * smsr_remainder[2]
                lim += small
    return float(sign * lim)


def _min_limit(min_value):
    smsr = _deconstruct(min_value)
    sign = smsr[0]
    magnitude = smsr[1]
    scale = smsr[2]
    remainder = smsr[3]
    lim = 0
    if sign < 0:
        if magnitude < 0:
            return -1
        if magnitude >= 0:
            lim = np.power(10, magnitude) * (scale)
            if remainder > 0:
                smsr_remainder = _deconstruct(remainder)
                small_mag = max((smsr_remainder[1] + 1), np.floor(magnitude / 2))
                small = np.power(10, np.sign(magnitude) * small_mag)
                lim += small
    return float(sign * lim)


def _find_recommended_upper_limit(df: pd.DataFrame):
    if len(df["value"]) < 100:
        max_value = max(df["value"])
    else:
        q_1, q_3 = np.quantile(df["value"], [0.25, 0.75])
        iqr = q_3 - q_1
        max_value = max(df["value"][df["value"] <= q_3 + 1.5 * iqr])

    rec_high = 0
    if max_value != 0:
        rec_high = _max_limit(max_value)
    return rec_high


def _find_recommended_lower_limit(df: pd.DataFrame):
    if len(df["value"]) < 100:
        min_value = min(df["value"])
    else:
        q_1, q_3 = np.quantile(df["value"], [0.25, 0.75])
        iqr = q_3 - q_1
        min_value = min(df["value"][df["value"] >= q_1 - 1.5 * iqr])

    rec_low = 0
    if min_value != 0:
        rec_low = _min_limit(min_value)
    return rec_low


def _is_valid_input(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    data_type = analysis_input.metadata.get_field(fields.DataType)
    if data_type not in [DataType.FLOAT64, DataType.FLOAT32, None]:
        return "Data type is not a float", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    data = analysis_input.data.dropna()
    if len(data) == 0:
        return timeseer.AnalysisResult(condition_message="No data")

    dimensions_zero_min = _make_units_dir()

    if _unit_dir(analysis_input) in dimensions_zero_min:
        recommended_lower_limit = 0
    else:
        recommended_lower_limit = _find_recommended_lower_limit(data)

    if _unit_dir(analysis_input) == _get_dimensionality("pH"):
        recommended_upper_limit = 14
    else:
        recommended_upper_limit = _find_recommended_upper_limit(data)

    calculated_metadata = [
        timeseer.CalculatedMetadata("functional lower limit", recommended_lower_limit),
        timeseer.CalculatedMetadata("functional upper limit", recommended_upper_limit),
    ]
    return timeseer.AnalysisResult(calculated_metadata=calculated_metadata)
