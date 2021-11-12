from pathlib import Path
from typing import List, TypedDict

import FreeCAD as App
from FreeCAD import Console, Document, Placement

from .find_object_by_label import find_object_by_label

__all__ = ['get_furl_transforms']


class Transform(TypedDict):
    """An object representing a 3D transformation in Axis–angle representation."""

    name: str
    """Name for transform."""

    position: List[float]
    """3 element list containing x, y, and z coordinates."""

    axis: List[float]
    """Axis of rotation, 3 element list for x, y, and z axes."""

    angle: float
    """Angle of rotation (in radians)."""


def get_furl_transforms(root_document: Document) -> List[Transform]:
    root_document_path = Path(root_document.FileName)
    documents_path = root_document_path.parent
    tail_document_path = documents_path.joinpath('Tail', 'Tail.FCStd')
    tail_document = App.openDocument(str(tail_document_path))
    tail = find_object_by_label(tail_document, 'Tail')
    if len(tail.InList) == 0:
        Console.PrintWarning(f'{tail.Label} has no parents.\n')
        return None
    if len(tail.InList) > 1:
        Console.PrintWarning(
            f'{tail.Label} has more than 1 parent. Choosing 1st.\n')
    tail_parent = tail.InList[0]
    parent_placement = calculate_global_placement(tail_parent)
    hinge_outer = find_object_by_label(tail_document, 'Hinge_Outer')
    return [
        placement_to_dict('parent', parent_placement),
        placement_to_dict('tail', tail.Placement),
        placement_to_dict('hinge', hinge_outer.Placement)
    ]


def placement_to_dict(name: str, placement: Placement) -> Transform:
    return {
        'name': name,
        'position': list(placement.Base),
        'axis': list(placement.Rotation.Axis),
        'angle': placement.Rotation.Angle
    }


def calculate_global_placement(child: object, placements: Placement = []) -> Placement:
    placements.append(child.Placement)
    in_list = child.InList
    num_in = len(in_list)
    if len(in_list) == 0:
        global_placement = Placement()
        placements.reverse()  # Reverse list in order of parent to child.
        for placement in placements:
            global_placement *= placement
        return global_placement
    if num_in > 1:
        Console.PrintWarning(
            f'{child.Label} has more than 1 parent. Choosing 1st.\n')
    parent = in_list[0]
    return calculate_global_placement(
        parent, placements
    )
