"""The provided limits are expected to be close to the recommended limits based on historical data.

<p>Limits can be set either in historian databases, manual, via spec sheets etc.
These limits should be related to the expected operating range of the corresponding sensor.
If historical analysis demonstrates that the actual operating range is significantly different
from the provided limits, this could mean that the limits were wrongly initiated.
</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).
This check is True if there is more than 50% difference in any limit or range.</p>
<div class="ts-check-impact">
<p>Conservatively configured limits can lead to a potential alarm flood. Reversily,
too relaxed limits causes missing important warning signals by for instance masking drift.</p>
</div>
"""

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype
from pint import UndefinedUnitError

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame, Metadata
from timeseer.analysis.utils import get_unit_registry
from timeseer.metadata import fields


_CHECK_NAME = "Improbable limits"
_EVENT_FRAME_NAME = "Improbable limits"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Improbable limits",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 12,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
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


def _unit_dir(metadata: Metadata):
    input_dimension = _get_dimensionality(metadata.get_field(fields.Unit))
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


def _are_hist_limits_close_to_metadata(
    rec_lower, rec_upper, meta_lower, meta_upper
):  # pylint: disable=too-many-return-statements
    rec_range = rec_upper - rec_lower
    meta_range = meta_upper - meta_lower

    if rec_range == 0 or meta_range == 0:
        return False

    if meta_lower == 0:
        if abs(rec_upper / meta_upper) > 2:
            return False
        if rec_lower <= -1:
            return False
        if rec_upper == 0:
            return False
        if abs(meta_upper / rec_upper) > 2:
            return False
    else:
        if (rec_range / meta_range) > 2:
            return False
        if (meta_range / rec_range) > 2:
            return False
        if abs(rec_upper - meta_upper) > (min(rec_range, meta_range) * 0.5):
            return False
        if abs(rec_lower - meta_lower) > (min(rec_range, meta_range) * 0.5):
            return False
    return True


def _are_limits_probable(metadata: Metadata, data: pd.DataFrame) -> bool:

    dimensions_zero_min = _make_units_dir()

    if _unit_dir(metadata) in dimensions_zero_min:
        rec_lower = 0
    else:
        rec_lower = _find_recommended_lower_limit(data)

    if _unit_dir(metadata) == _get_dimensionality("pH"):
        rec_upper = 14
    else:
        rec_upper = _find_recommended_upper_limit(data)

    if _are_hist_limits_close_to_metadata(
        rec_lower,
        rec_upper,
        metadata.get_field(fields.LimitLowFunctional),
        metadata.get_field(fields.LimitHighFunctional),
    ):
        return True

    return False


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    metadata = analysis_input.metadata
    limit_low = metadata.get_field(fields.LimitLowFunctional)
    limit_high = metadata.get_field(fields.LimitHighFunctional)

    if limit_low is None:
        return AnalysisResult(condition_message="No functional lower limit")
    if limit_high is None:
        return AnalysisResult(condition_message="No functional upper limit")

    if limit_low >= limit_high:
        return AnalysisResult(
            condition_message="Functional lower limit is higher than the functional upper limit"
        )

    data = analysis_input.data.dropna()
    if len(data) == 0:
        return AnalysisResult(condition_message="No data")
    if is_string_dtype(data["value"]):
        return AnalysisResult(condition_message="Can not be a string")

    event_frames = []
    if not _are_limits_probable(metadata, data):
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    return AnalysisResult(event_frames=event_frames)
