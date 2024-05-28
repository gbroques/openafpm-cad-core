from .wind_turbine_shape import WindTurbineShape


def map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius: float) -> WindTurbineShape:
    if rotor_disk_radius < 187.5:
        return WindTurbineShape.T
    elif rotor_disk_radius < 275:
        return WindTurbineShape.H
    else:
        return WindTurbineShape.STAR
