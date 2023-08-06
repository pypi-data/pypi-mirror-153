"""All values should appear in the dictionary.

<p>
Dictionaries map numerical values to textual labels.
For example, a valve could be 'OPEN' (1) or 'CLOSED' (2).
If the numerical value 3 appears in the data stream, this value can not be
presented to analytics users and analytics tooling can fail because it can not
map the value.
</p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where a value is present that is not in the dictionary.
Imagine that 100 points are analyzed in a given time-frame and there are 10 points with values
outside the dictionary.
The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points their value is in the dictionary.</p>
<div class="ts-check-impact">
<p>
Values outside the domain of the dictionary can hamper (autoamated) downstream analytics or visualization.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, DataType
from timeseer.analysis.utils import event_frames_from_dataframe
from timeseer.metadata import fields

_CHECK_NAME = "Values in dictionary"
_EVENT_FRAME_NAME = "Values not in dictionary"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Completeness",
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [
        {"min_series": 1, "min_data_points": 1, "data_type": [DataType.DICTIONARY]}
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    dictionary = analysis_input.metadata.get_field(fields.Dictionary)
    if dictionary is None or len(dictionary.mapping) == 0:
        return AnalysisResult(condition_message="No dictionary")
    data = analysis_input.data
    mask = data["value"].isin(dictionary.mapping.keys())

    interval_grp = (mask != mask.shift().bfill()).cumsum()
    intervals = (
        data.assign(interval_grp=interval_grp)[~mask]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _EVENT_FRAME_NAME

    return AnalysisResult(
        event_frames=list(event_frames_from_dataframe(intervals)),
    )
