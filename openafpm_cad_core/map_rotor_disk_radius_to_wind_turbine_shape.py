from .wind_turbine_shape import WindTurbineShape

__all__ = ['map_rotor_disk_radius_to_wind_turbine_shape']

H_SHAPE_LOWER_BOUND = 187.5
STAR_SHAPE_LOWER_BOUND = 275


def map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius: float) -> WindTurbineShape:
    if rotor_disk_radius < H_SHAPE_LOWER_BOUND:
        return WindTurbineShape.T
    elif rotor_disk_radius < STAR_SHAPE_LOWER_BOUND:
        return WindTurbineShape.H
    else:
        return WindTurbineShape.STAR
