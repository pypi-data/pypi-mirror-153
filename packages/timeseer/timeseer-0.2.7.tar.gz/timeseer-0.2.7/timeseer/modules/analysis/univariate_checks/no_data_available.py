"""The data in a time series should be present within the analysis timeframe.

<p>
The data in a time series should be present within the analysis timeframe.
</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
No input - No output.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, EventFrame

_CHECK_NAME = "Data available"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Completeness",
            "event_frames": ["No data"],
            "data_type": "bool",
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    no_data = len(analysis_input.data) == 0
    frames = []
    if no_data:
        frames.append(
            EventFrame(
                type="No data",
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=frames, condition_message="OK exclude")
