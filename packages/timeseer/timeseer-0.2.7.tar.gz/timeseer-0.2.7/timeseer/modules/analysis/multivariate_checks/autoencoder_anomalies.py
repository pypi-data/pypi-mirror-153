"""Identification of outliers based on autoencoder reconstruction error.

<p>This check identifies periods of anomalies based autoencoded deep neural
network architecture. It is based on the assumption that normal data is easy
to reconstruct (encode) while anomalous data will have a higher error.</p>
<p><img src='../static/images/reporting/multivariate_anomaly.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where an autoencoder anomaly occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 10 autoencoder anomalies. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no autoencoder anomaly occurs.</p>
<div class="ts-check-impact">
<p>The presence of anomalies detected by the autoencoder might indicate process upsets as well
as istrumentation issues.</p>
</div>
"""

import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer, MinMaxScaler

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import event_frames_from_dataframe


_CHECK_NAME = "Auto-encoder outlier"
_EVENT_FRAME_NAME = "Auto-encoder outlier"
_MIN_SERIES = 3

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": _MIN_SERIES,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.DICTIONARY,
                DataType.CATEGORICAL,
            ],
        }
    ],
    "signature": "multivariate",
}


def _detect_mad_outliers(points):
    median = np.median(points, axis=0)
    deviation = np.abs(points - median)
    med_abs_deviation = np.median(deviation)
    modified_z_score = 0.6745 * deviation / med_abs_deviation

    return modified_z_score


def _get_intervals(df, anomalies_mse, event_type):
    anomalies = pd.Series(data=anomalies_mse, index=df.index)
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()

    intervals = (
        df.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = event_type
    return intervals


def _get_active_points(concatenated_df):
    pipeline = Pipeline([("normalizer", Normalizer()), ("scaler", MinMaxScaler())])
    pipeline.fit(concatenated_df)
    train_data = pipeline.transform(concatenated_df)
    n_latent = int(np.ceil(np.log2(concatenated_df.shape[1])))
    reg = MLPRegressor(
        hidden_layer_sizes=(n_latent),
        activation="tanh",
        solver="adam",
        learning_rate_init=0.0001,
        max_iter=20,
        tol=0.0000001,
        verbose=False,
    )
    reg.fit(train_data, train_data)

    reconstructions = reg.predict(train_data)
    mse = np.mean(np.power(train_data - reconstructions, 2), axis=1)

    threshold = 3.5
    mad_z_scores = _detect_mad_outliers(mse)
    return mad_z_scores > threshold


def _clean_input(inputs):
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


def _run_autoencoder_anomaly_detection(inputs: list[AnalysisInput]) -> list[EventFrame]:
    concatenated_df = _clean_input(inputs)
    if len(concatenated_df) < 30:
        return []

    active_points = _get_active_points(concatenated_df)
    intervals = _get_intervals(concatenated_df, active_points, _EVENT_FRAME_NAME)

    frames = event_frames_from_dataframe(intervals)

    return list(frames)


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def run(  # pylint: disable=missing-function-docstring
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    event_frames = _run_autoencoder_anomaly_detection(inputs)

    return AnalysisResult(event_frames=event_frames)
