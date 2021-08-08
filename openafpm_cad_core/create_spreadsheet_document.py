import string
from typing import Any, Dict, List

import FreeCAD as App
from FreeCAD import Document

from .cell import Cell, Style
from .h_shape_cells import h_shape_cells
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .star_shape_cells import star_shape_cells
from .t_shape_cells import t_shape_cells

__all__ = ['create_spreadsheet_document']


def create_spreadsheet_document(magnafpm_parameters: MagnafpmParameters,
                                furling_parameters: FurlingParameters,
                                user_parameters: UserParameters) -> Document:
    static_parameters = _get_static_parameters()
    calculated_parameters = _get_calculated_parameters()
    parameters_by_key = {
        'MagnAFPM': magnafpm_parameters,
        'OpenFurl': furling_parameters,
        'User': user_parameters,
    }
    cells = _build_cells(parameters_by_key)
    cells.extend(static_parameters)
    cells.extend(calculated_parameters)
    document = App.newDocument('Master of Puppets')

    _add_spreadsheet(document, 'Spreadsheet', cells)
    _add_spreadsheet(document, 'TShape', t_shape_cells)
    _add_spreadsheet(document, 'HShape', h_shape_cells)
    _add_spreadsheet(document, 'StarShape', star_shape_cells)
    _add_spreadsheet(document, 'Hub', _get_hub_parameters_by_key())
    _add_spreadsheet(document, 'Tail', _get_tail_parameters_by_key())
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


def _get_static_parameters() -> List[List[Cell]]:
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


def _get_calculated_parameters() -> List[List[Cell]]:
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


