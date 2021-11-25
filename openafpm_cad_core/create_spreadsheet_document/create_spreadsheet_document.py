from typing import List

import FreeCAD as App
from FreeCAD import Document

from ..parameter_groups import (FurlingParameters, MagnafpmParameters,
                                UserParameters)
from .alternator_cells import alternator_cells
from .cell import Cell, Style
from .fastener_cells import fastener_cells
from .high_end_stop_cells import high_end_stop_cells
from .hub_cells import hub_cells
from .parameters_by_key_to_cells import parameters_by_key_to_cells
from .populate_spreadsheet import populate_spreadsheet
from .tail_cells import tail_cells
from .yaw_bearing_cells import yaw_bearing_cells

__all__ = ['create_spreadsheet_document']


def create_spreadsheet_document(name: str,
                                magnafpm_parameters: MagnafpmParameters,
                                furling_parameters: FurlingParameters,
                                user_parameters: UserParameters) -> Document:
    cells = parameters_by_key_to_cells({
        'MagnAFPM': magnafpm_parameters,
        'Furling': furling_parameters,
        'User': user_parameters,
    })

    static_cells = _get_static_cells()
    cells.extend(static_cells)

    document = App.newDocument(name)

    _add_spreadsheet(document, 'Spreadsheet', cells)
    _add_spreadsheet(document, 'Hub', hub_cells)
    _add_spreadsheet(document, 'Fastener', fastener_cells)
    _add_spreadsheet(document, 'Alternator', alternator_cells)
    _add_spreadsheet(document, 'YawBearing', yaw_bearing_cells)
    _add_spreadsheet(document, 'Tail', tail_cells)
    _add_spreadsheet(document, 'HighEndStop', high_end_stop_cells)
    document.recompute()
    return document


def _add_spreadsheet(document: Document,
                     name: str,
                     cells: List[List[Cell]]) -> None:
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    populate_spreadsheet(sheet, cells)


def _get_static_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        [
            Cell('AlternatorTiltAngle'),
            Cell('=4deg', alias='AlternatorTiltAngle'),
            Cell('See right-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".')
        ],
    ]
