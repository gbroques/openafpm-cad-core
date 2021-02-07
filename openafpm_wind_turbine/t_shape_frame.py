import os
import math

from .channel_section import make_channel_section, make_end_bracket
from .common import (enforce_recompute_last_spreadsheet, find_object_by_label,
                     make_compound)

__all__ = [
    'assemble_t_shape_frame',
    'calculate_t_channel_section_height',
    'distance_between_stub_axle_shaft_and_tail_hinge_end_bracket'
]


def assemble_t_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    channel_section = make_channel_section(document,
                                           frame_path,
                                           metal_length_l,
                                           channel_section_height)
    end_bracket = make_end_bracket(
        document, frame_path, channel_section_height)
    tail_hinge_end_bracket_label = 'TailHingeEndBracketFix'
    _merge_piece(document, frame_path, tail_hinge_end_bracket_label)
    tail_hinge_end_bracket = find_object_by_label(
        document, tail_hinge_end_bracket_label)
    return make_compound(document, 'Frame', [
        channel_section,
        end_bracket,
        tail_hinge_end_bracket
    ])


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def calculate_t_channel_section_height(rotor_radius,
                                       coil_leg_width,
                                       metal_thickness_l,
                                       yaw_pipe_radius,
                                       offset):
    resine_stator_outer_radius = rotor_radius + coil_leg_width + 20
    X = distance_between_stub_axle_shaft_and_tail_hinge_end_bracket(
        rotor_radius, metal_thickness_l, yaw_pipe_radius, offset)
    return resine_stator_outer_radius - 25 + X


def distance_between_stub_axle_shaft_and_tail_hinge_end_bracket(rotor_radius,
                                                                metal_thickness_l,
                                                                yaw_pipe_radius,
                                                                offset):
    I = -0.0056 * rotor_radius ** 2 + 2.14 * rotor_radius - 171
    X = offset - (I + metal_thickness_l + yaw_pipe_radius)
    return X


def tail_hinge_end_bracket_length(rotor_radius,
                                  coil_leg_width,
                                  metal_thickness_l,
                                  yaw_pipe_radius,
                                  offset):
    ResineStatorOuterRadius = rotor_radius + coil_leg_width + 20
    EX = distance_between_stub_axle_shaft_and_tail_hinge_end_bracket(
        rotor_radius,
        metal_thickness_l,
        yaw_pipe_radius,
        offset
    )
    Beta = math.sqrt(ResineStatorOuterRadius ** 2 - (25 + EX) ** 2)
    return 2 * Beta + 2 * 20
