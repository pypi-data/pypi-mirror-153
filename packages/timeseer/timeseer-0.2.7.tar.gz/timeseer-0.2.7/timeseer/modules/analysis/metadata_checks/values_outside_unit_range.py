"""For certain units (e.g. pH) there is a limited range values can take.

<p>This check validates whether for a specific set of units, the configured limits fall
within the expected deterministic range.</p>
<p class="scoring-explanation">The score for this checks is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Mismatches between unit range and physical limits are data hygiene bugs.
</p>
</div>
"""

from enum import Enum, auto
from typing import Optional

import numpy as np

from pint import UndefinedUnitError

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import get_unit_registry
from timeseer.metadata import fields

_FUNCTIONAL_CHECK_NAME = "Values outside unit range"
_PHYSICAL_CHECK_NAME = "Values outside unit range (physical limits)"
_FUNCTIONAL_EVENT_FRAME_NAME = "Values outside unit range"
_PHYSICAL_EVENT_FRAME_NAME = "Values outside unit range (physical limits)"

META = {
    "checks": [
        {
            "name": _FUNCTIONAL_CHECK_NAME,
            "kpi": "Metadata",
            "group": "Unit",
            "event_frames": [_FUNCTIONAL_EVENT_FRAME_NAME],
            "data_type": "bool",
        },
        {
            "name": _PHYSICAL_CHECK_NAME,
            "kpi": "Metadata",
            "group": "Unit",
            "event_frames": [_PHYSICAL_EVENT_FRAME_NAME],
            "data_type": "bool",
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


class LimitType(Enum):
    """Choose whether to use physical or functional limits."""

    PHYSICAL = auto()
    FUNCTIONAL = auto()


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


def _limit_settings_outside_range(
    analysis_input: AnalysisInput,
    limit_type: LimitType,
    min_value: float,
    max_value: float,
) -> Optional[bool]:
    if limit_type == LimitType.PHYSICAL:
        limit_low = analysis_input.metadata.get_field(fields.LimitLowPhysical)
        limit_high = analysis_input.metadata.get_field(fields.LimitHighPhysical)
    else:
        limit_low = analysis_input.metadata.get_field(fields.LimitLowFunctional)
        limit_high = analysis_input.metadata.get_field(fields.LimitHighFunctional)
    if limit_low and limit_low < min_value:
        return True
    if limit_high and limit_high > max_value:
        return True
    if not (limit_low or limit_high):
        return None
    return False


def _get_dimensionality(unit):
    ureg = get_unit_registry()
    try:
        return ureg.get_dimensionality(unit)
    except (UndefinedUnitError, AttributeError, ValueError, KeyError):
        return "Unknown"


def _unit_dir(unit):
    input_dimension = _get_dimensionality(unit)
    return input_dimension


def _run_values_outside_unit_range_check(
    unit, analysis_input: AnalysisInput, limit_type: LimitType
) -> Optional[bool]:
    dimensions_zero_min = _make_units_dir()
    if _unit_dir(unit) not in dimensions_zero_min:
        return None
    if _unit_dir(unit) == _get_dimensionality("pH"):
        return _limit_settings_outside_range(
            analysis_input, limit_type, min_value=0, max_value=14
        )
    return _limit_settings_outside_range(
        analysis_input, limit_type, min_value=0, max_value=np.inf
    )


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    unit = analysis_input.metadata.get_field(fields.Unit)
    if unit is None:
        return AnalysisResult(condition_message="No unit")

    event_frames = []

    functional_score = _run_values_outside_unit_range_check(
        unit, analysis_input, LimitType.FUNCTIONAL
    )
    if functional_score is not None and functional_score is True:
        event_frames.append(
            EventFrame(
                type=_FUNCTIONAL_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    physical_score = _run_values_outside_unit_range_check(
        unit, analysis_input, LimitType.PHYSICAL
    )

    if physical_score is not None and physical_score is True:
        event_frames.append(
            EventFrame(
                type=_PHYSICAL_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    return AnalysisResult(event_frames=event_frames)
