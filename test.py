"""
FreeCAD Macro to test openafpm_cad_core package.
"""
import sys

sys.path.append('/home/g/Desktop/squashfs-root/usr/lib/')
from enum import Enum, unique

from openafpm_cad_core.app import get_default_parameters, visualize


@unique
class WindTurbine(Enum):
    T_SHAPE = 'T Shape'
    H_SHAPE = 'H Shape'
    STAR_SHAPE = 'Star Shape'

parameters = get_default_parameters(WindTurbine.T_SHAPE.value)

wind_turbine = visualize(
    parameters['magnafpm'],
    parameters['user'], 
    parameters['furling'])

obj_file_contents = wind_turbine.to_obj()

with open('wind-turbine.obj', 'w') as f:
    f.write(obj_file_contents)
    print('wind-turbine.obj created.')
