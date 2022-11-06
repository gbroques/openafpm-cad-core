from typing import List

import FreeCAD  # Needed for freecad_to_obj Draft dependency
import freecad_to_obj

from .find_object_by_label import find_object_by_label
from .load import Assembly, load_assembly
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['assembly_to_obj']


def assembly_to_obj(assembly: Assembly,
                    magnafpm_parameters: MagnafpmParameters,
                    furling_parameters: FurlingParameters,
                    user_parameters: UserParameters) -> str:
    root_document, spreadsheet_document = load_assembly(assembly,
                                                        magnafpm_parameters,
                                                        furling_parameters,
                                                        user_parameters)
    obj = find_object_by_label(
        root_document, root_document.Name)
    export_kwargs = get_export_kwargs(assembly)
    obj_file_contents = freecad_to_obj.export([obj], **export_kwargs)
    return obj_file_contents


def get_export_kwargs(assembly: Assembly):
    if assembly == Assembly.WIND_TURBINE:
        return {
            'object_name_getter': object_name_getter,
            'keep_unresolved': keep_unresolved_for_wind_turbine
        }
    elif assembly == Assembly.STATOR_MOLD:
        return {
            'keep_unresolved': keep_unresolved_for_stator_mold
        }
    else:
        return {}


def object_name_getter(obj: object, path: List[object]) -> str:
    rotor_disk_labels = {
        'Rotor_ResinCast',
        'Rotor_Magnets'
    }
    if obj.Label in rotor_disk_labels:
        is_front = any([o.Label.endswith('Front') for o in path])
        label_suffix = 'Front' if is_front else 'Back'
        return obj.Label + '_' + label_suffix
    return obj.Label


def keep_unresolved_for_wind_turbine(obj: object, path: List[object]) -> bool:
    return obj.Label in {
        'Frame',
        'YawBearing',
        'Tail_Hinge_Outer',
        'Tail_Hinge_Inner',
        'Vane_Bracket_Top',
        'Tail_Stop_HighEnd'
    }


def keep_unresolved_for_stator_mold(obj: object, path: List[object]) -> bool:
    return obj.Label in {
        'LocatingBolts',
        'Bolts',
        'Nuts',
        'Screws'
    }
