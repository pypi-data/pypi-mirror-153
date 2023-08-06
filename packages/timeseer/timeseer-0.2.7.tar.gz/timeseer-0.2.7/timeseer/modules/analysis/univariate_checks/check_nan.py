"""There should be no NaN values in the data.

<p>It is possible for values to be recorded in a non-numerical format due to preprocessing or network issues.
These values are indicated as NaN (Not-a-Number).
Non-numerical reading of a sensor or dividing by zero in preprocessing are typical examples of this issue.</p>
<p><img src='../static/images/reporting/nan.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where the corresponding value is not defined (i.e. NaN).
Imagine that 100 points are analyzed in a given time-frame
and there are 10 points whose value is NaN.
The score for this check in that case would be
90% = 1 - 10 / 100. Which means that 90% of all points have valid values.</p>
<div class="ts-check-impact">
<p>
NaNs can hamper (automated) downstream analytics.
</p>
</div>
"""

import pandas as pd
import numpy as np

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.analysis.utils import event_frames_from_dataframe

_CHECK_NAME = "NaNs"

META: dict = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Completeness",
            "event_frames": ["NaN"],
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 1}],
    "signature": "univariate",
}


def _get_intervals(
    outliers: pd.Series, df: pd.DataFrame, event_type: str
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


def _get_active_points(df: pd.DataFrame) -> pd.Series:
    return df["value"].isna()


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_nan_check(df: pd.DataFrame) -> list[EventFrame]:
    df = _clean_dataframe(df)

    active_points = _get_active_points(df)
    intervals = _get_intervals(active_points, df, "NaN")
    frames = event_frames_from_dataframe(intervals)

    if len(df) == 1:
        if np.isnan(df["value"][0]):
            return list(frames)
        return []

    return list(frames)


def _is_valid_input(median_archival_step: list[float]) -> tuple[str, bool]:
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival step", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]
    message, is_ok = _is_valid_input(median_archival_step)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames = _run_nan_check(analysis_input.data)
    return AnalysisResult(event_frames=frames)
