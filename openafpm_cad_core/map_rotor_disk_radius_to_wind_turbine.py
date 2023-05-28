from .wind_turbine import WindTurbine


def map_rotor_disk_radius_to_wind_turbine(rotor_disk_radius: float) -> WindTurbine:
    if rotor_disk_radius < 187.5:
        return WindTurbine.T_SHAPE
    elif rotor_disk_radius < 275:
        return WindTurbine.H_SHAPE
    else:
        return WindTurbine.STAR_SHAPE
