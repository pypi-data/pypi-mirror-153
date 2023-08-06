""" Calculate the distributed quantile sketch of the time series. """

import jsonpickle

from ddsketch.ddsketch import DDSketch
from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType


META: dict = {
    "statistics": [
        {"name": "Value Sketch"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64, None],
        }
    ],
    "signature": "univariate",
}


def _clean_dataframe(df):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_get_sketch(analysis_input, previous_sketch):
    df = _clean_dataframe(analysis_input.data)
    if len(df) == 0:
        return previous_sketch

    if previous_sketch is None:
        previous_sketch = DDSketch(0.001)

    for v in df["value"]:
        previous_sketch.add(v)

    return previous_sketch


def _is_valid_input(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    previous_sketch = None
    relevant_statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == META["statistics"][0]["name"]
    ]
    if relevant_statistics is not None and len(relevant_statistics) != 0:
        previous_sketch = jsonpickle.decode(relevant_statistics[0])

    sketch = _run_get_sketch(analysis_input, previous_sketch)
    if sketch is None:
        return timeseer.AnalysisResult(condition_message="No sketch")

    sketch_statistic = timeseer.Statistic(
        META["statistics"][0]["name"], "sketch", jsonpickle.encode(sketch)
    )
    return timeseer.AnalysisResult(statistics=[sketch_statistic])
