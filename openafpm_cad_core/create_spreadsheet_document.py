import string
from typing import Any, Dict, List

import FreeCAD as App
from FreeCAD import Document

from .alternator_cells import alternator_cells
from .cell import Cell, Style
from .h_shape_cells import h_shape_cells
from .hub_cells import hub_cells
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .star_shape_cells import star_shape_cells
from .t_shape_cells import t_shape_cells
from .tail_cells import tail_cells

__all__ = ['create_spreadsheet_document']


def create_spreadsheet_document(magnafpm_parameters: MagnafpmParameters,
                                furling_parameters: FurlingParameters,
                                user_parameters: UserParameters) -> Document:
    static_cells = _get_static_cells()
    calculated_cells = _get_calculated_cells()
    parameters_by_key = {
        'MagnAFPM': magnafpm_parameters,
        'OpenFurl': furling_parameters,
        'User': user_parameters,
    }
    cells = _build_cells(parameters_by_key)
    cells.extend(static_cells)
    cells.extend(calculated_cells)
    document = App.newDocument('Master of Puppets')

    _add_spreadsheet(document, 'Spreadsheet', cells)
    _add_spreadsheet(document, 'Alternator', alternator_cells)
    _add_spreadsheet(document, 'TShape', t_shape_cells)
    _add_spreadsheet(document, 'HShape', h_shape_cells)
    _add_spreadsheet(document, 'StarShape', star_shape_cells)
    _add_spreadsheet(document, 'Hub', hub_cells)
    _add_spreadsheet(document, 'Tail', tail_cells)
    document.recompute()
    return document


def _add_spreadsheet(document: Document, name: str, cells: List[List[Cell]]) -> None:
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    _populate_spreadsheet_with_cells(sheet, cells)


def _build_cells(parameters_by_key: Dict[str, Dict[str, Any]]) -> List[List[Cell]]:
    cells = []
    for key, parameters in parameters_by_key.items():
        cells.append([Cell(key, styles=[Style.UNDERLINE])])
        cells.extend(_dict_to_cells(parameters))
    return cells


def _dict_to_cells(dictionary: Dict[str, Any]) -> List[List[Cell]]:
    return [
        [Cell(key), Cell(str(value), alias=key)]
        for key, value in dictionary.items()
    ]


def _populate_spreadsheet_with_cells(spreadsheet, cells: List[List[Cell]]) -> None:
    for row_index in range(len(cells)):
        for col_index in range(len(cells[row_index])):
            row_num = row_index + 1
            col_num = col_index + 1
            column = map_number_to_column(col_num)
            cell_address = column + str(row_num)
            cell = cells[row_index][col_index]
            spreadsheet.set(cell_address, cell.content)
            spreadsheet.setAlias(cell_address, cell.alias)
            spreadsheet.setStyle(cell_address, cell.style)
            spreadsheet.setAlignment(cell_address, cell.alignment)
            spreadsheet.setBackground(cell_address, cell.background)
            spreadsheet.setForeground(cell_address, cell.foreground)


def map_number_to_column(number: int) -> str:
    """
    >>> map_number_to_column(1)
    'A'

    >>> map_number_to_column(2)
    'B'

    >>> map_number_to_column(26)
    'Z'

    >>> map_number_to_column(27)
    'AA'

    >>> map_number_to_column(28)
    'AB'

    >>> map_number_to_column(52)
    'AZ'

    >>> map_number_to_column(702)
    'ZZ'
    """
    if number < 1:
        raise ValueError('Number {} must be greater than 0.'.format(number))
    num_letters = len(string.ascii_uppercase)
    if number > num_letters:
        first = map_number_to_column((number - 1) // num_letters)
        second = map_number_to_column(number % num_letters)
        return first + second
    return string.ascii_uppercase[number - 1]


def map_column_to_number(column: str) -> int:
    """
    >>> map_column_to_number('A')
    1

    >>> map_column_to_number('B')
    2

    >>> map_column_to_number('Z')
    26

    >>> map_column_to_number('AA')
    27

    >>> map_column_to_number('AB')
    28

    >>> map_column_to_number('AZ')
    52

    >>> map_column_to_number('ZZ')
    702
    """
    sum = 0
    for char in column:
        if char not in string.ascii_uppercase:
            raise ValueError(
                'Column "{}" must only contain uppercase ASCII characters.'.format(column))
        value = string.ascii_uppercase.find(char) + 1
        num_letters = len(string.ascii_uppercase)
        sum = sum * num_letters + value
    return sum


def _get_static_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        [
            Cell('YawBearingTailHingeJunctionHeight'), Cell('92.5',
                                                            alias='YawBearingTailHingeJunctionHeight')
        ],
        [
            Cell('YawBearingTailHingeJunctionChamfer'), Cell('15',
                                                             alias='YawBearingTailHingeJunctionChamfer')
        ],
    ]


def _get_calculated_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Calculated', styles=[Style.UNDERLINE])
        ],
        [
            Cell('StatorMountingStudsLength'), Cell('=RotorDiskRadius < 275 ? 150 : 200',
                                                    alias='StatorMountingStudsLength')
        ],
        [
            Cell('ResineStatorOuterRadius'), Cell('=RotorDiskRadius < 275 ? (RotorDiskRadius + CoilLegWidth + 20) : (RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
                                                  alias='ResineStatorOuterRadius')
        ],
        [
            Cell('YawPipeScaleFactor'), Cell('=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
                                             alias='YawPipeScaleFactor')
        ],
        [
            Cell('YawPipeLength'), Cell('=RotorDiskRadius * YawPipeScaleFactor * 2',
                                        alias='YawPipeLength')
        ],
        [
            Cell('YawBearingTopPlateHoleRadius'), Cell('=RotorDiskRadius < 187.5 ? 10 : 15',
                                                       alias='YawBearingTopPlateHoleRadius')
        ],
        [
            Cell('HingeInnerBodyOuterRadius'), Cell('=RotorDiskRadius < 187.5 ? 24.15 : (RotorDiskRadius < 275 ? 38 : 44.5)',
                                                    alias='HingeInnerBodyOuterRadius')
        ],
        [
            Cell('HingeInnerBodyLength'), Cell('=0.8 * 2 * RotorDiskRadius',
                                               alias='HingeInnerBodyLength')
        ],
        [
            Cell('HingeOuterBodyLength'), Cell('=HingeInnerBodyLength - YawBearingTailHingeJunctionHeight - 10 - 10',
                                               alias='HingeOuterBodyLength')
        ],
        [
            Cell('hypotenuse'), Cell('=(YawBearingTailHingeJunctionHeight - FlatMetalThickness) / cos(VerticalPlaneAngle)',
                                     alias='hypotenuse')
        ],
        [
            Cell('YawBearingTailHingeJunctionInnerWidth'), Cell('=sqrt(hypotenuse ^ 2 - (YawBearingTailHingeJunctionHeight - FlatMetalThickness) ^ 2)',
                                                                alias='YawBearingTailHingeJunctionInnerWidth')
        ],
        [
            Cell('YawBearingTailHingeJunctionFullWidth'), Cell('=YawPipeRadius + HingeInnerBodyOuterRadius + YawBearingTailHingeJunctionInnerWidth',
                                                               alias='YawBearingTailHingeJunctionFullWidth')
        ]
    ]
