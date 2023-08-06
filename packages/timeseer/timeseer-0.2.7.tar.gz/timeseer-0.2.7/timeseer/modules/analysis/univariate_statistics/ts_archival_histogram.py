"""Calculate the histogram of a (unevenly spaced) time series."""

import numpy as np
import pandas as pd

import timeseer

from timeseer import DataType

META: dict = {
    "statistics": [{"name": "Archival Histogram"}],
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
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_ts_archival_histogram(df: pd.DataFrame):
    clean_df = _clean_dataframe(df)
    if len(clean_df) < 30:
        return None, None

    meas_times = clean_df.index.to_series()
    diff_times = (meas_times - meas_times.shift()).dt.total_seconds()

    try:
        hist, bin_edges = np.histogram(
            diff_times,
            range=(np.nanmin(diff_times), np.nanmax(diff_times)),
            bins=20,
        )
        return hist, bin_edges
    except (ValueError, TypeError):
        return None, None


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    hist, bin_edges = _run_ts_archival_histogram(analysis_input.data)
    if hist is None:
        return timeseer.AnalysisResult(condition_message="No histogram")

    histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())

    return timeseer.AnalysisResult(
        statistics=[
            timeseer.Statistic(META["statistics"][0]["name"], "histogram", histogram),
        ]
    )