def _get_tail_parameters_by_key() -> List[List[Cell]]:
    return [
        [
            Cell('Inputs', styles=[Style.UNDERLINE])
        ],
        [
            Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                          alias='RotorDiskRadius')
        ],
        [
            Cell('BracketLength'), Cell('=Spreadsheet.BracketLength',
                                        alias='BracketLength')
        ],
        [
            Cell('HingeInnerBodyOuterRadius'), Cell('=Spreadsheet.HingeInnerBodyOuterRadius',
                                                    alias='HingeInnerBodyOuterRadius')
        ],
        [
            Cell('VerticalPlaneAngle'), Cell('=Spreadsheet.VerticalPlaneAngle',
                                             alias='VerticalPlaneAngle')
        ],
        [
            Cell('HingeInnerBodyLength'), Cell('=Spreadsheet.HingeInnerBodyLength',
                                               alias='HingeInnerBodyLength')
        ],
        [
            Cell('HingeOuterBodyLength'), Cell('=Spreadsheet.HingeOuterBodyLength',
                                               alias='HingeOuterBodyLength')
        ],
        [
            Cell('YawBearingTailHingeJunctionHeight'), Cell('=Spreadsheet.YawBearingTailHingeJunctionHeight',
                                                            alias='YawBearingTailHingeJunctionHeight')
        ],
        [
            Cell('YawBearingTailHingeJunctionFullWidth'), Cell('=Spreadsheet.YawBearingTailHingeJunctionFullWidth',
                                                               alias='YawBearingTailHingeJunctionFullWidth')
        ],
        [
            Cell('YawBearingTailHingeJunctionInnerWidth'), Cell('=Spreadsheet.YawBearingTailHingeJunctionInnerWidth',
                                                                alias='YawBearingTailHingeJunctionInnerWidth')
        ],
        [
            Cell('YawBearingTailHingeJunctionChamfer'), Cell('=Spreadsheet.YawBearingTailHingeJunctionChamfer',
                                                             alias='YawBearingTailHingeJunctionChamfer')
        ],
        [
            Cell('YawPipeRadius'), Cell('=Spreadsheet.YawPipeRadius',
                                        alias='YawPipeRadius')
        ],
        [
            Cell('HorizontalPlaneAngle'), Cell('=Spreadsheet.HorizontalPlaneAngle',
                                               alias='HorizontalPlaneAngle')
        ],
        [
            Cell('FlatMetalThickness'), Cell('=Spreadsheet.FlatMetalThickness',
                                             alias='FlatMetalThickness')
        ],
        [
            Cell('BoomPipeRadius'), Cell('=Spreadsheet.BoomPipeRadius',
                                         alias='BoomPipeRadius')
        ],
        [
            Cell('Vane', styles=[Style.UNDERLINE])
        ],
        [
            Cell('DistanceToFirstHole'), Cell('=BracketLength / 10',
                                              alias='DistanceToFirstHole')
        ],
        [
            Cell('DistanceBetweenHoles'), Cell('=BracketLength / 2',
                                               alias='DistanceBetweenHoles')
        ],
        [
            Cell('VaneBracketAngle'), Cell('45',
                                           alias='VaneBracketAngle')
        ],
        [
            Cell('Tail Hinge Pipe X Z', styles=[Style.UNDERLINE])
        ],
        [
            Cell('XRotationOffset'), Cell('=HingeInnerBodyOuterRadius - cos(VerticalPlaneAngle) * HingeInnerBodyOuterRadius',
                                          alias='XRotationOffset')
        ],
        [
            Cell('TrigOffset'), Cell('=tan(VerticalPlaneAngle) * (YawBearingTailHingeJunctionHeight - FlatMetalThickness) + XRotationOffset',
                                     alias='TrigOffset')
        ],
        [
            Cell('TailHingePipeX'), Cell('=HingeInnerBodyOuterRadius + YawPipeRadius - YawBearingTailHingeJunctionChamfer + YawBearingTailHingeJunctionInnerWidth - TrigOffset',
                                         alias='TailHingePipeX')
        ],
        [
            Cell('TailHingePipeZ'), Cell('=-HingeInnerBodyOuterRadius * sin(VerticalPlaneAngle)',
                                         alias='TailHingePipeZ')
        ],
        [
            Cell('Outer Tail Hinge X Z', styles=[Style.UNDERLINE])
        ],
        [
            Cell('PipeHeightOffset'), Cell('=HingeInnerBodyLength - HingeOuterBodyLength',
                                           alias='PipeHeightOffset')
        ],
        [
            Cell('XXX'), Cell('=sin(VerticalPlaneAngle) * PipeHeightOffset',
                              alias='XXX')
        ],
        [
            Cell('ZZZ'), Cell('=cos(VerticalPlaneAngle) * PipeHeightOffset',
                              alias='ZZZ')
        ],
        [
            Cell('OuterTailHingeX'), Cell('=XXX + TailHingePipeX',
                                          alias='OuterTailHingeX')
        ],
        [
            Cell('OuterTailHingeZ'), Cell('=ZZZ + TailHingePipeZ',
                                          alias='OuterTailHingeZ')
        ],
        [
            Cell('Outer Tail Hinge Low End Stop', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TailBoomTriangularBraceWidth'), Cell('=0.27 * RotorDiskRadius',
                                                       alias='TailBoomTriangularBraceWidth')
        ],
        [
            Cell('h1'), Cell('=-(TailHingePipeZ / cos(VerticalPlaneAngle))',
                             alias='h1')
        ],
        [
            Cell('h2'), Cell('=YawBearingTailHingeJunctionHeight / cos(VerticalPlaneAngle)',
                             alias='h2')
        ],
        [
            Cell('OuterHingeJunctionVerticalGap'), Cell('=HingeInnerBodyLength - HingeOuterBodyLength - h2 - h1',
                                                        alias='OuterHingeJunctionVerticalGap')
        ],
        [
            Cell('HorizontalPipeLength'), Cell('=sin(90 - VerticalPlaneAngle) * YawPipeRadius',
                                               alias='HorizontalPipeLength')
        ],
        [
            Cell('HorizontalEstimate'), Cell('=cos(90 - VerticalPlaneAngle) * (TailBoomTriangularBraceWidth + OuterHingeJunctionVerticalGap)',
                                             alias='HorizontalEstimate')
        ],
        [
            Cell('HorizontalDistanceBetweenOuterYawPipes'), Cell('=YawBearingTailHingeJunctionFullWidth + HorizontalEstimate + HorizontalPipeLength - HingeInnerBodyOuterRadius',
                                                                 alias='HorizontalDistanceBetweenOuterYawPipes')
        ],
        [
            Cell('OuterTailHingeLowEndStopAngle'), Cell('=-(90deg - atan(YawPipeRadius / HorizontalDistanceBetweenOuterYawPipes))',
                                                        alias='OuterTailHingeLowEndStopAngle')
        ],
        [
            Cell('Tail Boom Triangular Brace', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TailBoomTriangularBraceXOffset'), Cell('=sin(VerticalPlaneAngle) * TailBoomTriangularBraceWidth',
                                                         alias='TailBoomTriangularBraceXOffset')
        ],
        [
            Cell('TailBoomTriangularBraceZOffset'), Cell('=cos(VerticalPlaneAngle) * TailBoomTriangularBraceWidth',
                                                         alias='TailBoomTriangularBraceZOffset')
        ],
        [
            Cell('Tail Angle', styles=[Style.UNDERLINE])
        ],
        [
            Cell('DefaultTailAngle'), Cell('110',
                                           alias='DefaultTailAngle')
        ],
        [
            Cell('TailAngle'), Cell('=180 - HorizontalPlaneAngle - DefaultTailAngle',
                                    alias='TailAngle')
        ],
        [
            Cell('Tail', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TailXInitial'), Cell('=cos(VerticalPlaneAngle) * YawPipeRadius',
                                       alias='TailXInitial')
        ],
        [
            Cell('TailZOffset'), Cell('=-sin(VerticalPlaneAngle) * YawPipeRadius',
                                      alias='TailZOffset')
        ],
        [
            Cell('P', styles=[Style.UNDERLINE])
        ],
        [
            Cell('Px'), Cell('=TailXInitial + OuterTailHingeX + TailBoomTriangularBraceXOffset',
                             alias='Px')
        ],
        [
            Cell('Py'), Cell('0',
                             alias='Py')
        ],
        [
            Cell('Pz'), Cell('=BoomPipeRadius + TailZOffset + OuterTailHingeZ + TailBoomTriangularBraceZOffset',
                             alias='Pz')
        ],
        [
            Cell('C', styles=[Style.UNDERLINE])
        ],
        [
            Cell('Cx'), Cell('=OuterTailHingeX',
                             alias='Cx')
        ],
        [
            Cell('Cy'), Cell('0',
                             alias='Cy')
        ],
        [
            Cell('Cz'), Cell('=OuterTailHingeZ',
                             alias='Cz')
        ],
        [
            Cell('Q', styles=[Style.UNDERLINE])
        ],
        [
            Cell('Qx'), Cell('=Px - Cx',
                             alias='Qx')
        ],
        [
            Cell('Qy'), Cell('=Py - Cy',
                             alias='Qy')
        ],
        [
            Cell('Qz'), Cell('=Pz - Cz',
                             alias='Qz')
        ],
        [
            Cell('A', styles=[Style.UNDERLINE])
        ],
        [
            Cell('Ax'), Cell('=sin(VerticalPlaneAngle)',
                             alias='Ax')
        ],
        [
            Cell('Ay'), Cell('0',
                             alias='Ay')
        ],
        [
            Cell('Az'), Cell('=cos(VerticalPlaneAngle)',
                             alias='Az')
        ],
        # Rotation Matrix from Axis and Angle
        # Formula: https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        [
            Cell('r1', styles=[Style.UNDERLINE])
        ],
        [
            Cell('r11'), Cell('=cos(TailAngle) + Ax ^ 2 * (1 - cos(TailAngle))',
                              alias='r11')
        ],
        [
            Cell('r12'), Cell('=Ax * Ay * (1 - cos(TailAngle)) - Az * sin(TailAngle)',
                              alias='r12')
        ],
        [
            Cell('r13'), Cell('=Ax * Az * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
                              alias='r13')
        ],
        [
            Cell('r2', styles=[Style.UNDERLINE])
        ],
        [
            Cell('r21'), Cell('=Ay * Ax * (1 - cos(TailAngle)) + Az * sin(TailAngle)',
                              alias='r21')
        ],
        [
            Cell('r22'), Cell('=cos(TailAngle) + Ay ^ 2 * (1 - cos(TailAngle))',
                              alias='r22')
        ],
        [
            Cell('r23'), Cell('=Ay * Az * (1 - cos(TailAngle)) - Ax * sin(TailAngle)',
                              alias='r23')
        ],
        [
            Cell('r3', styles=[Style.UNDERLINE])
        ],
        [
            Cell('r31'), Cell('=Az * Ax * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
                              alias='r31')
        ],
        [
            Cell('r32'), Cell('=Az * Ay * (1 - cos(TailAngle)) + Ax * sin(TailAngle)',
                              alias='r32')
        ],
        [
            Cell('r33'), Cell('=cos(TailAngle) + Az ^ 2 * (1 - cos(TailAngle))',
                              alias='r33')
        ],
        # Rotation Matrix * (P - C)
        [
            Cell('R', styles=[Style.UNDERLINE])
        ],
        [
            Cell('Rx'), Cell('=r11 * Qx + r12 * Qy + r13 * Qz',
                             alias='Rx')
        ],
        [
            Cell('Ry'), Cell('=r21 * Qx + r22 * Qy + r23 * Qz',
                             alias='Ry')
        ],
        [
            Cell('Rz'), Cell('=r31 * Qx + r32 * Qy + r33 * Qz',
                             alias='Rz')
        ],
        [
            Cell('Tail X Y Z', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TailX'), Cell('=Cx + Rx',
                                alias='TailX')
        ],
        [
            Cell('TailY'), Cell('=Cy + Ry',
                                alias='TailY')
        ],
        [
            Cell('TailZ'), Cell('=Cz + Rz',
                                alias='TailZ')
        ]
    ]


