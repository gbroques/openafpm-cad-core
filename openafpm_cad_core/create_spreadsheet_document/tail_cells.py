from typing import List

from .cell import Alignment, Cell, Color, Style

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
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('TailHingeJunctionChamfer'),
        Cell('15',
             alias='TailHingeJunctionChamfer')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    # TODO: Move to yaw_bearing_cells ===================================================
    [
        Cell('YawPipeScaleFactor'), Cell('=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
                                         alias='YawPipeScaleFactor')
    ],
    [
        Cell('YawPipeLength'), Cell('=RotorDiskRadius * YawPipeScaleFactor * 2',
                                    alias='YawPipeLength')
    ],
    [
        Cell('YawBearingTopPlateHoleRadius'), Cell('=RotorDiskRadius < 187.5 ? 10 : 15',
                                                   alias='YawBearingTopPlateHoleRadius')
    ],
    # ===================================================================================
    [
        Cell('Hinge', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('InnerPipe', styles=[Style.UNDERLINE])
    ],
    [
        # Hinge Inner Pipe Table Header
        Cell(background=Color.LIGHT_GRAY.value),
        Cell('Radius', styles=[Style.UNDERLINE]),
        Cell('Length', styles=[Style.UNDERLINE])
    ],
    [
        # TShape row
        Cell('TShape'),
        Cell('24.15',
             alias='TShapeHingeInnerPipeRadius'),
        Cell(background=Color.LIGHT_GRAY.value)
    ],
    [
        # HShape row
        Cell('HShape'),
        Cell('38',
             alias='HShapeHingeInnerPipeRadius'),
        Cell(background=Color.LIGHT_GRAY.value)
    ],
    [
        # StarShape row
        Cell('StarShape'),
        Cell('44.5',
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
    # Vane
    # ----
    [
        Cell('Vane', styles=[Style.UNDERLINE, Style.BOLD])
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
    # Tail Hinge Pipe X Z (Tail_Hinge_Inner Pipe)
    # -------------------------------------------
    [
        Cell('Tail Hinge Pipe X Z', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('XRotationOffset'), Cell('=HingeInnerPipeRadius - cos(VerticalPlaneAngle) * HingeInnerPipeRadius',
                                      alias='XRotationOffset')
    ],
    [
        Cell('TrigOffset'), Cell('=tan(VerticalPlaneAngle) * (TailHingeJunctionHeight - FlatMetalThickness) + XRotationOffset',
                                 alias='TrigOffset')
    ],
    [
        Cell('TailHingePipeX'), Cell('=HingeInnerPipeRadius + YawPipeRadius - TailHingeJunctionChamfer + TailHingeJunctionInnerWidth - TrigOffset',
                                     alias='TailHingePipeX')
    ],
    [
        Cell('TailHingePipeZ'), Cell('=-HingeInnerPipeRadius * sin(VerticalPlaneAngle)',
                                     alias='TailHingePipeZ')
    ],
    # Outer Tail Hinge X Z
    # --------------------
    [
        Cell('Outer Tail Hinge X Z', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('PipeHeightOffset'), Cell('=HingeInnerPipeLength - HingeOuterPipeLength',
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
        Cell('TailBoomTriangularBraceWidth'), Cell('=HingeOuterPipeLength - DistanceOfBoomFromTopOfOuterTailHinge - BoomPipeTailHingeHypotenuse',
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
        Cell('Outer Tail Hinge Low End Stop',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('h1'), Cell('=-(TailHingePipeZ / cos(VerticalPlaneAngle))',
                         alias='h1')
    ],
    [
        Cell('h2'), Cell('=TailHingeJunctionHeight / cos(VerticalPlaneAngle)',
                         alias='h2')
    ],
    [
        Cell('OuterHingeJunctionVerticalGap'), Cell('=HingeInnerPipeLength - HingeOuterPipeLength - h2 - h1',
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
        Cell('HorizontalDistanceBetweenOuterYawPipes'), Cell('=TailHingeJunctionFullWidth + HorizontalEstimate + HorizontalPipeLength - HingeInnerPipeRadius',
                                                             alias='HorizontalDistanceBetweenOuterYawPipes')
    ],
    [
        Cell('OuterTailHingeLowEndStopAngle'), Cell('=-(90deg - atan(YawPipeRadius / HorizontalDistanceBetweenOuterYawPipes))',
                                                    alias='OuterTailHingeLowEndStopAngle')
    ],
    [
        Cell('LowEndStopLengthToYawPipe'), Cell('=sin(VerticalPlaneAngle) * HingeOuterPipeLength + YawPipeRadius * 2',
                                                alias='LowEndStopLengthToYawPipe')
    ],
    [
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
