import sys

from FreeCAD import Console


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
