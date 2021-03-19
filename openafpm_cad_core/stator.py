import os

from .common import enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['make_stator']


def make_stator(base_path,
                document,
                stator_name,
                coils):
    stator_path = os.path.join(base_path, 'Stator')

    stator_resin_cast_label = 'StatorResinCast'
    _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label)
    stator_resin_cast = find_object_by_label(document, stator_resin_cast_label)

    stator = document.addObject('App::DocumentObjectGroup', stator_name)

    stator.addObjects([
        stator_resin_cast,
        coils
    ])
    return stator


def _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label):
    document.mergeProject(
        os.path.join(stator_path, stator_resin_cast_label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
