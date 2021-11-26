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

from .cell import Cell, Style

__all__ = ['hub_cells']

light_gray = (0.752941, 0.752941, 0.752941, 1.0)

hub_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('HubHolesPlacement'), Cell('=Spreadsheet.HubHolesPlacement',
                                        alias='HubHolesPlacement')
    ],
    [
        Cell('HubHoles'), Cell('=Spreadsheet.HubHoles',
                               alias='HubHoles')
    ],
    [
        Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                      alias='RotorDiskRadius')
    ],
    [
        Cell('Dimensions', styles=[Style.UNDERLINE])
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
        Cell(background=light_gray),
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
        Cell('85', alias='StarShapeFrameSidePadWidth'),
        Cell('47.5', alias='StarShapeRotorSidePadRadius'),
        Cell('75', alias='StarShapeRotorSidePadWidth'),
        Cell('6', alias='StarShapeNumberOfHoles'),
        Cell('30', alias='StarShapeStubAxleShaftRadius')
    ],
    [
        # Value Row
        Cell('Value'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeMiddlePadRadiusMargin : (RotorDiskRadius < 275 ? HShapeMiddlePadRadiusMargin : StarShapeMiddlePadRadiusMargin)',
             alias='MiddlePadRadiusMargin'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeProtrudingPadThickness : (RotorDiskRadius < 275 ? HShapeProtrudingPadThickness : StarShapeProtrudingPadThickness)',
             alias='ProtrudingPadThickness'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadRadius : (RotorDiskRadius < 275 ? HShapeFrameSidePadRadius : StarShapeFrameSidePadRadius)',
             alias='FrameSidePadRadius'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadWidth : (RotorDiskRadius < 275 ? HShapeFrameSidePadWidth : StarShapeFrameSidePadWidth)',
             alias='FrameSidePadWidth'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadRadius : (RotorDiskRadius < 275 ? HShapeRotorSidePadRadius : StarShapeRotorSidePadRadius)',
             alias='RotorSidePadRadius'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadWidth : (RotorDiskRadius < 275 ? HShapeRotorSidePadWidth : StarShapeRotorSidePadWidth)',
             alias='RotorSidePadWidth'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfHoles : (RotorDiskRadius < 275 ? HShapeNumberOfHoles : StarShapeNumberOfHoles)',
             alias='NumberOfHoles'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeStubAxleShaftRadius : (RotorDiskRadius < 275 ? HShapeStubAxleShaftRadius : StarShapeStubAxleShaftRadius)',
             alias='StubAxleShaftRadius')
    ],
    [
        Cell('Common', styles=[Style.UNDERLINE])
    ],
    [
        Cell('MiddlePadRadius'), Cell('=HubHolesPlacement + HubHoles + MiddlePadRadiusMargin',
                                      alias='MiddlePadRadius')
    ],
    [
        Cell('MiddlePadThickness'), Cell('16',
                                         alias='MiddlePadThickness')
    ],
    [
        Cell('CoverThickness'), Cell('10',
                                     alias='CoverThickness')
    ]
]
