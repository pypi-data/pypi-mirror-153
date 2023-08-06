"""Within a flow the difference in archival rates between the series is investigated.

<p class="scoring-explanation">The score of this check is calculated based on the
minimum (f_min) and maximum (f_max) archival frequency.</p>

<div class="ts-check-impact">
<p>Differences in archival rates means that for downstream analysis many more interpolated
values might need to be used for at least on of the series. This could hinder reliability
of the outcome of those analysis.</p>
</div>
"""

import pandas as pd
import numpy as np

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    MultivariateAnalysisInput,
    Statistic,
)


_STATISTIC_NAME = "Archival consistency"

META = {
    "run": "before",
    "statistics": [
        {"name": _STATISTIC_NAME},
    ],
    "conditions": [
        {
            "min_series": 2,
        }
    ],
    "signature": "multivariate",
}


def _consistency_score(archivals: pd.DataFrame):
    sorted_archivals = np.sort(archivals)
    sorted_archivals = np.round(sorted_archivals / 10) * 10
    log_diff = np.log10(np.nanmax(sorted_archivals) / np.nanmin(sorted_archivals))
    _, cts = np.unique(sorted_archivals, return_counts=True)
    pcts = cts / len(sorted_archivals)
    return max(pcts) / (log_diff + 1)


def _get_archival_time_median(statistics: list[Statistic]):
    median_archival_step = [
        statistic.result
        for statistic in statistics
        if statistic.name == "Archival time median"
    ]
    if median_archival_step is None or len(median_archival_step) == 0:
        return np.nan
    return median_archival_step[0]


def _run_archival_ratio(inputs: list[AnalysisInput]):
    archival_rates = pd.DataFrame(
        map(lambda x: _get_archival_time_median(x.statistics), inputs)
    )
    archival_rates = archival_rates.dropna()
    if len(archival_rates) == 0:
        return None
    return _consistency_score(archival_rates)


# pylint: disable=missing-function-docstring
def run(
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = analysis_input.inputs

    archival_ratio = _run_archival_ratio(inputs)
    if archival_ratio is None:
        return AnalysisResult()
    statistic = Statistic(_STATISTIC_NAME, "float", archival_ratio)
    return AnalysisResult(statistics=[statistic])
