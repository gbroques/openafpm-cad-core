import sys

from FreeCAD import Console, Vector
import Draft


def enforce_recompute_last_spreadsheet(document):
    sheets = document.findObjects('Spreadsheet::Sheet')
    last_sheet = sheets[len(sheets) - 1]
    last_sheet.enforceRecompute()


def make_compound(document, name, objects):
    compound = document.addObject('Part::Compound', name)
    compound.Links = objects
    return compound


def _with_error_exit(find_object_by_label):
    def wrapped(document, label):
        result = find_object_by_label(document, label)
        if result is None:
            Console.PrintError(
                'No object with Label "{}" found in document. Check {}.FCStd.'.format(label, label))
            sys.exit(1)
        return result
    return wrapped


@_with_error_exit
def find_object_by_label(document, label):
    objects = document.getObjectsByLabel(label)
    if len(objects) == 0:
        return None
    return objects[0]


def find_expression(expression_engine_tuples, key):
    matches = list(
        filter(lambda pair: pair[0] == key, expression_engine_tuples))
    if len(matches) == 0:
        return None
    return matches[0]


def clone_body(document, name, body_to_clone):
    body = document.addObject('PartDesign::Body', name)
    clone = document.addObject(
        'PartDesign::FeatureBase', body_to_clone.Label + 'Clone')
    clone.BaseFeature = body_to_clone
    clone.Placement = body_to_clone.Placement
    body.Group = [clone]
    body.Tip = clone
    return body


# TODO: Use https://wiki.freecadweb.org/Draft_PolarArray
#       when upgrading to FreeCAD 19.
def create_polar_array(part, n, y_offset):
    array = [part]
    Draft.move(part, Vector(0, y_offset, 0))
    exterior_angle = _calculate_exterior_angle(n)
    previous = part
    for i in range(n - 1):
        copy = Draft.rotate(previous, exterior_angle, Vector(
            0, 0, 0), axis=Vector(0, 0, 1), copy=True)
        array.append(copy)
        previous = copy
    return array


def _calculate_exterior_angle(n):
    """
    Calculate exterior angle for an "n" sided regular polygon.

    Reference:
    https://www.mathsisfun.com/geometry/regular-polygons.html
    """
    return 360 / n
