from typing import List

from .spreadsheet import Cell

__all__ = ['generate_width_across_corners_cells']


def generate_width_across_corners_cells(
        parameter_name: str,
        prefix: str,
        radius: str,
) -> List[List[Cell]]:
    return [
        [
            Cell(parameter_name),
            Cell(f'Select C (MAX) based on {radius}.'),
            Cell('https://www.atlrod.com/metric-hex-bolt-dimensions/')
        ],
        [
            Cell(f'{prefix}range7'),
            Cell(f'={radius} <= 18 ? 63.51 : 75.05',
                 alias=f'{prefix}range7'),
        ],
        [
            Cell(f'{prefix}range6'),
            Cell(f'={radius} <= 15 ? 53.12 : {prefix}range7',
                 alias=f'{prefix}range6')
        ],
        [
            Cell(f'{prefix}range5'),
            Cell(f'={radius} <= 12 ? 41.57 : {prefix}range6',
                 alias=f'{prefix}range5'),
        ],
        [
            Cell(f'{prefix}range4'),
            Cell(f'={radius} <= 10 ? 34.64 : {prefix}range5',
                 alias=f'{prefix}range4'),
        ],
        [
            Cell(f'{prefix}range3'),
            Cell(f'={radius} <= 8 ? 27.71 : {prefix}range4',
                 alias=f'{prefix}range3'),
        ],
        [
            Cell(f'{prefix}range2'),
            Cell(f'={radius} <= 7 ? 24.25 : {prefix}range3',
                 alias=f'{prefix}range2'),
        ],
        [
            Cell(f'{prefix}range1'),
            Cell(f'={radius} <= 6 ? 20.78 : {prefix}range2',
                 alias=f'{prefix}range1'),
        ],
        [
            Cell(parameter_name),
            Cell(f'={radius} <= 5 ? 18.48 : {prefix}range1',
                 alias=parameter_name),
        ]
    ]
