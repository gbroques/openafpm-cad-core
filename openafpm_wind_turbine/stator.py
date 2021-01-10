import os

import FreeCAD as App

from .common import enforce_recompute_last_spreadsheet

__all__ = ['load_stator']


def load_stator(base_path, has_separate_master_files, document, stator_resin_cast_label):
    stator_path = os.path.join(base_path, 'Stator')
    if has_separate_master_files:
        _open_stator_master(stator_path)
    _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label)


def _open_stator_master(stator_path):
    App.openDocument(os.path.join(stator_path, 'MasterStator.FCStd'))


def _merge_stator_resin_cast(document, stator_path, stator_resin_cast_label):
    document.mergeProject(
        os.path.join(stator_path, stator_resin_cast_label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
