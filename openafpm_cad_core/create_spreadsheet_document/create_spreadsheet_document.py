from typing import Dict, List

import FreeCAD as App
from FreeCAD import Document

from ..parameter_groups import (FurlingParameters, MagnafpmParameters,
                                UserParameters)
from .alternator_cells import alternator_cells
from .cell import Cell
from .fastener_cells import get_fastener_cells
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
    cells_by_spreadsheet_name = {
        'Spreadsheet': cells,
        'Fastener': get_fastener_cells(),
        'Hub': hub_cells,
        'Alternator': alternator_cells,
        'YawBearing': yaw_bearing_cells,
        'Tail': tail_cells,
        'HighEndStop': high_end_stop_cells
    }
    return create_document(name, cells_by_spreadsheet_name)


def create_document(name: str,
                    cells_by_spreadsheet_name: Dict[str, List[List[Cell]]]) -> Document:
    document = App.newDocument(name)
    add_spreadsheets(document, cells_by_spreadsheet_name)
    document.recompute()
    return document


def add_spreadsheets(document: Document,
                     cells_by_spreadsheet_name: Dict[str, List[List[Cell]]]) -> None:
    for spreadsheet_name, cells in cells_by_spreadsheet_name.items():
        _add_spreadsheet(document, spreadsheet_name, cells)


def _add_spreadsheet(document: Document,
                     name: str,
                     cells: List[List[Cell]]) -> None:
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    populate_spreadsheet(sheet, cells)
