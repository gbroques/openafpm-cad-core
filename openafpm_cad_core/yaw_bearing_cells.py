from typing import List

from .cell import Alignment, Cell, Style

__all__ = ['yaw_bearing_cells']

#: Cells defining the Yaw Bearing spreadsheet.
yaw_bearing_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('YawPipeRadius'), Cell('=Spreadsheet.YawPipeRadius',
                                    alias='YawPipeRadius')
    ],
    [
        Cell('FlatMetalThickness'), Cell('=Spreadsheet.FlatMetalThickness',
                                         alias='FlatMetalThickness')
    ],
    [
        Cell('MetalLengthL'), Cell('=Spreadsheet.MetalLengthL',
                                   alias='MetalLengthL')
    ],
    [
        Cell('Offset'), Cell('=Spreadsheet.Offset',
                             alias='Offset')
    ],
    [
        Cell('Width'), Cell('=HShape.MM',
                            alias='Width')
    ],
    [
        Cell('L'), Cell('=HShape.L',
                        alias='L')
    ],
    [
        Cell('LOffset'), Cell('=HShape.LOffset',
                              alias='LOffset')
    ],
    [
        Cell('TopAngle'), Cell('=HShape.TopAngle',
                               alias='TopAngle')
    ],
    [
        Cell('Side', styles=[Style.UNDERLINE])
    ],
    [
        Cell('HalfWidth'), Cell('=Width / 2',
                                alias='HalfWidth')
    ],
    [
        Cell('DistanceBetweenTopAndPipe'), Cell('=HalfWidth - YawPipeRadius',
                                                alias='DistanceBetweenTopAndPipe')
    ],
    # Protect against negative number for T Shape when Side is not tangent to Yaw Pipe.
    [
        Cell('AV'), Cell('=FlatMetalThickness - DistanceBetweenTopAndPipe > 0 ? FlatMetalThickness - DistanceBetweenTopAndPipe : FlatMetalThickness',
                         alias='AV')
    ],
    [
        Cell('VO'), Cell('=YawPipeRadius - AV',
                         alias='VO')
    ],
    [
        Cell('X',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Z',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('=sqrt(YawPipeRadius ^ 2 - VO ^ 2)',
             alias='SideX',
             horizontal_alignment=Alignment.RIGHT),
        Cell('=-Width',
             alias='SideY',
             horizontal_alignment=Alignment.RIGHT),
        Cell('=-HalfWidth',
             alias='SideZ',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('SideLength', styles=[Style.UNDERLINE])
    ],
    [
        Cell('AdjacentSide'), Cell('=Width / tan(TopAngle)',
                                   alias='AdjacentSide')
    ],
    [
        Cell('HypotenuseTopTriangle'), Cell('=AdjacentSide / sin(TopAngle)',
                                            alias='HypotenuseTopTriangle')
    ],
    [
        Cell('SideChannelSectionOverhangDistance'), Cell('=HypotenuseTopTriangle - MetalLengthL * 2',
                                                         alias='SideChannelSectionOverhangDistance')
    ],
    [
        Cell('HalfSideChannelSectionOverhangDistance'), Cell('=SideChannelSectionOverhangDistance / 2',
                                                             alias='HalfSideChannelSectionOverhangDistance')
    ],
    [
        Cell('SideDistanceToReachAlternatorChannel'), Cell('=HalfSideChannelSectionOverhangDistance / sin(TopAngle)',
                                                           alias='SideDistanceToReachAlternatorChannel')
    ],
    [
        Cell('SideLength'), Cell('=L - AdjacentSide - YawPipeRadius - SideX + SideDistanceToReachAlternatorChannel - FlatMetalThickness + LOffset',
                                 alias='SideLength')
    ]
]
