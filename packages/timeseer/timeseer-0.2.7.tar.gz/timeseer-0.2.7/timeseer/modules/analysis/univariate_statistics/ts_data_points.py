""" Calculates the number of data points and the data points per day and per hour in a time series. """

from datetime import timedelta
from timeseer import AnalysisInput, AnalysisResult, Statistic

_STATISTIC_NAME = "Data points"

META = {
    "statistics": [
        {"name": _STATISTIC_NAME},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
        }
    ],
    "signature": "univariate",
}


def _get_timespan(analysis_input: AnalysisInput) -> timedelta:
    first_timestamp = analysis_input.data.index.to_series()[0].to_pydatetime()
    last_timestamp = analysis_input.data.index.to_series()[-1].to_pydatetime()
    return last_timestamp - first_timestamp


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    total_data_points = len(analysis_input.data.dropna())
    result = [("Total", total_data_points)]

    if total_data_points == 0:
        return AnalysisResult(statistics=[Statistic(_STATISTIC_NAME, "table", result)])

    timespan = _get_timespan(analysis_input)

    if timespan.days > 0:
        result.append(
            (
                "Average per day",
                int(total_data_points / (timespan.total_seconds() / 60 / 60 / 24)),
            )
        )

    if timespan.total_seconds() > 0:
        result.append(
            (
                "Average per hour",
                int(total_data_points / (timespan.total_seconds() / 60 / 60)),
            )
        )

    return AnalysisResult(statistics=[Statistic(_STATISTIC_NAME, "table", result)])
