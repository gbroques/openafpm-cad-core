import os

import FreeCAD as App

from .common import (create_polar_array, enforce_recompute_last_spreadsheet,
                     find_object_by_label, make_compound)

__all__ = ['make_coils']


def make_coils(common_path, document, number_of_coils, y_offset):
    App.setActiveDocument(document.Name)
    coil_label = 'Coil'
    _merge_coil(document, common_path, coil_label)
    coil = find_object_by_label(document, coil_label)
    document.recompute()
    coils = create_polar_array(coil, number_of_coils, y_offset)
    return make_compound(document, 'Coils', coils)


def _merge_coil(document, common_path, coil_label):
    document.mergeProject(
        os.path.join(common_path, coil_label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
