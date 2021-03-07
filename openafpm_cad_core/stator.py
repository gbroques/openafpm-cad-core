import os

import FreeCAD as App

from .coil import make_coils
from .common import enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['make_stator']


def make_stator(base_path,
                has_separate_master_files,
                document,
                stator_name,
                number_of_coils,
                inner_stator_hole_radius):
    stator_path = os.path.join(base_path, 'Stator')
    if has_separate_master_files:
        _open_stator_master(stator_path)

    stator_resin_cast_label = 'StatorResinCast'
    _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label)
    stator_resin_cast = find_object_by_label(document, stator_resin_cast_label)

    coils = make_coils(stator_path, document,
                       number_of_coils, inner_stator_hole_radius)

    stator = document.addObject('App::DocumentObjectGroup', stator_name)

    stator.addObjects([
        stator_resin_cast,
        coils
    ])
    return stator


def _open_stator_master(stator_path):
    App.openDocument(os.path.join(stator_path, 'MasterStator.FCStd'))


def _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label):
    document.mergeProject(
        os.path.join(stator_path, stator_resin_cast_label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
