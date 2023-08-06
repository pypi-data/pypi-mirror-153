"""The unit should not be one non-letter character or all the same non-letter characters.

<p>Units aid in the interpretation of measurement readings. Often series naming conventions
show some insight into the type of sensor (e.g. PI for pressure indicator).
Due to time constraints or as a placeholder often "--" or similar is used.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).
This check belongs to the score group Unit.
If this check is True, it means that the score for group Unit will be 0%.</p>
<div class="ts-check-impact">
<p>
Interpreting a dimensionless variable can lead to wrong conclusions and actions
(e.g. bara vs barg vs kPa vs ...). When combining data from different sensors of a similar type,
comparisons without units are impossible. Without units the interpretation of the sensibility of
a measurement value is hindered.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.metadata import fields

_CHECK_NAME = "Unit is interpretable"
_EVENT_FRAME_NAME = "Unit is interpretable"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Unit",
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
    unit = analysis_input.metadata.get_field(fields.Unit)
    if unit == "":
        return AnalysisResult(condition_message="No unit")
    unique_chars = set(unit)
    different_character_count = len(unique_chars)
    event_frames = []
    if different_character_count == 1 and unit[0] in [">", "-", "<"]:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
