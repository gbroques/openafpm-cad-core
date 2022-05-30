"""
FreeCAD macro to get part count.
"""
import json

from openafpm_cad_core.app import WindTurbine, get_default_parameters
from openafpm_cad_core.get_part_count import get_part_count

parameters = get_default_parameters(WindTurbine.T_SHAPE)
count_by_label_and_type_id = get_part_count(
    parameters['magnafpm'],
    parameters['furling'],
    parameters['user'])
print(json.dumps(count_by_label_and_type_id, indent=2))
