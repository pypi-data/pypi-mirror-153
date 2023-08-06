"""Analysis on the variation in the archival time distribution per value range.

<p>Overcompression is a consequence of settings in a compression algorithm that
cause the archived data to no longer represent the real system accurately. Within traditional
historians this is typically caused by setting too high values for exception and/or compression.
A significant difference in median inter-archival time between normal values and extreme could indicate
issues with the compression parameters.</p>
<p><img src='../static/images/reporting/value_archival.svg'></p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

import jsonpickle

import timeseer
from timeseer import DataType

_CHECK_NAME = "Compression - value dependent archival rate"

META = {
    "checks": [{"name": _CHECK_NAME, "kpi": "Accuracy", "data_type": "bool"}],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _run_value_dependent_archival_check(extremes_sketch, base_sketch):
    extremes_q25, extremes_q75 = [
        extremes_sketch.get_quantile_value(q) for q in [0.25, 0.75]
    ]
    base_q25, base_q75 = [base_sketch.get_quantile_value(q) for q in [0.25, 0.75]]
    if not (base_q25 > extremes_q75 or extremes_q25 > base_q75):
        return False
    return True


def _get_relevant_statistic(analysis_input, stat_name):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    extremes_sketch = _get_relevant_statistic(
        analysis_input, "Extremes Archival Sketch"
    )
    base_sketch = _get_relevant_statistic(analysis_input, "Base Archival Sketch")
    if extremes_sketch is None:
        return timeseer.AnalysisResult(condition_message="No extreme archival sketch")
    if base_sketch is None:
        return timeseer.AnalysisResult(condition_message="No base archival sketch")

    score = _run_value_dependent_archival_check(extremes_sketch, base_sketch)
    check = timeseer.CheckResult(_CHECK_NAME, float(score))
    return timeseer.AnalysisResult([check])
