import os

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .common import (enforce_recompute_last_spreadsheet, find_object_by_label,
                     make_compound)

__all__ = ['make_channel_section']


def make_channel_section(document, frame_path, metal_length_l, channel_section_height):
    angled_channel_section_label = 'AngledChannelSection'
    _merge_piece(document, frame_path, angled_channel_section_label)
    left_angled_channel_section = find_object_by_label(
        document,
        angled_channel_section_label)
    document.recompute()
    App.setActiveDocument(document.Name)
    right_angled_channel_section = document.copyObject(left_angled_channel_section, True)
    right_angled_channel_section.Placement = Placement(
        Vector(metal_length_l, 0, 0), Rotation(Vector(0, 0, 1), 90))
    left_angled_channel_section.Placement = Placement(
        Vector(-metal_length_l, 0, channel_section_height), Rotation(-90, 180, 0))
    channel_section_name = 'ChannelSection'
    return make_compound(document, channel_section_name, [
        left_angled_channel_section,
        right_angled_channel_section
    ])


def make_end_bracket(document, frame_path, channel_section_height):
    end_bracket_label = 'EndBracket'
    _merge_piece(document, frame_path, end_bracket_label)
    end_bracket = find_object_by_label(
        document,
        end_bracket_label)
    document.recompute()
    App.setActiveDocument(document.Name)
    placement = Placement(end_bracket.Placement)
    placement.move(Vector(0, 0, channel_section_height))
    end_bracket.Placement = placement
    return end_bracket


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
