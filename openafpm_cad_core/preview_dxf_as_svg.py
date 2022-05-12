from itertools import groupby
from typing import Iterator, List, Optional, Set, Tuple, TypedDict

import Draft
from FreeCAD import BoundBox, Console, Units

from .get_2d_projection import get_2d_projection


class FlatObject(TypedDict):
    label: str
    svg: str
    bound_box: BoundBox
    material: str
    thickness: float


def preview_dxf_as_svg(export_set: Set[object],
                       precision: int = 2,
                       font_size: int = 72,
                       font_family: str = 'sans-serif',
                       padding: int = 16,
                       row_gap: int = 64,
                       column_gap: int = 32,
                       text_margin_bottom: int = 48,
                       stroke_width: float = 2.5,
                       foreground: str = '#FFFFFF',
                       background: str = '#000000') -> str:
    """Preview the DXF export as SVG.

    Flat parts are grouped by material and thickness.

    Some of the following code is adapted from importSVG.export:
    https://github.com/FreeCAD/FreeCAD/blob/0.19.4/src/Mod/Draft/importSVG.py#L1772-L1883
    """
    flat_objects = [
        get_flat_object(o, precision, stroke_width, foreground)
        for o in export_set
    ]
    svg_elements = []
    # Keep track of the widest row, or the width of the SVG document.
    width = 0
    group_y = 0  # Keep track of the height of the SVG document.
    group_y += padding
    for flat_objects, material, thickness in iterate_by_material_and_thickness(flat_objects):
        group_x = 0
        group_x += padding
        group_y += font_size
        formatted_thickness = '{:.2f}'.format(thickness)
        text_element = get_text_element(
            group_x, group_y, material, formatted_thickness, font_size, font_family, foreground)
        svg_elements.append(text_element)
        group_y += text_margin_bottom
        y_max = 0  # Keep track of the tallest object in each row.
        for flat_object in flat_objects:
            bound_box = flat_object['bound_box']
            x = group_x + -bound_box.XMin
            y = group_y + bound_box.YMax
            group_element = get_group_element(
                x, y, flat_object['label'], flat_object['svg'])
            svg_elements.append(group_element)
            group_x += bound_box.XLength
            group_x += padding
            if group_x > width:
                width = group_x
            group_x += column_gap
            if bound_box.YLength > y_max:
                y_max = bound_box.YLength
        group_y += y_max
        group_y += row_gap
        group_y += padding
    return (
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {group_y}">' +
        f'<rect width="100%" height="100%" fill="{background}"/>' +
        '\n'.join(svg_elements) +
        '</svg>'
    )


def get_text_element(x, y, material, thickness, font_size, font_family, fill) -> str:
    unit = get_unit()
    return (
        f'<text x="{x}" y="{y}" font-size="{font_size}" font-family="{font_family}" fill="{fill}">'
        f'{material} {thickness} {unit}' +
        f'</text>'
    )


def get_group_element(x, y, title, children) -> str:
    return (
        # pointer-events bounding-box,
        # for displaying title when hovering over parts where the path isn't filled in.
        # See: https://stackoverflow.com/a/19845004
        f'<g transform="translate({x}, {y}) scale(1, -1)" pointer-events="bounding-box">' +
        f'<title>{title}</title>' +
        children +
        '</g>'
    )


def iterate_by_material_and_thickness(flat_objects: List[FlatObject]) -> Iterator[Tuple[List[object], str, float]]:
    for key, grouped_objects in group_by_material_and_thickness(flat_objects).items():
        sorted_objects = sort_by_bound_box_then_label_descending(
            grouped_objects)
        material, thickness = key
        yield sorted_objects, material, thickness


def sort_by_bound_box_then_label_descending(flat_objects: List[FlatObject]) -> List[FlatObject]:
    return sorted(
        flat_objects,
        key=lambda o: (o['bound_box'].DiagonalLength, o['label']),
        reverse=True)


def group_by_material_and_thickness(objects: List[FlatObject]) -> dict:
    def keyfunc(obj):
        return (obj['material'], obj['thickness'])
    sorted_objects = sorted(objects, key=keyfunc)
    iterator = groupby(sorted_objects, key=keyfunc)
    return {k: list(v) for k, v in iterator}


def get_flat_object(obj: object,
                    precision: int = 2,
                    stroke_width: float = 2.5,
                    foreground: str = '#FFFFFF') -> FlatObject:
    two_dimensional_projection = get_2d_projection(obj)
    svg = Draft.get_svg(two_dimensional_projection,
                        linewidth=stroke_width, color=foreground)
    bound_box = get_bound_box(two_dimensional_projection)
    return {
        'label': obj.Label,
        'svg': svg,
        'bound_box': bound_box,
        'material': get_material(obj),
        'thickness': round(get_thickness(obj), ndigits=precision)
    }


def get_thickness(obj: object) -> float:
    bound_box = obj.Shape.optimalBoundingBox()
    return min([
        bound_box.XLength,
        bound_box.YLength,
        bound_box.ZLength
    ])


def get_unit() -> str:
    # https://forum.freecadweb.org/viewtopic.php?f=10&t=48451&start=10#p415233
    return Units.schemaTranslate(
        Units.Quantity(1, Units.Length),
        Units.getSchema())[2]


def get_material(obj: object) -> str:
    if is_wooden(obj.Label):
        return 'Plywood'
    else:
        return 'Steel'


def is_wooden(label: str) -> bool:
    wooden_labels = ['Tail_Vane']
    wooden_label_fragments = ['Mold', 'CoilWinder']
    return (
        any([wooden_label == label for wooden_label in wooden_labels]) or
        any([fragment in label for fragment in wooden_label_fragments])
    )


def get_bound_box(obj: object) -> Optional[BoundBox]:
    bound_box = BoundBox()
    if (hasattr(obj, 'Shape')
            and obj.Shape
            and obj.Shape.BoundBox.isValid()):
        bound_box.add(obj.Shape.BoundBox)
    else:
        Console.PrintWarning(
            f'{obj.Label} has no Shape, calculating manual bounding box.')
        bound_box.add(Draft.get_bbox(obj))

    if not bound_box.isValid():
        Console.PrintError(
            f'{obj.Label} does not have a a valid bounding box.')
        return None
    return bound_box
