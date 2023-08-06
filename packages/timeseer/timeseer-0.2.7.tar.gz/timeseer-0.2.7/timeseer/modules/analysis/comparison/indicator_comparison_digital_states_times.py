"""Check for a change after a critical event based on classification.

<p>This check identifies whether there is a significant difference in
a series before and after a critical event based on cluster distances.</p>
<div class="ts-check-impact">
<p>Changes in the behavior of a series after a critical event, such as a
maintenance, turnaround or other types of interventions could indicate
human error. This can range from physical damage to a sensor, to forgotten
control strategy updates.</p>
</div>"""


import pandas as pd
import numpy as np

from scipy.stats import chisquare

from timeseer import AnalysisResult, CheckResult, ComparisonAnalysisInput, DataType

_CHECK_NAME = "Comparison change digital states times"

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
            "min_data_points": 1,
            "data_type": [DataType.STRING, DataType.DICTIONARY, DataType.CATEGORICAL],
        }
    ],
    "signature": "comparison",
}


def _clean_data(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _are_similar_state_times(before, after):
    before_values = np.array(before["state_times"])
    after_values = np.array(
        after["state_times"] / sum(after["state_times"]) * sum(before["state_times"])
    )
    _, p_value = chisquare(before_values, after_values)
    return p_value >= 0.05


def _run_compare_digital_states(analysis_input: ComparisonAnalysisInput):
    df_before = _clean_data(analysis_input.reference_data)
    df_after = _clean_data(analysis_input.data)

    if len(df_before) == 0 or len(df_after) == 0:
        return None

    if set(df_before["value"]) != set(df_after["value"]):
        return False

    df_before["state_times"] = list(
        (
            pd.Series(df_before.index).shift(-1) - pd.Series(df_before.index)
        ).dt.total_seconds()
    )
    df_after["state_times"] = list(
        (
            pd.Series(df_after.index).shift(-1) - pd.Series(df_after.index)
        ).dt.total_seconds()
    )

    return _are_similar_state_times(
        df_before.groupby(["value"]).sum(), df_after.groupby(["value"]).sum()
    )


def run(
    analysis_input: ComparisonAnalysisInput,
):  # pylint: disable=missing-function-docstring

    is_change = _run_compare_digital_states(analysis_input)
    if is_change is None:
        return AnalysisResult()

    check = CheckResult(_CHECK_NAME, float(is_change))

    return AnalysisResult(check_results=[check])
