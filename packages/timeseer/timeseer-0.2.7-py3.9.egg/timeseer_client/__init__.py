"""Timeseer Client provides convenient remote access to Timeseer.

Data, metadata and event frames are exposed as Python objects."""

from kukur import (
    DataType,
    Dictionary,
    InterpolationType,
    Metadata,
    SeriesSearch,
    SeriesSelector,
)

from .internal import (
    AugmentationStrategy,
    ProcessType,
    TimeseerClientException,
    UnknownAugmentationStrategyException,
)
from .internal.client import Client
from .internal.filters import filter_event_frames, filter_series
from .metadata.fields import register_custom_fields


register_custom_fields(Metadata)


__all__ = [
    "AugmentationStrategy",
    "Client",
    "DataType",
    "Dictionary",
    "InterpolationType",
    "Metadata",
    "ProcessType",
    "SeriesSearch",
    "SeriesSelector",
    "TimeseerClientException",
    "UnknownAugmentationStrategyException",
    "filter_event_frames",
    "filter_series",
]
