import os
from FreeCAD import Placement, Vector

from .common import find_object_by_label, make_compound

__all__ = ['make_hub']


def make_hub(base_path,
             document,
             name):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    hub_path = os.path.join(base_path, 'Hub')

    stub_axle_shaft_label = 'StubAxleShaft'
    _merge_document(document, hub_path, stub_axle_shaft_label)
    stub_axle_shaft = find_object_by_label(document, stub_axle_shaft_label)
    move_stub_axle_shaft(stub_axle_shaft)

    flange_label = 'Flange'
    _merge_document(document, hub_path, flange_label)
    flange = find_object_by_label(document, flange_label)

    hub = document.addObject('App::Part','Hub')
    hub.addObject(stub_axle_shaft)
    hub.addObject(flange)

    return hub


def _merge_document(document, path, name):
    document.mergeProject(
        os.path.join(path, name + '.FCStd'))


def move_stub_axle_shaft(stub_axle_shaft):
    placement = Placement()
    placement.move(Vector(0, 0, 50))
    stub_axle_shaft.Placement = placement
