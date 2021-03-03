from FreeCAD import Placement, Rotation, Vector

from .common import create_polar_array, make_compound


def make_rotor_magnets(document,
                       length,
                       width,
                       thickness,
                       number_of_magnets,
                       rotor_radius):
    magnet = make_magnet(document, length, width, thickness)
    y_offset = rotor_radius - length
    array = create_polar_array(magnet, number_of_magnets, y_offset)
    return make_compound(document, 'Magnets', array)


def make_magnet(document,
                length,
                width,
                thickness):
    magnet = document.addObject('Part::Box', 'Magnet')
    magnet.Length = length
    magnet.Width = width
    magnet.Height = thickness
    magnet.Placement = Placement(
        Vector(width / 2, 0, thickness), Rotation(Vector(0, 0, 1), 90))
    return magnet
