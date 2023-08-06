"""Time series data should have strict increasing timestamps.

<p>Duplicate time stamps can occur because of connection issues, causing the system
to rely on buffered data. Another common cause for duplicates is the daylight saving time
not handled correctly in the source.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
Misaligned ordering of timestamps can hamper (automated) downstream analytics.
</p>
</div>
"""

from datetime import timedelta, timezone

from timeseer import AnalysisInput, AnalysisResult, EventFrame

_CHECK_NAME = "No duplicate timestamps"
_EVENT_FRAME_NAME = "Duplicate timestamp"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "kpi": "Integrity",
            "data_type": "bool",
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 2}],
    "signature": "univariate",
}


def _find_duplicate_timestamps(df):
    duplicates = df.loc[
        df.index.to_series().diff() == timedelta(0)
    ].index.drop_duplicates(keep="last")
    for ts in duplicates.array:
        py_ts = ts.to_pydatetime().replace(tzinfo=timezone.utc)
        yield EventFrame(_EVENT_FRAME_NAME, py_ts, py_ts)


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    duplicate_timestamps = list(_find_duplicate_timestamps(analysis_input.data))
    return AnalysisResult(event_frames=duplicate_timestamps)
