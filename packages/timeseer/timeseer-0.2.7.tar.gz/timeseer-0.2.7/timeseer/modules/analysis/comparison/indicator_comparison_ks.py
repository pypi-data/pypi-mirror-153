"""check for a change after a critical event based on Kolmogorov-Smirnoff.

<p>This check identifies whether there is a significant difference in the
distribution of a series before and after a critical event.</p>
<div class="ts-check-impact">
<p>Changes in the behavior of a series after a critical event, such as a
maintenance, turnaround or other types of interventions could indicate
human error. This can range from physical damage to a sensor, to forgotten
control strategy updates.</p>
</div>"""

import pandas as pd

from scipy import stats

from timeseer import (
    AnalysisResult,
    CheckResult,
    ComparisonAnalysisInput,
    DataType,
    ProcessType,
)


_CHECK_NAME = "Comparison change ks"

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


def _run_compare_ks(analysis_input: ComparisonAnalysisInput):
    assert analysis_input.reference_data is not None
    df_before = _clean_data(analysis_input.reference_data["value"])
    df_after = _clean_data(analysis_input.data["value"])

    if len(df_before) == 0 or len(df_after) == 0:
        return None

    _, p_value = stats.ttest_ind(df_before, df_after)
    return p_value >= 0.05


def run(
    analysis_input: ComparisonAnalysisInput,
):  # pylint: disable=missing-function-docstring
    is_change = _run_compare_ks(analysis_input)
    if is_change is None:
        return AnalysisResult()

    check = CheckResult(_CHECK_NAME, float(is_change))

    return AnalysisResult(check_results=[check])
