""" Calculate the distributed staleness sketch of the time series. """

import jsonpickle
from ddsketch.ddsketch import DDSketch

import numpy as np

import timeseer


META: dict = {
    "statistics": [
        {"name": "Stale Sketch"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
        }
    ],
    "signature": "univariate",
}


def _get_repeated_lengths(df):
    active_points = df["value"].eq(df["value"].shift().bfill()).astype(bool)
    interval_grp = (active_points != active_points.shift().bfill()).cumsum()
    active_points[active_points.isna()] = 0
    active_points = np.array(active_points, dtype=bool)
    intervals = (
        df.assign(interval_grp=interval_grp)[active_points]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    return intervals


def _clean_dataframe(df):
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_get_sketch(analysis_input, sketch):
    df = _clean_dataframe(analysis_input.data)
    if len(df) == 0:
        return sketch

    if sketch is None:
        sketch = DDSketch(0.001)

    repeated_lengths = _get_repeated_lengths(df)
    for _, row in repeated_lengths.iterrows():
        sketch.add((row["end_date"] - row["start_date"]).total_seconds())

    return sketch


def _get_relevant_statistic(analysis_input, stat_name):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    previous_sketch = _get_relevant_statistic(analysis_input, "Stale Sketch")

    sketch = _run_get_sketch(analysis_input, previous_sketch)
    if sketch is None:
        return timeseer.AnalysisResult(condition_message="No stale sketch")

    sketch_statistic = timeseer.Statistic(
        META["statistics"][0]["name"], "sketch", jsonpickle.encode(sketch)
    )
    return timeseer.AnalysisResult(statistics=[sketch_statistic])
