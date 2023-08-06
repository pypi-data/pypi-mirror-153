"""Check for a change after a critical event based on cluster distances.

<p>This check identifies whether there is a significant difference in
a series before and after a critical event based on cluster distances.</p>
<div class="ts-check-impact">
<p>Changes in the behavior of a series after a critical event, such as a
maintenance, turnaround or other types of interventions could indicate
human error. This can range from physical damage to a sensor, to forgotten
control strategy updates.</p>
</div>"""

from scipy.spatial.distance import cdist

import numpy as np
import pandas as pd

from timeseer import (
    AnalysisResult,
    CheckResult,
    ComparisonAnalysisInput,
    DataType,
    ProcessType,
)


_CHECK_NAME = "Comparison change cluster"

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
            "process_type": [ProcessType.CONTINUOUS, ProcessType.REGIME],
        }
    ],
    "signature": "comparison",
}


def _clean_data(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _no_overlap_quantiles(first, second, third):
    if (
        min(first) > max(third)
        or min(third) > max(first)
        or min(second) > max(third)
        or min(third) > max(second)
    ):
        return True
    return False


def _run_compare_cluster(analysis_input: ComparisonAnalysisInput):
    df_before = _clean_data(analysis_input.reference_data)[["value"]]
    df_after = _clean_data(analysis_input.data)[["value"]]

    if len(df_before) == 0 or len(df_after) == 0:
        return None

    sel_before = np.random.choice(
        range(len(df_before)), min(1000, len(df_before)), replace=False
    )
    sel_after = np.random.choice(
        range(len(df_after)), min(1000, len(df_after)), replace=False
    )
    dist_before = np.quantile(
        cdist(
            df_before.iloc[sel_before],
            df_before.iloc[sel_before],
            metric="minkowski",
            p=1,
        ).flatten(),
        [0.25, 0.75],
    )
    dist_after = np.quantile(
        cdist(
            df_after.iloc[sel_after], df_after.iloc[sel_after], metric="minkowski", p=1
        ).flatten(),
        [0.25, 0.75],
    )
    dist_between = np.quantile(
        cdist(
            df_before.iloc[sel_before],
            df_after.iloc[sel_after],
            metric="minkowski",
            p=1,
        ).flatten(),
        [0.25, 0.75],
    )
    if _no_overlap_quantiles(dist_before, dist_after, dist_between):
        return False
    return True


def run(
    analysis_input: ComparisonAnalysisInput,
):  # pylint:disable=missing-function-docstring

    is_change = _run_compare_cluster(analysis_input)
    if is_change is None:
        return AnalysisResult()

    check = CheckResult(_CHECK_NAME, float(is_change))

    return AnalysisResult(check_results=[check])
