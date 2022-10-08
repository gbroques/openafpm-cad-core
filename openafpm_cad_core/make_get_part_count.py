import logging
from collections import defaultdict
from typing import Any, Callable, List

import FreeCAD as App
from FreeCAD import Document

from .find_object_by_label import find_object_by_label

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link', 'Part::Mirroring'}


def make_get_part_count(root_documents: List[Document],
                        number_of_coils_per_phase: int) -> Callable[[object], int]:
    count_by_label_and_type_id = defaultdict(int)

    delimiter = ';'

    def visit(obj: object) -> None:
        if obj.TypeId not in ASSEMBLY_TYPE_IDS:
            label_and_type_id = obj.Label + delimiter + obj.TypeId
            count_by_label_and_type_id[label_and_type_id] += 1
    for root_document in root_documents:
        root_object = find_object_by_label(root_document, root_document.Name)
        traverse([root_object], visit)

    for label_and_type_id in count_by_label_and_type_id.keys():
        label, type_id = label_and_type_id.split(delimiter)
        if label.startswith('Stator_CoilWinder'):
            count_by_label_and_type_id[label_and_type_id] *= number_of_coils_per_phase
        if label.startswith('Rotor_Mold'):
            # Assume user wants 2 rotor molds since it's generally
            # easier to cast both rotors at the same time.
            count_by_label_and_type_id[label_and_type_id] *= 2
        # Subtract 2 from count of back rotor disk to account for Magnet Jig & Rotor Mold assemblies.
        if label.startswith('Rotor_Disk_Back'):
            count_by_label_and_type_id[label_and_type_id] -= 2

    def get_part_count(obj: object) -> int:
        return count_by_label_and_type_id[obj.Label + delimiter + obj.TypeId]
    return get_part_count


def traverse(objects: List[object],
             visit: Callable[[object, list], Any]) -> None:
    for obj in objects:
        visit(obj)
        if obj.TypeId in ASSEMBLY_TYPE_IDS:
            children = _get_children(obj)
            if any([child is None for child in children]):
                logging.warn(f'child of {obj.Label} ({obj.TypeId}) is None.')
                documents = list(App.listDocuments().keys())
                document_list = '\n'.join(documents)
                logging.warn('Document List:\n%s', document_list)
            traverse(children, visit)


def _get_children(obj):
    if obj.TypeId == 'App::Part':
        return obj.Group
    elif obj.TypeId == 'App::Link':
        return [obj.LinkedObject]
    elif obj.TypeId == 'Part::Mirroring':
        return [obj.Source]
    else:
        return []
