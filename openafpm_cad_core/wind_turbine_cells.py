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
        Cell('FlatMetalThickness'),
        Cell('WindTurbineShape')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.WindTurbineShape',
             alias='WindTurbineShape')
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
        Cell('AlternatorTiltAngle'),
        Cell('AlternatorPlacement'),
        Cell('FramePlacement')
    ],
    [
        Cell('=Alternator.AlternatorTiltAngle',
             alias='AlternatorTiltAngle'),
        Cell('=Alternator.AlternatorPlacement',
             alias='AlternatorPlacement'),
        Cell('=Alternator.FramePlacement',
             alias='FramePlacement')
    ],
    [
        Cell('T Shape', styles=[Style.ITALIC])
    ],
    [
        Cell('k')
    ],
    [
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
        Cell('ExtendedTopPlacement'),
        Cell('MM'),
        Cell('L'),
    ],
    [
        Cell('=YawBearing.ExtendedTopPlacement',
             alias='ExtendedTopPlacement'),
        Cell('=YawBearing.MM',
             alias='MM'),
        Cell('=YawBearing.L',
             alias='L'),
    ],
    [
        Cell('HighEndStop', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('YawPipeLength')
    ],
    [
        Cell('=HighEndStop.YawPipeLength',
             alias='YawPipeLength')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius'),
        Cell('YawBearingZPosition')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
        Cell('=-Offset',
             alias='YawBearingZPosition')
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
        # Origin of yaw bearing is between yaw pipe and top plate.
        Cell('=(YawPipeLength - FlatMetalThickness) / 2',
             alias='SmallYawBearingY'),
        Cell('=YawBearingZPosition',
             alias='SmallYawBearingZ'),
    ],
    # LargeYawBearing
    # ---------------
    [
        Cell('LargeYawBearing',
             styles=[Style.UNDERLINE, Style.BOLD]),
    ],
    [
        Cell('SpaceBetweenMiddleBracketAndTopEndBracket'),
        Cell('LargeYawBearingYAdjustment'),
        Cell('LargeYawBearingYPreAlternatorTilt')
    ],
    [
        # MetalLengthL / 2 could be replaced by DistanceBetweenCenterOfHoleAndFrameEdge from Alternator.
        Cell('=StarShapeChannelSectionHeight / 2 - MetalLengthL / 2',
             alias='SpaceBetweenMiddleBracketAndTopEndBracket'),
        Cell('=(SpaceBetweenMiddleBracketAndTopEndBracket - (SideWidth + FlatMetalThickness)) / 2',
             alias='LargeYawBearingYAdjustment'),
        Cell('=MetalLengthL / 2 + SideWidth + LargeYawBearingYAdjustment',
             alias='LargeYawBearingYPreAlternatorTilt')
    ],
    [
        Cell('LargeYawBearingZPosition'),
        Cell('LargeYawBearingXPosition'),
        Cell('YawBearingXOffset'),
        Cell('AlternatorLinkYOffset')
    ],
    [
        Cell('=YawBearingZPosition',
             alias='LargeYawBearingZPosition'),
        Cell('=LargeYawBearingZPosition - FrameZ + LargeYawBearingXOffset',
             alias='LargeYawBearingXPosition'),
        Cell('=WindTurbineShape == <<T>> ? SmallYawBearingX : LargeYawBearingX',
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
        Cell('=WindTurbineShape == <<Star>> ? StarShapeChannelSectionHeight : HShapeChannelSectionHeight',
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
        Cell('=WindTurbineShape == <<Star>> ? StarShapeYawBearingY : HShapeYawBearingY',
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
        Cell('=-SmallYawBearingY - FlatMetalThickness',
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
        # Referenced from Frame_Shape_T document.
        Cell('=(YawPipeLength + FlatMetalThickness) / 2',
             alias='SmallVerticalDistanceFromCenter')
    ],
    [
        Cell('LargeVerticalDistanceFromCenter'),
        Cell('=LargeYawBearingY',
             alias='LargeVerticalDistanceFromCenter')
    ],
    [
        Cell('VerticalDistanceFromCenter'),
        Cell('=WindTurbineShape == <<T>> ? SmallVerticalDistanceFromCenter : LargeVerticalDistanceFromCenter',
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
                                '=WindTurbineShape == <<T>> ? SmallYawBearingY : LargeYawBearingY',
                                '=WindTurbineShape == <<T>> ? SmallYawBearingZ : LargeYawBearingZ'),
                            axis=('0', '1', '0'),
                            angle='=WindTurbineShape == <<T>> ? SmallYawBearingAngle : LargeYawBearingAngle'),
    *create_placement_cells(name='AlternatorLink',
                            base=(
                                '=YawBearingX - YawBearingX * cos(AlternatorTiltAngle) + AlternatorXoffset',
                                '=AlternatorLinkYOffset',
                                '0'),
                            axis=('0', '0', '1'),
                            angle='=AlternatorTiltAngle'),
    *create_placement_cells(name='TailAssemblyLink',
                            base=(
                                '=WindTurbineShape == <<T>> ? SmallTailHingeX : LargeTailHingeX',
                                '=WindTurbineShape == <<T>> ? SmallTailHingeY : LargeTailHingeY',
                                '=WindTurbineShape == <<T>> ? SmallTailHingeZ : LargeTailHingeZ'),
                            # Equivalent to (0°, -90°, 270°) in yaw-pitch-roll.
                            axis=('0.58', '0.58', '0.58'),
                            angle='=240deg'),
    # Length from top of channel section to weld flat bar (H & Star shape)
    # -----------------------------------------------------------------------
    [
        Cell('Length from top of channel section to weld flat bar (H & Star shape)', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('GlobalChannelSectionTopPoint'),
        Cell('=AlternatorLinkPlacement * AlternatorPlacement * FramePlacement * vector(-MetalLengthL; -ChannelSectionHeight / 2; 0)',
             alias='GlobalChannelSectionTopPoint')
    ],
    [
        Cell('GlobalChannelSectionMidPoint'),
        # vector (L; 0; MM) local to YawBearing_Extended_Top document.
        Cell('=YawBearingPlacement * ExtendedTopPlacement * vector(L; 0; MM)',
             alias='GlobalChannelSectionBottomPoint')
    ],
    [
        Cell('LengthFromTopOfChannelSectionToWeldTopBarVector'),
        Cell('=GlobalChannelSectionTopPoint - GlobalChannelSectionBottomPoint',
             alias='LengthFromTopOfChannelSectionToWeldTopBarVector')
    ],
    [
        Cell('LengthFromTopOfChannelSectionToWeldTopBar'),
        Cell('=LengthFromTopOfChannelSectionToWeldTopBarVector.Length',
             alias='LengthFromTopOfChannelSectionToWeldTopBar')
    ]
]
