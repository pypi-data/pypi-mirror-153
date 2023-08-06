"""Identify series based on deduced regex.

<p>This returns suggestions for pairs to be treated as series group.</p>"""

from typing import List
from uuid import UUID

import numpy as np
import pandas as pd

import timeseer

from timeseer import AnalysisInput, AnalysisResult, SeriesId


_CHECK_NAME = "Series set regex discovery"

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
            "min_series": 3,
            "min_weeks": 0,
            "min_data_points": 0,
        }
    ],
}


def _determine_char_type(char):
    if char.isnumeric():
        return "DIGIT"
    if char.isalpha():
        return "CHARACTER"
    if char.isspace():
        return "WHITESPACE"
    return "SPECIAL"


def _get_current_regex_part(current_type, name, last_index_of_type, idx):
    if current_type == "DIGIT":
        regex_part = "\\d{" + str(last_index_of_type) + "}"
    elif current_type == "CHARACTER":
        regex_part = "[a-zA-Z]{" + str(last_index_of_type) + "}"
    elif current_type == "WHITESPACE":
        regex_part = "\\s{" + str(last_index_of_type) + "}"
    elif current_type == "SPECIAL":
        regex_part = "[" + name[idx - 1] + "]"
    return regex_part


def _create_generic_regex(name, idx, last_index_of_type, regex_part):
    if (idx - last_index_of_type) <= 0:
        return "^" + regex_part
    if (idx + last_index_of_type) > len(name):
        return ".*" + regex_part + "$"
    return ".{" + str(idx - last_index_of_type) + "}" + regex_part


def _get_current_regex_part_for_last_char(name, char, idx):
    if _determine_char_type(char) == "DIGIT":
        regex_part = "\\d{1}"
    elif _determine_char_type(char) == "CHARACTER":
        regex_part = "[a-zA-Z]{1}"
    elif _determine_char_type(char) == "WHITESPACE":
        regex_part = "\\s{1}"
    elif _determine_char_type(char) == "SPECIAL":
        regex_part = "[" + name[idx] + "]"
    return regex_part


def _get_regex_based_on_name(name):
    last_index_of_type = -1
    current_type = _determine_char_type(name[0])
    regex_string = ""
    generic_regex_for_name = []

    for idx, char in enumerate(name):
        last_index_of_type += 1

        # Check whether we have to close a logical part
        if (
            _determine_char_type(char) != current_type
            or _determine_char_type(char) == "SPECIAL"
            or idx == len(name) - 1
        ):

            last_char_different = False

            # If last char has same type, extend length of current type
            if idx == len(name) - 1:
                if _determine_char_type(char) == current_type:
                    last_index_of_type += 1
                if _determine_char_type(char) != current_type:
                    last_char_different = True

            regex_part = _get_current_regex_part(
                current_type, name, last_index_of_type, idx
            )

            regex_string += regex_part
            if current_type != "SPECIAL":
                generic_regex_for_name.append(
                    _create_generic_regex(name, idx, last_index_of_type, regex_part)
                )

            if last_char_different:
                regex_part = _get_current_regex_part_for_last_char(name, char, idx)
                regex_string += regex_part
                generic_regex_for_name.append(
                    _create_generic_regex(name, idx, last_index_of_type, regex_part)
                )

            current_type = _determine_char_type(char)
            last_index_of_type = 0
    return regex_string, generic_regex_for_name


def _get_series_regex_matrix(names):
    """This function finds:
     * all global regex - i.e. trying to match entire series names and
     * generic regex subsets of these global regex containing sequences of [a-zA-Z] or digits
    Several extensions are possible:
     * creating specific regex by taking parts of the actual series names
     * grouping based on np.unique on location wise matches to the generic regex subsets
     * removing location specific matches
     * removing start / end matches
    """
    series_regex_matrix = pd.DataFrame(data={"blank": False}, index=names)

    generic_regex = set()

    # Global complete RegEx structure
    while not series_regex_matrix.any(1).all():
        current_name = series_regex_matrix[(~series_regex_matrix).all(1)].index[0]

        regex_string, generic_for_name = _get_regex_based_on_name(current_name)

        matches = series_regex_matrix.index.str.match(regex_string)
        matches_column = pd.DataFrame(data={regex_string: matches}, index=names)
        series_regex_matrix = pd.concat([series_regex_matrix, matches_column], axis=1)

        generic_regex = generic_regex.union(generic_for_name)

    # For each generic RegEx add a column
    for expression in generic_regex:
        matches = series_regex_matrix.index.str.match(expression)
        matches_column = pd.DataFrame(data={expression: matches}, index=names)
        series_regex_matrix = pd.concat([series_regex_matrix, matches_column], axis=1)
    return series_regex_matrix


def _run_regex_recommendation(inputs: List[AnalysisInput]) -> List[List[UUID]]:
    relevant_series_ids = np.array(
        [analysis_input.metadata.series.series_id for analysis_input in inputs]
    )
    names = np.array(
        [
            analysis_input.metadata.series.name
            for analysis_input in inputs
            if analysis_input.metadata.series.name not in ("", None)
        ]
    )

    # Create matrix and only keep non-trivial groups (2-4) members for now
    min_members = 2
    max_members = len(inputs) - 1
    series_regex_matrix = _get_series_regex_matrix(names).reset_index(drop=True)
    relevant_idx = (series_regex_matrix.sum() >= min_members) & (
        series_regex_matrix.sum() <= max_members
    )
    rel_groups = series_regex_matrix.loc[:, relevant_idx]

    connected_groups = []
    for i in range(rel_groups.shape[1]):
        connected_groups.append(
            np.array(rel_groups.reset_index(drop=True).index[rel_groups.iloc[:, i]])
        )

    unique_cg = [list(x) for x in set(tuple(x) for x in connected_groups)]

    return [relevant_series_ids[group] for group in unique_cg]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = analysis_input.inputs

    suggestions = _run_regex_recommendation(inputs)
    return AnalysisResult(
        series_sets={
            "naming pattern": [
                [SeriesId(suggestion) for suggestion in group] for group in suggestions
            ],
        }
    )
