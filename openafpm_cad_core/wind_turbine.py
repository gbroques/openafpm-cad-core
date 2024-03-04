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

    T_SHAPE_2F = 'T Shape 2F'
    """2 meter diameter wind turbine with a T-shape frame and (F)errite magnets.

    Useful for testing triangular coils and the outer magnet jig.
    """
    H_SHAPE_4F = 'H Shape 4F'
    """4 meter diameter wind turbine with a H-shape frame and (F)errite magnets.

    Useful for testing triangular coils with a reduced coil leg width.
    """
