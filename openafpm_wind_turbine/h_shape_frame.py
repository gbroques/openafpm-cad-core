import os

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .common import enforce_recompute_last_spreadsheet, find_object_by_label
from .channel_section import make_channel_section

__all__ = ['assemble_h_shape_frame', 'calculate_h_channel_section_height']


def assemble_h_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    make_channel_section(document,
                         frame_path,
                         metal_length_l,
                         channel_section_height)


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
