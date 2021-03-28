import os
from FreeCAD import Placement, Vector

from .common import find_object_by_label

__all__ = ['make_hub']


def make_hub(hub_path, document):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    hub_label = 'Hub'
    _merge_document(document, hub_path, hub_label)

    # Flange contains formula references to external cross-document spreadsheet
    # if hasattr(flange, 'Group'):
    #     for item in flange.Group:
    #         item.enforceRecompute()

    hub = find_object_by_label(document, hub_label)

    return hub


def _merge_document(document, path, name):
    document.mergeProject(
        os.path.join(path, name + '.FCStd'))
