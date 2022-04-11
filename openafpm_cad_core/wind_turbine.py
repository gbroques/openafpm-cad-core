"""Module defining wind turbine variants.
"""

from enum import Enum, unique

__all__ = ['WindTurbine']


@unique
class WindTurbine(Enum):
    """Enumeration of wind turbine variants."""

    T_SHAPE = 'T Shape'
    """Smallest wind turbine with a frame shaped like a "T"."""

    H_SHAPE = 'H Shape'
    """Medium-sized wind turbine with a frame shaped like an "H"."""

    STAR_SHAPE = 'Star Shape'
    """Largest wind turbine with a frame shaped like a six-pointed star."""
