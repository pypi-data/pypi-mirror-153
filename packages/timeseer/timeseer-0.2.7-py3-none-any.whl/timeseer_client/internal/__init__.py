"""Implementation details for the Timeseer Client.

Only use classes and functions defined in timeseer_client."""

from enum import Enum


class AugmentationStrategy(Enum):
    """AugmentationStrategy dictates what happens to filtered data points while augmenting based on event frames."""

    REMOVE = "remove values"
    HOLD_LAST = "hold last value"
    LINEAR_INTERPOLATION = "linear interpolation"
    KNN_IMPUTATION = "knn imputation"
    MEAN = "mean"


class TimeseerClientException(Exception):
    """Base class for Timeseer client exceptions.

    Use this to catch any exception that originates in the client."""


class AugmentationException(TimeseerClientException):
    """Exception raised when augmentation strategy fails."""


class UnknownAugmentationStrategyException(TimeseerClientException):
    """Raised when the augmentation strategy is not known."""


class ProcessType(Enum):
    """ProcessType represents the process type of a time series."""

    CONTINUOUS = "CONTINUOUS"
    REGIME = "REGIME"
    BATCH = "BATCH"
    COUNTER = "COUNTER"
