"""Data type deduced by actual values.

<p>This check tries to identify the type of data that is being measured:
<ul>
<li>FLOAT32/FLOAT64</li>
<li>CATEGORICAL</li>
<li>STRING</li>
<li>DICTIONARY</li>
</ul>
</p>
<div class="ts-check-impact">
<p>Not having the right data type can cause issues with interpretation of the data and
automatization of analytics solutions. For instance if a series is misinterpreted as
FLOAT64 but in reality is a categorical values then performing calculations on this serie
might lead to unexpected result. In categorical series it is not necessart that labels
relate to distance. E.g. labels (0, ..., 10) does not mean that values of 0 are further
away from 10 than values of 9. They are merely different categories.
</p>
</div>
"""

from pandas.api.types import is_string_dtype

import numpy as np
import timeseer


META = {
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


# Code is duplicated in deduced_process_type
def _check_data_type(df):  # pylint: disable=too-many-return-statements
    if len(df) >= 300:
        if (
            df["value"].nunique() <= 10 and all(isinstance(x, int) for x in df["value"])
        ) or all(x in range(-101, 101) for x in df["value"].to_numpy()):
            return "CATEGORICAL"
    if is_string_dtype(df["value"]):
        return "STRING"
    if isinstance(df["value"][0], np.float64):
        return "FLOAT64"
    if isinstance(df["value"][0], np.float32):
        return "FLOAT32"
    if isinstance(df["value"][0], (np.int, np.int16, np.int64, np.int32)):
        return "FLOAT32"

    return None


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    result = _check_data_type(analysis_input.data)
    if result is None:
        return timeseer.AnalysisResult(condition_message="Data type is none")

    calculated_metadata = [timeseer.CalculatedMetadata("data type", result)]
    return timeseer.AnalysisResult(calculated_metadata=calculated_metadata)
