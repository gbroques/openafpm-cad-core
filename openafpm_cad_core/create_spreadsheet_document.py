import FreeCAD as App

__all__ = ['create_spreadsheet_document']


def create_spreadsheet_document(magnafpm_parameters: dict,
                                furling_parameters: dict,
                                user_parameters: dict):
    calculated_parameters = _get_calculated_parameters()
    parameters_by_key = {
        'MagnAFPM': magnafpm_parameters,
        'OpenFurl': furling_parameters,
        'User': user_parameters,
        'Calculated': calculated_parameters
    }
    document = App.newDocument('Master of Puppets')

    _add_spreadsheet(document, 'Spreadsheet', parameters_by_key)
    _add_spreadsheet(document, 'TShape', _get_t_shape_parameters_by_key())
    _add_spreadsheet(document, 'HShape', _get_h_shape_parameters_by_key())
    _add_spreadsheet(document, 'StarShape', _get_star_shape_parameters_by_key())
    _add_spreadsheet(document, 'Hub', _get_hub_parameters_by_key())
    document.recompute()
    return document


def _add_spreadsheet(document, name, parameters_by_key):
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    cells = _build_cells(parameters_by_key)
    _populate_spreadsheet(sheet, cells)


def _build_cells(parameters_by_key):
    cells = []
    for key, parameters in parameters_by_key.items():
        cells.append([key, ''])
        cells.extend(_dict_to_cells(parameters))
    return cells


def _dict_to_cells(dictionary):
    return [[key, value] for key, value in dictionary.items()]


def _populate_spreadsheet(spreadsheet, cells):
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


def _get_calculated_parameters():
    return {
        'ResineStatorOuterRadius': '=RotorDiskRadius < 275 ? (RotorDiskRadius + CoilLegWidth + 20) : (RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
        'YawPipeScaleFactor': '=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
        'YawPipeLength': '=RotorDiskRadius * YawPipeScaleFactor * 2',
        'YawBearingTopPlateHoleRadius': '=RotorDiskRadius < 187.5 ? 10 : 15',
        'HingeInnerBodyOuterRadius': '=RotorDiskRadius < 187.5 ? 24.15 : (RotorDiskRadius < 275 ? 38 : 44.5)',
        'HingeInnerBodyLength': '=0.8 * 2 * RotorDiskRadius',
        'YawBearingTailHingeJunctionHeight': '85',
        'HingeOuterBodyLength': '=HingeInnerBodyLength - YawBearingTailHingeJunctionHeight - 10 - 10',
        'YawBearingTailHingeJunctionChamfer': '15',
        'hypotenuse': '=(YawBearingTailHingeJunctionHeight - FlatMetalThickness) / cos(VerticalPlaneAngle)',
        'YawBearingTailHingeJunctionInnerWidth': '=sqrt(hypotenuse ^ 2 - (YawBearingTailHingeJunctionHeight - FlatMetalThickness) ^ 2)',
        'YawBearingTailHingeJunctionFullWidth': '=YawPipeRadius + HingeInnerBodyOuterRadius + YawBearingTailHingeJunctionInnerWidth'
    }


def _get_t_shape_parameters_by_key():
    return {
        'Inputs': {
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius',
            'Offset': '=Spreadsheet.Offset',
            'YawPipeRadius': '=Spreadsheet.YawPipeRadius',
            'MetalThicknessL': '=Spreadsheet.MetalThicknessL',
            'MetalLengthL': '=Spreadsheet.MetalLengthL',
            'ResineStatorOuterRadius': '=Spreadsheet.ResineStatorOuterRadius',
            'Holes': '=Spreadsheet.Holes'
        },
        'Yaw Bearing to Frame Junction': {
            'I': '=1 / 70 * (sqrt(77280 * RotorDiskRadius - 9503975) + 235)',
            'j': '=0.32 * RotorDiskRadius - 3',
            'k': '=0.2 * RotorDiskRadius - 5'
        },
        'Frame': {
            'X': '=Offset - (I + YawPipeRadius)',
            # 30 degrees because 360 / 3 = 120 - 90 = 30.
            # Divide by 3 for because the T Shape has 3 holes.
            # cos(30) * ResineStatorOuterRadius = bottom of right triangle
            # * 2 to get both sides.
            # 40 = 2 * margin. margin is the distance from the hole to the edge of the metal.
            # Add the radius for holes on each side, + Spreadsheet.Holes * 2.
            'a': '=cos(30) * ResineStatorOuterRadius * 2 + 40 + Holes * 2',
            # Total vertical distance of T Shape from bottom hole to two top holes.
            # This is the opposite, or vertical left side of the right triangle plus,
            # the stator resin cast radius.
            'TShapeVerticalDistance': '=(sin(30) * ResineStatorOuterRadius) + ResineStatorOuterRadius',
            # Subtract MetalLengthL as the top holes and bottom hole are centered in the brackets.
            # MetalLengthL is the length of the brackets.
            'BC': '=TShapeVerticalDistance - MetalLengthL',
            'D': '=MetalLengthL * 2'
        }
    }


def _get_h_shape_parameters_by_key():
    return {
        'Inputs': {
            'RotorDiskRadius': '=Spreadsheet.RotorDiskRadius',
            'Offset': '=Spreadsheet.Offset',
            'YawPipeRadius': '=Spreadsheet.YawPipeRadius',
            'MetalLengthL': '=Spreadsheet.MetalLengthL',
            'ResineStatorOuterRadius': '=Spreadsheet.ResineStatorOuterRadius'
        },
        'Frame': {
            'Delta': '=100 - 8 * (25 - ResineStatorOuterRadius * ResineStatorOuterRadius)',
            'Alpha': '=(10 + Delta ^ 0.5) / 4',
            # G is determined by trigonometry from the radius of the holes in the frame.
            # 40 = 2 * margin. margin is the distance from the hole to the edge of the metal.
            'G': '=2 * Alpha + 40',
            'H': '=G - 2 * MetalLengthL',  # To make the frame square
            'MM': '=RotorDiskRadius < 275 ? 100 : 115',
            'L': '=YawPipeRadius + Offset / cos(45) + 0.5 * MM * cos(45)',
        }
    }


def _get_star_shape_parameters_by_key():
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


def _get_hub_parameters_by_key():
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
