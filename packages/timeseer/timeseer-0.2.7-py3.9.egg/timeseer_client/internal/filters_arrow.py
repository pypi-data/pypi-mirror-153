"""Filter event frames in Arrow tables or merge Arrow-backed event frame lists."""

from typing import List
from datetime import datetime

import pyarrow as pa
import pyarrow.compute as pc

from timeseer_client.internal import AugmentationException, AugmentationStrategy


def filter_series(
    series: pa.Table,
    event_frames: pa.Table,
    augmentation_strategy: AugmentationStrategy,
) -> pa.Table:
    """Filter the even_frames out of the series based on the strategy."""

    if augmentation_strategy == AugmentationStrategy.KNN_IMPUTATION:
        raise AugmentationException()

    total = pa.array([True] * series.num_rows)

    for index, frame in enumerate(event_frames["start_date"]):
        # pylint: disable=no-member
        on_or_after = pc.less(series["ts"], frame)
        before = pc.greater(series["ts"], event_frames["end_date"][index])
        out_event_frame = pc.or_(on_or_after, before)
        total = pc.and_(total, out_event_frame)

    if augmentation_strategy == AugmentationStrategy.HOLD_LAST:
        return _hold_last_value(series, total)

    if augmentation_strategy == AugmentationStrategy.LINEAR_INTERPOLATION:
        return _linear_interpolation(series, total)

    if augmentation_strategy == AugmentationStrategy.MEAN:
        return _mean_imputation(series, total)

    return series.filter(total)


def filter_event_frames(
    event_frames: pa.Table, start_date: datetime, end_date: datetime
) -> pa.Table:
    """Restrict time range to filter event frames."""
    if event_frames.num_rows == 0:
        return event_frames

    new_start_dates = []
    new_end_dates = []
    total: List[bool] = [True] * event_frames.num_rows
    for index, start_date_frame in enumerate(event_frames["start_date"]):
        end_date_frame = event_frames["end_date"][index]
        # pylint: disable=no-member
        out_start = pc.greater_equal(start_date_frame, pa.scalar(end_date))
        out_end = pc.less_equal(end_date_frame, pa.scalar(start_date))
        new_start_date = start_date_frame.as_py()
        new_end_date = end_date_frame.as_py()
        if out_start.as_py() or out_end.as_py():
            total[index] = False
        if pc.less(start_date_frame, pa.scalar(start_date)).as_py():
            new_start_date = start_date
        if pc.greater(end_date_frame, pa.scalar(end_date)).as_py():
            new_end_date = end_date
        new_start_dates.append(new_start_date)
        new_end_dates.append(new_end_date)
    new_table = event_frames.set_column(
        0, "start_date", pa.array(new_start_dates, type=pa.timestamp("us", tz="UTC"))
    )
    new_table = new_table.set_column(
        1, "end_date", pa.array(new_end_dates, type=pa.timestamp("us", tz="UTC"))
    )
    return new_table.filter(total)


def _hold_last_value(series: pa.Table, out_of_event_frames: pa.array) -> pa.Table:
    new_values = []
    new_ts = []
    last_acceptable = None
    for index, out_of_frame in enumerate(out_of_event_frames.to_pylist()):
        new_value = series["value"][index].as_py()

        if out_of_frame:
            last_acceptable = series["value"][index].as_py()
        else:
            if last_acceptable is None:
                continue
            new_value = last_acceptable

        new_values.append(new_value)
        new_ts.append(series["ts"][index].as_py())

    filtered_series = pa.Table.from_arrays(
        [pa.array(new_ts), pa.array(new_values)], ["ts", "value"]
    )
    return filtered_series


def _linear_interpolation(series: pa.Table, out_of_event_frames: pa.array) -> pa.Table:
    new_values = []
    new_ts = []
    series_to_filter_count = 0
    last_acceptable = None
    for index, out_of_frame in enumerate(out_of_event_frames.to_pylist()):
        if out_of_frame:
            if series_to_filter_count != 0 and last_acceptable is not None:

                for element in range(series_to_filter_count):
                    numerator = (
                        series["ts"][index - (series_to_filter_count - element)].as_py()
                        - series["ts"][index - (series_to_filter_count + 1)].as_py()
                    )
                    denominator = (
                        series["ts"][index].as_py()
                        - series["ts"][index - (series_to_filter_count + 1)].as_py()
                    )
                    time_interpolation = numerator / denominator
                    new_value = (
                        last_acceptable * (1 - time_interpolation)
                        + series["value"][index].as_py() * time_interpolation
                    )
                    new_values.append(new_value)
                    new_ts.append(
                        series["ts"][index - (series_to_filter_count - element)].as_py()
                    )

            last_acceptable = series["value"][index].as_py()
            new_ts.append(series["ts"][index].as_py())
            new_values.append(last_acceptable)
            series_to_filter_count = 0
        else:
            series_to_filter_count = series_to_filter_count + 1
    return pa.Table.from_arrays(
        [pa.array(new_ts), pa.array(new_values)], ["ts", "value"]
    )


def _mean_imputation(series: pa.Table, out_of_event_frames: pa.array) -> pa.Table:
    median_value = pc.mean(series["value"])  # pylint: disable=E1101
    new_values = []
    new_ts = []
    last_acceptable = median_value.as_py()
    for index, out_of_frame in enumerate(out_of_event_frames.to_pylist()):
        new_value = series["value"][index].as_py()

        if out_of_frame:
            last_acceptable = median_value.as_py()
        else:
            if last_acceptable is None:
                continue
            new_value = last_acceptable

        new_values.append(new_value)
        new_ts.append(series["ts"][index].as_py())
    return pa.Table.from_arrays(
        [pa.array(new_ts), pa.array(new_values)], ["ts", "value"]
    )
