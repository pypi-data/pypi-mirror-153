"""Frequency of sampling / archival rate should be similar for most days.

<p>In general the variation in most processes remains reasonably stable.
Under stable conditions the inter-archival time should also remain similar.
Sensor issues could cause archival rate to become more fluctuant.</p>
<p><img src='../static/images/reporting/frequency.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames in which the archival frequency is considered an outlier compared to the overall mean
time between archivals.
E.g. assume a total period being
analyzed of 1 year and 2 event-frames of 1 month and 2 months respectively. The score of this check
will then be 75% = 1 - 3 / 12. Which means that in 75% of time no variance drift is detected.</p>
<div class="ts-check-impact">
<p>
Frequency changes in archival rate might be caused by changing compression settings which could
lead to an infidel representation of the system. Another possibility is temporary disconnects or outages
of the sensor / network.
This could also be caused by network attacks where data is being manipulated before going to the historian.
</p>
</div>
"""

from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from timeseer import AnalysisInput, AnalysisResult, EventFrame

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)

_CHECK_NAME = "Consistent daily archival frequency"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Consistency",
            "event_frames": ["Daily frequency outlier"],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 4,
            "min_data_points": 300,
        }
    ],
    "signature": "univariate",
}


def _get_median_diff_times(df):
    # If only one value in a day, we assume 1 sample per day
    if len(df) <= 1:
        return 24 * 60 * 60

    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times = diff_times.dropna()
    diff_times = diff_times.apply(timedelta.total_seconds)
    return diff_times.median()


def _get_daily_diff_times(df):
    resampled_daily_diff_medians = df.resample("1D").apply(_get_median_diff_times)
    return resampled_daily_diff_medians


def _get_intervals(outliers, df, event_type):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["end_date"] = outlier_intervals["end_date"] + timedelta(days=1)
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] >= df.index[-1]
    return intervals


def _get_quantiles_and_iqr(diff_times):
    q25, q75 = np.nanquantile(diff_times, [0.25, 0.75])
    iqr = q75 - q25
    return q25, q75, iqr


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_daily_frequency_outlier_check(
    analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)
    df_daily = df.resample("1D").mean()

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    diff_times_resampled = _get_daily_diff_times(df)["value"].values

    q25, q75, iqr = _get_quantiles_and_iqr(diff_times_resampled)
    outliers = (diff_times_resampled > (q75 + 3 * iqr)) | (
        diff_times_resampled < (q25 - 3 * iqr)
    )

    intervals = _get_intervals(
        outliers, df.resample("D").asfreq(), "Daily frequency outlier"
    )
    intervals = _handle_open_intervals(df_daily, intervals)
    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    all_frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df_daily.index[-1]

    return list(all_frames), last_analyzed_point


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data frame", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_daily_frequency_outlier_check(
        analysis_input, open_event_frames
    )

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
