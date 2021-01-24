import Draft
import FreeCAD as App
from FreeCAD import Placement, Vector, Rotation

from .common import make_compound


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
    threads = _create_polar_array(thread, n, hub_holes_placement)
    return make_compound(document, name, threads)


def _create_polar_array(part, n, y_offset):
    array = [part]
    Draft.move(part, Vector(0, y_offset, 0))
    exterior_angle = _calculate_exterior_angle(n)
    App.DraftWorkingPlane.alignToPointAndAxis(
        Vector(0, 0, 0), Vector(0, 0, 1), 0)
    previous = part
    for i in range(n - 1):
        clone = Draft.clone(previous)
        Draft.rotate(clone, exterior_angle, Vector(
            0, 0, 0), axis=Vector(0, 0, 1), copy=False)
        array.append(clone)
        previous = clone
    return array


def _calculate_exterior_angle(n):
    """
    Calculate exterior angle for an "n" sided regular polygon.

    Reference:
    https://www.mathsisfun.com/geometry/regular-polygons.html
    """
    return 360 / n
