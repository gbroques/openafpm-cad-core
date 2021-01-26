import os

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .common import enforce_recompute_last_spreadsheet, find_object_by_label
from .channel_section import make_channel_section, make_end_bracket

__all__ = ['assemble_t_shape_frame', 'calculate_t_channel_section_height']


def assemble_t_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    make_channel_section(document,
                         frame_path,
                         metal_length_l,
                         channel_section_height)
    make_end_bracket(document, frame_path, channel_section_height)


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
    i = -0.0056 * rotor_radius ** 2 + 2.14 * rotor_radius - 171
    distance_x = offset - (i + metal_thickness_l + yaw_pipe_radius)
    return resine_stator_outer_radius - 25 + distance_x
