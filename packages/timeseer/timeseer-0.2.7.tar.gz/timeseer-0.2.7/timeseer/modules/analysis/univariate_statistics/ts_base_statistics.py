""" Calculate the min, mean ad max of an (unevenly spaced) time series. """

import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype
from statsmodels.stats.weightstats import DescrStatsW

import timeseer

from timeseer import DataType
from timeseer.metadata import fields


META: dict = {
    "statistics": [
        {"name": "Mean"},
        {"name": "Min"},
        {"name": "Max"},
        {"name": "Median"},
        {"name": "Standard Deviation"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
        }
    ],
    "signature": "univariate",
}


def _get_weights_unequally_spaced(df: pd.DataFrame):
    times = (
        (df.index.to_series() - df.index.to_series().shift()).dt.total_seconds()
    ).to_numpy()
    total_duration = np.nansum(times)
    weights = np.empty(len(times))
    weights[0] = 0.5 * times[1] / total_duration
    weights[-1] = 0.5 * times[-1] / total_duration
    if len(times) > 2:
        for i in range(1, (len(times) - 1)):
            weights[i] = 0.5 * (times[i] + times[i + 1]) / total_duration
    return weights


def _run_ts_mean(values, weights):
    return DescrStatsW(values, weights=weights).mean


def _run_ts_std(values, weights):
    return DescrStatsW(values, weights=weights).std


def _run_ts_median(values, weights):
    return DescrStatsW(values, weights).quantile(np.array([0.5]))


def _is_valid_input(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if len(_clean_dataframe(analysis_input.data).dropna()) < 2:
        return "No clean data", False

    data_type = analysis_input.metadata.get_field(fields.DataType)
    if data_type not in [DataType.FLOAT64, DataType.FLOAT32, None]:
        return "Data is not a float", False
    return "OK", True


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].sort_index()


# pylint: disable=missing-function-docstring, too-many-locals
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    clean_df = _clean_dataframe(analysis_input.data)
    values = clean_df["value"].to_numpy()
    weights = _get_weights_unequally_spaced(clean_df)

    weights = weights[~np.isnan(values)]
    values = values[~np.isnan(values)]

    mean = _run_ts_mean(values, weights)
    median = _run_ts_median(values, weights)
    std = _run_ts_std(values, weights)
    stat_mean = timeseer.Statistic(META["statistics"][0]["name"], "hidden", float(mean))
    stat_min = timeseer.Statistic(
        META["statistics"][1]["name"],
        "hidden",
        float(analysis_input.data["value"].min(skipna=True)),
    )
    stat_max = timeseer.Statistic(
        META["statistics"][2]["name"],
        "hidden",
        float(analysis_input.data["value"].max(skipna=True)),
    )
    stat_median = timeseer.Statistic(
        META["statistics"][3]["name"], "hidden", float(median)
    )
    stat_std = timeseer.Statistic(META["statistics"][4]["name"], "hidden", float(std))

    values = [
        ("Min", float(analysis_input.data["value"].min(skipna=True))),
        ("Max", float(analysis_input.data["value"].max(skipna=True))),
        ("Mean", float(mean)),
        ("Median", float(median)),
        ("Std", float(std)),
    ]
    table_statistics = timeseer.Statistic("Value statistics", "table", values)
    statistics = [
        stat_mean,
        stat_min,
        stat_max,
        stat_median,
        stat_std,
        table_statistics,
    ]
    return timeseer.AnalysisResult(
        statistics=statistics,
    )
