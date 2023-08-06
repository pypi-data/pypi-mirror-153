"""Quality flags from the data source should not be marked as 'bad'.

<p>
This check identifies whether the quality, if defined, is marked as 'bad' in the source.
</p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where the corresponding quality in the source is marked as 'bad'.
Imagine that 100 points are analyzed in a given time-frame
and there are 10 points whose quality is marked as bad.
The score for this check in that case would be
90% = 1 - 10 / 100. Which means that 90% of all points are marked as 'good'.</p>
<div class="ts-check-impact">
<p>
Data points that are marked as 'bad' in the source is an indication of an unreliable data point.
</p>
</div>
"""

import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, EventFrame
from timeseer.analysis.utils import event_frames_from_dataframe

_CHECK_NAME = "Source bad quality flags"
_EVENT_FRAME_NAME = "Source bad quality flag"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Completeness",
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 1}],
    "signature": "univariate",
}


def _get_intervals(
    outliers: pd.DataFrame, df: pd.DataFrame, event_type: str
) -> pd.DataFrame:
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


def _get_active_points(df: pd.DataFrame) -> pd.DataFrame:
    return df["quality"].isin([0])


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_quality_check(df: pd.DataFrame) -> list[EventFrame]:
    df = _clean_dataframe(df)

    active_points = _get_active_points(df)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)

    frames = event_frames_from_dataframe(intervals)

    return list(frames)


def _is_valid_input(
    data: pd.DataFrame, median_archival_step: list[float]
) -> tuple[str, bool]:
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival step", False
    if "quality" not in data:
        return "No quality flags from data source", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    message, is_ok = _is_valid_input(analysis_input.data, median_archival_step)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames = _run_quality_check(analysis_input.data)

    return AnalysisResult(event_frames=frames)
