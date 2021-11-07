from typing import List

from .cell import Cell, Style

__all__ = ['star_shape_cells']

#: Cells defining the Star Shape spreadsheet.
star_shape_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('Holes'), Cell('=Spreadsheet.Holes',
                            alias='Holes')
    ],
    [
        Cell('MetalLengthL'), Cell('=Spreadsheet.MetalLengthL',
                                   alias='MetalLengthL')
    ],
    [
        Cell('StatorHolesCircumradius'), Cell('=Alternator.StatorHolesCircumradius',
                                              alias='StatorHolesCircumradius')
    ],
    [
        Cell('Frame', styles=[Style.UNDERLINE])
    ],
    [
        Cell('a'), Cell('=2 * sin(30) * StatorHolesCircumradius + 2 * (25 + Holes)',
                        alias='a')
    ],
    [
        Cell('B'), Cell('=2 * StatorHolesCircumradius * ((1 - sin(30) * sin(30))^0.5) - MetalLengthL',
                        alias='B')
    ],
    # 25 is the margin from the holes to the edge of the metal.
    [
        Cell('C'), Cell('=StatorHolesCircumradius - MetalLengthL + Holes + 25',
                        alias='C')
    ]
]
