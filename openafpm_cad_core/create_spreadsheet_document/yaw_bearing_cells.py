from typing import List

from .cell import Alignment, Cell, Style

__all__ = ['yaw_bearing_cells']

# The following ASCII diagram (not drawn to scale) is a Bottom View depiction of YawBearing_Extended_Assembly.
# 
# It explains below AV, VO, and SideX calcuation.
# A, V, and O are points, denoted by "•".
# AV and VO are line segments from the corresponding points.
#
# Additionally, it includes L and MM dimensions mentioned in below spreadsheet cells.
#
#                                                            SideX
#                                                         <--------->
#                                                                     A
#                      ^  +-------------------------------+---------•-------------+   ^
#                      |  |                               |         |             |   |
#  FlatMetalThickness  |  |           Side                |         | V           |   |
#                      |  |                               |   , + ~ • ~ + ,       |   |
#                      v  +-------------------------------+ '       |       ' ,   |   |
#                                  /                    ,           |           , |   |
#                                 /                    ,            |            ,|   |
#                                /                    ,             | O           ,   |
#                          Top  /                     ,             •             ,   |  MM
#                              /                      ,                           ,   |
#                             /                        ,                         ,|   |
#                            /                          ,                       , |   |
#                           /                   Yaw Pipe  ,                  , '  |   |
#                          /                                ' + , _ _ _ ,  '      |   |
#                         /                                                       |   |
#                        / 45°                                                    |   |
#                       +---------------------------------------------------------+   v
#
#                       <--------------------------------------------------------->
#                                                     L
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The following ASCII diagram (not drawn to scale) is a Bottom View depiction of the Top piece.
# See YawBearing_Extended_Top document.
#
#                             ↗         +-----------------------------------------+   ^
#                            /         /|                                         |   |
#                           /         / |                                         |   |
#                          /         /  |                                         |   |
#                         /         /   |                                         |   |
#                        /         /    |                                         |   |
# HypotenuseTopTriangle /         /     |                                         |   |
#                      /         /      |                                         |   |
#                     /    Top  /       |                                         |   |  MM
#                    /         /        | AdjacentSide                            |   |
#                   /         /         |                                         |   |
#                  /         /          |                                         |   |
#                 /         /           |                                         |   |
#                /         /            |                                         |   |
#               /         /            _|                                         |   |
#              ↙         / 45°        | |                                         |   |
#                       +---------------+-----------------------------------------+   v
#
#                       <--------------------------------------------------------->
#                                                     L
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The following ASCII diagram (not drawn to scale) is a Top View depiction,
# of the Top piece meeting the Channel Sections of Alternator Frame.
#
#                                          +                               ^
#                   Frame Channel Sections |\                              |
#                                          | \                             |
#               ^   +----------------------+  \                            |
#               |   +--------------------+ |   \                           |
#               |                        | |45° \                          |
#               |                        | |     \                         |
#               |                        | |      \                        |
#  MetalLengthL |                        | |       \                       |
#               |                        | |        \                      |
#               |                        | |         \                     |
#               |                        | |          \                    |
#               |                        | |           \                   |
#               |                        | |            \                  |
#  Alternator   V                Center  +-+             \                 |  HypotenuseTopTriangle
#                                        | |              \                |
#                                        | |               \               |
#                                        | |                \              |
#                                        | |                 \             |
#                                        | |                  \            |
#                                        | |                   \           |
#                                        | |                    \          |
#                                        | |                     \         |
#                                        | |                      \        |
#                  +---------------------+ |                       \       |
#                  +-----------------------+                        \      |
#               ^                        \ |          Top            \     |
#               |                         \|\                         \    |
#               V                          + \                         \   V
#  HalfSideChannelSectionOverhangDistance   \ \                         \
#                                            \ \                         \
#                                             \ \                         \
#
#                                             Side
#                                        (underneath Top)
#

#: Cells defining the Yaw Bearing spreadsheet.
yaw_bearing_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('YawPipeRadius'),
        Cell('FlatMetalThickness'),
        Cell('MetalLengthL'),
    ],
    [
        Cell('=Spreadsheet.YawPipeRadius',
             alias='YawPipeRadius'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL')
    ],
    [
        Cell('Offset'),
        Cell('RotorDiskRadius'),
        Cell('AlternatorTiltAngle')
    ],
    [
        Cell('=Spreadsheet.Offset',
             alias='Offset'),
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.AlternatorTiltAngle',
             alias='AlternatorTiltAngle')
    ],
    [
        Cell('Extended Yaw Bearing (H & Star Shape)', styles=[Style.UNDERLINE])
    ],
    [
        # See diagram on left-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".
        # M is a reserved alias in FreeCAD.
        # TODO: Use standard prefix for this. Such as dimM for "dimension M"?
        Cell('MM (M)'),
        Cell('TopAngle')
    ],
    [
        Cell('=RotorDiskRadius < 275 ? 100 : 115',
             alias='MM'),
        Cell('=45deg',
             alias='TopAngle')
    ],
    [
        Cell('LOffset'),
        # See diagram on left-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".
        Cell('L'),
        Cell('LargeYawBearingXOffset'),
    ],
    [
        # Ensure Side piece (undeneath Top flat bar to stiffen it),
        # reaches the Channel Section of the Alternator due to Alternator tilt angle.
        # This shortens L, and we adjust the Yaw Bearing in the X direction to compensate for it.
        Cell('=tan(AlternatorTiltAngle) * MM + cos(TopAngle) * FlatMetalThickness',
             alias='LOffset'),
        Cell('=YawPipeRadius + Offset / cos(TopAngle) + 0.5 * MM - LOffset',
             alias='L'),
        Cell('=LOffset * cos(TopAngle)',
             alias='LargeYawBearingXOffset')
    ],
    [
        Cell('Side', styles=[Style.UNDERLINE])
    ],
    [
        Cell('HalfWidth'), Cell('=MM / 2',
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
        Cell('=-MM',
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
        Cell('AdjacentSide'), Cell('=MM / tan(TopAngle)',
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
