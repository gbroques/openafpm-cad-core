from collections import defaultdict
from typing import Any, Callable, List

from .find_object_by_label import find_object_by_label
from .load import load_all
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link', 'Part::Mirroring'}


def get_part_count(magnafpm_parameters: MagnafpmParameters,
                   furling_parameters: FurlingParameters,
                   user_parameters: UserParameters):
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters)
    count_by_label_and_type_id = defaultdict(int)

    def visit(obj: object) -> None:
        if obj.TypeId not in ASSEMBLY_TYPE_IDS:
            label_and_type_id = obj.Label + ':' + obj.TypeId
            count_by_label_and_type_id[label_and_type_id] += 1
    for root_document in root_documents:
        root_object = find_object_by_label(root_document, root_document.Name)
        traverse([root_object], visit)
    return count_by_label_and_type_id


def traverse(objects: List[object],
             visit: Callable[[object, list], Any]) -> None:
    for obj in objects:
        visit(obj)
        if obj.TypeId in ASSEMBLY_TYPE_IDS:
            children = _get_children(obj)
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
