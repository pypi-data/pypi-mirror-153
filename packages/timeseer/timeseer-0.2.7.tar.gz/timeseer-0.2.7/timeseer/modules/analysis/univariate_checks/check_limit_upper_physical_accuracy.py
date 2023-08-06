"""Upper limit set by the metadata should not be exceeded, taking into account the uncertainty
as defined by the accuracy in the metadata.

<p>Every measurement has an inherent uncertainty given by precision of the measuring
instrument as well as potential compression settings in the historian. So every value
should be interpreted with uncertainty bounds. This check identifies whether the upper limit,
if defined, is crossed taking these uncertainty bounds into account.</p>
<p><img src='../static/images/reporting/limits_accuracy.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where the corresponding value is above the given limit, taking into account the accuracy.
Imagine that 100 points are analyzed in a given time-frame
and there are 10 points whose value - accuracy is above the given limit.
The score for this check in that case would be
90% = 1 - 10 / 100. Which means that 90% of all points lie inside the limit even taken accuracy
into account.</p>
<div class="ts-check-impact">
<p>
When the sensor spec limits are exceeded this is an indication of sensor failure. This might mean the
sensor needs to be recalibrated.
</p>
</div>
"""

import pandas as pd

from pandas.api.types import is_string_dtype

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame, Metadata
from timeseer.analysis.utils import event_frames_from_dataframe
from timeseer.metadata import fields

_CHECK_NAME = "Out-of-bounds (upper, physical, accuracy)"
_EVENT_FRAME_NAME = "Out of bounds (upper, physical, accuracy)"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _get_intervals(outliers, df, event_type):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _get_active_points(df: pd.DataFrame, metadata: Metadata):
    limit_high = metadata.get_field(fields.LimitHighPhysical)
    accuracy = metadata.get_field(fields.Accuracy)
    assert limit_high is not None
    assert accuracy is not None
    return df["value"] > limit_high - accuracy


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_limit_accuracy_check(metadata: Metadata, df: pd.DataFrame) -> list[EventFrame]:
    df = _clean_dataframe(df)

    active_points = _get_active_points(df, metadata)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    frames = event_frames_from_dataframe(intervals)

    return list(frames)


def _is_input_valid(
    analysis_input: AnalysisInput, median_archival_step: list[float]
) -> tuple[str, bool]:
    if analysis_input.metadata.get_field(fields.Accuracy) is None:
        return "No accuracy", False
    if analysis_input.metadata.get_field(fields.LimitHighPhysical) is None:
        return "No physical upper limit", False
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival step", False
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    message, is_ok = _is_input_valid(analysis_input, median_archival_step)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames = _run_limit_accuracy_check(analysis_input.metadata, analysis_input.data)
    return AnalysisResult(event_frames=frames)
