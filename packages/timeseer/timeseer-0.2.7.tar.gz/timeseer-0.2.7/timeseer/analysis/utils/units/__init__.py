"""Utility functions for unit conversions."""

from pathlib import Path
from pint import UnitRegistry


def get_unit_registry() -> UnitRegistry:
    """Return a pint UnitRegistry configured for Timeseer."""
    return UnitRegistry(str(Path(__file__).parent.resolve()) + "/default_replace.txt")
