from typing import List

from .cell import Cell, Style

__all__ = ['hub_cells']

#: Cells defining the Hub spreadsheet.
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
        Cell('Middle Pad', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeMiddlePadRadiusMargin'), Cell('15',
                                                  alias='TShapeMiddlePadRadiusMargin')
    ],
    [
        Cell('HShapeMiddlePadRadiusMargin'), Cell('15',
                                                  alias='HShapeMiddlePadRadiusMargin')
    ],
    [
        Cell('StarShapeMiddlePadRadiusMargin'), Cell('20',
                                                     alias='StarShapeMiddlePadRadiusMargin')
    ],
    [
        Cell('MiddlePadRadiusMargin'), Cell('=RotorDiskRadius < 187.5 ? TShapeMiddlePadRadiusMargin : (RotorDiskRadius < 275 ? HShapeMiddlePadRadiusMargin : StarShapeMiddlePadRadiusMargin)',
                                            alias='MiddlePadRadiusMargin')
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
        Cell('Common', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeProtrudingPadThickness'), Cell('5',
                                                   alias='TShapeProtrudingPadThickness')
    ],
    [
        Cell('HShapeProtrudingPadThickness'), Cell('5',
                                                   alias='HShapeProtrudingPadThickness')
    ],
    [
        Cell('StarShapeProtrudingPadThickness'), Cell('10',
                                                      alias='StarShapeProtrudingPadThickness')
    ],
    [
        Cell('ProtrudingPadThickness'), Cell('=RotorDiskRadius < 187.5 ? TShapeProtrudingPadThickness : (RotorDiskRadius < 275 ? HShapeProtrudingPadThickness : StarShapeProtrudingPadThickness)',
                                             alias='ProtrudingPadThickness')
    ],
    [
        Cell('CoverThickness'), Cell('10',
                                     alias='CoverThickness')
    ],
    [
        Cell('Frame Side Pad', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeFrameSidePadRadius'), Cell('32.5',
                                               alias='TShapeFrameSidePadRadius')
    ],
    [
        Cell('HShapeFrameSidePadRadius'), Cell('42.5',
                                               alias='HShapeFrameSidePadRadius')
    ],
    [
        Cell('StarShapeFrameSidePadRadius'), Cell('52.5',
                                                  alias='StarShapeFrameSidePadRadius')
    ],
    [
        Cell('FrameSidePadRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadRadius : (RotorDiskRadius < 275 ? HShapeFrameSidePadRadius : StarShapeFrameSidePadRadius)',
                                         alias='FrameSidePadRadius')
    ],
    [
        Cell('TShapeFrameSidePadWidth'), Cell('45',
                                              alias='TShapeFrameSidePadWidth')
    ],
    [
        Cell('HShapeFrameSidePadWidth'), Cell('45',
                                              alias='HShapeFrameSidePadWidth')
    ],
    [
        Cell('StarShapeFrameSidePadWidth'), Cell('85',
                                                 alias='StarShapeFrameSidePadWidth')
    ],
    [
        Cell('FrameSidePadWidth'), Cell('=RotorDiskRadius < 187.5 ? TShapeFrameSidePadWidth : (RotorDiskRadius < 275 ? HShapeFrameSidePadWidth : StarShapeFrameSidePadWidth)',
                                        alias='FrameSidePadWidth')
    ],
    [
        Cell('Rotor Side Pad', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeRotorSidePadRadius'), Cell('28',
                                               alias='TShapeRotorSidePadRadius')
    ],
    [
        Cell('HShapeRotorSidePadRadius'), Cell('31',
                                               alias='HShapeRotorSidePadRadius')
    ],
    [
        Cell('StarShapeRotorSidePadRadius'), Cell('47.5',
                                                  alias='StarShapeRotorSidePadRadius')
    ],
    [
        Cell('RotorSidePadRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadRadius : (RotorDiskRadius < 275 ? HShapeRotorSidePadRadius : StarShapeRotorSidePadRadius)',
                                         alias='RotorSidePadRadius')
    ],
    [
        Cell('TShapeRotorSidePadWidth'), Cell('40',
                                              alias='TShapeRotorSidePadWidth')
    ],
    [
        Cell('HShapeRotorSidePadWidth'), Cell('40',
                                              alias='HShapeRotorSidePadWidth')
    ],
    [
        Cell('StarShapeRotorSidePadWidth'), Cell('75',
                                                 alias='StarShapeRotorSidePadWidth')
    ],
    [
        Cell('RotorSidePadWidth'), Cell('=RotorDiskRadius < 187.5 ? TShapeRotorSidePadWidth : (RotorDiskRadius < 275 ? HShapeRotorSidePadWidth : StarShapeRotorSidePadWidth)',
                                        alias='RotorSidePadWidth')
    ],
    [
        Cell('Number of Holes', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeNumberOfHoles'), Cell('4',
                                          alias='TShapeNumberOfHoles')
    ],
    [
        Cell('HShapeNumberOfHoles'), Cell('5',
                                          alias='HShapeNumberOfHoles')
    ],
    [
        Cell('StarShapeNumberOfHoles'), Cell('6',
                                             alias='StarShapeNumberOfHoles')
    ],
    [
        Cell('NumberOfHoles'), Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfHoles : (RotorDiskRadius < 275 ? HShapeNumberOfHoles : StarShapeNumberOfHoles)',
                                    alias='NumberOfHoles')
    ],
    [
        Cell('Stub Axle Shaft Radius', styles=[Style.UNDERLINE])
    ],
    [
        Cell('TShapeStubAxleShaftRadius'), Cell('18',
                                                alias='TShapeStubAxleShaftRadius')
    ],
    [
        Cell('HShapeStubAxleShaftRadius'), Cell('22.5',
                                                alias='HShapeStubAxleShaftRadius')
    ],
    [
        Cell('StarShapeStubAxleShaftRadius'), Cell('30',
                                                   alias='StarShapeStubAxleShaftRadius')
    ],
    [
        Cell('StubAxleShaftRadius'), Cell('=RotorDiskRadius < 187.5 ? TShapeStubAxleShaftRadius : (RotorDiskRadius < 275 ? HShapeStubAxleShaftRadius : StarShapeStubAxleShaftRadius)',
                                          alias='StubAxleShaftRadius')
    ]
]
