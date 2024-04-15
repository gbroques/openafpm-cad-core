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
            Cell('HolesDiameter'),
            Cell('=Spreadsheet.HolesDiameter',
                 alias='HolesDiameter')
        ],
        [
            Cell('HubHolesDiameter'),
            Cell('=Spreadsheet.HubHolesDiameter',
                 alias='HubHolesDiameter')
        ],
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        [
            Cell('HolesRadius'),
            Cell('=HolesDiameter / 2',
                 alias='HolesRadius')
        ],
        [
            Cell('HubHolesRadius'),
            Cell('=HubHolesDiameter / 2',
                 alias='HubHolesRadius')
        ],
        # Hex nut thickness equations are derived from
        # plugging in BS 4190 Metric Hexagon Nut Black Thickness into
        # linear equation function finder.
        # http://www.worldfastener.com/bs-4190-metric-hexagon-nuts/
        # https://www.dcode.fr/function-equation-finder
        [
            Cell('HexNutThickness'),
            Cell('=1.64 * HolesRadius + 0.35',
                 alias='HexNutThickness')
        ],
        [
            Cell('HubHexNutThickness'),
            Cell('=1.64 * HubHolesRadius + 0.35',
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
            Cell('HubHolesBoltLength'),
            Cell('50',
                 alias='HubHolesBoltLength')
        ],
        [
            Cell('WoodScrewDiameter'),
            Cell('5',
                 alias='WoodScrewDiameter')
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
            'HolesRadius'
        ),
        *generate_width_across_corners_cells(
            'HubHolesWidthAcrossCorners',
            'HHWAC',
            'HubHolesRadius'
        )
    ]
