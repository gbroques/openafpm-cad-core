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
        Cell('AlternatorTiltAngle'),
        Cell('I')
    ],
    [
        Cell('=Alternator.AlternatorTiltAngle',
             alias='AlternatorTiltAngle'),
        Cell('=Master_of_Puppets#Alternator.I',
             alias='I')
    ],
    [
        Cell('Pipe', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('ScaleFactor'), Cell('=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
                                  alias='YawPipeScaleFactor')
    ],
    [
        # This is the "projected" yaw pipe length.
        # The actual yaw pipe length is calculated later in the HighEndStop spreadsheet
        # after the position of the safety catch is determined.
        Cell('ProjectedLength'), Cell('=RotorDiskRadius * YawPipeScaleFactor * 2',
                                      alias='YawPipeProjectedLength')
    ],
    [
        Cell('Plate', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('CornerChamferLength'),
        Cell('10', alias='YawBearingPlateCornerChamferLength')
    ],
    [
        Cell('TopHoleRadius'), Cell('=RotorDiskRadius < 187.5 ? 10 : 17.5',
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
        Cell('=YawPipeProjectedLength * 0.25',
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
        # Distance Top piece of Yaw Bearing is greater than where it meets the Frame of the Alternator.
        Cell('TopFrameJunctionOverhangDistance'),
        Cell('=Epsilon + Gamma',
             alias='TopFrameJunctionOverhangDistance')
    ],
    [
        Cell('Mhypotenuse'),
        Cell('=MetalLengthL * 2 + TopFrameJunctionOverhangDistance',
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
        Cell('MMhypotenuse')
    ],
    [
        Cell('=hypot(MM; MM)',
             alias='MMhypotenuse')
    ],
    [
        Cell('AlternatorCenterRatio'),
        # See diagram on left-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".
        Cell('L'),
        Cell('LargeYawBearingXOffset')
    ],
    [
        Cell('=(MetalLengthL * 2 - TopFrameJunctionOverhangDistance) / 2 / MMhypotenuse',
             alias='AlternatorCenterRatio'),
        Cell('=YawPipeRadius + (Offset / cos(TopAngle)) + (AlternatorCenterRatio * MM)',
             alias='L'),
        Cell('=TopFrameJunctionOverhangDistance / 2',
             alias='LargeYawBearingXOffset')
    ],
    [
        Cell('Side', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('CanSideExtendToMiddleOfYawBearingPipe')
    ],
    [
        Cell('=(MM - YawPipeDiameter) / 2 > FlatMetalThickness ? True : False',
             alias='CanSideExtendToMiddleOfYawBearingPipe')
    ],
    [
        Cell('HalfWidth'), Cell('=MM / 2',
                                alias='HalfWidth')
    ],
    [
        Cell('DistanceBetweenTopAndPipe'), Cell('=HalfWidth - YawPipeRadius',
                                                alias='DistanceBetweenTopAndPipe')
    ],
    [
        Cell('DistanceBetweenSideAndPipe'), Cell('=CanSideExtendToMiddleOfYawBearingPipe == True ? DistanceBetweenTopAndPipe - FlatMetalThickness : 0',
                                                 alias='DistanceBetweenSideAndPipe')
    ],
    [
        # Protect against negative number for T Shape when Side is not tangent to Yaw Pipe.
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
        Cell('=CanSideExtendToMiddleOfYawBearingPipe == False ? sqrt(YawPipeRadius ^ 2 - VO ^ 2) : 0',
             alias='SideX',
             horizontal_alignment=Alignment.RIGHT),
        Cell('=-SideWidth',
             alias='SideY',
             horizontal_alignment=Alignment.RIGHT),
        Cell('=-HalfWidth + DistanceBetweenSideAndPipe',
             alias='SideZ',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('SideLength', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # Short for (Adj)acent since this is used in a right triangle calculation later.
        Cell('Adj'),
        Cell('=L - MM - YawPipeRadius',
             alias='Adj')
    ],
    # Variables for when side does NOT extend to middle of yaw bearing pipe
    # ---------------------------------------------------------------------
    [
        Cell('DistanceSideExtendsFromFrameAtJunction'),
        Cell('=TopFrameJunctionOverhangDistance - hypot(DistanceBetweenSideAndPipe; DistanceBetweenSideAndPipe)',
             alias='DistanceSideExtendsFromFrameAtJunction')
    ],
    [
        Cell('Eta'),
        Cell('=hypot(DistanceSideExtendsFromFrameAtJunction; DistanceSideExtendsFromFrameAtJunction)',
             alias='Eta')
    ],
    [
        # Distance to extend side from top to frame
        Cell('Theta'),
        Cell('=Eta - FlatMetalThickness',
             alias='Theta')
    ],
    # Variables for when side extends to middle of yaw bearing pipe
    # -------------------------------------------------------------
    [
        # Angle side about Y-axis slightly when MetalLengthL is at its maximum for H & Star Shape.
        # tan(SideYAngle) = opposite / adjacent
        Cell('SideYAngle'),
        Cell('=atan(DistanceBetweenSideAndPipe / Adj)',
             alias='SideYAngle')
    ],
    [
        # Short for (Hyp)otenuse
        Cell('Hyp'),
        Cell('=hypot(DistanceBetweenSideAndPipe; Adj)',
             alias='Hyp')
    ],
    [
        Cell('Iota'),
        Cell('=FlatMetalThickness * tan(TopAngle - SideYAngle)',
             alias='Iota')
    ],
    [
        Cell('Kappa'),
        Cell('=FlatMetalThickness / sin(TopAngle + SideYAngle)',
             alias='Kappa')
    ],
    [
        Cell('Lambda'),
        Cell('=TopFrameJunctionOverhangDistance - Kappa',
             alias='Lambda')
    ],
    [
        Cell('Zeta'),
        Cell('=Lambda / cos(TopAngle + SideYAngle)',
             alias='Zeta')
    ],
    [
        Cell('SideLength'),
        Cell('=CanSideExtendToMiddleOfYawBearingPipe == True ? ' +
             'Hyp + Iota + Zeta : ' +
             'Adj - SideX + DistanceBetweenSideAndPipe + Theta',
             alias='SideLength')
    ],
    [
        Cell('ArcWireSupport', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Thickness'),
        Cell('Width'),
        Cell('Hole_y')
    ],
    [
        Cell('5',
             alias='ArcWireSupportThickness'),
        Cell('=FlatMetalThickness',
             alias='ArcWireSupportWidth'),
        Cell('=YawPipeRadius + I',
             alias='Hole_y')
    ],
    [
        Cell('SmallLength'),
        Cell('LargeLength'),
        Cell('Length')
    ],
    [
        Cell('=Hole_y - YawBearingPlateTopHoleRadius',
             alias='ArcWireSupportSmallLength'),
        # Hypotenuse of isosceles right triangle = a * sqrt(2)
        # https://mathworld.wolfram.com/IsoscelesRightTriangle.html
        Cell('=HalfWidth * sqrt(2) - YawBearingPlateTopHoleRadius - ArcWireSupportWidth / 2',
             alias='ArcWireSupportLargeLength'),
        Cell('=RotorDiskRadius < 187.5 ? ArcWireSupportSmallLength : ArcWireSupportLargeLength',
             alias='ArcWireSupportLength')
    ]
]
