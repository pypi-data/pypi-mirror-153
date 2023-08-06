"""The last archived timestamp of a series."""

import timeseer

_STATISTIC_NAME = "Archival time: latest"

META = {
    "statistics": [{"name": _STATISTIC_NAME}],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:

    last_timestamp = analysis_input.data.index.to_series()[-1].to_pydatetime()
    return timeseer.AnalysisResult(
        statistics=[timeseer.Statistic(_STATISTIC_NAME, "datetime", last_timestamp)]
    )
