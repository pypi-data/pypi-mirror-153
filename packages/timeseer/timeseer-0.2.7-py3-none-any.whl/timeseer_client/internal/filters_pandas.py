"""Filter event frames in Pandas DataFrames tables or merge DataFrame-backed event frame lists."""

from datetime import datetime
from typing import List
import pandas as pd
import numpy as np

try:
    from sklearn.impute import KNNImputer

    HAS_SKLEARN = True
except Exception:  # pylint: disable=broad-except
    HAS_SKLEARN = False

from timeseer_client.internal import AugmentationException, AugmentationStrategy


def filter_series(
    series: pd.DataFrame,
    event_frames: pd.DataFrame,
    augmentation_strategy: AugmentationStrategy,
    context: List[pd.DataFrame],
) -> pd.DataFrame:
    """Filter the even_frames out of the series with the given strategy."""

    has_datetime_index = False
    if len(series.columns) == 1:
        has_datetime_index = True
        series = series.reset_index()

    if augmentation_strategy == AugmentationStrategy.KNN_IMPUTATION:
        if len(context) == 0:
            raise AugmentationException("KNN imputation requires context.")
        if not HAS_SKLEARN:
            raise AugmentationException(
                "sklearn is required to perform KNN imputation."
            )

    out_event_frame = [True] * len(series)
    for index, start_date in enumerate(event_frames["start_date"]):
        out_event_frame = out_event_frame & (
            (series["ts"] < start_date)
            | (series["ts"] > event_frames["end_date"][index])
        )

    if augmentation_strategy == AugmentationStrategy.HOLD_LAST:
        result = _hold_last_value(series, out_event_frame)

    if augmentation_strategy == AugmentationStrategy.LINEAR_INTERPOLATION:
        result = _linear_interpolation(series, out_event_frame)

    if augmentation_strategy == AugmentationStrategy.KNN_IMPUTATION:
        result = _knn_imputation(series, out_event_frame, context)

    if augmentation_strategy == AugmentationStrategy.MEAN:
        result = _mean_imputation(series, out_event_frame)

    if augmentation_strategy == AugmentationStrategy.REMOVE:
        result = series.loc[out_event_frame]

    if has_datetime_index:
        return result.set_index("ts", drop=True)
    return result


def filter_event_frames(
    event_frames: pd.DataFrame, start_date: datetime, end_date: datetime
) -> pd.DataFrame:
    """Restrict time range to filter event frames."""
    if len(event_frames) == 0:
        return event_frames

    filtered = event_frames.loc[
        (event_frames["start_date"] > pd.to_datetime(end_date))
        | (event_frames["end_date"] > pd.to_datetime(start_date))
    ].copy()

    filtered.loc[
        filtered["start_date"] < pd.to_datetime(start_date), "start_date"
    ] = pd.to_datetime(start_date)
    filtered.loc[
        filtered["end_date"] > pd.to_datetime(end_date), "end_date"
    ] = pd.to_datetime(end_date)
    return filtered


def _hold_last_value(
    series: pd.DataFrame, out_of_event_frames: List[bool]
) -> pd.DataFrame:
    last_acceptable = None
    count = 0
    for index, out_of_frame in enumerate(out_of_event_frames):
        if out_of_frame:
            last_acceptable = series["value"][index]
        else:
            if last_acceptable is None:
                count = count + 1
            series.loc[index, "value"] = last_acceptable
    series = series.loc[count:]
    return series.reset_index(drop=True)


def _linear_interpolation(
    series: pd.DataFrame, out_of_event_frames: List[bool]
) -> pd.DataFrame:
    series_to_filter_count = 0
    last_acceptable = None
    remove_first_elements = 0
    for index, out_of_frame in enumerate(out_of_event_frames):
        if out_of_frame:
            if series_to_filter_count != 0 and last_acceptable is not None:
                for element in range(series_to_filter_count):
                    numerator = (
                        series["ts"][index - (series_to_filter_count - element)]
                        - series["ts"][index - (series_to_filter_count + 1)]
                    )
                    denominator = (
                        series["ts"][index]
                        - series["ts"][index - (series_to_filter_count + 1)]
                    )
                    time_interpolation = numerator / denominator
                    new_value = (
                        last_acceptable * (1 - time_interpolation)
                        + series["value"][index] * time_interpolation
                    )
                    series.loc[
                        index - (series_to_filter_count - element), "value"
                    ] = new_value
            if last_acceptable is None:
                remove_first_elements = series_to_filter_count

            last_acceptable = series["value"][index]
            series_to_filter_count = 0
        else:
            series_to_filter_count = series_to_filter_count + 1

    series = series.loc[
        remove_first_elements : (len(out_of_event_frames) - series_to_filter_count - 1)
    ]
    return series.reset_index(drop=True)


def _knn_imputation(
    series: pd.DataFrame, out_of_event_frames: List[bool], context: List[pd.DataFrame]
):
    series.loc[~np.array(out_of_event_frames), ("value")] = np.nan
    series = series.set_index("ts", drop=True)
    context = [serie.set_index("ts", drop=True) for serie in context]

    concatenated_df = pd.concat(
        [series, *context], axis=1, sort=False, ignore_index=True
    )
    imputer = KNNImputer(n_neighbors=5)
    imputed_df = pd.DataFrame(
        data=imputer.fit_transform(concatenated_df), index=concatenated_df.index
    )
    imputed_df = imputed_df.loc[series.index, 0].reset_index()
    imputed_df.columns = ["ts", "value"]
    return imputed_df


def _mean_imputation(
    series: pd.DataFrame, out_of_event_frames: List[bool]
) -> pd.DataFrame:
    mean = np.mean(series["value"])
    series.loc[~np.array(out_of_event_frames), ("value")] = np.nan
    series = series.set_index("ts", drop=True)
    series = series.fillna(mean)
    series.reset_index()
    return series
