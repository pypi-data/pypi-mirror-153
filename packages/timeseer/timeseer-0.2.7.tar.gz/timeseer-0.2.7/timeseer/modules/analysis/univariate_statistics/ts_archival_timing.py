"""Min, mean and max time between archival.

<p>In historians points are often stored not at fixed time intervals,
but based on approximations. This means that the rate at which points are stored
(archived) is not fixed.
These statistics also provide initial insights in certain data captation issues.
For example a 0 or negative minimal archival points to timestamp duplicates or out of order samples.</p>"""

import pandas as pd
import numpy as np

import timeseer


META: dict = {
    "statistics": [
        {"name": "Archival time mean"},
        {"name": "Archival time min"},
        {"name": "Archival time max"},
        {"name": "Archival time median"},
    ],
    "run": "before",
    "conditions": [{"min_series": 1, "min_data_points": 1}],
    "signature": "univariate",
}


def _archival_timing_trivial(analysis_input: timeseer.AnalysisInput):
    start_date = analysis_input.evaluation_time_range.start_date
    end_date = analysis_input.evaluation_time_range.end_date
    archival_timing = (end_date - start_date).total_seconds()
    return (archival_timing, archival_timing, archival_timing, archival_timing)


def _run_ts_archival_timing(analysis_input: timeseer.AnalysisInput):
    df = analysis_input.data

    if len(df) == 1:
        return _archival_timing_trivial(analysis_input)

    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()

    median_archival_step = pd.Timedelta(np.median(diff_times))
    if len(diff_times) < 3:
        median_archival_step = np.mean(diff_times)

    return (
        np.min(diff_times).total_seconds(),
        np.mean(diff_times).total_seconds(),
        np.max(diff_times).total_seconds(),
        median_archival_step.total_seconds(),
    )


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:

    (
        archival_min,
        archival_mean,
        archival_max,
        archival_median,
    ) = _run_ts_archival_timing(analysis_input)
    check_mean = timeseer.Statistic(
        META["statistics"][0]["name"], "hidden", float(archival_mean)
    )
    check_min = timeseer.Statistic(
        META["statistics"][1]["name"], "hidden", float(archival_min)
    )
    check_max = timeseer.Statistic(
        META["statistics"][2]["name"], "hidden", float(archival_max)
    )
    check_median = timeseer.Statistic(
        META["statistics"][3]["name"], "hidden", float(archival_median)
    )

    values = [
        ("Min", float(archival_min)),
        ("Max", float(archival_max)),
        ("Mean", float(archival_mean)),
        ("Median", float(archival_median)),
    ]
    table_statistics = timeseer.Statistic("Archival statistics (sec)", "table", values)
    return timeseer.AnalysisResult(
        statistics=[check_min, check_mean, check_max, check_median, table_statistics]
    )
