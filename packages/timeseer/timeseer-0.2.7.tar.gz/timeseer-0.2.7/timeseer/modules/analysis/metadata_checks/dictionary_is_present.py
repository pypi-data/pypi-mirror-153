"""Time series of type DICTIONARY should reference an existing dictionary.

<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Values in a time series of type DICTIONARY map to textual labels.
This conveys meaning to analytics users.
A time series that is missing this dictionary will be confusing as the user
will be presented with numerical values only.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Dictionary is present"
_EVENT_FRAME_NAME = "Dictionary is present"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Data types",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "data_type": [DataType.DICTIONARY],
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    dictionary = analysis_input.metadata.get_field(fields.Dictionary)
    event_frames = []
    if dictionary is None or len(dictionary.mapping) == 0:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    return AnalysisResult(event_frames=event_frames)
