"""Time series should indicate their interpolation type.

<p>
It is often required to know the value of a time series between recorded data
points.
</p>
<p>
Two types of interpolation are commonly used:
</p>
<dl>
    <dt>LINEAR interpolation</dt>
    <dd>The value is interpolated linearly between the previously recorded and the next value.</dd>

    <dt>STEPPED interpolation</dt>
    <dd>The value is assumed to be equal to the previously recorded value.</dd>
</dl>
<p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Without a well-defined interpolation type, linear interpolation can happen when
stepped interpolation was required, for example for setpoints. Furthermore correlation analysis
between two series will be skewed when (at least one of) the series are not interpolated correct.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Interpolation type is present"
_EVENT_FRAME_NAME = "Interpolation type is present"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Metadata",
            "group": "Interpolation type",
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
    interpolation_type = analysis_input.metadata.get_field(fields.InterpolationType)

    event_frames = []
    if interpolation_type is None:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )

    return AnalysisResult(event_frames=event_frames)
