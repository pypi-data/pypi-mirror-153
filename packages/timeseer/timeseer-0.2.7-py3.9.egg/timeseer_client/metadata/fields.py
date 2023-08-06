"""Extra typed metadata fields."""

from typing import Any, Optional

from kukur.metadata import MetadataField

# pylint: disable=unused-import
from kukur.metadata.fields import (  # noqa: F401
    Accuracy,
    AccuracyPercentage,
    DataType,
    Description,
    Dictionary,
    DictionaryName,
    InterpolationType,
    LimitHighFunctional,
    LimitHighPhysical,
    LimitLowFunctional,
    LimitLowPhysical,
    Unit,
)


from timeseer_client.internal import ProcessType as TSProcessType


def _process_type_to_json(process_type: Optional[TSProcessType]) -> Optional[str]:
    if process_type is None:
        return None
    return process_type.value


def _process_type_from_json(process_type: Optional[str]) -> Optional[TSProcessType]:
    if process_type is None:
        return None
    return TSProcessType(process_type)


def _parse_float(number: Optional[Any]) -> Optional[float]:
    if number is None or number == "":
        return None
    return float(number)


ProcessType = MetadataField[Optional[TSProcessType]](
    "process type",
    default=None,
    serialized_name="processType",
    serialize=_process_type_to_json,
    deserialize=_process_type_from_json,
)


SensorModel = MetadataField[Optional[str]](
    "sensor model", default=None, serialized_name="sensorModel"
)


SamplingRate = MetadataField[Optional[float]](
    "sampling rate",
    default=None,
    serialized_name="samplingRate",
    deserialize=_parse_float,
)


def register_custom_fields(cls):
    """Register all typed metadata fields with the given class."""
    cls.register_field(ProcessType)
    cls.register_field(SensorModel, after_field=LimitHighFunctional)
    cls.register_field(SamplingRate, after_field=AccuracyPercentage)


__all__ = [
    "Accuracy",
    "AccuracyPercentage",
    "DataType",
    "Description",
    "Dictionary",
    "DictionaryName",
    "InterpolationType",
    "LimitHighFunctional",
    "LimitLowFunctional",
    "LimitHighPhysical",
    "LimitLowPhysical",
    "ProcessType",
    "SamplingRate",
    "SensorModel",
    "Unit",
]
