"""Identify highly correlated tag pairs within a given set of tags.

<p>This returns suggestions for pairs to be treated as redundant sensors.</p>"""

from typing import List
from uuid import UUID

import networkx as nx
import numpy as np
import pandas as pd

from networkx.algorithms.components import connected_components

import timeseer

from timeseer import AnalysisInput, AnalysisResult, DataType, SeriesId
from timeseer.metadata import fields


_CHECK_NAME = "Series set discovery"

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
            "min_series": 2,
            "min_weeks": 0,
            "min_data_points": 0,
            "data_type": [
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.DICTIONARY,
                DataType.CATEGORICAL,
            ],
        }
    ],
}


def _is_series_relevant(analysis_input: AnalysisInput) -> bool:
    data_type = analysis_input.metadata.get_field(fields.DataType)
    if data_type is not None and data_type == DataType.STRING:
        return False
    if analysis_input.calculated_metadata is not None:
        calculated_data_type = analysis_input.calculated_metadata.get_field(
            fields.DataType
        )
        if calculated_data_type is not None and calculated_data_type == DataType.STRING:
            return False
    return True


def _get_relevant_series(inputs) -> List[AnalysisInput]:
    return [
        analysis_input
        for analysis_input in inputs
        if _is_series_relevant(analysis_input)
    ]


def _run_correlation_recommendation(inputs: List[AnalysisInput]) -> List[List[UUID]]:
    relevant_series = _get_relevant_series(inputs)
    concatenated_df = (
        pd.concat(
            [
                series.data["value"][
                    ~series.data["value"].index.duplicated(keep="first")
                ]
                for series in relevant_series
            ],
            axis=1,
            sort=False,
        )
        .interpolate("linear")
        .dropna()
    )

    relevant_series_ids = np.array(
        [analysis_input.metadata.series.series_id for analysis_input in relevant_series]
    )
    concatenated_df.columns = relevant_series_ids
    concatenated_df = concatenated_df[(concatenated_df != 0).all(1)]
    concatenated_df = concatenated_df.dropna()

    correlation_matrix = abs(concatenated_df.corr()) > 0.9
    square_distance_matrix = np.array(correlation_matrix)

    connected_graph = nx.from_numpy_matrix(
        square_distance_matrix, create_using=nx.MultiGraph
    )
    graph_components = list(connected_components(connected_graph))
    return [
        relevant_series_ids[np.array(list(group))]
        for group in graph_components
        if len(group) > 1
    ]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = analysis_input.inputs

    suggestions = _run_correlation_recommendation(inputs)
    return AnalysisResult(
        series_sets=dict(
            correlation=[
                [SeriesId(suggestion) for suggestion in group] for group in suggestions
            ]
        )
    )
