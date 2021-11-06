from typing import List, Tuple

from .cell import Alignment, Cell, Style

__all__ = ['high_end_stop_cells']


def create_placement_cells(name: str,
                           base: Tuple[str, str, str],
                           axis: Tuple[str, str, str],
                           angle: str) -> List[List[Cell]]:
    def namespace(s): return name + s
    x, y, z = base
    X, Y, Z = namespace('X'), namespace('Y'), namespace('Z')
    Base = namespace('Base')
    Ax, Ay, Az = axis
    Axis = namespace('Axis')
    Angle = namespace('Angle')
    Rotation = namespace('Rotation')
    Placement = namespace('Placement')
    return [
        [
            Cell(name, styles=[Style.UNDERLINE])
        ],
        [
            Cell('x', horizontal_alignment=Alignment.RIGHT),
            Cell('y', horizontal_alignment=Alignment.RIGHT),
            Cell('z', horizontal_alignment=Alignment.RIGHT)
        ],
        [
            Cell(x, alias=X),
            Cell(y, alias=Y),
            Cell(z, alias=Z),
        ],
        [
            Cell('Base'),
            Cell('Axis'),
            Cell('Angle')
        ],
        [
            Cell(f'=create(<<vector>>; {X}; {Y}; {Z})',
                 alias=Base),
            Cell(f'=create(<<vector>>; {Ax}; {Ay}; {Az})', alias=Axis),
            Cell(angle, alias=Angle)
        ],
        [
            Cell('Rotation'),
            Cell('Placement')
        ],
        [
            Cell(f'=create(<<rotation>>; {Axis}; {Angle})', alias=Rotation),
            Cell(
                f'=create(<<placement>>; {Base}; {Rotation})', alias=Placement)
        ]
    ]


def concatenate_cells(a: List[List[Cell]],
                      b: List[List[Cell]]) -> List[List[Cell]]:
    cells = []
    for i in range(len(a)):
        row = a[i] + b[i]
        cells.append(row)
    return cells


