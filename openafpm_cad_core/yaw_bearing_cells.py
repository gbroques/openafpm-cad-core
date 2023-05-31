"""The following ASCII diagram (not drawn to scale) is a Bottom View depiction of ``YawBearing_Extended_Assembly``.

It explains below ``AV``, ``VO``, and ``SideX`` calcuations.

``A``, ``V``, and ``O`` are points, denoted by "•".

``AV`` and ``VO`` are line segments from the corresponding points.

Additionally, it includes ``L`` and ``MM`` dimensions mentioned in below spreadsheet cells.

::

                                                              SideX
                                                           <--------->
                                                                       A
                        ^  +-------------------------------+---------•-------------+   ^
                        |  |                               |         |             |   |
    FlatMetalThickness  |  |           Side                |         | V           |   |
                        |  |                               |   , + ~ • ~ + ,       |   |
                        v  +-------------------------------+ '       |       ' ,   |   |
                                    /                    ,           |           , |   |
                                   /                    ,            |            ,|   |
                                  /                    ,             | O           ,   |
                            Top  /                     ,             •             ,   |  MM
                                /                      ,                           ,   |
                               /                        ,                         ,|   |
                              /                          ,                       , |   |
                             /                   Yaw Pipe  ,                  , '  |   |
                            /                                ' + , _ _ _ ,  '      |   |
                           /                                                       |   |
                          / 45°                                                    |   |
                         +---------------------------------------------------------+   v
                         <--------------------------------------------------------->
                                                       L

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following ASCII diagram (not drawn to scale) is a Bottom View depiction of the Top piece.

See ``YawBearing_Extended_Top`` document.

::

                                ↗         +-----------------------------------------+   ^
                               /         /|                                         |   |
                              /         / |                                         |   |
                             /         /  |                                         |   |
                            /         /   |                                         |   |
                           /         /    |                                         |   |
    HypotenuseTopTriangle /         /     |                                         |   |
                         /         /      |                                         |   |
                        /    Top  /       |                                         |   |  MM
                       /         /        | AdjacentSide                            |   |
                      /         /         |                                         |   |
                     /         /          |                                         |   |
                    /         /           |                                         |   |
                   /         /            |                                         |   |
                  /         /            _|                                         |   |
                 ↙         / 45°        | |                                         |   |
                          +---------------+-----------------------------------------+   v
                          <--------------------------------------------------------->
                                                        L

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following ASCII diagram (not drawn to scale) is a Top View depiction,
of the Top piece meeting the Channel Sections of Alternator Frame.

::

                                            +                                ^
                     Frame Channel Sections |\\                              |
                                            | \\                             |
                 ^   +----------------------+  \\                            |
                 |   +--------------------+ |   \\                           |
                 |                        | |45° \\                          |
                 |                        | |     \\                         |
                 |                        | |      \\                        |
    MetalLengthL |                        | |       \\                       |
                 |                        | |        \\                      |
                 |                        | |         \\                     |
                 |                        | |          \\                    |
                 |                        | |           \\                   |
                 |                        | |            \\                  |
    Alternator   V                Center  +-+             \\                 |  HypotenuseTopTriangle
                                          | |              \\                |
                                          | |               \\               |
                                          | |                \\              |
                                          | |                 \\             |
                                          | |                  \\            |
                                          | |                   \\           |
                                          | |                    \\          |
                                          | |                     \\         |
                                          | |                      \\        |
                    +---------------------+ |                       \\       |
                    +-----------------------+                        \\      |
                 ^                        \ |          Top            \\     |
                 |                         \|\                         \\    |
                 V                          + \                         \\   V
    HalfSideChannelSectionOverhangDistance   \ \                         \\
                                              \ \                         \\
                                               \ \                         \\
                                               Side
                                          (underneath Top)
"""
from typing import List

from .spreadsheet import Alignment, Cell, Style

__all__ = ['yaw_bearing_cells']

