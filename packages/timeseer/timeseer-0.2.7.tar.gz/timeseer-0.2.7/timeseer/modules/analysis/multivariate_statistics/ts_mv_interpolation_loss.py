"""Interpolation information loss over all series in a flow.

<p>The Interpolation Information Loss (IIL) is a measure to indicate how much
of the variance is lost when interpolating time series at a particular frequency.
It is well known that just resampling at fixed intervals can cause missing extremes
and hence create data that is no longer representative for the system.

The multivariate IIL assumes a worst case and aggregates all individual IILs accordingly</p>"""

import itertools

from typing import List

import timeseer

from timeseer import DataType


META = {
    "run": "before",
    "conditions": [
        {
            "min_series": 2,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "multivariate",
}

sort_mapping = {
    "1s": 1,
    "5s": 5,
    "15s": 15,
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "12h": 3600 * 12,
    "24h": 3600 * 24,
}


def _by_time(name: str):
    return sort_mapping[name[32:-1]]


def _run_multivariate_interpolation_information_loss(
    analysis_input: timeseer.MultivariateAnalysisInput,
) -> List[timeseer.Statistic]:
    stats = list(
        itertools.chain.from_iterable(
            [info.statistics for info in analysis_input.inputs]
        )
    )

    names = list(
        set(
            stat.name for stat in stats if "Interpolation information loss" in stat.name
        )
    )

    statistics = []
    for name in names:
        results = [stat.result for stat in stats if stat.name == name]
        if len(results) != len(analysis_input.inputs):
            continue
        statistics.append(
            timeseer.Statistic(f"Multivariate {name.lower()}", "hidden", max(results))
        )

    table_names = list(
        set(
            stat.name
            for stat in stats
            if "Interpolation information loss (" in stat.name
        )
    )
    values = []
    for name in sorted(table_names, key=_by_time):
        results = [stat.result for stat in stats if stat.name == name]
        if len(results) != len(analysis_input.inputs):
            continue
        values.append((name[32:-1], max(results)))

    table_statistics = timeseer.Statistic(
        "Multivariate Interpolation Information Loss", "table", values
    )
    return statistics, table_statistics


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.MultivariateAnalysisInput,
) -> timeseer.AnalysisResult:
    statistics, table_statistics = _run_multivariate_interpolation_information_loss(
        analysis_input
    )
    statistics.append(table_statistics)
    return timeseer.AnalysisResult(statistics=statistics)
