"""
Module defining wind turbine variants or types.
"""

from enum import Enum, unique

__all__ = ['WindTurbine']


@unique
class WindTurbine(Enum):
    T_SHAPE = 'T Shape'
    H_SHAPE = 'H Shape'
    STAR_SHAPE = 'Star Shape'
