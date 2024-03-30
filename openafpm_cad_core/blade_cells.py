from typing import List

from .plywood_thickness import PlywoodThickness
from .spreadsheet import Cell, Style

__all__ = ['blade_cells']


blade_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('RotorDiameter'),
    ],
    [
        Cell('=Spreadsheet.RotorDiameter',
             alias='RotorDiameter'),
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('BladeAssemblyBackDiskDiameter'),
        Cell('BladeAssemblyFrontTriangleSideLength')
    ],
    [
        Cell('=0.106 * RotorDiameter - 3.121',
             alias='BladeAssemblyBackDiskDiameter'),
        Cell('=0.147 * RotorDiameter + 6.213',
             alias='BladeAssemblyFrontTriangleSideLength')
    ],
    [
        Cell('BladeTemplateDim_V'),
        Cell('BladeTemplateDim_W')
    ],
    [
        Cell('=0.086 * RotorDiameter - 10.669',
             alias='BladeTemplateDim_V'),
        Cell('=0.018 * RotorDiameter + 12.986',
             alias='BladeTemplateDim_W')
    ],
    [
        Cell('UnroundedBladeAssemblyPlateThickness'),
    ],
    [
        Cell('=0.004 * RotorDiameter + 2.426',
             alias='UnroundedBladeAssemblyPlateThickness'),
    ],
    [
        Cell('BladeAssemblyPlateThickness', styles=[Style.UNDERLINE]),
        Cell('Round to nearest plywood thickness')
    ],
    [
        Cell('Range13'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 37.5 ? {PlywoodThickness.MM_35.value} : {PlywoodThickness.MM_40.value}',
             alias='Range13')
    ],
    [
        Cell('Range12'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 32.5 ? {PlywoodThickness.MM_30.value} : Range13',
             alias='Range12')
    ],
    [
        Cell('Range11'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 28.5 ? {PlywoodThickness.MM_27.value} : Range12',
             alias='Range11')
    ],
    [
        Cell('Range10'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 26 ? {PlywoodThickness.MM_24.value} : Range11',
             alias='Range10')
    ],
    [
        Cell('Range9'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 22.5 ? {PlywoodThickness.MM_21.value} : Range10',
             alias='Range9')
    ],
    [
        Cell('Range8'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 20.5 ? {PlywoodThickness.MM_20.value} : Range9',
             alias='Range8')
    ],
    [
        Cell('Range7'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 19 ? {PlywoodThickness.MM_18.value} : Range8',
             alias='Range7')
    ],
    [
        Cell('Range6'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 16.5 ? {PlywoodThickness.MM_15.value} : Range7',
             alias='Range6')
    ],
    [
        Cell('Range5'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 13.5 ? {PlywoodThickness.MM_12.value} : Range6',
             alias='Range5')
    ],
    [
        Cell('Range4'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 11 ? {PlywoodThickness.MM_10.value} : Range5',
             alias='Range4')
    ],
    [
        Cell('Range3'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 9.5 ? {PlywoodThickness.MM_9.value} : Range4',
             alias='Range3')
    ],
    [
        Cell('Range2'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 8.5 ? {PlywoodThickness.MM_8.value} : Range3',
             alias='Range2')
    ],
    [
        Cell('Range1'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 7 ? {PlywoodThickness.MM_6.value} : Range2',
             alias='Range1')
    ],
    [
        Cell('BladeAssemblyPlateThickness'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 5 ? {PlywoodThickness.MM_4.value} : Range1',
             alias='BladeAssemblyPlateThickness')
    ],
    [
        Cell('UnroundedNumberOfScrews'),
        Cell('NumberOfScrews')
    ],
    [
        Cell('=0.013 * RotorDiameter + 16.929',
             alias='UnroundedNumberOfScrews'),
        # Round down to nearest multiple of 3.
        Cell('=UnroundedNumberOfScrews - mod(UnroundedNumberOfScrews; 3)',
             alias='NumberOfScrews')
    ],
    [
        Cell('NumberOfScrewsPerBlade'),
        Cell('NumberOfInnerScrews'),
        Cell('NumberOfOuterScrews')
    ],
    [
        Cell('=NumberOfScrews / 3',
             alias='NumberOfScrewsPerBlade'),
        Cell('=round(NumberOfScrewsPerBlade * 0.43)',
             alias='NumberOfInnerScrews'),
        Cell('=NumberOfScrewsPerBlade - NumberOfInnerScrews',
             alias='NumberOfOuterScrews')
    ],
    [
        Cell('LessThan3000'),
        Cell('GreaterThanOrEqualTo3000'),
        Cell('BladeThickness')
    ],
    [
        Cell('=RotorDiameter * 0.0083333333333 + 20 ',
             alias='LessThan3000'),
        Cell('=RotorDiameter * 0.025 - 30',
             alias='GreaterThanOrEqualTo3000'),
        Cell('=RotorDiameter < 3000 ? LessThan3000 : GreaterThanOrEqualTo3000',
             alias='BladeThickness')
    ]
]
