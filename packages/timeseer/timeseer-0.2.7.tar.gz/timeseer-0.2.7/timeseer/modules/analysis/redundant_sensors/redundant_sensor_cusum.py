"""Identification of sensor drift between 2 series by means of cusum.

<p>This check identifies periods where for redundant sensors values of one of the
sensors starts to drift away from the other one.</p>
<p><img src='../static/images/reporting/sensor_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where sensor drift is identified. Imagine that 100 points are analyzed in a given time-frame
and that drift is detected for 10 (consecutive) points. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no drift occurs.</p>
<div class="ts-check-impact">
<p>Changes in a physical relation between a set of series could indicate process or instrumentation issues.</p>

</div>
"""

import pandas as pd
import numpy as np

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import event_frames_from_dataframe


_CHECK_NAME = "Redundant sensor drift"
_EVENT_FRAME_NAME = "Redundant sensor drift"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Accuracy",
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": 2,
            "max_series": 2,
        },
        {
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        },
    ],
    "signature": "bivariate",
}


def cusum(
    drift_series, threshold, anomaly_threshold
):  # pylint: disable=missing-function-docstring
    series = np.array(drift_series["drifts"], dtype=float)
    series = series / np.nanstd(series)

    positive_cusum = (series * 0).copy()
    negative_cusum = positive_cusum.copy()
    for i in np.arange(len(series)):
        if i == 0:
            positive_cusum[i] = series[i]
            negative_cusum[i] = series[i]
        else:
            positive_cusum[i] = np.max(
                [0, series[i] - threshold + positive_cusum[i - 1]]
            )
            negative_cusum[i] = np.max(
                [0, -threshold - series[i] + negative_cusum[i - 1]]
            )
    anomalies = (positive_cusum > anomaly_threshold) | (
        negative_cusum > anomaly_threshold
    )
    return anomalies


def _get_intervals(anomalies, df):
    anomalies = pd.Series(data=anomalies, index=df.index)
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()

    intervals = (
        df.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _EVENT_FRAME_NAME
    return intervals


def _get_result_per_serie(serie, df) -> BivariateCheckResult:
    anomalies = cusum(serie, 0.5, 3)
    intervals = _get_intervals(anomalies, df)

    frames = event_frames_from_dataframe(intervals)

    return BivariateCheckResult(
        _CHECK_NAME,
        serie["series_x"],
        serie["series_y"],
        event_frames=list(frames),
    )


def _get_individual_difference_series(diff_matrix, series):
    results = []
    for i in range(len(series) - 1):
        for j in range(i + 1, len(series)):
            results.append(
                {
                    "series_x": series[i],
                    "series_y": series[j],
                    "drifts": [difference[i, j] for difference in diff_matrix],
                }
            )
    return results


def _make_diff_matrix(df):
    diff_matrix = np.zeros((df.shape[0], df.shape[1], df.shape[1]))
    for i in range(df.shape[1] - 1):
        for j in range(i + 1, df.shape[1]):
            diff_matrix[:, i, j] = df.iloc[:, i] - df.iloc[:, j]
    return diff_matrix


def _clean_input(inputs, selected_index):
    index = inputs[selected_index].data.index
    return (
        pd.concat(
            [
                series.data["value"][
                    ~series.data["value"].index.duplicated(keep="first")
                ]
                for series in inputs
            ],
            axis=1,
            sort=False,
        )
        .reindex(index)
        .interpolate("linear")
        .dropna()
        .sort_index()
    )


def _get_median_archival_step(df):
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    return pd.Timedelta(np.median(diff_times)).total_seconds()


def _run_detect_redundant_sensor_cusum(
    inputs: list[AnalysisInput],
) -> list[BivariateCheckResult]:
    median_archival_step1 = _get_median_archival_step(inputs[0].data)
    median_archival_step2 = _get_median_archival_step(inputs[1].data)
    selected_index = 1
    if median_archival_step1 > median_archival_step2:
        selected_index = 0
    concatenated_df = _clean_input(inputs, selected_index)

    diff_matrix = _make_diff_matrix(concatenated_df)

    series = [series.metadata.series for series in inputs]
    individual_difference_series = _get_individual_difference_series(
        diff_matrix, series
    )

    return [
        _get_result_per_serie(serie, concatenated_df)
        for serie in individual_difference_series
    ]


def run(
    analysis_input: MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring
    inputs = analysis_input.inputs

    results = _run_detect_redundant_sensor_cusum(inputs)

    return AnalysisResult(bivariate_check_results=results)
