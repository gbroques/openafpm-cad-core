import os

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .common import enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['make_frame']


def assemble_t_shape_frame(document, frame_path, metal_length_l):
    angled_channel_section_label = 'AngledChannelSection'
    _merge_piece(document, frame_path, angled_channel_section_label)
    left_angled_channel_section = find_object_by_label(
        document,
        angled_channel_section_label)
    document.recompute()
    App.setActiveDocument(document.Name)
    right_angled_channel_section = Draft.clone(left_angled_channel_section)
    right_angled_channel_section.Placement = Placement(
        Vector(metal_length_l, 0, 0), Rotation(Vector(0, 0, 1), 90))
    Draft.move(left_angled_channel_section, Vector(-metal_length_l, 0, 0))


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
