"""Identify periods in series where there is a dominant oscillation frequency.

<p>For most sensors the presence of oscillations is an indication of an underlying problem.
This could be, for instance, due to problems with a controller (either directly or upstream).</p>
<p><img src='../static/images/reporting/oscillation.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing oscillations. E.g. assume a total period being analyzed of 100 points and
1 event-frame of 60 points with oscillations.
The score of this check will then be 40% = 1 - 60/100. Which means that in 40% of
time no oscillation is detected.</p>
<div class="ts-check-impact">
<p>
Oscillations typically lead to higher variability in the product quality and more stress on the control
system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

import logging

from timeseer import AnalysisInput, AnalysisResult, DataType


from timeseer.analysis.utils.oscillations import control_loop_oscillation


_CHECK_NAME = "Control Loop Oscillation"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["Control Loop Oscillation"],
            "weight": 1,
        }
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


def _is_correct_series(analysis_input: AnalysisInput) -> tuple[str, bool]:
    position = analysis_input.metadata.get_field_by_name("control loop")
    if position in ["OP", "PV"]:
        return "OK", True
    return "Only applicable to PV and OP", False


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:

    message, is_ok = _is_correct_series(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    return control_loop_oscillation.run(analysis_input)
