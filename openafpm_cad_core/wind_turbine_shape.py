"""Module defining wind turbine shapes.
"""

from enum import Enum, unique

__all__ = ['WindTurbineShape']


@unique
class WindTurbineShape(Enum):
    """Enumeration of wind turbine shapes."""

    T = 'T Shape'
    """Smallest wind turbine with a frame shaped like a "T"."""

    H = 'H Shape'
    """Medium-sized wind turbine with a frame shaped like an "H"."""

    STAR = 'Star Shape'
    """Largest wind turbine with a frame shaped like a six-pointed star."""
