from typing import List

from .cell import Cell, Style
from .create_rotate_point_cells import create_rotate_point_cells

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
    [
        Cell('BoomLength'), Cell('=Spreadsheet.BoomLength',
                                 alias='BoomLength')
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
        Cell('TailBoomTriangularBraceLength'), Cell('=BoomLength / 3',
                                                    alias='TailBoomTriangularBraceLength')
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
        Cell('LowEndStopLengthToYawPipe'), Cell('=sin(VerticalPlaneAngle) * HingeOuterBodyLength + YawPipeRadius * 2',
                                                alias='LowEndStopLengthToYawPipe')
    ],
    [
        Cell('OuterTailHingeLowEndStopLength'), Cell('=LowEndStopLengthToYawPipe * 1.2',
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
    *create_rotate_point_cells(
        # Namespace
        'Tail',
        (   # Point
            '=NonRotatedTailX + OuterTailHingeXOffset - OuterTailHingeNegativeXOffset',
            '0',
            '=NonRotatedTailZ + OuterTailHingeZOffset'
        ),
        (   # Center
            '=OuterTailHingeX',
            '0',
            '=OuterTailHingeZ'
        ),
        (   # Rotation Axis
            '=sin(VerticalPlaneAngle)',
            '0',
            '=cos(VerticalPlaneAngle)'
        ),
        # Angle
        '=180 - HorizontalPlaneAngle - DefaultTailAngle'
    ),
    [
        Cell('TailBoomTriangularBraceZAxisAngle'), Cell('=asin(TailY / TailBoomTriangularBraceWidth)',
                                                        alias='TailBoomTriangularBraceZAxisAngle')
    ]
]
