"""The data in a time series should match the data type indicated in the metadata.

<p>
Time series data can be numerical or textual.
Operations that have a defined result on numerical data often don't on textual data.
For example, when treated as textual data, 8 is a larger number than 10.
</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Mismatched data types can hamper downstream (automated) analytics.
</p>
</div>
"""

import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Data matches data type"
_EVENT_FRAME_NAME = "Data matches data type"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Integrity",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 1}],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    data_type = analysis_input.metadata.get_field(fields.DataType)
    if data_type is None:
        return AnalysisResult(condition_message="No data type")

    if len(analysis_input.data) == 0:
        is_valid = True
    elif data_type in [DataType.FLOAT32, DataType.FLOAT64, DataType.DICTIONARY]:
        is_valid = pd.api.types.is_numeric_dtype(analysis_input.data["value"])
    elif data_type == DataType.STRING:
        is_valid = pd.api.types.is_string_dtype(analysis_input.data["value"])
    else:
        return AnalysisResult(condition_message="No valid data type")
    event_frames = []
    if not is_valid:
        event_frames.append(
            EventFrame(
                type="No data",
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
