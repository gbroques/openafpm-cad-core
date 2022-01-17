from typing import List

from .spreadsheet import Alignment, Cell, Color, Style

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
        Cell('YawPipeRadius'),
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle')
    ],
    [
        Cell('=Spreadsheet.YawPipeRadius',
             alias='YawPipeRadius'),
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle')
    ],
    [
        Cell('BoomPipeRadius'),
        Cell('BoomLength')
    ],
    [
        Cell('=Spreadsheet.BoomLength',
             alias='BoomLength'),
        Cell('=Spreadsheet.BoomPipeRadius',
             alias='BoomPipeRadius')
    ],
    # Hinge
    # -----
    [
        # Inner and Outer Pipe dimensions for Hinge are described
        # in a table on page 31 of "A Wind Turbine Recipe Book (2014)".
        Cell('Hinge', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('InnerPipe', styles=[Style.UNDERLINE])
    ],
    [
        # Hinge Inner Pipe Table Header
        # Pipe sizes (outer diameter in mm) 33.4, 42.2, 48.3, 60.3, 73, 88.9, 101.6, 114.3, 127, 141.3
        Cell(background=Color.LIGHT_GRAY.value),
        Cell('Radius', styles=[Style.UNDERLINE]),
        Cell('Length', styles=[Style.UNDERLINE])
    ],
    [
        # TShape row
        Cell('TShape'),
        Cell('24.15', # 48.3 diameter
             alias='TShapeHingeInnerPipeRadius'),
        Cell(background=Color.LIGHT_GRAY.value)
    ],
    [
        # HShape row
        Cell('HShape'),
        Cell('36.5', # 73 diameter
             alias='HShapeHingeInnerPipeRadius'),
        Cell(background=Color.LIGHT_GRAY.value)
    ],
    [
        # StarShape row
        Cell('StarShape'),
        Cell('50.8', # 101.6 diameter
             alias='StarShapeHingeInnerPipeRadius'),
        Cell(background=Color.LIGHT_GRAY.value)
    ],
    [
        Cell('Value'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeHingeInnerPipeRadius : (RotorDiskRadius < 275 ? HShapeHingeInnerPipeRadius : StarShapeHingeInnerPipeRadius)',
             alias='HingeInnerPipeRadius'),
        Cell('=0.8 * 2 * RotorDiskRadius', alias='HingeInnerPipeLength')
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
    [
        Cell('OuterPipe', styles=[Style.UNDERLINE])
    ],
    [
        Cell('Radius'),
        Cell('=YawPipeRadius',
             alias='HingeOuterPipeRadius')
    ],
    [
        Cell('Length'),
        # TODO: Why - 10 - 10?
        Cell('=HingeInnerPipeLength - TailHingeJunctionHeight - 10 - 10',
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
    # Tail Hinge Pipe X Z
    # -------------------
    # Document: Tail_Hinge_Inner
    # Part: Pipe
    [
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
        Cell('OuterTailHingeX'), Cell('=XXX + TailHingePipeX',
                                      alias='OuterTailHingeX')
    ],
    [
        Cell('OuterTailHingeZ'), Cell('=ZZZ + TailHingePipeZ',
                                      alias='OuterTailHingeZ')
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
        Cell('BoomPipeHeight'), Cell('=BoomPipeRadius * 2',
                                     alias='BoomPipeHeight')
    ],
    [
        Cell('BoomPipeTailHingeHypotenuse'), Cell('=BoomPipeHeight / sin(90 - VerticalPlaneAngle)',
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
    # Outer Tail Hinge Low End Stop
    # -----------------------------
    # Document: Tail_Hinge_Outer, Part: Stop_LowEnd
    # Document: Tail_Stop_LowEnd, Part: Tail_Stop_LowEnd
    [
        Cell('Outer Tail Hinge Low End Stop',
             styles=[Style.UNDERLINE, Style.BOLD])
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
        Cell('h2'), Cell('=TailHingeJunctionHeight / cos(VerticalPlaneAngle)',
                         alias='h2')
    ],
    [
        # Along the slant, in the center of the tail hinge pipes.
        # Distance between top of junction and bottom of outer tail hinge pipe.
        Cell('OuterHingeJunctionVerticalGap'), Cell('=HingeInnerPipeLength - HingeOuterPipeLength - h2 - h1',
                                                    alias='OuterHingeJunctionVerticalGap')
    ],
    [
        #    ^
        #    |
        #    |      |\  90 - VerticalPlaneAngle
        #    |      |◡\
        #    |      |  \
        #    |      |   \  YawPipeRadius
        #    |      |    \
        #  z |      |     \
        #    |      |_     \
        #    |      |_|_____\
        #    |
        #    |  HorizontalPipeLength
        #    |
        #    +---------------------------------->
        #                     x
        #
        # sin(90 - VerticalPlaneAngle) = HorizontalPipeLength / YawPipeRadius
        #
        Cell('HorizontalPipeLength'), Cell('=sin(90 - VerticalPlaneAngle) * YawPipeRadius',
                                           alias='HorizontalPipeLength')
    ],
    [
        #
        #     ^
        #     |
        #     |                                    /|
        #     |                                   /◡|
        #     |                                  /  |
        #     | TailBoomTriangularBraceWidth +  /   |
        #   z | OuterHingeJunctionVerticalGap  /    |
        #     |                               /     |
        #     |                              /     _|
        #     |  90 - VerticalPlaneAngle    /_)___|_|
        #     |
        #     |                         HorizontalEstimate
        #     |
        #     +---------------------------------------------->
        #                          x
        #
        # cos(90 - VerticalPlaneAngle) = HorizontalEstimate / (TailBoomTriangularBraceWidth + OuterHingeJunctionVerticalGap)
        #
        Cell('HorizontalEstimate'), Cell('=cos(90 - VerticalPlaneAngle) * (TailBoomTriangularBraceWidth + OuterHingeJunctionVerticalGap)',
                                         alias='HorizontalEstimate')
    ],
    [
        # (TailHingeJunctionFullWidth - HingeInnerPipeRadius) is distance from center of yaw bearing pipe,
        # to the top of the junction where it curves and meets the inner tail hinge pipe.
        Cell('HorizontalDistanceBetweenOuterYawPipes'), Cell('=(TailHingeJunctionFullWidth - HingeInnerPipeRadius) + HorizontalPipeLength + HorizontalEstimate',
                                                             alias='HorizontalDistanceBetweenOuterYawPipes')
    ],
    [
        # Triangle formed with yaw bearing pipe and opposite side of outer tail hinge pipe.
        Cell('OuterTailHingeLowEndStopAngle'), Cell('=-(90deg - atan(YawPipeRadius / HorizontalDistanceBetweenOuterYawPipes))',
                                                    alias='OuterTailHingeLowEndStopAngle')
    ],
    [
        # Relative to Tail_Hinge_Outer
        Cell('OuterTailHingeLowEndStopZ'), Cell('=TailBoomTriangularBraceWidth - FlatMetalThickness',
                                                alias='OuterTailHingeLowEndStopZ')
    ],
    [
        Cell('LowEndStopPlacement'),
        Cell('=create(<<placement>>; create(<<vector>>; 0; 0; OuterTailHingeLowEndStopZ); create(<<rotation>>; create(<<vector>>; 0; 0; 1); OuterTailHingeLowEndStopAngle))',
             alias='LowEndStopPlacement')
    ],
    [
        Cell('LowEndStopLengthToYawPipe'), Cell('=sin(VerticalPlaneAngle) * HingeOuterPipeLength + YawPipeRadius * 2',
                                                alias='LowEndStopLengthToYawPipe')
    ],
    [
        # * 1.2 to make low end stop extend past yaw bearing point of contact by a centimeter or two.
        Cell('OuterTailHingeLowEndStopLength'), Cell('=LowEndStopLengthToYawPipe * 1.2',
                                                     alias='OuterTailHingeLowEndStopLength')
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
        Cell('NonRotatedTailX'), Cell('=TailXInitial + OuterTailHingeX',
                                      alias='NonRotatedTailX')
    ],
    [
        Cell('OuterTailHingeTruncatedHypotenuse'), Cell('=HingeOuterPipeLength - DistanceOfBoomFromTopOfOuterTailHinge',
                                                        alias='OuterTailHingeTruncatedHypotenuse')
    ],
    [
        Cell('OuterTailHingeXOffset'),
        Cell('=cos(90 - VerticalPlaneAngle) * OuterTailHingeTruncatedHypotenuse',
             alias='OuterTailHingeXOffset')
    ],
    [
        Cell('OuterTailHingeNegativeXOffset'), Cell('=BoomPipeHeight / tan(90 - VerticalPlaneAngle)',
                                                    alias='OuterTailHingeNegativeXOffset')
    ],
    [
        Cell('NonRotatedTailZ'), Cell('=OuterTailHingeZ - BoomPipeRadius + TailZOffset',
                                      alias='NonRotatedTailZ')
    ],
    [
        Cell('OuterTailHingeZOffset'), Cell('=sin(90 - VerticalPlaneAngle) * OuterTailHingeTruncatedHypotenuse',
                                            alias='OuterTailHingeZOffset')
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
        Cell('=NonRotatedTailX + OuterTailHingeXOffset - OuterTailHingeNegativeXOffset',
             alias='PointX'),
        Cell('0',
             alias='PointY'),
        Cell('=NonRotatedTailZ + OuterTailHingeZOffset',
             alias='PointZ'),
        Cell('=create(<<vector>>; PointX; PointY; PointZ)',
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
        Cell('=OuterTailHingeX',
             alias='CenterX'),
        Cell('0',
             alias='CenterY'),
        Cell('=OuterTailHingeZ',
             alias='CenterZ'),
        Cell('=create(<<vector>>; CenterX; CenterY; CenterZ)',
             alias='Center')
    ],
    [
        # Axis of Rotation
        Cell('TailAxis', styles=[Style.UNDERLINE])
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
        Cell('=create(<<vector>>; TailAxisX; TailAxisY; TailAxisZ)',
             alias='TailAxis')
    ],
    [
        Cell('Angle'),
        Cell('Rotation'),
        Cell('RotatedPoint')
    ],
    [
        Cell('=180 - HorizontalPlaneAngle - DefaultTailAngle',
             alias='TailAngle'),
        Cell('=create(<<rotation>>; TailAxis; TailAngle)',
             alias='TailRotation'),
        Cell('=Center + TailRotation * (Point - Center)', alias='RotatedPoint')
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
        Cell('=.RotatedPoint.x', alias='TailX'),
        Cell('=.RotatedPoint.y', alias='TailY'),
        Cell('=.RotatedPoint.z', alias='TailZ')
    ],
    [
        Cell('TailBoomTriangularBraceZAxisAngle'), Cell('=asin(TailY / TailBoomTriangularBraceWidth)',
                                                        alias='TailBoomTriangularBraceZAxisAngle')
    ]
]