def _get_hub_parameters_by_key() -> List[List[Cell]]:
    return [
        [
            Cell('Inputs', styles=[Style.UNDERLINE])
        ],
        [
            Cell('HubHolesPlacement'), Cell('=Spreadsheet.HubHolesPlacement',
                                            alias='HubHolesPlacement')
        ],
        [
            Cell('HubHoles'), Cell('=Spreadsheet.HubHoles',
                                   alias='HubHoles')
        ],
        [
            Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                          alias='RotorDiskRadius')
        ],
        [
            Cell('Middle Pad', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeMiddlePadRadiusMargin'), Cell('15',
                                                      alias='TShapeMiddlePadRadiusMargin')
        ],
        [
            Cell('HShapeMiddlePadRadiusMargin'), Cell('15',
                                                      alias='HShapeMiddlePadRadiusMargin')
        ],
        [
            Cell('StarShapeMiddlePadRadiusMargin'), Cell('20',
                                                         alias='StarShapeMiddlePadRadiusMargin')
        ],
        [
            Cell('MiddlePadRadiusMargin'), Cell('=RotorDiskRadius < 187.5 ? TShapeMiddlePadRadiusMargin : (RotorDiskRadius < 275 ? HShapeMiddlePadRadiusMargin : StarShapeMiddlePadRadiusMargin)',
                                                alias='MiddlePadRadiusMargin')
        ],
        [
            Cell('MiddlePadRadius'), Cell('=HubHolesPlacement + HubHoles + MiddlePadRadiusMargin',
                                          alias='MiddlePadRadius')
        ],
        [
            Cell('MiddlePadThickness'), Cell('16',
                                             alias='MiddlePadThickness')
        ],
        [
            Cell('Common', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeProtrudingPadThickness'), Cell('5',
                                                       alias='TShapeProtrudingPadThickness')
        ],
        [
            Cell('HShapeProtrudingPadThickness'), Cell('5',
                                                       alias='HShapeProtrudingPadThickness')
        ],
        [
            Cell('StarShapeProtrudingPadThickness'), Cell('10',
                                                          alias='StarShapeProtrudingPadThickness')
        ],
        [
            Cell('ProtrudingPadThickness'), Cell('=RotorDiskRadius < 187.5 ? TShapeProtrudingPadThickness : (RotorDiskRadius < 275 ? HShapeProtrudingPadThickness : StarShapeProtrudingPadThickness)',
                                                 alias='ProtrudingPadThickness')
        ],
        [
            Cell('CoverThickness'), Cell('10',
                                         alias='CoverThickness')
        ],
        [
            Cell('Frame Side Pad', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeFrameSidePadRadius'), Cell('32.5',
                                                   alias='TShapeFrameSidePadRadius')
        ],
        [
            Cell('HShapeFrameSidePadRadius'), Cell('42.5',
                                                   alias='HShapeFrameSidePadRadius')
        ],
        [
            Cell('StarShapeFrameSidePadRadius'), Cell('52.5',
                                                      alias='StarShapeFrameSidePadRadius')
        ],
        [
            Cell('FrameSidePadRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadRadius : (RotorDiskRadius < 275 ? HShapeFrameSidePadRadius : StarShapeFrameSidePadRadius)',
                                             alias='FrameSidePadRadius')
        ],
        [
            Cell('TShapeFrameSidePadWidth'), Cell('45',
                                                  alias='TShapeFrameSidePadWidth')
        ],
        [
            Cell('HShapeFrameSidePadWidth'), Cell('45',
                                                  alias='HShapeFrameSidePadWidth')
        ],
        [
            Cell('StarShapeFrameSidePadWidth'), Cell('85',
                                                     alias='StarShapeFrameSidePadWidth')
        ],
        [
            Cell('FrameSidePadWidth'), Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadWidth : (RotorDiskRadius < 275 ? HShapeFrameSidePadWidth : StarShapeFrameSidePadWidth)',
                                            alias='FrameSidePadWidth')
        ],
        [
            Cell('Rotor Side Pad', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeRotorSidePadRadius'), Cell('28',
                                                   alias='TShapeRotorSidePadRadius')
        ],
        [
            Cell('HShapeRotorSidePadRadius'), Cell('31',
                                                   alias='HShapeRotorSidePadRadius')
        ],
        [
            Cell('StarShapeRotorSidePadRadius'), Cell('47.5',
                                                      alias='StarShapeRotorSidePadRadius')
        ],
        [
            Cell('RotorSidePadRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadRadius : (RotorDiskRadius < 275 ? HShapeRotorSidePadRadius : StarShapeRotorSidePadRadius)',
                                             alias='RotorSidePadRadius')
        ],
        [
            Cell('TShapeRotorSidePadWidth'), Cell('40',
                                                  alias='TShapeRotorSidePadWidth')
        ],
        [
            Cell('HShapeRotorSidePadWidth'), Cell('40',
                                                  alias='HShapeRotorSidePadWidth')
        ],
        [
            Cell('StarShapeRotorSidePadWidth'), Cell('75',
                                                     alias='StarShapeRotorSidePadWidth')
        ],
        [
            Cell('RotorSidePadWidth'), Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadWidth : (RotorDiskRadius < 275 ? HShapeRotorSidePadWidth : StarShapeRotorSidePadWidth)',
                                            alias='RotorSidePadWidth')
        ],
        [
            Cell('Number of Holes', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeNumberOfHoles'), Cell('4',
                                              alias='TShapeNumberOfHoles')
        ],
        [
            Cell('HShapeNumberOfHoles'), Cell('5',
                                              alias='HShapeNumberOfHoles')
        ],
        [
            Cell('StarShapeNumberOfHoles'), Cell('6',
                                                 alias='StarShapeNumberOfHoles')
        ],
        [
            Cell('NumberOfHoles'), Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfHoles : (RotorDiskRadius < 275 ? HShapeNumberOfHoles : StarShapeNumberOfHoles)',
                                        alias='NumberOfHoles')
        ],
        [
            Cell('Stub Axle Shaft Radius', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TShapeStubAxleShaftRadius'), Cell('18',
                                                    alias='TShapeStubAxleShaftRadius')
        ],
        [
            Cell('HShapeStubAxleShaftRadius'), Cell('22.5',
                                                    alias='HShapeStubAxleShaftRadius')
        ],
        [
            Cell('StarShapeStubAxleShaftRadius'), Cell('30',
                                                       alias='StarShapeStubAxleShaftRadius')
        ],
        [
            Cell('StubAxleShaftRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeStubAxleShaftRadius : (RotorDiskRadius < 275 ? HShapeStubAxleShaftRadius : StarShapeStubAxleShaftRadius)',
                                              alias='StubAxleShaftRadius')
        ]
    ]
