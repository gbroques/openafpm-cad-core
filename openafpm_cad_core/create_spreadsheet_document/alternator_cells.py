from typing import List

from .cell import Alignment, Cell, Style
from .create_euler_to_axis_angle_cells import create_euler_to_axis_angle_cells

__all__ = ['alternator_cells']

#: Cells defining the Alternator spreadsheet.
alternator_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('StatorThickness'),
        Cell('MechanicalClearance')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.StatorThickness',
             alias='StatorThickness'),
        Cell('=Spreadsheet.MechanicalClearance',
             alias='MechanicalClearance')
    ],
    [
        Cell('DiskThickness'),
        Cell('MagnetThickness'),
        Cell('MagnetLength')
    ],
    [
        Cell('=Spreadsheet.DiskThickness',
             alias='DiskThickness'),
        Cell('=Spreadsheet.MagnetThickness',
             alias='MagnetThickness'),
        Cell('=Spreadsheet.MagnetLength',
             alias='MagnetLength')
    ],
    [
        Cell('MetalLengthL'),
        Cell('MetalThicknessL'),
        Cell('CoilLegWidth')
    ],
    [
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL'),
        Cell('=Spreadsheet.MetalThicknessL',
             alias='MetalThicknessL'),
        Cell('=Spreadsheet.CoilLegWidth',
             alias='CoilLegWidth')
    ],
    [
        Cell('HexNutThickness'),
        Cell('DistanceThreadsExtendFromNuts'),
        Cell('WasherThickness')
    ],
    [
        Cell('=Spreadsheet.HexNutThickness',
             alias='HexNutThickness'),
        Cell('=Spreadsheet.DistanceThreadsExtendFromNuts',
             alias='DistanceThreadsExtendFromNuts'),
        Cell('=Spreadsheet.WasherThickness',
             alias='WasherThickness'),
    ],
    [
        Cell('MiddlePadThickness'),
        Cell('FrameSidePadWidth')
    ],
    [
        Cell('=Hub.MiddlePadThickness',
             alias='MiddlePadThickness'),
        Cell('=Hub.FrameSidePadWidth',
             alias='FrameSidePadWidth')
    ],
    [
        Cell('Stator', styles=[Style.UNDERLINE])
    ],
    [
        Cell('ResineStatorOuterRadius')
    ],
    [
        Cell('=RotorDiskRadius < 275 ? (RotorDiskRadius + CoilLegWidth + 20) : (RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
             alias='ResineStatorOuterRadius'),
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskThickness'),
        Cell('LengthOfTwoNuts'),
        Cell('StatorMountingStudsLength')
    ],
    [
        Cell('=MagnetThickness + DiskThickness', alias='RotorDiskThickness'),
        Cell('=HexNutThickness * 2', alias='LengthOfTwoNuts'),
        Cell('=DistanceThreadsExtendFromNuts * 2 + MetalThicknessL + HexNutThickness * 4 + MiddlePadThickness + RotorDiskThickness + MechanicalClearance + StatorThickness + WasherThickness + FrameHubZOffset',
             alias='StatorMountingStudsLength')
    ],
    [
        Cell('HubFrameOverlap'),
        Cell('FrameHubPadding'),
        Cell('FrameHubZOffset')
    ],
    [
        Cell('=FrameSidePadWidth - (MetalLengthL - MetalThicknessL + LengthOfTwoNuts)',
             alias='HubFrameOverlap'),
        Cell('20',
             alias='FrameHubPadding'),
        Cell('=HubFrameOverlap > 0 ? HubFrameOverlap + FrameHubPadding : 0',
             alias='FrameHubZOffset')
    ],
    [
        Cell('DistanceBetweenFrameAndBackRotor')
    ],
    [
        Cell('=MiddlePadThickness + LengthOfTwoNuts + FrameHubZOffset',
             alias='DistanceBetweenFrameAndBackRotor')
    ],
    [
        Cell('Rotor Mounting Studs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('DistanceBetweenRotorDisks'),
        Cell('NumberOfNutsBetweenRotorDisks'),
        Cell('NumberOfWashersBetweenRotorDisks')
    ],
    [
        Cell('=MagnetThickness * 2 + MechanicalClearance * 2 + StatorThickness',
             alias='DistanceBetweenRotorDisks'),
        Cell('=floor(DistanceBetweenRotorDisks / HexNutThickness)',
             alias='NumberOfNutsBetweenRotorDisks'),
        Cell('=floor(DistanceBetweenRotorDisks % HexNutThickness / WasherThickness)',
             alias='NumberOfWashersBetweenRotorDisks')
    ],
    [
        Cell('Frame', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Z',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('0',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameX'),
        Cell('0',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameY'),
        Cell('=StatorThickness / 2 + MechanicalClearance + RotorDiskThickness + MiddlePadThickness + MetalLengthL + LengthOfTwoNuts + FrameHubZOffset',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameZ')
    ],
    *create_euler_to_axis_angle_cells(
        'Alternator',
        (
            '=RotorDiskRadius < 187.5 ? 90 : 0',
            '=RotorDiskRadius < 187.5 ? 0 : 90',
            '=RotorDiskRadius < 187.5 ? -90 : -180'
        )
    )
]
