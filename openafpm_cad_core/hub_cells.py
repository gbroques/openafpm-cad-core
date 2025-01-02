"""The following ASCII diagram is a side view of the Hub with labels used in aliases for spreadsheet cells.

The two vertical lines labeled "Frame" and "Rotor" denote where they are in relation to the Hub.

The terms "Width" and "Radius" are used in the spreadsheet aliases.

Width dimensions are on the horizontal axis, and Radius dimensions are on vertical axis.

Each part of the hub is made from 2-dimensional sketches, and then "padded" to form a 3D solid.

For lack of better names, this is where the names "frame-side pad", "middle pad" and "rotor-side pad" come from.

::

            ^
            |                                          MiddlePad
            |
            |                  +                       +-------+    +
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  |      +----------------+       |    |
            |                  |      |                |       |    |
            |                  |      |                |       +-------+
            |               +---------+                |       |    |  |
    Radius  | StubAxleShaft |  |      |  FrameSidePad  |       |    |  | RotorSidePad
            |               |  |      |                |       |    |  |
            |               +---------+                |       |    |  |
            |                  |      |                |       +-------+
            |                  |      |                |       |    |
            |                  |      +----------------+       |    |
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  |                       |       |    |
            |                  +                       +-------+    +
            |
            |                Frame                                Rotor
            |
            +------------------------------------------------------------------------->
                                               Width

"""

from typing import List

from .spreadsheet import Cell, Color, Style

__all__ = ['hub_cells']

