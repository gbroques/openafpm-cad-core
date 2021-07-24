"""
Module defining wind turbine variants.
"""

from enum import Enum, unique

__all__ = ['WindTurbine']


@unique
class WindTurbine(Enum):
    """Enumeration of wind turbine variants."""
    T_SHAPE = 'T Shape'
    H_SHAPE = 'H Shape'
    STAR_SHAPE = 'Star Shape'
