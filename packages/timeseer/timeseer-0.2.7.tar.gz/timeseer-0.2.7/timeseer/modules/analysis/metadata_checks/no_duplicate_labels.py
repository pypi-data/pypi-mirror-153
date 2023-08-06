"""Dictionary labels should not be repeated with different values.

<p>Dictionaries, or 'digital sets' label discrete numerical values with a
textual representation.
For example, a valve could be 'OPEN' or 'CLOSED'.
'OPEN' could be stored as 1 and 'CLOSED' as 2.<p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Multiple numerical values should not be labeled the same.
This confuses analytics tooling that operates on numerical values, but allows
selection based on labels.</p>
</div>
"""

from collections import Counter

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Labels are not duplicated"
_EVENT_FRAME_NAME = "Labels are not duplicated"


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
    "conditions": [{"min_series": 1, "data_type": [DataType.DICTIONARY]}],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    dictionary = analysis_input.metadata.get_field(fields.Dictionary)
    if dictionary is None:
        return AnalysisResult(condition_message="No dictionary")

    counter = Counter(v for v in dictionary.mapping.values())
    has_duplicates = any(count > 1 for count in counter.values())
    event_frames = []
    if has_duplicates:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    return AnalysisResult(event_frames=event_frames)
