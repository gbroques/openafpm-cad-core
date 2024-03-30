import math
from itertools import groupby
from typing import Callable, Iterator, List, Optional, Set, Tuple, TypedDict

import Draft
from FreeCAD import BoundBox, Console, Units

from .get_2d_projection import get_2d_projection

__all__ = ['export_set_to_svg', 'get_svg_style_options']


class FlatObject(TypedDict):
    label: str
    count: int
    svg: str
    bound_box: BoundBox
    material: str
    thickness: float


def export_set_to_svg(export_set: Set[object],
                      get_part_count: Callable[[object], int],
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
    """Transform the DXF export set to SVG.

    Flat parts are grouped by material and thickness.

    Some of the following code is adapted from importSVG.export:
    https://github.com/FreeCAD/FreeCAD/blob/0.19.4/src/Mod/Draft/importSVG.py#L1772-L1883
    """
    flat_objects = [
        get_flat_object(o, get_part_count, precision, stroke_width, foreground)
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
        unit = get_unit()
        text_element = get_text_element(
            group_x, group_y, f'{material} {thickness} {unit}', font_size, font_family, foreground)
        svg_elements.append(text_element)
        group_y += text_margin_bottom
        # first object is the tallest object in each row.
        y_max = flat_objects[0]['bound_box'].YLength
        for flat_object in flat_objects:
            bound_box = flat_object['bound_box']
            x = group_x + -bound_box.XMin
            y = group_y + bound_box.YMax
            if bound_box.YLength < y_max:  # align pieces to bottom of row
                y_offset = 0 if is_close_to_zero(bound_box.YMin) \
                    else max(bound_box.YMax, -bound_box.YMin)
                y = group_y + y_max - y_offset
            group_element = get_group_element(
                x, y, flat_object['label'], flat_object['svg'])
            svg_elements.append(group_element)

            # text
            txt_y = group_y + y_max + font_size
            txt_size = font_size * 0.75  # 12 / 16
            text_element = get_text_element(
                group_x, txt_y, str(flat_object['count']), txt_size, font_family, foreground)
            svg_elements.append(text_element)

            group_x += bound_box.XLength
            group_x += padding
            if group_x > width:
                width = group_x
            group_x += column_gap
        group_y += y_max
        group_y += text_margin_bottom
        group_y += row_gap
        group_y += padding
    return (
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {group_y}">' +
        f'<rect width="100%" height="100%" fill="{background}"/>' +
        '\n'.join(svg_elements) +
        '</svg>'
    )


def get_svg_style_options(rotor_disk_radius: float) -> dict:
    # 0.48 comes from 150 (the default RotorDiskRadius for T shape)
    # divided by a desired 72 px which happens to look good.
    font_size = round(rotor_disk_radius * 0.48)
    padding = round(font_size * 0.222)  # 16 / 72 = 0.222 repeating
    row_gap = round(font_size * 0.889)  # 64 / 72 = 0.889 repeating
    column_gap = row_gap / 2  # 32 is half of 64
    text_margin_bottom = round(font_size * 0.667)  # 48 / 72 = 0.667 repeating
    return {
        'font_size': font_size,
        'padding': padding,
        'row_gap': row_gap,
        'column_gap': column_gap,
        'text_margin_bottom': text_margin_bottom
    }


def get_text_element(x, y, text, font_size, font_family, fill) -> str:
    return (
        f'<text x="{x}" y="{y}" font-size="{font_size}" font-family="{font_family}" fill="{fill}">'
        f'{text}' +
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
        sorted_objects = sort_by_y_length_then_label_descending(
            grouped_objects)
        material, thickness = key
        yield sorted_objects, material, thickness


def sort_by_y_length_then_label_descending(flat_objects: List[FlatObject]) -> List[FlatObject]:
    return sorted(
        flat_objects,
        key=lambda o: (o['bound_box'].YLength, o['label']),
        reverse=True)


def group_by_material_and_thickness(objects: List[FlatObject]) -> dict:
    def keyfunc(obj):
        return (obj['material'], obj['thickness'])
    sorted_objects = sorted(objects, key=keyfunc)
    iterator = groupby(sorted_objects, key=keyfunc)
    return {k: list(v) for k, v in iterator}


def get_flat_object(obj: object,
                    get_part_count: Callable[[object], int],
                    precision: int = 2,
                    stroke_width: float = 2.5,
                    foreground: str = '#FFFFFF') -> FlatObject:
    two_dimensional_projection = get_2d_projection(obj)
    svg = Draft.get_svg(two_dimensional_projection,
                        linewidth=stroke_width, color=foreground)
    bound_box = get_bound_box(two_dimensional_projection)
    return {
        'label': obj.Label,
        'count': get_part_count(obj),
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
    # TODO: Use materials upon upgrading to FreeCAD 22
    # https://forum.freecad.org/viewtopic.php?t=78242
    # https://github.com/FreeCAD/FreeCAD/pull/10690
    # https://wiki.freecad.org/Release_notes_0.22#Material
    # https://wiki.freecad.org/Material
    wooden_labels = [
        'Tail_Vane', 'Blade_Assembly_BackDisk', 'Blade_Assembly_FrontTriangle', 'Blade_Template'
    ]
    wooden_label_fragments = ['Mold', 'CoilWinder', 'MagnetJig']
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


def is_close_to_zero(value: float) -> bool:
    return math.isclose(value, 0, abs_tol=1.0e-7)
