import os

import FreeCAD as App

from .common import enforce_recompute_last_spreadsheet

__all__ = ['make_frame']


def make_frame(base_path,
               document,
               assemble_frame,
               metal_length_l,
               channel_section_height):
    frame_path = os.path.join(base_path, 'Frame')
    return assemble_frame(document,
                          frame_path,
                          metal_length_l,
                          channel_section_height)
