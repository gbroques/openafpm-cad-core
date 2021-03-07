import Draft
from FreeCAD import Placement, Vector, Rotation

from .common import make_compound, create_polar_array


__all__ = ['make_hub_threads']


def make_hub_threads(document,
                     name,
                     radius,
                     length,
                     n,
                     hub_holes_placement,
                     z_offset):
    thread = document.addObject('Part::Cylinder', 'Thread')
    thread.Placement = Placement(
        Vector(0, 0, z_offset), Rotation(Vector(0, 1, 0), 180))
    thread.Radius = radius
    thread.Height = length
    threads = create_polar_array(thread, n, hub_holes_placement)
    return make_compound(document, name, threads)
