"""Check for a change after a critical event based on classification.

<p>This check identifies whether there is a significant difference in
a series before and after a critical event based on cluster distances.</p>
<div class="ts-check-impact">
<p>Changes in the behavior of a series after a critical event, such as a
maintenance, turnaround or other types of interventions could indicate
human error. This can range from physical damage to a sensor, to forgotten
control strategy updates.</p>
</div>"""

from typing import Union

import numpy as np
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from timeseer import (
    AnalysisResult,
    CheckResult,
    ComparisonAnalysisInput,
    DataType,
    ProcessType,
)

_CHECK_NAME = "Comparison change classification"

META: dict = {
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


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_compare_classication(
    analysis_input: ComparisonAnalysisInput,
) -> Union[bool, None]:
    df_before = _clean_data(analysis_input.reference_data)[["value"]]
    df_after = _clean_data(analysis_input.data)[["value"]]

    if len(df_before) == 0 or len(df_after) == 0:
        return None

    sel_before = np.random.choice(range(len(df_before)), 1000)
    sel_after = np.random.choice(range(len(df_after)), 1000)
    df_before = df_before.assign(classlabel=np.ones(len(df_before))).iloc[sel_before]
    df_after = df_after.assign(classlabel=np.zeros(len(df_after))).iloc[sel_after]
    full_df = pd.concat([df_before, df_after])
    X = full_df.iloc[:, 0:-1]
    y = full_df.iloc[:, -1]
    clf = make_pipeline(StandardScaler(), SVC(gamma="auto"))
    clf.fit(X, y)
    y_hat = clf.predict(X)
    score = sum(y == y_hat) / len(full_df)
    return score <= 0.8


# pylint: disable=missing-function-docstring
def run(
    analysis_input: ComparisonAnalysisInput,
) -> AnalysisResult:

    is_change = _run_compare_classication(analysis_input)
    if is_change is None:
        return AnalysisResult()

    check = CheckResult(_CHECK_NAME, float(is_change))

    return AnalysisResult(check_results=[check])
