"""
Build H Shape Frame.

Also used by Star Shape Frame as it's really a superset of the H Frame.
"""
import os

import Draft
import FreeCAD as App
from FreeCAD import Placement, Rotation, Vector

from .channel_section import make_channel_section, make_end_bracket
from .common import enforce_recompute_last_spreadsheet, find_object_by_label

__all__ = ['build_h_shape_frame']


def buid_h_shape_frame(document, frame_path, metal_length_l, channel_section_height):
    make_channel_section(document,
                         frame_path,
                         metal_length_l,
                         channel_section_height)
    make_end_bracket(document, frame_path, channel_section_height)
    end_bracket_label = 'EndBracket'
    _merge_piece(document, frame_path, end_bracket_label)
    tail_hinge_end_bracket = find_object_by_label(
        document, end_bracket_label + '001')
    expression_tuple = find_expression(
        tail_hinge_end_bracket.ExpressionEngine, 'Placement.Base.x')
    if expression_tuple is None:
        App.Console.PrintError(
            'No expression with key "Placement.Base.x" found for EndBracket.')
        return None
    key, expression = expression_tuple
    positive_expression = expression.replace('-', '')
    base = tail_hinge_end_bracket.Placement.Base
    placement = Placement(base, Rotation(0, 90, 180))
    tail_hinge_end_bracket.Placement = placement
    tail_hinge_end_bracket.setExpression(key, positive_expression)


def find_expression(expression_engine_tuples, key):
    matches = list(
        filter(lambda pair: pair[0] == key, expression_engine_tuples))
    if len(matches) == 0:
        return None
    return matches[0]


def _merge_piece(document, path, label):
    document.mergeProject(
        os.path.join(path, label + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)
