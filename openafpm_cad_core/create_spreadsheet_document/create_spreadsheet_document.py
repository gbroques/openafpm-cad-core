from typing import List

import FreeCAD as App
from FreeCAD import Document

from ..parameter_groups import (FurlingParameters, MagnafpmParameters,
                                UserParameters)
from .alternator_cells import alternator_cells
from .cell import Cell, Style
from .h_shape_cells import h_shape_cells
from .high_end_stop_cells import high_end_stop_cells
from .hub_cells import hub_cells
from .parameters_by_key_to_cells import parameters_by_key_to_cells
from .populate_spreadsheet import populate_spreadsheet
from .tail_cells import tail_cells
from .yaw_bearing_cells import yaw_bearing_cells

__all__ = ['create_spreadsheet_document']


def create_spreadsheet_document(name: str,
                                magnafpm_parameters: MagnafpmParameters,
                                furling_parameters: FurlingParameters,
                                user_parameters: UserParameters) -> Document:
    cells = parameters_by_key_to_cells({
        'MagnAFPM': magnafpm_parameters,
        'OpenFurl': furling_parameters,
        'User': user_parameters,
    })

    static_cells = _get_static_cells()
    cells.extend(static_cells)

    calculated_cells = _get_calculated_cells()
    cells.extend(calculated_cells)

    fastener_cells = _get_fastener_cells()
    cells.extend(fastener_cells)

    document = App.newDocument(name)

    _add_spreadsheet(document, 'Spreadsheet', cells)
    _add_spreadsheet(document, 'Hub', hub_cells)
    _add_spreadsheet(document, 'Alternator', alternator_cells)
    _add_spreadsheet(document, 'YawBearing', yaw_bearing_cells)
    _add_spreadsheet(document, 'Tail', tail_cells)
    _add_spreadsheet(document, 'HighEndStop', high_end_stop_cells)
    document.recompute()
    return document


def _add_spreadsheet(document: Document,
                     name: str,
                     cells: List[List[Cell]]) -> None:
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)
    populate_spreadsheet(sheet, cells)


def _get_static_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Static', styles=[Style.UNDERLINE])
        ],
        [
            Cell('YawBearingTailHingeJunctionChamfer'), Cell('15',
                                                             alias='YawBearingTailHingeJunctionChamfer')
        ],
        [
            Cell('AlternatorTiltAngle'), Cell('=4deg',
                                              alias='AlternatorTiltAngle')
        ],
    ]


def _get_calculated_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Calculated', styles=[Style.UNDERLINE])
        ],
        [
            Cell('YawPipeScaleFactor'), Cell('=RotorDiskRadius < 187.5 ? 0.95 : 0.9',
                                             alias='YawPipeScaleFactor')
        ],
        [
            Cell('YawPipeLength'), Cell('=RotorDiskRadius * YawPipeScaleFactor * 2',
                                        alias='YawPipeLength')
        ],
        [
            Cell('YawBearingTopPlateHoleRadius'), Cell('=RotorDiskRadius < 187.5 ? 10 : 15',
                                                       alias='YawBearingTopPlateHoleRadius')
        ],
        [
            Cell('HingeInnerBodyOuterRadius'), Cell('=RotorDiskRadius < 187.5 ? 24.15 : (RotorDiskRadius < 275 ? 38 : 44.5)',
                                                    alias='HingeInnerBodyOuterRadius')
        ],
        [
            Cell('HingeInnerBodyLength'), Cell('=0.8 * 2 * RotorDiskRadius',
                                               alias='HingeInnerBodyLength')
        ],
        [
            Cell('YawBearingTailHingeJunctionHeight'), Cell('=HingeInnerBodyLength / 3',
                                                            alias='YawBearingTailHingeJunctionHeight')
        ],
        # TODO: Why - 10 - 10?
        [
            Cell('HingeOuterBodyLength'), Cell('=HingeInnerBodyLength - YawBearingTailHingeJunctionHeight - 10 - 10',
                                               alias='HingeOuterBodyLength')
        ],
        [
            Cell('hypotenuse'), Cell('=(YawBearingTailHingeJunctionHeight - FlatMetalThickness) / cos(VerticalPlaneAngle)',
                                     alias='hypotenuse')
        ],
        [
            Cell('YawBearingTailHingeJunctionInnerWidth'), Cell('=sqrt(hypotenuse ^ 2 - (YawBearingTailHingeJunctionHeight - FlatMetalThickness) ^ 2)',
                                                                alias='YawBearingTailHingeJunctionInnerWidth')
        ],
        [
            Cell('YawBearingTailHingeJunctionFullWidth'), Cell('=YawPipeRadius + HingeInnerBodyOuterRadius + YawBearingTailHingeJunctionInnerWidth',
                                                               alias='YawBearingTailHingeJunctionFullWidth')
        ]
    ]


def _get_fastener_cells() -> List[List[Cell]]:
    return [
        [
            Cell('Fastener', styles=[Style.UNDERLINE])
        ],
        [
            Cell('HexNutThickness'), Cell('10',
                                          alias='HexNutThickness')
        ],
        [
            Cell('WasherThickness'), Cell('2.5',
                                          alias='WasherThickness')
        ],
        [
            Cell('DistanceThreadsExtendFromNuts'), Cell('5',
                                                        alias='DistanceThreadsExtendFromNuts')
        ],
        [
            Cell('TailVaneBracketBoltLength'), Cell('=BracketThickness + VaneThickness + FlatMetalThickness + DistanceThreadsExtendFromNuts + WasherThickness',
                                                    alias='TailVaneBracketBoltLength')
        ]
    ]
