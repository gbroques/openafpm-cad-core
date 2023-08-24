from typing import List

from .create_placement_cells import create_placement_cells
from .pipe_size import PipeSize
from .spreadsheet import Alignment, Cell, Style

__all__ = ['tail_cells']

tail_cells: List[List[Cell]] = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('BracketLength'),
        Cell('FlatMetalThickness')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.BracketLength',
             alias='BracketLength'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness')
    ],
    [
        Cell('YawPipeDiameter'),
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle')
    ],
    [
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter'),
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle')
    ],
    [
        Cell('BoomPipeDiameter'),
        Cell('BoomLength')
    ],
    [
        Cell('=Spreadsheet.BoomLength',
             alias='BoomLength'),
        Cell('=Spreadsheet.BoomPipeDiameter',
             alias='BoomPipeDiameter')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius'),
        Cell('BoomPipeRadius')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
        Cell('=BoomPipeDiameter / 2',
             alias='BoomPipeRadius'),
    ],
    # Hinge
    # -----
    [
        # Inner and Outer Pipe dimensions for Hinge are described
        # in a table on page 31 of "A Wind Turbine Recipe Book (2014)".
        Cell('Hinge', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('InnerPipeRadius', styles=[Style.UNDERLINE]),
        Cell('Select one size small for inner hinge than outer hinge based on pipe size list.')
    ],
    [
        Cell('LargestPipeDiameter'),
        Cell(f'{PipeSize.OD_141_3.value}',
             alias='LargestPipeDiameter')
    ],
    [
        Cell('Range8'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_141_3.value} ? {PipeSize.OD_127_0.value} : LargestPipeDiameter',
             alias='Range8')
    ],
    [
        Cell('Range7'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_127_0.value} ? {PipeSize.OD_114_3.value} : Range8',
             alias='Range7')
    ],
    [
        Cell('Range6'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_114_3.value} ? {PipeSize.OD_101_6.value} : Range7',
             alias='Range6')
    ],
    [
        Cell('Range5'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_101_6.value} ? {PipeSize.OD_88_9.value} : Range6',
             alias='Range5')
    ],
    [
        Cell('Range4'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_88_9.value} ? {PipeSize.OD_73_0.value} : Range5',
             alias='Range4')
    ],
    [
        Cell('Range3'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_73_0.value} ? {PipeSize.OD_60_3.value} : Range4',
             alias='Range3')
    ],
    [
        Cell('Range2'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_60_3.value} ? {PipeSize.OD_48_3.value} : Range3',
             alias='Range2')
    ],
    [
        Cell('Range1'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_48_3.value} ? {PipeSize.OD_42_2.value} : Range2',
             alias='Range1')
    ],
    [
        Cell('InnerPipeDiameter'),
        Cell(f'=YawPipeDiameter <= {PipeSize.OD_42_2.value} ? {PipeSize.OD_33_4.value} : Range1',
             alias='HingeInnerPipeDiameter')
    ],
    [
        Cell('InnerPipeRadius'),
        Cell('=HingeInnerPipeDiameter / 2',
             alias='HingeInnerPipeRadius')
    ],
    [
        Cell('InnerPipeLength'),
        # TODO: Should this be a ratio of YawPipeLength? Like:
        #       =0.85 * YawPipeLength
        Cell('=0.8 * 2 * RotorDiskRadius',
             alias='HingeInnerPipeLength')
    ],
    [
        Cell('Junction', styles=[Style.UNDERLINE])
    ],
    [
        Cell('Height'),
        Cell('=HingeInnerPipeLength / 3',
             alias='TailHingeJunctionHeight')
    ],
    [
        Cell('hypotenuse'),
        Cell('=(TailHingeJunctionHeight - FlatMetalThickness) / cos(VerticalPlaneAngle)',
             alias='hypotenuse')
    ],
    [
        Cell('InnerWidth'),
        Cell('=sqrt(hypotenuse ^ 2 - (TailHingeJunctionHeight - FlatMetalThickness) ^ 2)',
             alias='TailHingeJunctionInnerWidth')
    ],
    [
        Cell('FullWidth'),
        Cell('=YawPipeRadius + HingeInnerPipeRadius + TailHingeJunctionInnerWidth',
             alias='TailHingeJunctionFullWidth')
    ],
    [
        Cell('Chamfer'),
        Cell('=YawPipeRadius / 2',
             alias='TailHingeJunctionChamfer')
    ],
    # Tail Hinge Pipe X Z
    # -------------------
    # Document: Tail_Hinge_Inner
    # Part: Pipe
    [
        # TODO: Adjust styles to only underline matching other subsections of "Hinge".
        Cell('Tail Hinge Pipe X Z', styles=[Style.UNDERLINE, Style.BOLD]),
        Cell('The following calculations are in the local coordinate space of Tail_Hinge_Inner.')
    ],
    [
        #
        # |       |
        # |       | Tail Hinge Inner Pipe
        # |       |
        # ----+----
        #
        # + denotes the center of rotation.
        #
        #   /
        #  /      /
        # /_     /  Rotated by VerticalPlaneAngle
        #    - _/
        #
        #    ^
        #    |
        #    |  |\
        #    |  | \
        #    |  |  \
        #    |  |   \ HingeInnerPipeRadius
        #    |  |    \
        #  z |  |     \
        #    |  |_     \
        #    |  |_|___(_+ VerticalPlaneAngle
        #    |
        #    |  <------->
        #    |  Adjacent
        #    |
        #    +-------------------------------->
        #                  x
        #
        # cos(VerticalPlaneAngle) = Adjacent / HingeInnerPipeRadius
        #
        Cell('Adjacent'),
        Cell('=cos(VerticalPlaneAngle) * HingeInnerPipeRadius',
             alias='Adjacent')
    ],
    [
        # XRotationOffset is the X distance the inner tail hinge pipe moves
        # by X when it's rotated by VerticalPlaneAngle about it's center.
        Cell('XRotationOffset'),
        Cell('=HingeInnerPipeRadius - Adjacent',
             alias='XRotationOffset')
    ],
    [
        Cell('JunctionBottom'),
        Cell('=TailHingeJunctionHeight - FlatMetalThickness',
             alias='JunctionBottom')
    ],
    [
        #     ^
        #     |
        #     |                  Opposite
        #     |                 __________
        #     |                 |_|      /
        #     |                 |       /
        #     |                 |      /
        #   z |  JunctionBottom |     /
        #     |                 |    /
        #     |                 |   /
        #     |                 |  /
        #     |                 |⌒/
        #     |                 |/  VerticalPlaneAngle
        #     |
        #     +---------------------------------------------->
        #                           x
        #
        # tan(VerticalPlaneAngle) = Opposite / JunctionBottom
        #
        Cell('Opposite'),
        Cell('=tan(VerticalPlaneAngle) * JunctionBottom',
             alias='Opposite')
    ],
    [
        # Adjust the X position of the inner tail hinge pipe for VerticalPlaneAngle rotation.
        Cell('TrigOffset'),
        Cell('=Opposite + XRotationOffset',
             alias='TrigOffset')
    ],
    [
        Cell('TailHingePipeX'),
        Cell('=YawPipeRadius - TailHingeJunctionChamfer + TailHingeJunctionInnerWidth + HingeInnerPipeRadius - TrigOffset',
             alias='TailHingePipeX')
    ],
    [
        #
        # |       |
        # |       | Tail Hinge Inner Pipe
        # |       |
        # ----+----
        #
        # + denotes the center of rotation.
        #
        #   /
        #  /      /
        # /_     /  Rotated by VerticalPlaneAngle
        #    - _/
        #
        #    ^
        #    |
        #    |                 |\
        #    |                 | \
        #    |                 |  \
        #    |  TailHingePipeZ |   \ HingeInnerPipeRadius
        #    |                 |    \
        #  z |                 |     \
        #    |                 |_     \
        #    |                 |_|___(_+ VerticalPlaneAngle
        #    |
        #    +---------------------------------------------->
        #                          x
        #
        # sin(VerticalPlaneAngle) = TailHingePipeZ / HingeInnerPipeRadius
        #
        Cell('TailHingePipeZ'),
        Cell('=-HingeInnerPipeRadius * sin(VerticalPlaneAngle)',
             alias='TailHingePipeZ')
    ],
    [
        Cell('OuterPipe', styles=[Style.UNDERLINE])
    ],
    [
        Cell('Radius'),
        Cell('=YawPipeRadius',
             alias='HingeOuterPipeRadius')
    ],
    [
        #
        #     ^
        #     |
        #     |  VerticalPlaneAngle  /|
        #     |                     /◡|
        #     |                    /  |
        #     |                   /   |  TailHingePipeZ
        #   z |              h1  /    |
        #     |                 /     |
        #     |                /     _|
        #     |               /_____|_|
        #     |
        #     +---------------------------------------------->
        #                          x
        #
        # cos(VerticalPlaneAngle) = TailHingePipeZ / h1
        #
        # h stands for hypotenuse
        #
        Cell('h1'), Cell('=-(TailHingePipeZ / cos(VerticalPlaneAngle))',
                         alias='h1')
    ],
    [
        #
        #     ^
        #     |
        #     |  VerticalPlaneAngle  /|
        #     |                     /◡|
        #     |                    /  |
        #     |                   /   |  TailHingeJunctionHeight
        #   z |              h2  /    |
        #     |                 /     |
        #     |                /     _|
        #     |               /_____|_|
        #     |
        #     +---------------------------------------------->
        #                          x
        #
        # cos(VerticalPlaneAngle) = TailHingeJunctionHeight / h2
        #
        # h stands for hypotenuse
        #
        Cell('h2'), Cell('=TailHingeJunctionHeight / cos(VerticalPlaneAngle)',
                         alias='h2')
    ],
    [
        Cell('Length'),
        # 20 for padding
        Cell('=HingeInnerPipeLength - h1 - h2 - 20',
             alias='HingeOuterPipeLength')
    ],
    # Vane Bracket
    # ------------
    #
    #      DistanceBetweenHoles
    #      <---->
    # +-----------------+
    # |   o      o       \ 45° VaneBracketAngle
    # +-------------------+
    #
    # <-->
    # DistanceToFirstHole
    #
    [
        Cell('Vane Bracket', styles=[Style.UNDERLINE, Style.BOLD])
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
    # Outer Tail Hinge X Z
    # --------------------
    # Document: Tail
    # Part: Hinge_Outer
    [
        Cell('Outer Tail Hinge X Z', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # ASCII diagram showing the outer and inner pipes of the tail hinge before rotation.
        #                           ______
        #                        ^ |      | ^
        #                        | |      | |
        #  HingeOuterPipeLength  | |      | |
        #                        | |      | |
        #                        V |______| |
        #                         ^ |    |  |
        #       PipeHeightOffset  | |    |  |  HingeInnerPipeLength
        #                         | |    |  |
        #                         v |____|  V
        #
        Cell('PipeHeightOffset'), Cell('=HingeInnerPipeLength - HingeOuterPipeLength',
                                       alias='PipeHeightOffset')
    ],
    [
        #     ^
        #     |
        #     |           XXX
        #     |        __________
        #     |        |_|      /
        #     |        |       /
        #     |        |      /
        #   z |   ZZZ  |     /   PipeHeightOffset
        #     |        |    /
        #     |        |   /
        #     |        |  /
        #     |        |⌒/
        #     |        |/  VerticalPlaneAngle
        #     |
        #     +---------------------------------------------->
        #                           x
        #
        # sin(VerticalPlaneAngle) = XXX / PipeHeightOffset
        #
        # cos(VerticalPlaneAngle) = ZZZ / PipeHeightOffset
        #
        Cell('XXX'), Cell('=sin(VerticalPlaneAngle) * PipeHeightOffset',
                          alias='XXX')
    ],
    [
        Cell('ZZZ'), Cell('=cos(VerticalPlaneAngle) * PipeHeightOffset',
                          alias='ZZZ')
    ],
    [
        Cell('OuterTailHingeXPosition'), Cell('=XXX + TailHingePipeX',
                                      alias='OuterTailHingeXPosition')
    ],
    [
        Cell('OuterTailHingeZPosition'), Cell('=ZZZ + TailHingePipeZ',
                                      alias='OuterTailHingeZPosition')
    ],
    # Tail Boom Triangular Brace
    # --------------------------
    # Document: Tail_Boom_Support
    # Part: Tail_Boom_Support
    [
        Cell('Tail Boom Triangular Brace',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('BoomPipeTailHingeHypotenuse'), Cell('=BoomPipeDiameter / sin(90 - VerticalPlaneAngle)',
                                                  alias='BoomPipeTailHingeHypotenuse')
    ],
    [
        Cell('DistanceOfBoomFromTopOfOuterTailHinge'), Cell('10',
                                                            alias='DistanceOfBoomFromTopOfOuterTailHinge')
    ],
    [
        # Distance or length of tail boom support along the slant of the tail hinge.
        Cell('TailBoomTriangularBraceWidth'), Cell('=HingeOuterPipeLength - DistanceOfBoomFromTopOfOuterTailHinge - BoomPipeTailHingeHypotenuse',
                                                   alias='TailBoomTriangularBraceWidth')
    ],
    [
        Cell('TailBoomTriangularBraceLength'), Cell('=BoomLength / 3',
                                                    alias='TailBoomTriangularBraceLength')
    ],
    # Tail Angle
    # ----------
    [
        Cell('Tail Angle', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('DefaultTailAngle'), Cell('110',
                                       alias='DefaultTailAngle')
    ],
    # Tail
    # ----
    [
        Cell('Tail', styles=[Style.UNDERLINE, Style.BOLD])
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
        Cell('NonRotatedTailX'), Cell('=TailXInitial + OuterTailHingeXPosition',
                                      alias='NonRotatedTailX')
    ],
    [
        Cell('OuterTailHingeTruncatedHypotenuse'), Cell('=HingeOuterPipeLength - DistanceOfBoomFromTopOfOuterTailHinge',
                                                        alias='OuterTailHingeTruncatedHypotenuse')
    ],
    [
        Cell('OuterTailHingeXPositionOffset'),
        Cell('=cos(90 - VerticalPlaneAngle) * OuterTailHingeTruncatedHypotenuse',
             alias='OuterTailHingeXPositionOffset')
    ],
    [
        Cell('OuterTailHingeNegativeXOffset'), Cell('=BoomPipeDiameter / tan(90 - VerticalPlaneAngle)',
                                                    alias='OuterTailHingeNegativeXOffset')
    ],
    [
        Cell('NonRotatedTailZ'), Cell('=OuterTailHingeZPosition - BoomPipeRadius + TailZOffset',
                                      alias='NonRotatedTailZ')
    ],
    [
        Cell('OuterTailHingeZPositionOffset'), Cell('=sin(90 - VerticalPlaneAngle) * OuterTailHingeTruncatedHypotenuse',
                                            alias='OuterTailHingeZPositionOffset')
    ],
    [
        # Tail Position Before Rotation
        Cell('Point', styles=[Style.UNDERLINE])
    ],
    [
        Cell('x',
             horizontal_alignment=Alignment.RIGHT),
        Cell('y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('z',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Vector')
    ],
    [
        Cell('=NonRotatedTailX + OuterTailHingeXPositionOffset - OuterTailHingeNegativeXOffset',
             alias='PointX'),
        Cell('0',
             alias='PointY'),
        Cell('=NonRotatedTailZ + OuterTailHingeZPositionOffset',
             alias='PointZ'),
        Cell('=vector(PointX; PointY; PointZ)',
             alias='Point')
    ],
    [
        # Center of Rotation
        Cell('Center', styles=[Style.UNDERLINE])
    ],
    [
        Cell('x',
             horizontal_alignment=Alignment.RIGHT),
        Cell('y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('z',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Vector')
    ],
    [
        Cell('=OuterTailHingeXPosition',
             alias='CenterX'),
        Cell('0',
             alias='CenterY'),
        Cell('=OuterTailHingeZPosition',
             alias='CenterZ'),
        Cell('=vector(CenterX; CenterY; CenterZ)',
             alias='Center')
    ],
    [
        # Axis of Rotation
        Cell('TailAxisVector', styles=[Style.UNDERLINE])
    ],
    [
        Cell('x',
             horizontal_alignment=Alignment.RIGHT),
        Cell('y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('z',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Axis')
    ],
    [
        Cell('=sin(VerticalPlaneAngle)',
             alias='TailAxisX'),
        Cell('0',
             alias='TailAxisY'),
        Cell('=cos(VerticalPlaneAngle)',
             alias='TailAxisZ'),
        Cell('=vector(TailAxisX; TailAxisY; TailAxisZ)',
             alias='TailAxisVector')
    ],
    [
        Cell('Angle'),
        Cell('Rotation'),
        Cell('RotatedPoint')
    ],
    [
        Cell('=180 - HorizontalPlaneAngle - DefaultTailAngle',
             alias='TailRotationAngle'),
        Cell('=rotation(TailAxisVector; TailRotationAngle)',
             alias='TailRotationObject'),
        Cell('=Center + TailRotationObject * (Point - Center)', alias='RotatedPoint')
    ],
    [
        Cell('Tail', styles=[Style.UNDERLINE])
    ],
    [
        Cell('x',
             horizontal_alignment=Alignment.RIGHT),
        Cell('y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('z',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('=.RotatedPoint.x', alias='TailXPosition'),
        Cell('=.RotatedPoint.y', alias='TailYPosition'),
        Cell('=.RotatedPoint.z', alias='TailZPosition')
    ],
    [
        Cell('TailBoomTriangularBraceZAxisAngle'), Cell('=asin(TailYPosition / TailBoomTriangularBraceWidth)',
                                                        alias='TailBoomTriangularBraceZAxisAngle')
    ],
    [
        Cell('----------'), Cell('----------'), Cell('----------')
    ],
    # Placement
    # ---------
    [
        Cell('Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    *create_placement_cells(name='TailAssembly',
                            base=(
                                '=TailHingeJunctionChamfer * cos(180 - HorizontalPlaneAngle)',
                                '=TailHingeJunctionChamfer * sin(-(180 - HorizontalPlaneAngle))',
                                '0'),
                            axis=('0', '0', '-1'),
                            angle='=180 - HorizontalPlaneAngle'),
    *create_placement_cells(name='OuterTailHinge',
                            base=(
                                '=OuterTailHingeXPosition',
                                '0',
                                '=OuterTailHingeZPosition'),
                            axis=('0', '1', '0'),
                            angle='=VerticalPlaneAngle'),
    # TailBoomVaneAssemblyLink
    *create_placement_cells(name='Tail',
                            base=(
                                '=TailXPosition',
                                '=TailYPosition',
                                '=TailZPosition'),
                            axis=('0', '0', '1'),
                            angle='=TailRotationAngle'),
    [
        Cell('----------'), Cell('----------'), Cell('----------')
    ],
    # Calculated Placement
    # --------------------
    [
        Cell('Calculated Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('OuterTailHingeParentPlacement')
    ],
    [
        Cell('=TailAssemblyPlacement * OuterTailHingePlacement',
             alias='OuterTailHingeParentPlacement')
    ]
]
