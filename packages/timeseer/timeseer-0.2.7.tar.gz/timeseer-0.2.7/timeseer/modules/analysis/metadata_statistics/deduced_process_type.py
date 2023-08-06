"""Data type deduced by actual values.

<p>This check tries to identify the type of process behavior a series abides to:
<ul>
<li>BATCH</li>
<li>GRADE</li>
<li>CONTINUOUS</li>
<li>COUNTER</li>
</ul>
</p>
<div class="ts-check-impact">
<p>Process type influences the interpretation of a series and how to handle it in downstream
analytics. Behavior in a grade plant might differ drastically per regime and these changes
in behavior are not to be regarded as anomolous.
</p>
</div>
"""

import re

from typing import Optional

import networkx as nx
import numpy as np
import pandas as pd

from networkx.algorithms.components import connected_components
from pandas.api.types import is_string_dtype
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from pint import UndefinedUnitError

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import get_unit_registry
from timeseer.metadata import fields


META = {
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


def _get_min_max_or_bust(df):
    df = df.dropna()
    if len(df) < 30:
        return np.array([np.nan, np.nan])

    return np.nanquantile(df, [0.25, 0.75])


def _has_overlap(center1, center2):
    return not (min(center1) > max(center2) or min(center2) > max(center1))


def _no_overlap_in_relevant_clusters(clusters):
    if len(clusters) < 2:
        return False
    nb_overlap = 0
    for i in np.arange(0, len(clusters) - 1):
        for j in np.arange(i + 1, len(clusters)):
            if _has_overlap(clusters[i], clusters[j]):
                nb_overlap = nb_overlap + 1
    return (nb_overlap / len(clusters)) < 0.5


def _is_regime_cluster_based(df):
    min_resampled = df.resample("1W").apply(np.nanmin).interpolate("linear")
    max_resampled = df.resample("1W").apply(np.nanmax).interpolate("linear")
    resampled = (
        pd.concat([min_resampled, max_resampled], axis=1)
        .drop_duplicates()
        .dropna()
        .values
    )
    if len(resampled) >= 10:
        n_clusters = 5
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(resampled)
        if max(kmeans.labels_) < 3:
            return False
        counts = np.bincount(kmeans.labels_)
        if max(kmeans.labels_) < (n_clusters - 1):
            counts = np.concatenate(
                (counts, [0] * (n_clusters - max(kmeans.labels_) - 1))
            )
        rel_clusters = kmeans.cluster_centers_[counts >= 3]
        return _no_overlap_in_relevant_clusters(rel_clusters)
    return False


def _is_regime_graph_based(df):
    resampled = df.resample("1W").apply(_get_min_max_or_bust).apply(pd.Series)
    dists = pdist(resampled, _has_overlap)
    square_distance_matrix = squareform(dists)

    graph = nx.from_numpy_matrix(square_distance_matrix, create_using=nx.MultiGraph)
    connected_graph_components = list(connected_components(graph))

    return (
        len(connected_graph_components) > 3
        and len([g for g in connected_graph_components if len(g) >= 3]) > 3
    )


def _is_regime(df):
    return _is_regime_cluster_based(df) or _is_regime_graph_based(df)


def _frequent_consistent_pct90(df):
    q1, q9 = np.nanquantile(df["value"], [0.1, 0.9])
    resampled = df.resample("1D").apply(lambda x: any(x > q9) and any(x < q1))
    if (sum(resampled["value"]) / len(resampled)) > 0.8:
        return True
    return False


def _is_batch(df):
    if _frequent_consistent_pct90(df):
        return True
    return False


def _get_dimensionality(ureg, unit):
    try:
        return ureg.get_dimensionality(unit)
    except (UndefinedUnitError, AttributeError, ValueError, KeyError):
        return "Unknown"


def _is_counter(analysis_input: timeseer.AnalysisInput) -> bool:
    unit = analysis_input.metadata.get_field(fields.Unit)
    if unit is not None:
        ureg = get_unit_registry()
        dimensionality = _get_dimensionality(ureg, unit)
        if dimensionality.__str__() == "[time]":
            return True
    return False


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _check_process_type(analysis_input: timeseer.AnalysisInput) -> str:
    df = _clean_dataframe(analysis_input.data)
    if _is_counter(analysis_input):
        return "COUNTER"
    if _is_batch(df):
        return "BATCH"
    if _is_regime(df):
        return "REGIME"
    return "CONTINUOUS"


def _check_process_type_string(df: pd.DataFrame) -> str:
    if any(df["value"].str.contains("batch", flags=re.IGNORECASE)) or any(
        df["value"].str.contains("phase", flags=re.IGNORECASE)
    ):
        return "BATCH"
    if (
        any(df["value"].str.contains("regime", flags=re.IGNORECASE))
        or any(df["value"].str.contains("product", flags=re.IGNORECASE))
        or any(df["value"].str.contains("grade", flags=re.IGNORECASE))
    ):
        return "REGIME"
    return "CONTINUOUS"


def _check_process_type_dictionary(analysis_input: timeseer.AnalysisInput) -> str:
    dictionary = analysis_input.metadata.get_field(fields.Dictionary)
    if dictionary is None:
        return "REGIME"
    if any(
        True for v in dictionary.mapping.values() if "batch".upper() in v.upper()
    ) or any(True for v in dictionary.mapping.values() if "phase".upper() in v.upper()):
        return "BATCH"
    return "REGIME"


# This duplicates code in deduce_data_type check
# pylint: disable=too-many-return-statements
def _deduce_data_type(
    analysis_input: timeseer.AnalysisInput,
) -> Optional[timeseer.DataType]:
    df = analysis_input.data

    if len(_clean_dataframe(analysis_input.data)) == 0:
        return None

    if is_string_dtype(df["value"]):
        return DataType.STRING

    data_type = analysis_input.metadata.get_field(fields.DataType)
    if data_type is not None:
        if data_type == DataType.STRING and not is_string_dtype(df["value"]):
            return None
        return data_type

    if (
        df["value"].nunique() <= 10 and all(isinstance(x, int) for x in df["value"])
    ) or all(x in range(101) for x in df["value"].to_numpy()):
        return DataType.CATEGORICAL
    if isinstance(df["value"][0], np.float64):
        return DataType.FLOAT64
    if isinstance(df["value"][0], np.float32):
        return DataType.FLOAT32
    if isinstance(df["value"][0], int):
        return DataType.FLOAT32
    return None


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    result = None

    data_type = _deduce_data_type(analysis_input)
    if data_type in [DataType.FLOAT32, DataType.FLOAT64]:
        result = _check_process_type(analysis_input)
    if data_type == DataType.STRING:
        result = _check_process_type_string(analysis_input.data)
    if data_type in [DataType.DICTIONARY, DataType.CATEGORICAL]:
        result = _check_process_type_dictionary(analysis_input)

    if result is None:
        return timeseer.AnalysisResult(condition_message="Data type is none")

    calculated_metadata = [timeseer.CalculatedMetadata("process type", result)]

    return timeseer.AnalysisResult(calculated_metadata=calculated_metadata)
