import string
from typing import List, Tuple, Union

import FreeCAD as App
from FreeCAD import Document

from .cell import Cell, Style
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

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
        'Static': static_parameters,
        'Calculated': calculated_parameters
    }
    document = App.newDocument('Master of Puppets')

    _add_spreadsheet(document, 'Spreadsheet', parameters_by_key)
    _add_spreadsheet(document, 'TShape', _get_t_shape_cells())
    _add_spreadsheet(document, 'HShape', _get_h_shape_parameters_by_key())
    _add_spreadsheet(document, 'StarShape',
                     _get_star_shape_parameters_by_key())
    _add_spreadsheet(document, 'Hub', _get_hub_parameters_by_key())
    _add_spreadsheet(document, 'Tail', _get_tail_parameters_by_key())
    document.recompute()
    return document


def _add_spreadsheet(document: Document, name: str, contents: Union[dict, List[List[Cell]]]) -> None:
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    if type(contents) is dict:
        cells = _build_cells(contents)
        _populate_spreadsheet(sheet, cells)
    else:
        _populate_spreadsheet_with_cells(sheet, contents)


def _build_cells(parameters_by_key) -> List[Tuple[str, str]]:
    cells = []
    for key, parameters in parameters_by_key.items():
        cells.append((key, ''))
        cells.extend(_dict_to_cells(parameters))
    return cells


def _dict_to_cells(dictionary: dict) -> List[Tuple[str, str]]:
    return [(key, value) for key, value in dictionary.items()]


def _populate_spreadsheet(spreadsheet, cells: List[Tuple[str, str]]) -> None:
    for i, (key, value) in enumerate(cells):
        number = str(i + 1)
        key_cell = 'A' + number
        value_cell = 'B' + number
        spreadsheet.set(key_cell, key)
        spreadsheet.set(value_cell, str(value))
        if value:
            spreadsheet.setAlias(value_cell, key)
        else:
            spreadsheet.setStyle(key_cell, 'underline')


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


def _get_static_parameters() -> dict:
    return {
        'YawBearingTailHingeJunctionHeight': '92.5',
        'YawBearingTailHingeJunctionChamfer': '15',
    }


def _get_calculated_parameters() -> dict:
    return {
        'StatorMountingStudsLength': '=RotorDiskRadius < 275 ? 150 : 200',
        'ResineStatorOuterRadius': '=RotorDiskRadius < 275 ? (RotorDiskRadius + CoilLegWidth + 20) : (RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
        'YawPipeScaleFactor': '=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
        'YawPipeLength': '=RotorDiskRadius * YawPipeScaleFactor * 2',
        'YawBearingTopPlateHoleRadius': '=RotorDiskRadius < 187.5 ? 10 : 15',
        'HingeInnerBodyOuterRadius': '=RotorDiskRadius < 187.5 ? 24.15 : (RotorDiskRadius < 275 ? 38 : 44.5)',
        'HingeInnerBodyLength': '=0.8 * 2 * RotorDiskRadius',
        'HingeOuterBodyLength': '=HingeInnerBodyLength - YawBearingTailHingeJunctionHeight - 10 - 10',
        'hypotenuse': '=(YawBearingTailHingeJunctionHeight - FlatMetalThickness) / cos(VerticalPlaneAngle)',
        'YawBearingTailHingeJunctionInnerWidth': '=sqrt(hypotenuse ^ 2 - (YawBearingTailHingeJunctionHeight - FlatMetalThickness) ^ 2)',
        'YawBearingTailHingeJunctionFullWidth': '=YawPipeRadius + HingeInnerBodyOuterRadius + YawBearingTailHingeJunctionInnerWidth'
    }


