"""Time series data should have strict increasing timestamps.

<p>Out of order time stamps can occur because of connection issues, causing the system
to rely on buffered data. Another common cause for out of order samples isthe daylight saving time
not handled correctly in the source.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Misaligned ordering of timestamps can hamper (automated) downstream analytics.
</p>
</div>
"""

from datetime import timedelta

from timeseer import AnalysisInput, AnalysisResult, EventFrame

_CHECK_NAME = "No out-of-order samples"
_EVENT_FRAME = "No out-of-order samples"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Integrity",
            "event_frames": [_EVENT_FRAME],
            "data_type": "bool",
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 2}],
    "signature": "univariate",
}


def _any_out_of_order_samples(df):
    return any(df.index.to_series().diff() < timedelta(0))


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    out_of_order = _any_out_of_order_samples(analysis_input.data)
    event_frames = []
    if out_of_order is True:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
