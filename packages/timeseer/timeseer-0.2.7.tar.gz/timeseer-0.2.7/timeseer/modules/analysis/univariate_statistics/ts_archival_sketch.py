""" Calculate the distributed quantile sketch of the time series. """

import jsonpickle
import numpy as np

from ddsketch.ddsketch import DDSketch
from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType


META: dict = {
    "statistics": [
        {"name": "Archival Sketch"},
        {"name": "Extremes Archival Sketch"},
        {"name": "Base Archival Sketch"},
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


def _get_up_quantiles_and_iqr_from_values(values):
    rel_values = values[values > 0]
    if len(rel_values) == 0:
        return None, None, None
    q25, q75 = np.nanquantile(rel_values, [0.25, 0.75])
    iqr = q75 - q25
    return q25, q75, iqr


def _get_down_quantiles_and_iqr_from_values(values):
    rel_values = values[values < 0]
    if len(rel_values) == 0:
        return None, None, None
    q25, q75 = np.nanquantile(rel_values, [0.25, 0.75])
    iqr = q75 - q25
    return q25, q75, iqr


def _get_quantiles_and_iqr_from_sketch(sketch):
    q25, q75 = [sketch.get_quantile_value(q) for q in [0.25, 0.75]]
    iqr = q75 - q25
    return q25, q75, iqr


def _get_diff_times(df):
    meas_times = df.index.to_series()
    return (meas_times - meas_times.shift()).dt.total_seconds()


def _get_extremes_archival_sketch(
    diff_times, diff_values, extremes_archival_sketch, jump_up_sketch, jump_down_sketch
):
    if extremes_archival_sketch is None:
        extremes_archival_sketch = DDSketch(0.001)

    if jump_up_sketch is None:
        _, up_q75, up_iqr = _get_up_quantiles_and_iqr_from_values(diff_values)
    if jump_up_sketch is not None:
        _, up_q75, up_iqr = _get_quantiles_and_iqr_from_sketch(jump_up_sketch)
    if jump_down_sketch is None:
        down_q25, _, down_iqr = _get_down_quantiles_and_iqr_from_values(diff_values)
    if jump_down_sketch is not None:
        down_q25, _, down_iqr = _get_quantiles_and_iqr_from_sketch(jump_down_sketch)

    ups = np.array([False] * len(diff_values))
    downs = np.array([False] * len(diff_values))

    if up_q75 is not None:
        ups = np.array(diff_values > (up_q75 + 3 * up_iqr))
    if down_q25 is not None:
        downs = np.array(diff_values < (down_q25 - 3 * down_iqr))

    extremes = ups | downs

    for v in diff_times[extremes]:
        extremes_archival_sketch.add(v)

    return extremes_archival_sketch


# pylint: disable=too-many-locals
def _get_base_archival_sketch(
    diff_times, diff_values, base_archival_sketch, jump_up_sketch, jump_down_sketch
):
    if base_archival_sketch is None:
        base_archival_sketch = DDSketch(0.001)

    if jump_up_sketch is None:
        up_q25, up_q75, _ = _get_up_quantiles_and_iqr_from_values(diff_values)
    if jump_up_sketch is not None:
        up_q25, up_q75, _ = _get_quantiles_and_iqr_from_sketch(jump_up_sketch)
    if jump_down_sketch is None:
        down_q25, down_q75, _ = _get_down_quantiles_and_iqr_from_values(diff_values)
    if jump_down_sketch is not None:
        down_q25, down_q75, _ = _get_quantiles_and_iqr_from_sketch(jump_down_sketch)

    ups = np.array([False] * len(diff_values))
    downs = np.array([False] * len(diff_values))

    if up_q75 is not None:
        ups = np.array(diff_values <= up_q75) & np.array(diff_values >= up_q25)
    if down_q25 is not None:
        downs = np.array(diff_values <= down_q75) & np.array(diff_values >= down_q25)

    bases = ups | downs

    for v in diff_times[bases]:
        base_archival_sketch.add(v)

    return base_archival_sketch


def _get_archival_sketch(diff_times, archival_sketch):
    if archival_sketch is None:
        archival_sketch = DDSketch(0.001)

    for v in diff_times:
        archival_sketch.add(v)

    return archival_sketch


def _clean_dataframe(df):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


# pylint: disable=too-many-arguments
def _run_get_sketch(
    analysis_input,
    archival_sketch,
    extremes_archival_sketch,
    base_archival_sketch,
    jump_up_sketch,
    jump_down_sketch,
):
    df = _clean_dataframe(analysis_input.data)

    diff_times = _get_diff_times(df)
    diff_values = df["value"] - df["value"].shift()

    archival_sketch = _get_archival_sketch(diff_times, archival_sketch)
    extremes_archival_sketch = _get_extremes_archival_sketch(
        diff_times,
        diff_values,
        extremes_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    )
    base_archival_sketch = _get_base_archival_sketch(
        diff_times, diff_values, base_archival_sketch, jump_up_sketch, jump_down_sketch
    )

    return archival_sketch, extremes_archival_sketch, base_archival_sketch


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
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")
    extremes_archival_sketch = _get_relevant_statistic(
        analysis_input, "Extremes Archival Sketch"
    )
    base_archival_sketch = _get_relevant_statistic(
        analysis_input, "Base Archival Sketch"
    )
    jump_up_sketch = _get_relevant_statistic(analysis_input, "Jump Up Sketch")
    jump_down_sketch = _get_relevant_statistic(analysis_input, "Jump Down Sketch")

    archival_sketch, extremes_archival_sketch, base_archival_sketch = _run_get_sketch(
        analysis_input,
        archival_sketch,
        extremes_archival_sketch,
        base_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    )

    statistics = []
    if archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][0]["name"],
                "sketch",
                jsonpickle.encode(archival_sketch),
            )
        )
    if extremes_archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][1]["name"],
                "sketch",
                jsonpickle.encode(extremes_archival_sketch),
            )
        )
    if base_archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][2]["name"],
                "sketch",
                jsonpickle.encode(base_archival_sketch),
            )
        )

    if len(statistics) == 0:
        return timeseer.AnalysisResult(condition_message="No statistics")

    return timeseer.AnalysisResult(statistics=statistics)
