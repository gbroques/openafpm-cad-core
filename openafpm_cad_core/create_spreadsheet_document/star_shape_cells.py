from typing import List

from .cell import Cell, Style

__all__ = ['star_shape_cells']

#: Cells defining the Star Shape spreadsheet.
star_shape_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('ResineStatorOuterRadius'), Cell('=Alternator.ResineStatorOuterRadius',
                                              alias='ResineStatorOuterRadius')
    ],
    [
        Cell('Holes'), Cell('=Spreadsheet.Holes',
                            alias='Holes')
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
        Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                      alias='RotorDiskRadius')
    ],
    [
        Cell('CoilLegWidth'), Cell('=Spreadsheet.CoilLegWidth',
                                   alias='CoilLegWidth')
    ],
    [
        Cell('Frame', styles=[Style.UNDERLINE])
    ],
    [
        Cell('StatorHolesCircle'), Cell('=RotorDiskRadius + CoilLegWidth + 0.5 * (ResineStatorOuterRadius - (RotorDiskRadius + CoilLegWidth))',
                                        alias='StatorHolesCircle')
    ],
    [
        Cell('a'), Cell('=2 * sin(30) * StatorHolesCircle + 2 * (25 + Holes)',
                        alias='a')
    ],
    [
        Cell('B'), Cell('=2 * StatorHolesCircle * ((1 - sin(30) * sin(30))^0.5) - MetalLengthL',
                        alias='B')
    ],
    # 25 is the margin from the holes to the edge of the metal.
    [
        Cell('C'), Cell('=StatorHolesCircle - MetalLengthL + Holes + 25',
                        alias='C')
    ]
]