yaw_bearing_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('YawPipeDiameter'),
        Cell('FlatMetalThickness'),
        Cell('MetalLengthL'),
    ],
    [
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL')
    ],
    [
        Cell('Offset'),
        Cell('RotorDiskRadius')
    ],
    [
        Cell('=Spreadsheet.Offset',
             alias='Offset'),
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius')
    ],
    [
        Cell('Alternator', styles=[Style.UNDERLINE])
        # ------------------------------------------
    ],
    [
        Cell('AlternatorTiltAngle')
    ],
    [
        Cell('=Alternator.AlternatorTiltAngle',
             alias='AlternatorTiltAngle')
    ],
    [
        Cell('Pipe', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('ScaleFactor'), Cell('=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
                                  alias='YawPipeScaleFactor')
    ],
    [
        Cell('Length'), Cell('=RotorDiskRadius * YawPipeScaleFactor * 2',
                             alias='YawPipeLength')
    ],
    [
        Cell('Plate', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('CornerChamferLength'),
        Cell('10', alias='YawBearingPlateCornerChamferLength')
    ],
    [
        Cell('TopHoleRadius'), Cell('=RotorDiskRadius < 187.5 ? 10 : 15',
                                    alias='YawBearingPlateTopHoleRadius')
    ],
    [
        # Ensure Side piece (undeneath Top flat bar to stiffen it),
        # reaches the Channel Section of the Alternator due to Alternator tilt angle.
        Cell('Extended Yaw Bearing (H & Star Shape)',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('SideWidth'),
        Cell('=YawPipeLength * 0.25',
             alias='SideWidth')
    ],
    [
        Cell('TopAngle'),
        Cell('=45deg',
             alias='TopAngle')
    ],
    [
        # Distance of triangle formed from Side piece and channel section of Frame
        # due to tilt of Alternator.
        Cell('Gamma'),
        Cell('=tan(AlternatorTiltAngle) * SideWidth',
             alias='Gamma')
    ],
    [
        Cell('Delta'),
        Cell('=cos(TopAngle) * FlatMetalThickness',
             alias='Delta')
    ],
    [
        Cell('Epsilon'),
        Cell('=Delta * 2',
             alias='Epsilon')
    ],
    [
        Cell('Zeta'),
        Cell('=Epsilon + Gamma',
             alias='Zeta')
    ],
    [
        Cell('Mhypotenuse'),
        Cell('=MetalLengthL * 2 + Zeta',
             alias='Mhypotenuse')
    ],
    [
        Cell('YawPipeRadius'),
        Cell('Madjacent'),
        # See diagram on left-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".
        # M is a reserved alias in FreeCAD.
        # TODO: Use standard prefix for this. Such as dimM for "dimension M"?
        Cell('MM (M)')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
        Cell('=cos(TopAngle) * Mhypotenuse',
             alias='Madjacent'),
        # If M is less than the diameter of the Yaw Pipe, then set it to the diameter of the Yap Pipe.
        Cell('=Madjacent < YawPipeDiameter ? YawPipeDiameter : Madjacent',
             alias='MM')
    ],
    [
        Cell('MMhypotenuse'),
        # Distance Top piece of Yaw Bearing is greater than where it meets the Frame of the Alternator.
        Cell('TopFrameJunctionOverhangeDistance')
    ],
    [
        Cell('=hypot(MM; MM)',
             alias='MMhypotenuse'),
        Cell('=MMhypotenuse - MetalLengthL * 2',
             alias='TopFrameJunctionOverhangeDistance')

    ],
    [
        Cell('AlternatorCenterRatio'),
        # See diagram on left-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".
        Cell('L'),
        Cell('LargeYawBearingXOffset')
    ],
    [
        Cell('=(MetalLengthL * 2 - TopFrameJunctionOverhangeDistance) / 2 / MMhypotenuse',
             alias='AlternatorCenterRatio'),
        Cell('=YawPipeRadius + (Offset / cos(TopAngle)) + (AlternatorCenterRatio * MM)',
             alias='L'),
        Cell('=TopFrameJunctionOverhangeDistance / 2',
             alias='LargeYawBearingXOffset')
    ],
    [
        Cell('Side', styles=[Style.UNDERLINE, Style.BOLD])
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
        Cell('=-SideWidth',
             alias='SideY',
             horizontal_alignment=Alignment.RIGHT),
        Cell('=-HalfWidth',
             alias='SideZ',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('SideLength', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Eta'),
        Cell('=hypot(TopFrameJunctionOverhangeDistance; TopFrameJunctionOverhangeDistance)',
             alias='Eta')
    ],
    [
        Cell('Theta'),
        Cell('=Eta - FlatMetalThickness',
             alias='Theta')
    ],
    [
        Cell('SideLength'),
        Cell('=L - MM - YawPipeRadius - SideX + Theta',
             alias='SideLength')
    ]
]
