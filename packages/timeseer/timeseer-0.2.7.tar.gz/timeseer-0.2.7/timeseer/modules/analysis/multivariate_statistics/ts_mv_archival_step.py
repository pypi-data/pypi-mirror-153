"""Medean time between archival.

<p>In historians points are often stored not at fixed time intervals,
but based on approximations. This means that the rate at which points are stored
(archived) is not fixed.
These statistics also provide initial insights in certain data captation issues.</p>"""

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    MultivariateAnalysisInput,
    Statistic,
)


_STATISTIC_NAME = "Archival time median"

META = {
    "run": "before",
    "statistics": [
        {"name": _STATISTIC_NAME},
    ],
    "conditions": [
        {
            "min_series": 2,
            "min_data_points": 1,
        }
    ],
    "signature": "multivariate",
}


def _clean_input(inputs: list[AnalysisInput]) -> pd.DataFrame:
    return (
        pd.concat(
            [
                series.data[~series.data.index.duplicated(keep="first")]
                for series in inputs
            ],
            axis=1,
            sort=False,
        )
        .interpolate("linear")
        .dropna()
        .sort_index()
    )


def _get_mv_median_archival_step(df: pd.DataFrame) -> float:
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    return pd.Timedelta(np.median(diff_times)).total_seconds()


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


#  pylint: disable=missing-function-docstring
def run(analysis_input: MultivariateAnalysisInput) -> AnalysisResult:
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) == 0:
        return AnalysisResult()
    concatenated_df = _clean_input(inputs)
    archival_step = _get_mv_median_archival_step(concatenated_df)
    return AnalysisResult(
        statistics=[Statistic(_STATISTIC_NAME, "hidden", archival_step)]
    )
