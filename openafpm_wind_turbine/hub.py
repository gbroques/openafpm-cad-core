import os
from FreeCAD import Placement, Vector

from .common import find_object_by_label, make_compound

__all__ = ['make_hub']


def make_hub(base_path,
             document,
             name,
             stub_axle_shaft_z_offset):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    hub_path = os.path.join(base_path, 'Hub')

    stub_axle_shaft_label = 'StubAxleShaft'
    _merge_document(document, hub_path, stub_axle_shaft_label)
    stub_axle_shaft = find_object_by_label(document, stub_axle_shaft_label)
    move_stub_axle_shaft(stub_axle_shaft, stub_axle_shaft_z_offset)

    flange_label = 'Flange'
    _merge_document(document, hub_path, flange_label)
    flange = find_object_by_label(document, flange_label)
    # Flange contains formula references to external cross-document spreadsheet
    if hasattr(flange, 'Group'):
        for item in flange.Group:
            item.enforceRecompute()

    return make_compound(document, name, [
        stub_axle_shaft,
        flange
    ])


def _merge_document(document, path, name):
    document.mergeProject(
        os.path.join(path, name + '.FCStd'))


def move_stub_axle_shaft(stub_axle_shaft, z_offset):
    placement = Placement()
    placement.move(Vector(0, 0, z_offset))
    stub_axle_shaft.Placement = placement
