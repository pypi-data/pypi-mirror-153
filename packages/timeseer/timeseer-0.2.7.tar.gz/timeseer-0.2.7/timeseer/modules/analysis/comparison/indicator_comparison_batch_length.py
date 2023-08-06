"""Check for a change after a critical event based on classification.

<p>This check identifies whether there is a significant difference in
a series before and after a critical event based on cluster distances.</p>
<div class="ts-check-impact">
<p>Changes in the behavior of a series after a critical event, such as a
maintenance, turnaround or other types of interventions could indicate
human error. This can range from physical damage to a sensor, to forgotten
control strategy updates.</p>
</div>"""

import numpy as np
import pandas as pd

from scipy import stats

from timeseer import (
    AnalysisResult,
    CheckResult,
    ComparisonAnalysisInput,
    DataType,
    ProcessType,
)

_CHECK_NAME = "Comparison change batch length"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Validity",
            "data_type": "bool",
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
            "process_type": [ProcessType.BATCH],
        }
    ],
    "signature": "comparison",
}


def _clean_data(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_interval_lengths(outliers, df):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    interval_lengths = outlier_intervals["end_date"] - outlier_intervals["start_date"]
    return interval_lengths.dt.total_seconds()


def _run_compare_batch_length(analysis_input: ComparisonAnalysisInput):
    df_before = _clean_data(analysis_input.reference_data)
    df_after = _clean_data(analysis_input.data)

    if len(df_before) == 0 or len(df_after) == 0:
        return None

    nonzero_before = df_before["value"] > np.nanquantile(df_before["value"], 0.1)
    nonzero_after = df_after["value"] > np.nanquantile(df_after["value"], 0.1)
    before_lengths = _get_interval_lengths(nonzero_before, df_before)
    after_lengths = _get_interval_lengths(nonzero_after, df_after)

    if len(before_lengths) < 10 or len(after_lengths) < 10:
        return None

    if all(np.diff(np.concatenate((before_lengths, after_lengths))) == 0.0):
        return 1

    _, p_value = stats.ttest_ind(before_lengths, after_lengths)
    if np.isnan(p_value):
        return None

    return p_value >= 0.05


def run(
    analysis_input: ComparisonAnalysisInput,
):  # pylint: disable=missing-function-docstring

    is_change = _run_compare_batch_length(analysis_input)
    if is_change is None:
        return AnalysisResult()

    check = CheckResult(_CHECK_NAME, int(is_change))

    return AnalysisResult(check_results=[check])
