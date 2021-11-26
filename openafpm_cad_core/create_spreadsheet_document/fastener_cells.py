from typing import List

from .cell import Cell, Style

__all__ = ['get_fastener_cells']


def get_fastener_cells() -> List[List[Cell]]:
    """Get cells related to fasteners such as nuts and bolts.

    .. freecad-spreadsheet::
    """
    return [
        [
            Cell('Inputs', styles=[Style.UNDERLINE])
        ],
        [
            Cell('BracketThickness'),
            Cell('=Spreadsheet.BracketThickness',
                 alias='BracketThickness')
        ],
        [
            Cell('VaneThickness'),
            Cell('=Spreadsheet.VaneThickness',
                 alias='VaneThickness')

        ],
        [
            Cell('FlatMetalThickness'),
            Cell('=Spreadsheet.FlatMetalThickness',
                 alias='FlatMetalThickness')
        ],
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        [
            Cell('HexNutThickness'),
            Cell('10',
                 alias='HexNutThickness')
        ],
        [
            Cell('WasherThickness'),
            Cell('2.5',
                 alias='WasherThickness')
        ],
        [
            Cell('DistanceThreadsExtendFromNuts'),
            Cell('5',
                 alias='DistanceThreadsExtendFromNuts')
        ],
        [
            Cell('Calculated', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TailVaneBracketBoltLength'),
            Cell('=BracketThickness + VaneThickness + FlatMetalThickness + DistanceThreadsExtendFromNuts + WasherThickness',
                 alias='TailVaneBracketBoltLength')
        ]
    ]
