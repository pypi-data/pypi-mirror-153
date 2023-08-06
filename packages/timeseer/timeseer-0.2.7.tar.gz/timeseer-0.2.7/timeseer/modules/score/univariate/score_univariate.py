"""Timeseer score module that generates scores for non-metadata checks."""

from typing import Any, Dict

from timeseer import ScoreInput, ScoreOutput, ScoreResult

META: Dict[str, Any] = {
    "scores": [],  # accept all leftover checks
}


# pylint: disable=missing-function-docstring
def score(
    score_input: ScoreInput,
) -> ScoreOutput:
    return ScoreOutput(
        [
            ScoreResult(result.name, result.result)
            for result in score_input.check_results
        ]
    )
