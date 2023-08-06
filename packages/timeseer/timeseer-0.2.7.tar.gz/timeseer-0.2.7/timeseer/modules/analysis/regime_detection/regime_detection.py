"""Regime detection event frames.

<p></p>"""

from datetime import timedelta
from typing import Optional

import numpy as np
import pandas as pd
import pymannkendall as mk

from pandas.api.types import is_string_dtype
from ruptures import Pelt

import timeseer

from timeseer import DataType
from timeseer.analysis.utils import event_frames_from_dataframe

META = {
    "event_frames": ["Regime"],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _is_frame_long_enough(frame):
    return (frame.end_date - frame.start_date) >= timedelta(weeks=1)


def _filter_event_frames(all_frames):
    filter_iterator = filter(_is_frame_long_enough, all_frames)
    return filter_iterator


def _get_event_frames(df: pd.DataFrame, breakpoints, idx, interval_type):
    event_frames = pd.DataFrame(columns=["start_date", "end_date", "type"])

    start_dates = df.iloc[breakpoints[idx] - 1]
    end_dates = df.iloc[breakpoints[idx + 1] - 1]

    event_frames["start_date"] = start_dates["value"].index
    event_frames["end_date"] = end_dates["value"].index
    event_frames["type"] = interval_type

    return event_frames_from_dataframe(event_frames)


def _run_regime_detection(df2: pd.DataFrame) -> Optional[list[timeseer.EventFrame]]:
    df = df2.resample("1D").median().interpolate("time").dropna()

    if len(df) == 0:
        return None

    values = df["value"].values.flatten()
    penalty_value = 1
    model = "l1"
    min_size = 10
    jump = 5
    algo = Pelt(model=model, min_size=min_size, jump=jump).fit(values)
    breakpoints = np.array(algo.predict(pen=penalty_value))
    #  For each section check drift with MK
    idx = [
        i
        for i in range(len(breakpoints) - 1)
        if (breakpoints[i + 1] - breakpoints[i]) > 20
        and mk.original_test(
            values[breakpoints[i] + jump : breakpoints[i + 1] - jump], alpha=0.001
        ).trend
        == "no trend"
    ]
    if len(idx) == 0 or len(breakpoints) == 0:
        return []
    return list(
        _filter_event_frames(
            _get_event_frames(df, breakpoints, np.array(idx), "Regime")
        )
    )


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if is_string_dtype(analysis_input.data["value"]):
        return timeseer.AnalysisResult()
    frames = _run_regime_detection(analysis_input.data)
    if frames is None:
        return timeseer.AnalysisResult()
    return timeseer.AnalysisResult(event_frames=frames)
