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
        Cell('MetalThicknessL'),
        Cell('MagnetThickness')
    ],
    [
        Cell('=Spreadsheet.DiskThickness',
             alias='DiskThickness'),
        Cell('=Spreadsheet.MetalThicknessL',
             alias='MetalThicknessL'),
        Cell('=Spreadsheet.MagnetThickness',
             alias='MagnetThickness')
    ],
    [
        Cell('MiddlePadThickness'), Cell('FrameSidePadWidth')
    ],
    [
        Cell('=Hub.MiddlePadThickness',
             alias='MiddlePadThickness'),
        Cell('=Hub.FrameSidePadWidth',
             alias='FrameSidePadWidth')
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskThickness')
    ],
    [
        Cell('=MagnetThickness + DiskThickness', alias='RotorDiskThickness')
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
        Cell('=StatorThickness / 2 + MechanicalClearance + RotorDiskThickness + MiddlePadThickness + FrameSidePadWidth + MetalThicknessL',
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
