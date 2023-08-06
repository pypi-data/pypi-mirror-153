""" Calculate the distributed jump sketches of the time series. """

import jsonpickle

from ddsketch.ddsketch import DDSketch
from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType


META: dict = {
    "statistics": [
        {"name": "Jump Up Sketch"},
        {"name": "Jump Down Sketch"},
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
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_get_sketches(analysis_input, up_sketch, down_sketch):
    df = _clean_dataframe(analysis_input.data)
    if len(df) == 0:
        return up_sketch, down_sketch

    if up_sketch is None:
        up_sketch = DDSketch(0.001)
    if down_sketch is None:
        down_sketch = DDSketch(0.001)

    value_diff = df["value"].diff()

    up_values = value_diff[value_diff > 0]
    down_values = value_diff[value_diff < 0]

    for v in up_values:
        up_sketch.add(v)

    for v in down_values:
        down_sketch.add(v)

    return up_sketch, down_sketch


def _get_relevant_statistic(analysis_input, stat_name):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


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

    previous_up_sketch = _get_relevant_statistic(analysis_input, "Jump Up Sketch")
    previous_down_sketch = _get_relevant_statistic(analysis_input, "Jump Down Sketch")

    up_sketch, down_sketch = _run_get_sketches(
        analysis_input, previous_up_sketch, previous_down_sketch
    )

    statistics = []
    if up_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][0]["name"], "sketch", jsonpickle.encode(up_sketch)
            )
        )
    if down_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][1]["name"], "sketch", jsonpickle.encode(down_sketch)
            )
        )

    if len(statistics) == 0:
        return timeseer.AnalysisResult(condition_message="No statistics")

    return timeseer.AnalysisResult(statistics=statistics)