#: Cells defining the High End Stop spreadsheet.
high_end_stop_cells: List[List[Cell]] = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('FlatMetalThickness'),
        Cell('BoomPipeRadius'),
        Cell('Chamfer')
    ],
    [
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.BoomPipeRadius',
             alias='BoomPipeRadius'),
        Cell('=Spreadsheet.YawBearingTailHingeJunctionChamfer',
             alias='Chamfer')
    ],
    [
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle'),
        Cell('AlternatorTiltAngle')
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle'),
        Cell('=Spreadsheet.AlternatorTiltAngle',
             alias='AlternatorTiltAngle')
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('YawPipeLength'),
        Cell('YawPipeRadius')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.YawPipeLength',
             alias='YawPipeLength'),
        Cell('=Spreadsheet.YawPipeRadius',
             alias='YawPipeRadius')
    ],
    [
        Cell('FrameZ'),
        Cell('MetalLengthL'),
        Cell('MetalThicknessL')
    ],
    [
        Cell('=Alternator.FrameZ',
             alias='FrameZ'),
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL'),
        Cell('=Spreadsheet.MetalThicknessL',
             alias='MetalThicknessL')
    ],
    [
        Cell('TopAngle'),
        Cell('HShapeChannelSectionHeight'),
        Cell('StarShapeChannelSectionHeight')
    ],
    [
        Cell('=HShape.TopAngle',
             alias='TopAngle'),
        Cell('=HShape.H',
             alias='HShapeChannelSectionHeight'),
        Cell('=StarShape.B',
             alias='StarShapeChannelSectionHeight')
    ],
    [
        Cell('Width'),
        Cell('Offset'),
        Cell('LargeYawBearingXOffset')
    ],
    [
        Cell('=HShape.MM',
             alias='Width'),
        Cell('=Spreadsheet.Offset',
             alias='Offset'),
        Cell('=HShape.LargeYawBearingXOffset',
             alias='LargeYawBearingXOffset'),
    ],
    [
        Cell('TShape', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X'), Cell('a')
    ],
    [
        Cell('=TShape.X', alias='X'),
        Cell('=TShape.a', alias='a')
    ],
    [
        Cell('I'), Cell('k')
    ],
    [
        Cell('=TShape.I', alias='I'),
        Cell('=TShape.k', alias='k')
    ],
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('HighEndStopLength'),
        Cell('Margin')
    ],
    [
        Cell('110',
             alias='HighEndStopLength'),
        Cell('20', alias='Margin')
    ],
    [
        Cell('FurlAxis'),
        Cell('FurlAngle'),
        Cell('FurlRotation')
    ],
    [
        Cell('=create(<<vector>>; sin(VerticalPlaneAngle); 0; cos(VerticalPlaneAngle))',
             alias='FurlAxis'),
        Cell('=105deg',
             alias='FurlAngle'),
        Cell('=create(<<rotation>>; FurlAxis; FurlAngle)',
             alias='FurlRotation')
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
        Cell('=(-a / 2 + FlatMetalThickness + Margin * 2) * -1',
             alias='SmallYawBearingY'),
        Cell('=-X - YawPipeRadius * 2',
             alias='SmallYawBearingZ'),
    ],
    # LargeYawBearing
    # ---------------
    [
        Cell('LargeYawBearing',
             styles=[Style.UNDERLINE, Style.BOLD]),
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
        Cell('=MetalLengthL * 0.5 + FlatMetalThickness + Width + AlternatorLinkY',
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
        Cell('=LargeYawBearingZ - FrameZ + LargeYawBearingXOffset',
             alias='LargeYawBearingX'),
        Cell('=RotorDiskRadius < 275 ? HShapeYawBearingY : StarShapeYawBearingY',
             alias='LargeYawBearingY'),
        Cell('=-Offset',
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
        Cell('=a / 2 - Margin * 2',
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
                                '=RotorDiskRadius < 187.5 ? SmallYawBearingX : LargeYawBearingX',
                                '=RotorDiskRadius < 187.5 ? SmallYawBearingY : LargeYawBearingY',
                                '=RotorDiskRadius < 187.5 ? SmallYawBearingZ : LargeYawBearingZ'),
                            axis=('0', '1', '0'),
                            angle='=RotorDiskRadius < 187.5 ? SmallYawBearingAngle : LargeYawBearingAngle'),
    *create_placement_cells(name='AlternatorLink',
                            base=(
                                '=YawBearingX - YawBearingX * cos(AlternatorTiltAngle) + AlternatorXoffset',
                                '=-sin(AlternatorTiltAngle) * YawBearingX',
                                '0'),
                            axis=('0', '0', '1'),
                            angle='=AlternatorTiltAngle'),
    *create_placement_cells(name='TailHingeAssemblyLink',
                            base=(
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeX : LargeTailHingeX',
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeY : LargeTailHingeY',
                                '=RotorDiskRadius < 187.5 ? SmallTailHingeZ : LargeTailHingeZ'),
                            axis=('0.58', '0.58', '0.58'),
                            angle='=240deg'),
    *create_placement_cells(name='TailHingeAssembly',
                            base=(
                                '=Chamfer * cos(180 - HorizontalPlaneAngle)',
                                '=Chamfer * sin(-(180 - HorizontalPlaneAngle))',
                                '0'),
                            axis=('0', '0', '-1'),
                            angle='=180 - HorizontalPlaneAngle'),
    *create_placement_cells(name='OuterTailHinge',
                            base=(
                                '=Tail.OuterTailHingeX',
                                '0',
                                '=Tail.OuterTailHingeZ'),
                            axis=('0', '1', '0'),
                            angle='=VerticalPlaneAngle'),
    # TailBoomVaneAssemblyLink
    *create_placement_cells(name='Tail',
                            base=(
                                '=Tail.TailX',
                                '=Tail.TailY',
                                '=Tail.TailZ'),
                            axis=('0', '0', '1'),
                            angle='=Tail.TailAngle'),
    *create_placement_cells(name='TailBoomVaneAssembly',
                            base=('0', '0', '0'),
                            axis=('0', '1', '0'),
                            angle='90'),
    *create_placement_cells(name='OuterTailHingeHighEndStop',
                            base=(
                                '=FlatMetalThickness / 2',
                                '=BoomPipeRadius',
                                '0'),
                            axis=('0', '1', '0'),
                            angle='-90'),
    [
        Cell('OppositeEnd', styles=[Style.ITALIC]),
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('=OuterTailHingeHighEndStopX',
             alias='OuterTailHingeHighEndStopOppositeEndX'),
        Cell('=OuterTailHingeHighEndStopY',
             alias='OuterTailHingeHighEndStopOppositeEndY'),
        Cell('=HighEndStopLength',
             alias='OuterTailHingeHighEndStopOppositeEndZ'),
    ],
    [
        Cell('Base'),
        Cell('Placement')
    ],
    [
        Cell('=create(<<vector>>; OuterTailHingeHighEndStopOppositeEndX; OuterTailHingeHighEndStopOppositeEndY; OuterTailHingeHighEndStopOppositeEndZ)',
             alias='OuterTailHingeHighEndStopOppositeEndBase'),
        Cell('=create(<<placement>>; OuterTailHingeHighEndStopOppositeEndBase; OuterTailHingeHighEndStopRotation)',
             alias='OuterTailHingeHighEndStopOppositeEndPlacement')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('TailFurlBase'),
        Cell('TailFurlPlacement'),
        Cell('FurledHighEndStopGlobalParentPlacement'),
    ],
    [
        # C - rot.multVec(C)
        Cell('=.OuterTailHingeBase - FurlRotation * .OuterTailHingeBase',
             alias='TailFurlBase'),
        Cell('=create(<<placement>>; TailFurlBase; FurlRotation)',
             alias='TailFurlPlacement'),
        Cell('=TailHingeAssemblyLinkPlacement * TailHingeAssemblyPlacement * TailFurlPlacement * TailPlacement * TailBoomVaneAssemblyPlacement',
             alias='FurledHighEndStopGlobalParentPlacement')
    ],
    [
        Cell('OuterTailHingeHighEndStopFurledPlacement'),
        Cell('OuterTailHingeHighEndStopOppositeEndFurledPlacement')
    ],
    [
        Cell('=FurledHighEndStopGlobalParentPlacement * OuterTailHingeHighEndStopPlacement',
             alias='OuterTailHingeHighEndStopFurledPlacement'),
        Cell('=FurledHighEndStopGlobalParentPlacement * OuterTailHingeHighEndStopOppositeEndPlacement',
             alias='OuterTailHingeHighEndStopOppositeEndFurledPlacement')
    ],
    [
        Cell('OuterTailHingeHighEndStopFurledBase'),
        Cell('OuterTailHingeHighEndStopOppositeEndFurledBase')
    ],
    [
        Cell('=OuterTailHingeHighEndStopFurledPlacement.Base',
             alias='OuterTailHingeHighEndStopFurledBase'),
        Cell('=OuterTailHingeHighEndStopOppositeEndFurledPlacement.Base',
             alias='OuterTailHingeHighEndStopOppositeEndFurledBase')
    ],
    [
        Cell('References', styles=[Style.ITALIC, Style.UNDERLINE])
    ],
    [
        Cell('Finding a point on a 3d line',
             styles=[Style.ITALIC]),
        Cell('What is the equation for a 3D line?',
             styles=[Style.ITALIC]),
    ],
    [
        Cell('https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154'),
        Cell('https://math.stackexchange.com/questions/404440/what-is-the-equation-for-a-3d-line/404446#404446')
    ],
    [
        Cell('Zgiven'),
        Cell('T'),
        Cell('HighEndStopPointWhereZIsZero'),
        Cell('HighEndStopWidth', styles=[Style.BOLD, Style.UNDERLINE]),
    ],
    [
        # Center of Yaw Bearing
        Cell('=YawBearingZ', alias='Zgiven'),
        # T = Zgiven - Az / (Bz - Az)
        # See above "Finding a point on a 3d line" answer.
        Cell('=(Zgiven - .OuterTailHingeHighEndStopFurledBase.z) / (.OuterTailHingeHighEndStopOppositeEndFurledBase.z - .OuterTailHingeHighEndStopFurledBase.z)',
             alias='T'),
        Cell('=.OuterTailHingeHighEndStopFurledBase + T * (.OuterTailHingeHighEndStopOppositeEndFurledBase - .OuterTailHingeHighEndStopFurledBase)',
             alias='HighEndStopPointWhereZIsZero'),
        Cell('=abs(.HighEndStopPointWhereZIsZero.x) - YawPipeRadius + YawBearingX',
             alias='HighEndStopWidth')  # 57.12 desired for T Shape
    ],
    # SafetyCatch
    # -----------
    [
        Cell('SafetyCatch', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('SafetyCatchWidth'),
        Cell('=YawPipeRadius',
             alias='SafetyCatchWidth')
    ],
    [
        Cell('SafetyCatchLength'),
        Cell('=SafetyCatchWidth * 1.33',
             alias='SafetyCatchLength')
    ],
    [
        # of High End Stop
        Cell('UpperBottomLeftCorner'),
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; 0)',
             alias='UpperBottomLeftCorner')
    ],
    [
        Cell('UpperBottomLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * UpperBottomLeftCorner',
             alias='UpperBottomLeftCornerGlobal')
    ],
    [
        # of High End Stop
        Cell('UpperTopLeftCorner'),
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; HighEndStopLength)',
             alias='UpperTopLeftCorner')
    ],
    [
        Cell('UpperTopLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * UpperTopLeftCorner',
             alias='UpperTopLeftCornerGlobal')
    ],
    [
        # Zgiven
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Zupper'),
        Cell('=YawBearingZ + (SafetyCatchWidth / 2)',
             alias='Zupper')
    ],
    [
        # T
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Tupper'),
        Cell('=(Zupper - .UpperBottomLeftCornerGlobal.z) / (.UpperTopLeftCornerGlobal.z - .UpperBottomLeftCornerGlobal.z)',
             alias='Tupper')
    ],
    [
        Cell('SafetyCatchPosition'),
        Cell('=.UpperBottomLeftCornerGlobal + Tupper * (UpperTopLeftCornerGlobal - .UpperBottomLeftCornerGlobal)',
             alias='SafetyCatchPosition')
    ],
    [
        # Y position of the safety catch
        # in coordinate system relative to
        # yaw bearing centered at origin.
        # +3 for a little extra clearance.
        Cell('SafetyCatchY'),
        Cell('=.SafetyCatchPosition.y + 3',
             alias='SafetyCatchY')
    ]
]
