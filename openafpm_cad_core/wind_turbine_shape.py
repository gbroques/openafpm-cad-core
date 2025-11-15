"""Module defining wind turbine shapes.
"""

from enum import Enum, unique

__all__ = [
    'H_SHAPE_LOWER_BOUND',
    'STAR_SHAPE_LOWER_BOUND',
    'WindTurbineShape',
    'map_rotor_disk_radius_to_wind_turbine_shape'
]

H_SHAPE_LOWER_BOUND = 187.5
STAR_SHAPE_LOWER_BOUND = 275


@unique
class WindTurbineShape(Enum):
    """Enumeration of wind turbine shapes."""

    T = 'T Shape'
    """Smallest wind turbine with a frame shaped like a "T"."""

    H = 'H Shape'
    """Medium-sized wind turbine with a frame shaped like an "H"."""

    STAR = 'Star Shape'
    """Largest wind turbine with a frame shaped like a six-pointed star."""

    @staticmethod
    def from_string(string: str):
        return WindTurbineShape[string.upper()]

    def to_string(self):
        return self.value.split()[0]


def map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius: float) -> WindTurbineShape:
    if rotor_disk_radius < H_SHAPE_LOWER_BOUND:
        return WindTurbineShape.T
    elif rotor_disk_radius < STAR_SHAPE_LOWER_BOUND:
        return WindTurbineShape.H
    else:
        return WindTurbineShape.STAR