def _get_t_shape_cells() -> List[List[Cell]]:
    return [
        # Inputs
        # ------
        [Cell('Inputs', styles=[Style.UNDERLINE])],
        [Cell('RotorDiskRadius'), Cell(
            '=Spreadsheet.RotorDiskRadius', alias='RotorDiskRadius')],
        [Cell('Offset'), Cell('=Spreadsheet.Offset', alias='Offset')],
        [Cell('YawPipeRadius'), Cell(
            '=Spreadsheet.YawPipeRadius', alias='YawPipeRadius')],
        [Cell('MetalThicknessL'), Cell(
            '=Spreadsheet.MetalThicknessL', alias='MetalThicknessL')],
        [Cell('MetalLengthL'), Cell(
            '=Spreadsheet.MetalLengthL', alias='MetalLengthL')],
        [Cell('ResineStatorOuterRadius'), Cell('=Spreadsheet.ResineStatorOuterRadius',
                                               alias='ResineStatorOuterRadius')],
        [Cell('Holes'), Cell('=Spreadsheet.Holes', alias='Holes')],

        # Yaw Bearing to Frame Junction
        # -----------------------------
        [Cell('Yaw Bearing to Frame Junction', styles=[Style.UNDERLINE])],
        [Cell('I'), Cell(
            '=1 / 70 * (sqrt(77280 * RotorDiskRadius - 9503975) + 235)', alias='I')],
        [Cell('j'), Cell('=0.32 * RotorDiskRadius - 3', alias='j')],
        [Cell('k'), Cell('=0.2 * RotorDiskRadius - 5', alias='k')],

        # Frame
        # -----
        [Cell('Frame', styles=[Style.UNDERLINE])],
        [Cell('X'), Cell('=Offset - (I + YawPipeRadius)', alias='X')],
        # 30 degrees because 360 / 3 = 120 - 90 = 30.
        # Divide by 3 for because the T Shape has 3 holes.
        # cos(30) * ResineStatorOuterRadius = bottom of right triangle
        # * 2 to get both sides.
        # 40 = 2 * margin. margin is the distance from the hole to the edge of the metal.
        # Add the radius for holes on each side, + Spreadsheet.Holes * 2.
        [Cell('a'), Cell(
            '=cos(30) * ResineStatorOuterRadius * 2 + 40 + Holes * 2', alias='a')],
        # Total vertical distance of T Shape from bottom hole to two top holes.
        # This is the opposite, or vertical left side of the right triangle plus,
        # the stator resin cast radius.
        [Cell('TShapeVerticalDistance'), Cell('=(sin(30) * ResineStatorOuterRadius) + ResineStatorOuterRadius',
                                              alias='TShapeVerticalDistance')],
        # Subtract MetalLengthL as the top holes and bottom hole are centered in the brackets.
        # MetalLengthL is the length of the brackets.
        [Cell('BC'), Cell('=TShapeVerticalDistance - MetalLengthL', alias='BC')],
        [Cell('D'), Cell('=MetalLengthL * 2', alias='D')]
    ]


def _get_h_shape_parameters_by_key() -> dict:
    return {
        'Inputs': {
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius',
            'Offset': '=Spreadsheet.Offset',
            'YawPipeRadius': '=Spreadsheet.YawPipeRadius',
            'MetalLengthL': '=Spreadsheet.MetalLengthL',
            'ResineStatorOuterRadius': '=Spreadsheet.ResineStatorOuterRadius'
        },
        'Frame': {
            # https://calcresource.com/geom-rectangle.html
            'CentralAngle': '=360 / 4',
            'Theta': '=CentralAngle / 2',
            'Inradius': '=cos(Theta) * ResineStatorOuterRadius',
            'IsoscelesRightTriangleHypotenuseRatio': '=1 / cos(Theta)',
            'HorizontalDistanceBetweenHoles': '=ResineStatorOuterRadius * IsoscelesRightTriangleHypotenuseRatio',
            # Distance from hole to outside edge of frame.
            'HoleMargin': '20',
            'G': '=HorizontalDistanceBetweenHoles + HoleMargin * 2',
            'H': '=Inradius * 2 - MetalLengthL',  # To make the frame square.
            'MM': '=RotorDiskRadius < 275 ? 100 : 115',
            'L': '=YawPipeRadius + Offset / cos(Theta) + 0.5 * MM * cos(Theta)',
        }
    }


