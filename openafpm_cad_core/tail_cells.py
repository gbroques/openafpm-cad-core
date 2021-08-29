from typing import List

from .cell import Cell, Style

__all__ = ['tail_cells']

#: Cells defining the Tail spreadsheet.
tail_cells: List[List[Cell]] = [
    # Inputs
    # ------
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
    # Vane
    # ----
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
    # Tail Hinge Pipe X Z
    # -------------------
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
    # Outer Tail Hinge X Z
    # --------------------
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
    # Tail Boom Triangular Brace
    # --------------------------
    [
        Cell('Tail Boom Triangular Brace', styles=[Style.UNDERLINE])
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
        Cell('TailBoomTriangularBraceWidth'), Cell('=HingeOuterBodyLength - DistanceOfBoomFromTopOfOuterTailHinge - BoomPipeTailHingeHypotenuse',
                                                   alias='TailBoomTriangularBraceWidth')
    ],
    [
        Cell('TailBoomTriangularBraceXOffset'), Cell('=sin(VerticalPlaneAngle) * TailBoomTriangularBraceWidth',
                                                     alias='TailBoomTriangularBraceXOffset')
    ],
    [
        Cell('TailBoomTriangularBraceZOffset'), Cell('=cos(VerticalPlaneAngle) * TailBoomTriangularBraceWidth',
                                                     alias='TailBoomTriangularBraceZOffset')
    ],
    # Outer Tail Hinge Low End Stop
    # -----------------------------
    [
        Cell('Outer Tail Hinge Low End Stop', styles=[Style.UNDERLINE])
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
        Cell('OuterTailHingeLowEndStopLength'), Cell('=sin(VerticalPlaneAngle) * HingeOuterBodyLength + YawPipeRadius * 2',
                                                     alias='OuterTailHingeLowEndStopLength')
    ],
    # Tail Angle
    # ----------
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
    # Tail
    # ----
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
        Cell('NonRotatedTailX'), Cell('=TailXInitial + OuterTailHingeX',
                                      alias='NonRotatedTailX')
    ],
    [
        Cell('OuterTailHingeTruncatedHypotenuse'), Cell('=HingeOuterBodyLength - DistanceOfBoomFromTopOfOuterTailHinge',
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
        Cell('Px', styles=[Style.UNDERLINE]),
        Cell('Py', styles=[Style.UNDERLINE]),
        Cell('Pz', styles=[Style.UNDERLINE])
    ],
    [
        Cell('=NonRotatedTailX + OuterTailHingeXOffset - OuterTailHingeNegativeXOffset',
             alias='Px'),
        Cell('0',
             alias='Py'),
        Cell('=NonRotatedTailZ + OuterTailHingeZOffset',
             alias='Pz')
    ],
    [
        Cell('Cx', styles=[Style.UNDERLINE]),
        Cell('Cy', styles=[Style.UNDERLINE]),
        Cell('Cz', styles=[Style.UNDERLINE])
    ],
    [
        Cell('=OuterTailHingeX',
             alias='Cx'),
        Cell('0',
             alias='Cy'),
        Cell('=OuterTailHingeZ',
             alias='Cz')
    ],
    [
        Cell('Qx', styles=[Style.UNDERLINE]),
        Cell('Qy', styles=[Style.UNDERLINE]),
        Cell('Qz', styles=[Style.UNDERLINE])
    ],
    [
        Cell('=Px - Cx',
             alias='Qx'),
        Cell('=Py - Cy',
             alias='Qy'),
        Cell('=Pz - Cz',
             alias='Qz')
    ],
    [
        Cell('Ax', styles=[Style.UNDERLINE]),
        Cell('Ay', styles=[Style.UNDERLINE]),
        Cell('Az', styles=[Style.UNDERLINE])
    ],
    [
        Cell('=sin(VerticalPlaneAngle)',
             alias='Ax'),
        Cell('0',
             alias='Ay'),
        Cell('=cos(VerticalPlaneAngle)',
             alias='Az')
    ],
    [
        Cell('Rotation Matrix from Axis and Angle',
             styles=[Style.UNDERLINE]),
        Cell('Formula:'),
        Cell('https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle')
    ],
    [
        Cell('r11', styles=[Style.UNDERLINE]),
        Cell('r12', styles=[Style.UNDERLINE]),
        Cell('r13', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=cos(TailAngle) + Ax ^ 2 * (1 - cos(TailAngle))',
             alias='r11'),
        Cell('=Ax * Ay * (1 - cos(TailAngle)) - Az * sin(TailAngle)',
             alias='r12'),
        Cell('=Ax * Az * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
             alias='r13')
    ],
    [
        Cell('r21', styles=[Style.UNDERLINE]),
        Cell('r22', styles=[Style.UNDERLINE]),
        Cell('r23', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=Ay * Ax * (1 - cos(TailAngle)) + Az * sin(TailAngle)',
             alias='r21'),
        Cell('=cos(TailAngle) + Ay ^ 2 * (1 - cos(TailAngle))',
             alias='r22'),
        Cell('=Ay * Az * (1 - cos(TailAngle)) - Ax * sin(TailAngle)',
             alias='r23')
    ],
    [
        Cell('r31', styles=[Style.UNDERLINE]),
        Cell('r32', styles=[Style.UNDERLINE]),
        Cell('r33', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=Az * Ax * (1 - cos(TailAngle)) - Ay * sin(TailAngle)',
             alias='r31'),
        Cell('=Az * Ay * (1 - cos(TailAngle)) + Ax * sin(TailAngle)',
             alias='r32'),
        Cell('=cos(TailAngle) + Az ^ 2 * (1 - cos(TailAngle))',
             alias='r33')
    ],
    [
        Cell('Rotation Matrix * (P - C)',
             styles=[Style.UNDERLINE])
    ],
    [
        Cell('Rx', styles=[Style.UNDERLINE]),
        Cell('Ry', styles=[Style.UNDERLINE]),
        Cell('Rz', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=r11 * Qx + r12 * Qy + r13 * Qz',
             alias='Rx'),
        Cell('=r21 * Qx + r22 * Qy + r23 * Qz',
             alias='Ry'),
        Cell('=r31 * Qx + r32 * Qy + r33 * Qz',
             alias='Rz')
    ],
    [
        Cell('TailX', styles=[Style.UNDERLINE]),
        Cell('TailY', styles=[Style.UNDERLINE]),
        Cell('TailZ', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=Cx + Rx',
             alias='TailX'),
        Cell('=Cy + Ry',
             alias='TailY'),
        Cell('=Cz + Rz',
             alias='TailZ')
    ],
    [
        Cell('TailBoomTriangularBraceZAxisAngle'), Cell('=asin(TailY / TailBoomTriangularBraceWidth)',
                                                        alias='TailBoomTriangularBraceZAxisAngle')
    ]
]
