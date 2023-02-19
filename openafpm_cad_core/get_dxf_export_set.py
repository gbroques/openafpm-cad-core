from typing import List, Set

from FreeCAD import Document

from .find_object_by_label import find_object_by_label

FLAT_ATTRIBUTE = 'Openafpm_Flat'


__all__ = ['get_dxf_export_set']

def get_dxf_export_set(root_documents: List[Document]) -> Set[object]:
    export_set = set()
    for document in root_documents:
        root_object = find_object_by_label(document, document.Name)
        export_set.update(get_flat_objects([root_object], set()))
    return export_set


def get_flat_objects(
        objects: List[object],
        flat_objects: List[object] = set()) -> Set[object]:
    for child in objects:
        if child.Visibility:
            if child.TypeId == 'App::Link':
                get_flat_objects([child.LinkedObject], flat_objects)
            elif child.TypeId == 'App::Part':
                get_flat_objects(child.Group, flat_objects)
            elif hasattr(child, FLAT_ATTRIBUTE) and getattr(child, FLAT_ATTRIBUTE):
                flat_objects.add(child)
    return flat_objects
