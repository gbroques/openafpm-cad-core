import os
from math import cos, radians, sin, sqrt

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .build_h_shape_frame import buid_h_shape_frame
from .channel_section import make_channel_section
from .common import enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['assemble_star_shape_frame',
           'calculate_star_channel_section_height']


def assemble_star_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    buid_h_shape_frame(document,
                       frame_path,
                       metal_length_l,
                       channel_section_height)
    left_middle_bracket_label = 'LeftMiddleBracket'
    _merge_piece(document, frame_path, left_middle_bracket_label)
    left_middle_bracket = find_object_by_label(document, left_middle_bracket_label)
    placement = Placement(left_middle_bracket.Placement)
    placement.move(Vector(
        -metal_length_l,
        metal_length_l,
        (channel_section_height + metal_length_l) / 2))
    left_middle_bracket.Placement = placement
    right_middle_bracket_label = 'RightMiddleBracket'
    _merge_piece(document, frame_path, right_middle_bracket_label)
    right_middle_bracket = find_object_by_label(document, right_middle_bracket_label)
    placement = Placement(right_middle_bracket.Placement)
    placement.move(Vector(
        0,
        metal_length_l,
        (channel_section_height + metal_length_l) / 2))
    right_middle_bracket.Placement = placement

def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def calculate_star_channel_section_height(rotor_radius,
                                          coil_leg_width,
                                          metal_length_l):
    resine_stator_outer_radius = (
        rotor_radius + coil_leg_width + 20) / cos(radians(30))
    stator_holes_circle = (
        rotor_radius + coil_leg_width + 0.5 *
        (resine_stator_outer_radius - (rotor_radius + coil_leg_width))
    )
    return (
        2 * stator_holes_circle *
        sqrt(1 - sin(radians(30)) * sin(radians(30))) - metal_length_l
    )
