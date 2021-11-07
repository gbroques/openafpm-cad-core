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
        Cell('MetalLengthL'), Cell('=Spreadsheet.MetalLengthL',
                                   alias='MetalLengthL')
    ],
    [
        Cell('FlatMetalThickness'), Cell('=Spreadsheet.FlatMetalThickness',
                                         alias='FlatMetalThickness')
    ],
    [
        Cell('ResineStatorOuterRadius'), Cell('=Alternator.ResineStatorOuterRadius',
                                              alias='ResineStatorOuterRadius')
    ],
    [
        Cell('AlternatorTiltAngle'), Cell('=Spreadsheet.AlternatorTiltAngle',
                                          alias='AlternatorTiltAngle')
    ],
    [
        Cell('Frame', styles=[Style.UNDERLINE])
    ],
    # https://calcresource.com/geom-rectangle.html
    [
        Cell('CentralAngle'), Cell('=360 / 4',
                                   alias='CentralAngle')
    ],
    [
        Cell('Theta'), Cell('=CentralAngle / 2',
                            alias='Theta')
    ],
    [
        Cell('Inradius'), Cell('=cos(Theta) * ResineStatorOuterRadius',
                               alias='Inradius')
    ],
    [
        Cell('IsoscelesRightTriangleHypotenuseRatio'), Cell('=1 / cos(Theta)',
                                                            alias='IsoscelesRightTriangleHypotenuseRatio')
    ],
    [
        Cell('HorizontalDistanceBetweenHoles'), Cell('=ResineStatorOuterRadius * IsoscelesRightTriangleHypotenuseRatio',
                                                     alias='HorizontalDistanceBetweenHoles')
    ],
    # Distance from hole to outside edge of frame.
    [
        Cell('HoleMargin'), Cell('20',
                                 alias='HoleMargin')
    ],
    [
        Cell('G'), Cell('=HorizontalDistanceBetweenHoles + HoleMargin * 2',
                        alias='G')
    ],
    [
        Cell('H'), Cell('=Inradius * 2 - MetalLengthL',
                        alias='H')
    ],  # To make the frame square.
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
