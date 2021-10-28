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
        Cell('=Master_of_Puppets#Spreadsheet.YawBearingTailHingeJunctionChamfer',
             alias='Chamfer')
    ],
    [
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle')
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle')
    ],
    [
        Cell('YawPipeLength'),
        Cell('YawPipeRadius')
    ],
    [
        Cell('=Spreadsheet.YawPipeLength',
             alias='YawPipeLength'),
        Cell('=Spreadsheet.YawPipeRadius',
             alias='YawPipeRadius')
    ],
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('HighEndStopLength'),
        Cell('FurlAngle'),
        Cell('FurlRotation')
    ],
    [
        Cell('110',
             alias='HighEndStopLength'),
        Cell('=105deg',
             alias='FurlAngle'),
        Cell('=create(<<rotation>>; create(<<vector>>; sin(VerticalPlaneAngle); 0; cos(VerticalPlaneAngle)); FurlAngle)',
             alias='FurlRotation')
    ],
    # Placement
    # ---------
    [
        Cell('Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    *create_placement_cells(name='TailHingeAssemblyLink',
                            base=('0', '=-YawPipeLength / 2', '0'),
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
        Cell('PointWhereZEqualsZero'),
        Cell('HighEndStopWidth', styles=[Style.BOLD, Style.UNDERLINE]),
    ],
    [
        # Center of Yaw Bearing
        Cell('0', alias='Zgiven'),
        # T = Zgiven - Az / (Bz - Az)
        # See above "Finding a point on a 3d line" answer.
        Cell('=Zgiven - .OuterTailHingeHighEndStopFurledBase.z / (.OuterTailHingeHighEndStopOppositeEndFurledBase.z - .OuterTailHingeHighEndStopFurledBase.z)',
             alias='T'),
        Cell('=.OuterTailHingeHighEndStopFurledBase + T * (.OuterTailHingeHighEndStopOppositeEndFurledBase - .OuterTailHingeHighEndStopFurledBase)',
             alias='PointWhereZEqualsZero'),
        Cell('=abs(.PointWhereZEqualsZero.x) - YawPipeRadius',
             alias='HighEndStopWidth')
    ],
    [
        Cell('SafetyCatch', styles=[Style.UNDERLINE])
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('=-YawPipeRadius',
             alias='SafetyCatchX'),
        # FlatMetalThickness * 3 is a rough guess.
        # To ensure that the safety catch is above the high end stop.
        Cell('=.PointWhereZEqualsZero.y + FlatMetalThickness * 3',
             alias='SafetyCatchY'),
        Cell('=Zgiven',
             alias='SafetyCatchZ'),
    ],
    [
        Cell('Base')
    ],
    [
        Cell('=create(<<vector>>; SafetyCatchX; SafetyCatchY; SafetyCatchZ)',
             alias='SafetyCatchBase')
    ]
]
