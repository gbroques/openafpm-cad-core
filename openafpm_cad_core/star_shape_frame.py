import os
from math import cos, radians, sin, sqrt

from FreeCAD import Placement, Vector

from .build_h_shape_frame import buid_h_shape_frame
from .common import make_compound, enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['assemble_star_shape_frame',
           'calculate_star_channel_section_height']


def assemble_star_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    (channel_section,
     end_bracket,
     tail_hinge_end_bracket) = buid_h_shape_frame(document,
                                                  frame_path,
                                                  metal_length_l,
                                                  channel_section_height)
    left_middle_bracket, right_middle_bracket = _make_middle_brackets(document,
                                                                      frame_path,
                                                                      metal_length_l,
                                                                      channel_section_height)
    return make_compound(document, 'Frame', [
        channel_section,
        end_bracket,
        tail_hinge_end_bracket,
        left_middle_bracket,
        right_middle_bracket
    ])


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


def _make_middle_brackets(document, frame_path, metal_length_l, channel_section_height):
    # Left Middle Bracket
    left_middle_bracket_label = 'LeftMiddleBracket'
    _merge_piece(document, frame_path, left_middle_bracket_label)
    left_middle_bracket = find_object_by_label(
        document, left_middle_bracket_label)
    placement = Placement(left_middle_bracket.Placement)
    placement.move(Vector(
        0,
        0,
        (channel_section_height + metal_length_l) / 2))
    left_middle_bracket.Placement = placement

    # Right Middle Bracket
    right_middle_bracket_label = 'RightMiddleBracket'
    _merge_piece(document, frame_path, right_middle_bracket_label)
    right_middle_bracket = find_object_by_label(
        document, right_middle_bracket_label)
    placement = Placement(right_middle_bracket.Placement)
    placement.move(Vector(
        0,
        0,
        (channel_section_height + metal_length_l) / 2))
    right_middle_bracket.Placement = placement

    return left_middle_bracket, right_middle_bracket


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
