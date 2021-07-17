from typing import Callable, List

from FreeCAD import Placement

__all__ = ['resolve_objects']

ASSEMBLY_TYPE_IDS = {'App::Part', 'App::Link'}


def resolve_objects(objects: List[object],
                    keep_unresolved: Callable[[
                        object, List[object]], bool] = None,
                    path: list = [],
                    parent_placement: Placement = None,
                    chain: bool = True) -> dict:
    resolved = []
    for obj in objects:
        placement = obj.Placement
        if parent_placement:
            if chain:
                placement = parent_placement * placement
            else:
                placement = parent_placement
        stay_unresolved = keep_unresolved and keep_unresolved(obj, path)
        if obj.TypeId in ASSEMBLY_TYPE_IDS and not stay_unresolved:
            args = _get_resolve_objects_args(
                obj, keep_unresolved, path, placement)
            dictionaries = resolve_objects(*args)
            resolved.extend(dictionaries)
        else:
            if stay_unresolved and obj.TypeId == 'App::Link' and obj.LinkTransform:
                placement = placement * obj.LinkedObject.Placement
            resolved.append({
                'object': obj,
                'placement': placement,
                'path': path
            })
    return resolved


def _get_resolve_objects_args(obj, keep_unresolved, path, placement):
    path_with_obj = path + [obj]
    if obj.TypeId == 'App::Part':
        return [
            obj.Group,
            keep_unresolved,
            path_with_obj,
            placement,
            True
        ]
    elif obj.TypeId == 'App::Link':
        return [
            [obj.LinkedObject],
            keep_unresolved,
            path_with_obj,
            placement,
            obj.LinkTransform
        ]
