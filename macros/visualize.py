"""
FreeCAD macro to visualize wind turbine using default values.
"""
from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   visualize)

turbine = WindTurbine.STAR_SHAPE
parameters = get_default_parameters(turbine)

wind_turbine_model = visualize(
    parameters['magnafpm'],
    parameters['user'],
    parameters['furling'])

obj_file_contents = wind_turbine_model.to_obj()

filename = turbine.value.lower().replace(' ', '-')
with open(f'{filename}.obj', 'w') as f:
    f.write(obj_file_contents)
    print(f'{filename}.obj created.')
