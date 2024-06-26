from pathlib import Path
from typing import List, TypedDict

import FreeCAD as App
from FreeCAD import Console, Document, Placement

from .find_object_by_label import find_object_by_label
from .load import load_turbine
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['load_furl_transform']


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


class FurlTransform(TypedDict):
    """Transformation to furl the tail."""

    maximum_angle: float
    """The maximum angle (in degrees) the tail can furl
    before the high end stop hits the yaw bearing pipe.
    """

    transforms: List[Transform]
    """Series of 3D transformations needed to furl the tail."""


def load_furl_transform(magnafpm_parameters: MagnafpmParameters,
                        furling_parameters: FurlingParameters,
                        user_parameters: UserParameters) -> FurlTransform:
    root_document, spreadsheet_document = load_turbine(magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    return {
        'maximum_angle': get_maximum_furl_angle(spreadsheet_document),
        'transforms': get_furl_transforms(root_document)
    }


def get_maximum_furl_angle(spreadsheet_document: Document, ndigits: int = 2) -> float:
    return round(spreadsheet_document.HighEndStop.MaximumFurlAngle.Value, ndigits=ndigits)


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
