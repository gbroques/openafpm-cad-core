import os

from .build_h_shape_frame import buid_h_shape_frame
from .channel_section import make_channel_section, make_end_bracket
from .common import (enforce_recompute_last_spreadsheet, find_object_by_label,
                     make_compound)

__all__ = ['assemble_h_shape_frame', 'calculate_h_channel_section_height']


def assemble_h_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    (channel_section,
     end_bracket,
     tail_hinge_end_bracket) = buid_h_shape_frame(document,
                                                  frame_path,
                                                  metal_length_l,
                                                  channel_section_height)
    return make_compound(document, 'Frame', [
        channel_section,
        end_bracket,
        tail_hinge_end_bracket
    ])


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def calculate_h_channel_section_height(rotor_radius,
                                       coil_leg_width,
                                       metal_length_l):
    resine_stator_outer_radius = rotor_radius + coil_leg_width + 20
    delta = 100 - 8 * (25 - resine_stator_outer_radius *
                       resine_stator_outer_radius)
    alpha = (10 + delta ** 0.5) / 4
    depth_piece_g = 2 * alpha + 40
    return depth_piece_g - 2 * metal_length_l
