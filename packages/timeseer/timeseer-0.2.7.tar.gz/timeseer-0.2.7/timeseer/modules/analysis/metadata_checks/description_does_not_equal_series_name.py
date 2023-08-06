"""The description should not match the series name.

<p class="scoring-explanation">The score for this check is a simple boolean (True / False).
This check belongs to the score group Description.
If this check is True, it means that the score for group Description will be 0%.</p>
<div class="ts-check-impact">
<p>An interpretable description of series aids in onboarding and analysis by 3rd
parties that are less familiar with the process.
Due to time constraints sometimes the non-descriptive name of the series is copied for the description.
A good description provides information on the type as well as location of the sensor.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.metadata import fields

_CHECK_NAME = "Description does not equal series name"
_EVENT_FRAME_NAME = "Description does not equal series name"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Description",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    description = analysis_input.metadata.get_field(fields.Description)
    if description == "":
        return AnalysisResult(condition_message="description is empty")

    event_frames = []
    if description == analysis_input.metadata.series.name:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
