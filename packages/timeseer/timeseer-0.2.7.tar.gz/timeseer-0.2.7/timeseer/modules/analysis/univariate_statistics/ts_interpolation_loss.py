"""Interpolation information loss for a series at different frequencies.

<p>The Interpolation Information Loss is a measure to indicate how much
of the variance is lost when interpolating time series at a particular frequency.
It is well known that just resampling at fixed intervals can cause missing extremes
and hence create data that is no longer representative for the system.</p>"""

from datetime import timedelta

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType
from timeseer.metadata import fields


META = {
    "statistics": [],
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


freq_map = pd.DataFrame(
    {
        "keys": ["1s", "5s", "15s", "1m", "5m", "15m", "1h", "12h", "24h"],
        "values": [1, 5, 15, 60, 300, 900, 3600, 3600 * 12, 3600 * 24],
    }
)


def _get_bar_losses(ii_losses):
    values = [(loss["key"], loss["value"]) for loss in ii_losses]
    statistic = timeseer.Statistic("Interpolation information loss", "table", values)
    return statistic


def _get_statistics(ii_losses):
    statistics = [
        timeseer.Statistic(
            "Interpolation information loss (" + loss["key"] + ")",
            "hidden",
            loss["value"],
        )
        for loss in ii_losses
    ]
    return statistics


def _get_relevant_frequencies(median_archival_step):
    return freq_map[freq_map["values"] >= median_archival_step]


def _get_interpolation_style(analysis_input: timeseer.AnalysisInput) -> str:
    interpolation_type = analysis_input.metadata.get_field(fields.InterpolationType)
    if interpolation_type is None:
        return "linear"
    if interpolation_type == "STEPPED":
        return "pad"
    return "linear"


def _median_diff_times(df):
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    diff_times = diff_times[1:].apply(timedelta.total_seconds)
    return np.median(diff_times)


def _is_trivial(df):
    if df["value"].max() == df["value"].min():
        return True
    if all(df["value"].isna()):
        return True
    return False


def _clean_dataframe(df):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_iqr(df):
    q1, q9 = np.nanquantile(df, [0.1, 0.9])
    return q9 - q1


def _calculate_distance(raw_df, sampled_df):
    df = pd.DataFrame({"raw": raw_df["value"], "sampled": sampled_df["value"]})
    df = df.interpolate("linear")
    point_distance = df["raw"] - df["sampled"]
    return (
        np.nansum(abs(point_distance))
        / point_distance.notnull().sum()
        / _get_iqr(raw_df)
        * 100
    )


def _get_interpolation_information_loss(
    raw_df: pd.DataFrame, median_archival_step, interpolation_style="linear"
):
    raw_df = _clean_dataframe(raw_df)
    if _is_trivial(raw_df):
        return None

    frequencies = _get_relevant_frequencies(median_archival_step)
    if frequencies is None:
        return None

    losses = []
    for _, row in frequencies.iterrows():
        sampled_df = (
            raw_df.resample(rule=timedelta(seconds=row["values"]))
            .mean()
            .interpolate(interpolation_style)
        )
        losses.append(
            {"key": row["keys"], "value": _calculate_distance(raw_df, sampled_df)}
        )
    return losses


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if is_string_dtype(analysis_input.data["value"]):
        return timeseer.AnalysisResult(condition_message="Can not be a string")
    interpolation_style = _get_interpolation_style(analysis_input)
    median_archival_step = _median_diff_times(analysis_input.data)

    ii_losses = _get_interpolation_information_loss(
        analysis_input.data, median_archival_step, interpolation_style
    )
    if ii_losses is None:
        return timeseer.AnalysisResult(
            condition_message="No interpolation information loss"
        )
    statistics = _get_statistics(ii_losses)
    statistics.append(_get_bar_losses(ii_losses))

    return timeseer.AnalysisResult(statistics=statistics)
