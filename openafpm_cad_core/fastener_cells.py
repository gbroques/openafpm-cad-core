from typing import List

from .generate_width_across_corners_cells import \
    generate_width_across_corners_cells
from .spreadsheet import Cell, Style

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
            Cell('Holes'),
            Cell('=Spreadsheet.Holes',
                 alias='Holes')
        ],
        [
            Cell('HubHoles'),
            Cell('=Spreadsheet.HubHoles',
                 alias='HubHoles')
        ],
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        # Hex nut thickness equations are derived from
        # plugging in BS 4190 Metric Hexagon Nut Black Thickness into
        # linear equation function finder.
        # http://www.worldfastener.com/bs-4190-metric-hexagon-nuts/
        # https://www.dcode.fr/function-equation-finder
        [
            Cell('HexNutThickness'),
            Cell('=1.64 * Holes + 0.35',
                 alias='HexNutThickness')
        ],
        [
            Cell('HubHexNutThickness'),
            Cell('=1.64 * HubHoles + 0.35',
                 alias='HubHexNutThickness')
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
        ],
        *generate_width_across_corners_cells(
            'HolesWidthAcrossCorners',
            'HWAC',
            'Holes'
        ),
        *generate_width_across_corners_cells(
            'HubHolesWidthAcrossCorners',
            'HHWAC',
            'HubHoles'
        )
    ]
