"""
OP Anomalies
"""

from typing import Optional

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype
from scipy.stats import zscore

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    EventFrame,
    MultivariateAnalysisInput,
)

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
)


_CHECK_NAME = "OP Anomalies"
_EVENT_FRAME_NAME = "OP Anomaly"
_MIN_SERIES = 2

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": _MIN_SERIES,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64, DataType.CATEGORICAL],
        }
    ],
    "signature": "bivariate",
}


def _sort_positions(
    inputs: list[AnalysisInput],
) -> tuple[dict, dict]:
    df_dict = {}
    names_dict = {}
    for column in inputs:
        position = column.metadata.get_field_by_name("control loop")
        df = column.data
        df = df.rename({"value": position}, axis="columns")
        df_dict[position] = df
        names_dict[position] = column.metadata.series
    return df_dict, names_dict


def _match_ts_merge(df_dict: dict) -> Optional[pd.DataFrame]:
    if "OP" not in df_dict or "SP" not in df_dict:
        return None
    df = pd.concat([df_dict["OP"], df_dict["SP"]], axis=1)
    df["SP"] = df["SP"].interpolate(method="pad").bfill()
    df.dropna(subset=["OP"], inplace=True)
    return df


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_sp_events(df: pd.DataFrame):
    change_points = ~(df["SP"].eq(df["SP"].shift().bfill()))
    sp_events = df.iloc[0, :].to_frame().transpose()
    sp_events = pd.concat(
        [sp_events, df[change_points], df.iloc[-1, :].to_frame().transpose()]
    )
    return list(sp_events.index)


def _cusum(drift_series, likelihood_function, anomaly_threshold, standardize=True):
    normalized = drift_series.values / drift_series.values.std()
    if standardize:
        normalized = zscore(drift_series.values)
    s_high = np.zeros_like(normalized)
    s_low = np.zeros_like(normalized)
    for i in np.arange(1, len(normalized)):
        s_high[i] = np.max([0, normalized[i] - likelihood_function + s_high[i - 1]])
        s_low[i] = np.max([0, -likelihood_function - normalized[i] + s_low[i - 1]])
    anomalies = (s_high > anomaly_threshold) | (s_low > anomaly_threshold)
    return anomalies


def _get_active_points(df: pd.DataFrame):
    sp_events = _get_sp_events(df)
    median_archival_step = _get_mv_median_archival_step(df)
    active_points = pd.Series(data=0, index=df.index, dtype=bool)
    for i in range(1, len(sp_events)):
        segment_length = sp_events[i] - sp_events[i - 1]
        if segment_length.total_seconds() >= 100 * median_archival_step:
            segment = df.loc[sp_events[i - 1] : sp_events[i], :]
            op_cusum = _cusum(
                segment["OP"],
                likelihood_function=0.5,
                anomaly_threshold=3,
                standardize=True,
            )
            active_points.loc[segment.index] = op_cusum
    return active_points


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


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def _get_mv_median_archival_step(df):
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    return pd.Timedelta(np.median(diff_times)).total_seconds()


def _run_op_anomalies_detection(
    inputs: list[AnalysisInput],
) -> tuple[list[EventFrame], dict]:
    df_dict, names_dict = _sort_positions(inputs)
    df = _match_ts_merge(df_dict)
    if df is None:
        return [], {}
    df = _clean_dataframe(df)

    active_points = _get_active_points(df)
    intervals = _get_intervals(df, active_points, _EVENT_FRAME_NAME)

    frames = event_frames_from_dataframe(intervals)

    return list(frames), names_dict


def run(  # pylint: disable=missing-function-docstring
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    event_frames, names_dict = _run_op_anomalies_detection(inputs)

    results = [
        BivariateCheckResult(
            _CHECK_NAME,
            names_dict["OP"],
            names_dict["SP"],
            event_frames=event_frames,
        )
    ]

    return AnalysisResult(bivariate_check_results=results)
