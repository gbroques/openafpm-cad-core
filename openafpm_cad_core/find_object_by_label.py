from typing import Optional

from FreeCAD import Console, Document

__all__ = ['find_object_by_label']


def find_object_by_label(document: Document, label: str) -> Optional[object]:
    """Find an object in a document by the given label.

    Returns ``None`` if no object is found.
    """
    objects = document.getObjectsByLabel(label)
    if len(objects) == 0:
        Console.PrintError(
            f'No object with Label "{label}" found in document. Check {document.Name}.FCStd.')
        return None
    return objects[0]
