"""
FreeCAD macro to visualize wind turbine using default values.
"""
from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   visualize)

parameters = get_default_parameters(WindTurbine.T_SHAPE)

wind_turbine_model = visualize(
    parameters['magnafpm'],
    parameters['user'], 
    parameters['furling'])

obj_file_contents = wind_turbine_model.to_obj()

with open('wind-turbine.obj', 'w') as f:
    f.write(obj_file_contents)
    print('wind-turbine.obj created.')
