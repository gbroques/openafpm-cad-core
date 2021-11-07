from typing import List

from .cell import Cell, Style

__all__ = ['h_shape_cells']

#: Cells defining the H Shape spreadsheet.
h_shape_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                      alias='RotorDiskRadius')
    ],
    [
        Cell('Offset'), Cell('=Spreadsheet.Offset',
                             alias='Offset')
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
        Cell('AlternatorTiltAngle'), Cell('=Spreadsheet.AlternatorTiltAngle',
                                          alias='AlternatorTiltAngle')
    ],
    [
        Cell('MM'), Cell('=RotorDiskRadius < 275 ? 100 : 115',
                         alias='MM')
    ],
    [
        Cell('TopAngle'), Cell('=45deg',
                               alias='TopAngle')
    ],
    # Ensure Side piece (undeneath Top flat bar to stiffen it),
    # reaches the Channel Section of the Alternator due to Alternator tilt angle.
    # This shortens L, and we adjust the Yaw Bearing in the X direction to compensate for it.
    [
        Cell('LOffset'), Cell('=tan(AlternatorTiltAngle) * MM + cos(TopAngle) * FlatMetalThickness',
                              alias='LOffset')
    ],
    [
        Cell('L'), Cell('=YawPipeRadius + Offset / cos(TopAngle) + 0.5 * MM - LOffset',
                        alias='L')
    ],
    [
        Cell('LargeYawBearingXOffset'), Cell('=LOffset * cos(TopAngle)',
                                             alias='LargeYawBearingXOffset')
    ],
]
