"""Analysis on the variation in the archival time distribution.

<p>Overcompression is a consequence of settings in a compression algorithm that
cause the archived data to no longer represent the real system accurately. Within traditional
historians this is typically caused by setting the values for exception and/or compression too high.
Low variation in inter-archival time could indicate that the max-time for archival
is often reached.</p>
<p><img src='../static/images/reporting/flat_archival.svg'></p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

import numpy as np

import jsonpickle

from timeseer import AnalysisInput, AnalysisResult, EventFrame

_CHECK_NAME = "Compression - flat archival rate"
_EVENT_FRAME_NAME = "Compression - flat archival rate"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Accuracy",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [{"min_series": 1, "min_weeks": 1, "min_data_points": 300}],
    "signature": "univariate",
}


def _is_sampling_rate_too_regular(sketch):
    q1, q9 = [sketch.get_quantile_value(q) for q in [0.1, 0.9]]
    if np.isnan(q1) or np.isnan(q9):
        return 0
    if q1 == q9:
        return 1
    return 0


def _run_flat_check(archival_sketch):
    return _is_sampling_rate_too_regular(archival_sketch)


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    json_archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")
    if json_archival_sketch is None:
        return AnalysisResult(condition_message="No archival sketch")
    archival_sketch = jsonpickle.decode(json_archival_sketch)

    score = _run_flat_check(archival_sketch)
    event_frames = []
    if score == 1:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