def _get_tail_parameters_by_key() -> dict:
    return {
        'Inputs': {
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius',
            'BracketLength': '=Spreadsheet.BracketLength',
            'HingeInnerBodyOuterRadius': '=Spreadsheet.HingeInnerBodyOuterRadius',
            'VerticalPlaneAngle': '=Spreadsheet.VerticalPlaneAngle',
            'HingeInnerBodyLength': '=Spreadsheet.HingeInnerBodyLength',
            'HingeOuterBodyLength': '=Spreadsheet.HingeOuterBodyLength',
            'YawBearingTailHingeJunctionHeight': '=Spreadsheet.YawBearingTailHingeJunctionHeight',
            'YawBearingTailHingeJunctionFullWidth': '=Spreadsheet.YawBearingTailHingeJunctionFullWidth',
            'YawBearingTailHingeJunctionInnerWidth': '=Spreadsheet.YawBearingTailHingeJunctionInnerWidth',
            'YawBearingTailHingeJunctionChamfer': '=Spreadsheet.YawBearingTailHingeJunctionChamfer',
            'YawPipeRadius': '=Spreadsheet.YawPipeRadius',
            'HorizontalPlaneAngle': '=Spreadsheet.HorizontalPlaneAngle',
            'FlatMetalThickness': '=Spreadsheet.FlatMetalThickness',
            'BoomPipeRadius': '=Spreadsheet.BoomPipeRadius'
        },
        'Vane': {
            'DistanceToFirstHole': '=BracketLength / 10',
            'DistanceBetweenHoles': '=BracketLength / 2',
            'VaneBracketAngle': '45'
        },
        'Tail Hinge Pipe X Z': {
            'XRotationOffset': '=HingeInnerBodyOuterRadius - cos(VerticalPlaneAngle) * HingeInnerBodyOuterRadius',
            'TrigOffset': '=tan(VerticalPlaneAngle) * (YawBearingTailHingeJunctionHeight - FlatMetalThickness) + XRotationOffset',
            'TailHingePipeX': '=HingeInnerBodyOuterRadius + YawPipeRadius - YawBearingTailHingeJunctionChamfer + YawBearingTailHingeJunctionInnerWidth - TrigOffset',
            'TailHingePipeZ': '=-HingeInnerBodyOuterRadius * sin(VerticalPlaneAngle)'
        },
        'Outer Tail Hinge X Z': {
            'PipeHeightOffset': '=HingeInnerBodyLength - HingeOuterBodyLength',
            'XXX': '=sin(VerticalPlaneAngle) * PipeHeightOffset',
            'ZZZ': '=cos(VerticalPlaneAngle) * PipeHeightOffset',
            'OuterTailHingeX': '=XXX + TailHingePipeX',
            'OuterTailHingeZ': '=ZZZ + TailHingePipeZ'
        },
        'Outer Tail Hinge Low End Stop': {
            'TailBoomTriangularBraceWidth': '=0.27 * RotorDiskRadius',
            'h1': '=-(TailHingePipeZ / cos(VerticalPlaneAngle))',
            'h2': '=YawBearingTailHingeJunctionHeight / cos(VerticalPlaneAngle)',
            'OuterHingeJunctionVerticalGap': '=HingeInnerBodyLength - HingeOuterBodyLength - h2 - h1',
            'HorizontalPipeLength': '=sin(90 - VerticalPlaneAngle) * YawPipeRadius',
            'HorizontalEstimate': '=cos(90 - VerticalPlaneAngle) * (TailBoomTriangularBraceWidth + OuterHingeJunctionVerticalGap)',
            'HorizontalDistanceBetweenOuterYawPipes': '=YawBearingTailHingeJunctionFullWidth + HorizontalEstimate + HorizontalPipeLength - HingeInnerBodyOuterRadius',
            'OuterTailHingeLowEndStopAngle': '=-(90deg - atan(YawPipeRadius / HorizontalDistanceBetweenOuterYawPipes))'
        },
        'Tail Boom Triangular Brace': {
            'TailBoomTriangularBraceXOffset': '=sin(VerticalPlaneAngle) * TailBoomTriangularBraceWidth',
            'TailBoomTriangularBraceZOffset': '=cos(VerticalPlaneAngle) * TailBoomTriangularBraceWidth'
        },
        'Tail Angle': {
            'DefaultTailAngle': '110',
            'TailAngle': '=180 - HorizontalPlaneAngle - DefaultTailAngle'
        },
        'Tail': {
            'TailXInitial': '=cos(VerticalPlaneAngle) * YawPipeRadius',
            'TailZOffset': '=-sin(VerticalPlaneAngle) * YawPipeRadius'
        },
        'P': {
            'Px': '=TailXInitial + OuterTailHingeX + TailBoomTriangularBraceXOffset',
            'Py': '0',
            'Pz': '=BoomPipeRadius + TailZOffset + OuterTailHingeZ + TailBoomTriangularBraceZOffset'
        },
        'C': {
            'Cx': '=OuterTailHingeX',
            'Cy': '0',
            'Cz': '=OuterTailHingeZ'
        },
        'C': {
            'Cx': '=OuterTailHingeX',
            'Cy': '0',
            'Cz': '=OuterTailHingeZ'
        },
        'Q': {
            'Qx': '=Px - Cx',
            'Qy': '=Py - Cy',
            'Qz': '=Pz - Cz'
        },
        'A': {
            'Ax': '=sin(VerticalPlaneAngle)',
            'Ay': '0',
            'Az': '=cos(VerticalPlaneAngle)'
        },
        # Rotation Matrix from Axis and Angle
        # Formula: https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        'r1': {
            'r11': '=cos(TailAngle) + Ax ^ 2 * (1 - cos(TailAngle))',
            'r12': '=Ax * Ay * (1 - cos(TailAngle)) - Az * sin(TailAngle)',
            'r13': '=Ax * Az * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
        },
        'r2': {
            'r21': '=Ay * Ax * (1 - cos(TailAngle)) + Az * sin(TailAngle)',
            'r22': '=cos(TailAngle) + Ay ^ 2 * (1 - cos(TailAngle))',
            'r23': '=Ay * Az * (1 - cos(TailAngle)) - Ax * sin(TailAngle)',
        },
        'r3': {
            'r31': '=Az * Ax * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
            'r32': '=Az * Ay * (1 - cos(TailAngle)) + Ax * sin(TailAngle)',
            'r33': '=cos(TailAngle) + Az ^ 2 * (1 - cos(TailAngle))',
        },
        # Rotation Matrix * (P - C)
        'R': {
            'Rx': '=r11 * Qx + r12 * Qy + r13 * Qz',
            'Ry': '=r21 * Qx + r22 * Qy + r23 * Qz',
            'Rz': '=r31 * Qx + r32 * Qy + r33 * Qz'
        },
        'Tail X Y Z': {
            'TailX': '=Cx + Rx',
            'TailY': '=Cy + Ry',
            'TailZ': '=Cz + Rz'
        }
    }


