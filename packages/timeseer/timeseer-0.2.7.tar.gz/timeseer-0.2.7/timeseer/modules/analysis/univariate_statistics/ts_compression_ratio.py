"""The compression ratio based on sampling ratio."""

from timeseer.metadata import fields
from timeseer import AnalysisInput, AnalysisResult, Statistic

_STATISTIC_NAME = "Compression ratio"

META = {
    "statistics": [{"name": _STATISTIC_NAME}],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    sampling_rate = analysis_input.metadata.get_field(fields.SamplingRate)
    if sampling_rate is None:
        return AnalysisResult(condition_message="No sampling rate")
    meas_times = analysis_input.data.index.to_series()
    diff = meas_times[-1] - meas_times[0]
    range_seconds = diff.total_seconds()
    if range_seconds < sampling_rate:
        return AnalysisResult(statistics=[Statistic(_STATISTIC_NAME, "pct", 0)])
    original_count = int(range_seconds / sampling_rate) + 1
    compressed_count = len(analysis_input.data)
    compression_ratio = 100 * (1 - compressed_count / original_count)

    return AnalysisResult(
        statistics=[Statistic(_STATISTIC_NAME, "pct", compression_ratio)]
    )
