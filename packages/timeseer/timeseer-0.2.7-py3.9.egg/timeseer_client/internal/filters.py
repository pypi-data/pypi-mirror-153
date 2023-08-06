"""Filter time series data or event frames."""

from datetime import datetime
from typing import Optional

from kukur import InterpolationType

try:
    import pandas as pd
    from timeseer_client.internal import filters_pandas

    HAS_PANDAS = True
except Exception:  # pylint: disable=broad-except
    HAS_PANDAS = False

from timeseer_client.internal import (
    AugmentationStrategy,
    UnknownAugmentationStrategyException,
    filters_arrow,
)


def filter_series(
    series,
    event_frames,
    augmentation_strategy: AugmentationStrategy = AugmentationStrategy.REMOVE,
    interpolation_type: Optional[InterpolationType] = None,
    context=None,
):
    """Filter the time series in the time periods given by event_frames

    Args:
        series: a pyarrow Table or a pandas DataFrame with time series date
            Two columns are present: 'ts' and 'value'.
            A pandas DataFrame can contain a DatetimeIndex instead of the 'ts' column.
        event_frames: pyarrow Table or a pandas DataFrame with event frames.
            Three columns need to be present: 'type', 'start_date' and 'end_date'.
        augmentation_strategy: An enum to define which strategy to use when filtering.
            'REMOVE' (the default) removes the values, 'HOLD_LAST' keeps the last acceptable value,
            'LINEAR_INTERPOLATION' interpolates the last acceptable value and the next acceptable value
            and 'MEDIAN' interpolates with the median value.
            If no acceptable value exists, they are removed. 'KNN_IMPUTATION' uses context to find the
            k-nearest neighbors and takes the average.
        interpolation_type: Enum to define the interpolation type. 'LINEAR' or 'STEPPED'.
            Only linear interpolation types can be linearly interpolated in the augmentation strategy.
        context: A list of pd.DataFrame used for 'KNN_IMPUTATION' to find nearest neighbors
    Returns:
        A filtered pyarrow Table or a pandas DataFrame with 2 columns: 'ts' and 'value'.
        In case the pandas DataFrame provided in 'series' has a DatetimeIndex,
            the 'ts' column will not be present, but the DataFrame will have a DateTimeIndex.
    """
    if context is None:
        context = []

    if not isinstance(augmentation_strategy, AugmentationStrategy):
        raise UnknownAugmentationStrategyException()

    if (
        augmentation_strategy == AugmentationStrategy.LINEAR_INTERPOLATION
        and interpolation_type != InterpolationType.LINEAR
    ):
        augmentation_strategy = AugmentationStrategy.HOLD_LAST

    if len(series) == 0:
        return series

    if (
        HAS_PANDAS
        and isinstance(series, pd.DataFrame)
        and isinstance(event_frames, pd.DataFrame)
    ):
        return filters_pandas.filter_series(
            series, event_frames, augmentation_strategy, context
        )
    return filters_arrow.filter_series(series, event_frames, augmentation_strategy)


def filter_event_frames(event_frames, start_date: datetime, end_date: datetime):
    """Restrict the event frames to the given time range.

    Args:
        event_frames: a pyarrow Table or a pandas DataFrame with event frames.
        start_date: the start date of the range to filter event_frames.
        end_date: the end date of the range to filter event_frames.

    Returns::
        A filtered pyarrow Table or a pandas DataFrame with 5 columns.
        The first column ('start_date') contains the 'start_date' and 'end_date'.
        The second column ('end_date') contains the 'end_date'.
        The third column ('type') contains the type of the returned event frame as a string.
        Columns 4 ('series_source') and 5 ('series_name') contain the source and name of the series.
    """
    if HAS_PANDAS and isinstance(event_frames, pd.DataFrame):
        return filters_pandas.filter_event_frames(event_frames, start_date, end_date)
    return filters_arrow.filter_event_frames(event_frames, start_date, end_date)