def _get_star_shape_parameters_by_key() -> dict:
    return {
        'Inputs': {
            'ResineStatorOuterRadius': '=Spreadsheet.ResineStatorOuterRadius',
            'Holes': '=Spreadsheet.Holes',
            'Offset': '=Spreadsheet.Offset',
            'YawPipeRadius': '=Spreadsheet.YawPipeRadius',
            'MetalLengthL': '=Spreadsheet.MetalLengthL',
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius',
            'CoilLegWidth': '=Spreadsheet.CoilLegWidth',
        },
        'Frame': {
            'StatorHolesCircle': '=RotorDiskRadius + CoilLegWidth + 0.5 * (ResineStatorOuterRadius - (RotorDiskRadius + CoilLegWidth))',
            'a': '=2 * sin(30) * StatorHolesCircle + 2 * (25 + Holes)',
            'B': '=2 * StatorHolesCircle * ((1 - sin(30) * sin(30))^0.5) - MetalLengthL',
            # 25 is the margin from the holes to the edge of the metal.
            'C': '=StatorHolesCircle - MetalLengthL + Holes + 25',
            'MM': '=RotorDiskRadius < 275 ? 100 : 115',
            'L': '=YawPipeRadius + Offset / cos(45) + 0.5 * MM * cos(45)'
        }
    }