hub_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('HubPitchCircleDiameter'),
        Cell('HubHolesDiameter')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.HubPitchCircleDiameter',
             alias='HubPitchCircleDiameter'),
        Cell('=Spreadsheet.HubHolesDiameter',
             alias='HubHolesDiameter')
    ],
    [
        Cell('MetalLengthL'),
        Cell('RotorDiskCentralHoleDiameter'),
        Cell('RotorTopology')
    ],
    [
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL'),
        Cell('=Spreadsheet.RotorDiskCentralHoleDiameter',
             alias='RotorDiskCentralHoleDiameter'),
        Cell('=Spreadsheet.RotorTopology',
             alias='RotorTopology')
    ],
    [
        Cell('StatorThickness'),
        Cell('MagnetThickness'),
        Cell('MechanicalClearance')
    ],
    [
        Cell('=Spreadsheet.StatorThickness',
             alias='StatorThickness'),
        Cell('=Spreadsheet.MechanicalClearance',
             alias='MechanicalClearance'),
        Cell('=Spreadsheet.MagnetThickness',
             alias='MagnetThickness')
    ],
    [
        Cell('RotorDiskThickness')
    ],
    [
        Cell('=Spreadsheet.RotorDiskThickness',
             alias='RotorDiskThickness')
    ],
    [
        Cell('Fastener', styles=[Style.UNDERLINE])
    ],
    [
        Cell('HubHexNutThickness'),
        Cell('HexNutThickness'),
        Cell('WasherThickness')
    ],
    [
        Cell('=Fastener.HubHexNutThickness',
             alias='HubHexNutThickness'),
        Cell('=Fastener.HexNutThickness',
             alias='HexNutThickness'),
        Cell('=Fastener.WasherThickness',
             alias='WasherThickness')
    ],
    [
        Cell('Common', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('CoverThickness')
    ],
    [
        Cell('10',
             alias='CoverThickness')
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('RotorDiskCentralHoleRadius'),
        Cell('HubHolesRadius'),
        Cell('HubPitchCircleRadius')
    ],
    [
        Cell('=RotorDiskCentralHoleDiameter / 2',
             alias='RotorDiskCentralHoleRadius'),
        Cell('=HubHolesDiameter / 2',
             alias='HubHolesRadius'),
        Cell('=HubPitchCircleDiameter / 2',
             alias='HubPitchCircleRadius')
    ],
    [
        Cell('Dimensions', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # Row to group FrameSidePad and RotorSidePad columns together.
        Cell(),
        Cell(),
        Cell(),
        Cell('FrameSidePad', styles=[Style.BOLD, Style.UNDERLINE]),
        Cell(),
        Cell('RotorSidePad', styles=[Style.BOLD, Style.UNDERLINE])
    ],
    [
        # Dimensions Table Header
        Cell(background=Color.LIGHT_GRAY.value),
        Cell('MiddlePadRadiusMargin', styles=[Style.UNDERLINE]),
        # Both FrameSidePad and RotorSidePad "protrude" from the MiddlePad.
        # ProtrudingPadThickness controls the thickness for Frame and Rotor Side Pads.
        Cell('ProtrudingPadThickness', styles=[Style.UNDERLINE]),
        Cell('Radius', styles=[Style.UNDERLINE]),
        Cell('Width', styles=[Style.UNDERLINE]),
        Cell('Radius', styles=[Style.UNDERLINE]),
        Cell('Width', styles=[Style.UNDERLINE]),
        Cell('NumberOfHoles', styles=[Style.UNDERLINE]),
        Cell('StubAxleShaftRadius', styles=[Style.UNDERLINE])
    ],
    [
        # TShape Row
        Cell('TShape'),
        Cell('15', alias='TShapeMiddlePadRadiusMargin'),
        Cell('5', alias='TShapeProtrudingPadThickness'),
        Cell('32.5', alias='TShapeFrameSidePadRadius'),
        Cell('45', alias='TShapeFrameSidePadWidth'),
        Cell('28', alias='TShapeRotorSidePadRadius'),
        Cell('40', alias='TShapeRotorSidePadWidth'),
        Cell('4', alias='TShapeNumberOfHoles'),
        Cell('18', alias='TShapeStubAxleShaftRadius')
    ],
    [
        # HShape Row
        Cell('HShape'),
        Cell('15', alias='HShapeMiddlePadRadiusMargin'),
        Cell('5', alias='HShapeProtrudingPadThickness'),
        Cell('42.5', alias='HShapeFrameSidePadRadius'),
        Cell('45', alias='HShapeFrameSidePadWidth'),
        Cell('31', alias='HShapeRotorSidePadRadius'),
        Cell('40', alias='HShapeRotorSidePadWidth'),
        Cell('5', alias='HShapeNumberOfHoles'),
        Cell('22.5', alias='HShapeStubAxleShaftRadius')
    ],
    [
        # StarShape Row
        Cell('StarShape'),
        Cell('20', alias='StarShapeMiddlePadRadiusMargin'),
        Cell('10', alias='StarShapeProtrudingPadThickness'),
        Cell('52.5', alias='StarShapeFrameSidePadRadius'),
        Cell('55', alias='StarShapeFrameSidePadWidth'),
        Cell('47.5', alias='StarShapeRotorSidePadRadius'),
        Cell('75', alias='StarShapeRotorSidePadWidth'),
        Cell('6', alias='StarShapeNumberOfHoles'),
        Cell('30', alias='StarShapeStubAxleShaftRadius')
    ],
    [
        # Default Value Row
        Cell('Default Value'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeMiddlePadRadiusMargin : (RotorDiskRadius < 275 ? HShapeMiddlePadRadiusMargin : StarShapeMiddlePadRadiusMargin)',
             alias='MiddlePadRadiusMargin'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeProtrudingPadThickness : (RotorDiskRadius < 275 ? HShapeProtrudingPadThickness : StarShapeProtrudingPadThickness)',
             alias='ProtrudingPadThickness'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadRadius : (RotorDiskRadius < 275 ? HShapeFrameSidePadRadius : StarShapeFrameSidePadRadius)',
             alias='FrameSidePadRadius'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadWidth : (RotorDiskRadius < 275 ? HShapeFrameSidePadWidth : StarShapeFrameSidePadWidth)',
             alias='FrameSidePadWidth'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadRadius : (RotorDiskRadius < 275 ? HShapeRotorSidePadRadius : StarShapeRotorSidePadRadius)',
             alias='DefaultRotorSidePadRadius'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadWidth : (RotorDiskRadius < 275 ? HShapeRotorSidePadWidth : StarShapeRotorSidePadWidth)',
             alias='RotorSidePadWidth'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfHoles : (RotorDiskRadius < 275 ? HShapeNumberOfHoles : StarShapeNumberOfHoles)',
             alias='NumberOfHoles'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeStubAxleShaftRadius : (RotorDiskRadius < 275 ? HShapeStubAxleShaftRadius : StarShapeStubAxleShaftRadius)',
             alias='StubAxleShaftRadius')
    ],
    [
        # Value Row
        Cell('Value'),
        Cell(),
        Cell(),
        Cell(),
        Cell(),
        # Ensure rotor side pad of hub is smaller than central hole of rotor disk.
        # 3 mm is arbitrarily chosen to make it a "few" mm less than central hole of rotor disk.
        Cell('=DefaultRotorSidePadRadius >= RotorDiskCentralHoleRadius ? RotorDiskCentralHoleRadius - 3 : DefaultRotorSidePadRadius',
             alias='RotorSidePadRadius')
    ],
    [
        Cell('MiddlePad', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Radius'),
        Cell('Thickness')
    ],
    [
        Cell('=HubPitchCircleRadius + HubHolesRadius + MiddlePadRadiusMargin',
             alias='MiddlePadRadius'),
        Cell('16',
             alias='MiddlePadThickness')
    ],
    [
        Cell('StubAxleShaft', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('NonSingleRotorDistanceBetweenFrameAndMiddlePad'),
        Cell('DistanceBetweenStatorAndFrame'),
        Cell('RotorThickness')
    ],
    [
        Cell('=HubHexNutThickness * 2',
            alias='NonSingleRotorDistanceBetweenFrameAndMiddlePad'),
        Cell('=RotorTopology == <<Single>> ? HexNutThickness * 2 + WasherThickness + 5 : MiddlePadThickness + NonSingleRotorDistanceBetweenFrameAndMiddlePad + RotorThickness + MechanicalClearance',
            alias='DistanceBetweenStatorAndFrame'),
        Cell('=MagnetThickness + RotorDiskThickness',
             alias='RotorThickness')
    ],
    [
        Cell('DistanceStubAxleShaftExtendsBeyondTheFrame'),
        Cell('DistanceBetweenFrameAndMiddlePad', styles=[Style.BOLD]),
        Cell('Length', styles=[Style.BOLD])
    ],
    [
        Cell('20',
             alias='DistanceStubAxleShaftExtendsBeyondTheFrame'),
        Cell('=RotorTopology == <<Single>> ? DistanceBetweenStatorAndFrame + StatorThickness + MechanicalClearance + RotorThickness : NonSingleRotorDistanceBetweenFrameAndMiddlePad',
             alias='DistanceBetweenFrameAndMiddlePad'),
        Cell('=MiddlePadThickness + DistanceBetweenFrameAndMiddlePad + MetalLengthL + DistanceStubAxleShaftExtendsBeyondTheFrame',
             alias='StubAxleShaftLength')
    ]
]
