"""Last updated point should not be longer ago than a user-specified number of seconds.
"""

from datetime import timedelta

from timeseer import AnalysisInput, AnalysisResult, EventFrame

_CHECK_NAME = "Data older than threshold"
_EVENT_FRAME_NAME = "Data older than threshold"

META: dict = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


def _is_last_point_old(analysis_input: AnalysisInput) -> bool:
    last_recorded_time = analysis_input.data.index[-1]
    last_evaluation_date = analysis_input.evaluation_time_range.end_date

    threshold = analysis_input.parameters["threshold"]
    cutoff_date = last_evaluation_date - timedelta(seconds=threshold)
    return last_recorded_time <= cutoff_date


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(analysis_input.data) == 0:
        return "No data", False
    if "threshold" not in analysis_input.parameters:
        return "No threshold parameter provided", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    is_too_old = _is_last_point_old(analysis_input)
    event_frames = []
    if is_too_old is True:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.data.index[-1].to_pydatetime(),
                end_date=analysis_input.evaluation_time_range.end_date,
            )
        )
    return AnalysisResult(event_frames=event_frames)