def _get_hub_parameters_by_key() -> dict:
    return {
        'Inputs': {
            'HubHolesPlacement': '=Spreadsheet.HubHolesPlacement',
            'HubHoles': '=Spreadsheet.HubHoles',
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius'
        },
        'Middle Pad': {
            'TShapeMiddlePadRadiusMargin': '15',
            'HShapeMiddlePadRadiusMargin': '15',
            'StarShapeMiddlePadRadiusMargin': '20',
            'MiddlePadRadiusMargin': '=RotorDiskRadius < 187.5 ? TShapeMiddlePadRadiusMargin : (RotorDiskRadius < 275 ? HShapeMiddlePadRadiusMargin : StarShapeMiddlePadRadiusMargin)',
            'MiddlePadRadius': '=HubHolesPlacement + HubHoles + MiddlePadRadiusMargin',
            'MiddlePadThickness': '16'
        },
        'Common': {
            'TShapeProtrudingPadThickness': '5',
            'HShapeProtrudingPadThickness': '5',
            'StarShapeProtrudingPadThickness': '10',
            'ProtrudingPadThickness': '=RotorDiskRadius < 187.5 ? TShapeProtrudingPadThickness : (RotorDiskRadius < 275 ? HShapeProtrudingPadThickness : StarShapeProtrudingPadThickness)',
            'CoverThickness': '10'
        },
        'Frame Side Pad': {
            'TShapeFrameSidePadRadius': '32.5',
            'HShapeFrameSidePadRadius': '42.5',
            'StarShapeFrameSidePadRadius': '52.5',
            'FrameSidePadRadius': '=RotorDiskRadius < 187.5 ? TShapeFrameSidePadRadius : (RotorDiskRadius < 275 ? HShapeFrameSidePadRadius : StarShapeFrameSidePadRadius)',
            'TShapeFrameSidePadWidth': '45',
            'HShapeFrameSidePadWidth': '45',
            'StarShapeFrameSidePadWidth': '85',
            'FrameSidePadWidth': '=RotorDiskRadius < 187.5 ? TShapeFrameSidePadWidth : (RotorDiskRadius < 275 ? HShapeFrameSidePadWidth : StarShapeFrameSidePadWidth)'
        },
        'Rotor Side Pad': {
            'TShapeRotorSidePadRadius': '28',
            'HShapeRotorSidePadRadius': '31',
            'StarShapeRotorSidePadRadius': '47.5',
            'RotorSidePadRadius': '=RotorDiskRadius < 187.5 ? TShapeRotorSidePadRadius : (RotorDiskRadius < 275 ? HShapeRotorSidePadRadius : StarShapeRotorSidePadRadius)',
            'TShapeRotorSidePadWidth': '40',
            'HShapeRotorSidePadWidth': '40',
            'StarShapeRotorSidePadWidth': '75',
            'RotorSidePadWidth': '=RotorDiskRadius < 187.5 ? TShapeRotorSidePadWidth : (RotorDiskRadius < 275 ? HShapeRotorSidePadWidth : StarShapeRotorSidePadWidth)'
        },
        'Number of Holes': {
            'TShapeNumberOfHoles': '4',
            'HShapeNumberOfHoles': '5',
            'StarShapeNumberOfHoles': '6',
            'NumberOfHoles': '=RotorDiskRadius < 187.5 ? TShapeNumberOfHoles : (RotorDiskRadius < 275 ? HShapeNumberOfHoles : StarShapeNumberOfHoles)'
        },
        'Stub Axle Shaft Radius': {
            'TShapeStubAxleShaftRadius': '18',
            'HShapeStubAxleShaftRadius': '22.5',
            'StarShapeStubAxleShaftRadius': '30',
            'StubAxleShaftRadius': '=RotorDiskRadius < 187.5 ? TShapeStubAxleShaftRadius : (RotorDiskRadius < 275 ? HShapeStubAxleShaftRadius : StarShapeStubAxleShaftRadius)'
        }
    }
