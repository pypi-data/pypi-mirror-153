"""Calculate the histogram of a (unevenly spaced) time series."""

import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType

META: dict = {
    "statistics": [
        {"name": "Value histogram"},
        {"name": "Value: percentage of outliers"},
    ],
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


def _remove_outliers(values, weights):
    q25, q75 = np.nanquantile(values, [0.25, 0.75])
    iqr = q75 - q25
    return (
        values[(values <= q75 + 1.5 * iqr) & (values >= q25 - 1.5 * iqr)],
        weights[(values <= q75 + 1.5 * iqr) & (values >= q25 - 1.5 * iqr)],
    )


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_ts_histogram(df: pd.DataFrame):
    clean_df = _clean_dataframe(df)
    values = clean_df["value"].to_numpy()
    if len(clean_df["value"]) < 30:
        return None, None, None

    weights = _get_weights_unequally_spaced(clean_df)
    weights = weights[~np.isnan(values)]
    values = values[~np.isnan(values)]
    clean_values, clean_weights = _remove_outliers(values, weights)
    pct_outliers = 100 * (len(values) - (len(clean_values))) / len(values)
    clean_weights = [len(clean_weights) * i for i in clean_weights]
    try:
        hist, bin_edges = np.histogram(
            clean_values,
            range=(np.nanmin(clean_values), np.nanmax(clean_values)),
            bins=20,
            weights=clean_weights,
        )
        return hist, bin_edges, pct_outliers
    except (ValueError, TypeError):
        return None, None, None


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if is_string_dtype(analysis_input.data["value"]):
        return timeseer.AnalysisResult(condition_message="Can not be a string")

    hist, bin_edges, pct_outliers = _run_ts_histogram(analysis_input.data)
    if hist is None:
        return timeseer.AnalysisResult(condition_message="No histogram")

    histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())

    return timeseer.AnalysisResult(
        statistics=[
            timeseer.Statistic(META["statistics"][0]["name"], "histogram", histogram),
            timeseer.Statistic(META["statistics"][1]["name"], "pct", pct_outliers),
        ]
    )
