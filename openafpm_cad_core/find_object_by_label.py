import sys

from FreeCAD import Console

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
