from typing import List

from .cell import Cell, Style

__all__ = ['tail_cells']

#: Cells defining the Tail spreadsheet.
tail_cells: List[List[Cell]] = [
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
