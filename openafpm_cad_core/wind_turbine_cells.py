from typing import List

from .create_placement_cells import create_placement_cells
from .spreadsheet import Alignment, Cell, Style

__all__ = ['wind_turbine_cells']


wind_turbine_cells: List[List[Cell]] = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('FlatMetalThickness')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness')
    ],
    [
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle'),
        Cell('Offset')
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle'),
        Cell('=Spreadsheet.Offset',
             alias='Offset')
    ],
    [
        Cell('YawPipeDiameter'),
        Cell('MetalLengthL'),
        Cell('MetalThicknessL')
    ],
    [
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter'),
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL'),
        Cell('=Spreadsheet.MetalThicknessL',
             alias='MetalThicknessL')
    ],
    [
        Cell('Alternator', styles=[Style.UNDERLINE])
        # ------------------------------------------
    ],
    [
        Cell('FrameZ'),
        Cell('HShapeChannelSectionHeight'),
        Cell('StarShapeChannelSectionHeight')
    ],
    [
        Cell('=Alternator.FrameZ',
             alias='FrameZ'),
        Cell('=Alternator.HH',
             alias='HShapeChannelSectionHeight'),
        Cell('=Alternator.B',
             alias='StarShapeChannelSectionHeight')
    ],
    [
        Cell('AlternatorTiltAngle')
    ],
    [
        Cell('=Alternator.AlternatorTiltAngle',
             alias='AlternatorTiltAngle')
    ],
    [
        Cell('T Shape', styles=[Style.ITALIC])
    ],
    [
        Cell('X'), Cell('TShapeTwoHoleEndBracketLength (A)')
    ],
    [
        Cell('=Alternator.X', alias='X'),
        Cell('=Alternator.TShapeTwoHoleEndBracketLength',
             alias='TShapeTwoHoleEndBracketLength')
    ],
    [
        Cell('I'), Cell('k')
    ],
    [
        Cell('=Alternator.I', alias='I'),
        Cell('=Alternator.k', alias='k')
    ],
    [
        Cell('YawBearing', styles=[Style.UNDERLINE])
        # ------------------------------------------
    ],
    [
        Cell('TopAngle'),
        Cell('SideWidth'),
        Cell('LargeYawBearingXOffset')
    ],
    [
        Cell('=YawBearing.TopAngle',
             alias='TopAngle'),
        Cell('=YawBearing.SideWidth',
             alias='SideWidth'),
        Cell('=YawBearing.LargeYawBearingXOffset',
             alias='LargeYawBearingXOffset'),
    ],
    [
        Cell('YawPipeLength')
    ],
    [
        Cell('=YawBearing.YawPipeLength',
             alias='YawPipeLength')
    ],
    [
        Cell('Tail', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('Chamfer'),
        Cell('LowEndStopPlacement'),
        Cell('LowEndStopLengthToYawPipe')
    ],
    [
        Cell('=Tail.TailHingeJunctionChamfer',
             alias='Chamfer'),
        Cell('=Tail.LowEndStopPlacement',
             alias='LowEndStopPlacement'),
        Cell('=Tail.LowEndStopLengthToYawPipe',
             alias='LowEndStopLengthToYawPipe')
    ],
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Margin')
    ],
    [
        Cell('20', alias='Margin')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
    ],
    # SmallYawBearing
    # ---------------
    [
        Cell('SmallYawBearing',
             styles=[Style.UNDERLINE, Style.BOLD]),
    ],
    [
        Cell('Angle'),
    ],
    [
        Cell('=90deg', alias='SmallYawBearingAngle'),
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT),
    ],
    [
        Cell('=-FrameZ - YawPipeRadius - k + MetalLengthL - MetalThicknessL',
             alias='SmallYawBearingX'),
        Cell('=(-TShapeTwoHoleEndBracketLength / 2 + FlatMetalThickness + Margin * 2) * -1',
             alias='SmallYawBearingY'),
        Cell('=-X - YawPipeDiameter',
             alias='SmallYawBearingZ'),
    ],
    # LargeYawBearing
    # ---------------
    [
        Cell('LargeYawBearing',
             styles=[Style.UNDERLINE, Style.BOLD]),
    ],
    [
        Cell('SpaceBetweenMiddleBrackentAndTopEndBracket'),
        Cell('LargeYawBearingYAdjustment'),
        Cell('LargeYawBearingYPreAlternatorTilt')
    ],
    [
        Cell('=StarShapeChannelSectionHeight / 2 - MetalLengthL * 0.5',
             alias='SpaceBetweenMiddleBrackentAndTopEndBracket'),
        Cell('=(SpaceBetweenMiddleBrackentAndTopEndBracket - (SideWidth + FlatMetalThickness)) / 2',
             alias='LargeYawBearingYAdjustment'),
        Cell('=MetalLengthL * 0.5 + SideWidth + LargeYawBearingYAdjustment',
             alias='LargeYawBearingYPreAlternatorTilt')
    ],
    [
        Cell('LargeYawBearingZPosition'),
        Cell('LargeYawBearingXPosition'),
        Cell('YawBearingXOffset'),
        Cell('AlternatorLinkYOffset')
    ],
    [
        Cell('=-Offset',
             alias='LargeYawBearingZPosition'),
        Cell('=LargeYawBearingZPosition - FrameZ + LargeYawBearingXOffset',
             alias='LargeYawBearingXPosition'),
        Cell('=RotorDiskRadius < 187.5 ? SmallYawBearingX : LargeYawBearingX',
             alias='YawBearingXOffset'),
        Cell('=-sin(AlternatorTiltAngle) * YawBearingXOffset',
             alias='AlternatorLinkYOffset')
    ],
    [
        Cell('ChannelSectionHeight'),
        Cell('HShapeYawBearingY'),
        Cell('StarShapeYawBearingY')
    ],
    [
        Cell('=RotorDiskRadius < 275 ? HShapeChannelSectionHeight : StarShapeChannelSectionHeight',
             alias='ChannelSectionHeight'),
        Cell('=ChannelSectionHeight * 0.25',
             alias='HShapeYawBearingY'),
        Cell('=LargeYawBearingYPreAlternatorTilt',
             alias='StarShapeYawBearingY')
    ],
    [
        Cell('Angle')
    ],
    [
        Cell('=-TopAngle',
             alias='LargeYawBearingAngle')
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT),
    ],
    [
        Cell('=LargeYawBearingXPosition',
             alias='LargeYawBearingX'),
        Cell('=RotorDiskRadius < 275 ? HShapeYawBearingY : StarShapeYawBearingY',
             alias='LargeYawBearingY'),
        Cell('=LargeYawBearingZPosition',
             alias='LargeYawBearingZ'),
    ],
    # SmallTailHinge
    # --------------
    [
        Cell('SmallTailHinge',
             styles=[Style.UNDERLINE, Style.BOLD]),
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT),
    ],
    [
        Cell('=SmallYawBearingX',
             alias='SmallTailHingeX'),
        Cell('=-YawPipeLength / 2',
             alias='SmallTailHingeY'),
        Cell('=SmallYawBearingZ',
             alias='SmallTailHingeZ'),
    ],
    # LargeTailHinge
    # --------------
    [
        Cell('LargeTailHinge',
             styles=[Style.UNDERLINE, Style.BOLD]),
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT),
    ],
    [
        Cell('=LargeYawBearingX',
             alias='LargeTailHingeX'),
        Cell('=-(YawPipeLength - LargeYawBearingY)',
             alias='LargeTailHingeY'),
        Cell('=LargeYawBearingZ',
             alias='LargeTailHingeZ'),
    ],
    # VerticalDistanceFromCenter
    # --------------------------
    [
        Cell('VerticalDistanceFromCenter',
             styles=[Style.UNDERLINE, Style.BOLD]),
        Cell('Vertical distance of Yaw Bearing from Center of Hub',
             styles=[Style.ITALIC])
    ],
    [
        Cell('SmallVerticalDistanceFromCenter'),
        Cell('=TShapeTwoHoleEndBracketLength / 2 - Margin * 2',
             alias='SmallVerticalDistanceFromCenter')
    ],
    [
        Cell('LargeVerticalDistanceFromCenter'),
        Cell('=LargeYawBearingY',
             alias='LargeVerticalDistanceFromCenter')
    ],
    [
        Cell('VerticalDistanceFromCenter'),
        Cell('=RotorDiskRadius < 187.5 ? SmallVerticalDistanceFromCenter : LargeVerticalDistanceFromCenter',
             alias='VerticalDistanceFromCenter')
    ],
    [
        Cell('AlternatorXoffset'),
        Cell('=cos(90deg - AlternatorTiltAngle) * VerticalDistanceFromCenter',
             alias='AlternatorXoffset')
    ],
    # Placement
    # ---------
    [
        Cell('Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    *create_placement_cells(name='YawBearing',
                            base=(
                                '=YawBearingXOffset',
                                '=RotorDiskRadius < 187.5 ? SmallYawBearingY : LargeYawBearingY',
                                '=RotorDiskRadius < 187.5 ? SmallYawBearingZ : LargeYawBearingZ'),
                            axis=('0', '1', '0'),
                            angle='=RotorDiskRadius < 187.5 ? SmallYawBearingAngle : LargeYawBearingAngle'),
    *create_placement_cells(name='AlternatorLink',
                            base=(
                                '=YawBearingX - YawBearingX * cos(AlternatorTiltAngle) + AlternatorXoffset',
                                '=AlternatorLinkYOffset',
                                '0'),
                            axis=('0', '0', '1'),
                            angle='=AlternatorTiltAngle'),
    *create_placement_cells(name='TailAssemblyLink',
                            base=(
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeX : LargeTailHingeX',
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeY : LargeTailHingeY',
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeZ : LargeTailHingeZ'),
                            # Equivalent to (0°, -90°, 270°) in yaw-pitch-roll.
                            axis=('0.58', '0.58', '0.58'),
                            angle='=240deg')
]
