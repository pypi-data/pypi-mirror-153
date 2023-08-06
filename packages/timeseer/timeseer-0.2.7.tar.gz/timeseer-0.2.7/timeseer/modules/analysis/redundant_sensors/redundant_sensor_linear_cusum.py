"""Identification of drift between 2 series that should have a linear relation by means of cusum.

<p>This check identifies periods where the values from sensors that are in a linear relationship
start to drift away from their expected values.</p>
<p><img src='../static/images/reporting/sensor_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where  drift is identified. Imagine that 100 points are analyzed in a given time-frame
and that drift is detected for 10 (consecutive) points. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no drift occurs.</p>
<div class="ts-check-impact">
<p>Changes in a physical relation between a set of series could indicate process or instrumentation issues.</p>
</div>
"""

import pandas as pd
import numpy as np

from scipy.stats import zscore

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import event_frames_from_dataframe


_CHECK_NAME = "Linear redundant sensor drift"
_EVENT_FRAME_NAME = "Linear redundant sensor drift"

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


def _clean_input(inputs):
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
        .interpolate("linear")
        .dropna()
        .sort_index()
    )


def _linear_regression_model(df):
    df_x = df.iloc[:, 0].values
    df_y = df.iloc[:, 1].values
    line = np.polyfit(df_x, df_y, 1)
    return line


def _moving_window_regression_models(df):
    window = int(np.floor(len(df) * 0.2))
    step = int(np.floor(len(df) * 0.02))
    models = []
    start = 0
    for _ in range(40):
        start = start + step
        end = start + window
        df_slice = df.iloc[start:end, :]
        line = _linear_regression_model(df_slice)
        models.append(line)
    start = start + step
    df_slice = df.iloc[start:, :]
    line = _linear_regression_model(df_slice)
    models.append(line)

    return models


def _moving_window_regression_error(df: pd.DataFrame):
    models = _moving_window_regression_models(df)
    models_arr = np.column_stack(models)
    models_df = pd.DataFrame(data={"slope": models_arr[0], "intercept": models_arr[1]})

    median_slope = models_df["slope"].median()
    median_intercept = models_df.loc[models_df["slope"] == median_slope][
        "intercept"
    ].values[0]

    X = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    y_prediction = X * median_slope + median_intercept
    error = y - y_prediction

    return error


def _cusum(drift_series, likelihood_function, anomaly_threshold):
    normalized = zscore(drift_series[0]["drifts"][0])
    s_high = np.zeros_like(normalized)
    s_low = np.zeros_like(normalized)
    for i in np.arange(1, len(normalized)):
        s_high[i] = np.max([0, normalized[i] - likelihood_function + s_high[i - 1]])
        s_low[i] = np.max([0, -likelihood_function - normalized[i] + s_low[i - 1]])
    anomalies = (s_high > anomaly_threshold) | (s_low > anomaly_threshold)
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


def _get_result_per_series(series, df) -> BivariateCheckResult:
    anomalies = _cusum(series, 0.5, 3)
    intervals = _get_intervals(anomalies, df)
    frames = event_frames_from_dataframe(intervals)

    return BivariateCheckResult(
        _CHECK_NAME,
        series[0]["series_x"],
        series[0]["series_y"],
        event_frames=list(frames),
    )


def _get_individual_difference_series(error, series):
    results = []
    results.append({"series_x": series[0], "series_y": series[1], "drifts": [error]})
    return results


def _run_detect_redundant_sensor_cusum(
    inputs: list[AnalysisInput],
) -> BivariateCheckResult:
    concatenated_df = _clean_input(inputs)

    error = _moving_window_regression_error(concatenated_df)

    series = [series.metadata.series for series in inputs]
    individual_difference_series = _get_individual_difference_series(error, series)

    return _get_result_per_series(individual_difference_series, concatenated_df)


def run(
    analysis_input: MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring
    inputs = analysis_input.inputs

    results = _run_detect_redundant_sensor_cusum(inputs)

    return AnalysisResult(bivariate_check_results=[results])
