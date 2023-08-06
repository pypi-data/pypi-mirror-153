"""For percentage accuracy the value should be between 0 and 100.

<p>This check validates whether the accuracy percentage falls
within the expected range between 0 and 100.</p>
<p class="scoring-explanation">The score for this checks is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Badly configured accuracy percentage can cause a wrong accuracy calculation.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Accuracy percentage is within range"
_EVENT_FRAME_NAME = "Accuracy percentage is within range"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Accuracy",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {"min_series": 1, "data_type": [DataType.FLOAT32, DataType.FLOAT64]}
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    accuracy_percentage = analysis_input.metadata.get_field(fields.AccuracyPercentage)
    if accuracy_percentage is None:
        return AnalysisResult(condition_message="No accuracy percentage")
    event_frames = []
    if accuracy_percentage < 0 or accuracy_percentage > 100:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
