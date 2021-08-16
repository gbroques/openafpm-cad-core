from typing import List, Tuple

from .cell import Cell, Style


def create_euler_to_axis_angle_cells(alias_namespace: str,
                                     euler_angles: Tuple[str, str, str]) -> List[List[Cell]]:
    x, y, z = euler_angles
    def alias(a): return alias_namespace + a
    Alpha = alias('Alpha')
    Beta = alias('Beta')
    Gamma = alias('Gamma')
    R11 = alias('R11')
    R12 = alias('R12')
    R13 = alias('R13')
    R21 = alias('R21')
    R22 = alias('R22')
    R23 = alias('R23')
    R31 = alias('R31')
    R32 = alias('R32')
    R33 = alias('R33')
    TraceR = alias('TraceR')
    Angle = alias('Angle')
    U11 = alias('U11')
    U12 = alias('U12')
    U13 = alias('U13')
    NormalizationFactor = alias('NormalizationFactor')
    return [
        # Euler Angles
        [
            Cell('Euler Angles', styles=[Style.UNDERLINE]),
            Cell('Rotation order is Z, Y, X')
        ],
        [
            Cell('Z'), Cell('Y'), Cell('X')
        ],
        [
            Cell(z, alias=Alpha),
            Cell(y, alias=Beta),
            Cell(x, alias=Gamma)
        ],
        # Rotation Matrix
        [
            Cell('Rotation Matrix', styles=[Style.UNDERLINE])
        ],
        [
            Cell('R11'), Cell('R12'), Cell('R13')
        ],
        [
            Cell(f'=cos({Alpha}) * cos({Beta})',
                 alias=R11),
            Cell(f'=cos({Alpha}) * sin({Beta}) * sin({Gamma}) - cos({Gamma}) * sin({Alpha})',
                 alias=R12),
            Cell(f'=sin({Alpha}) * sin({Gamma}) + cos({Alpha}) * cos({Gamma}) * sin({Beta})',
                 alias=R13)
        ],
        [
            Cell('R21'), Cell('R22'), Cell('R23')
        ],
        [
            Cell(f'=cos({Beta}) * sin({Alpha})',
                 alias=R21),
            Cell(f'=cos({Alpha}) * cos({Gamma}) + sin({Alpha}) * sin({Beta}) * sin({Gamma})',
                 alias=R22),
            Cell(f'=cos({Gamma}) * sin({Alpha}) * sin({Beta}) - cos({Alpha}) * sin({Gamma})',
                 alias=R23)
        ],
        [
            Cell('R31'), Cell('R32'), Cell('R33')
        ],
        [
            Cell(f'=-sin({Beta})',
                 alias=R31),
            Cell(f'=cos({Beta}) * sin({Gamma})',
                 alias=R32),
            Cell(f'=cos({Beta}) * cos({Gamma})',
                 alias=R33)
        ],
        # Angle
        [
            Cell('Angle', styles=[Style.UNDERLINE])
        ],
        [
            Cell('TraceR'),
            Cell(f'={R11} + {R22} + {R33}',
                 alias=TraceR)
        ],
        [
            Cell('Angle', styles=[Style.BOLD]),
            Cell(f'=acos({TraceR} - 0.5)',
                 alias=Angle)
        ],
        # Axis
        [
            Cell('Axis', styles=[Style.UNDERLINE])
        ],
        [
            Cell('U11'), Cell('U21'), Cell('U31'),
        ],
        [
            Cell(f'={R32} - {R23}', alias=U11),
            Cell(f'={R13} - {R31}', alias=U12),
            Cell(f'={R21} - {R12}', alias=U13)
        ],
        [
            Cell('NormalizationFactor')
        ],
        [
            Cell(f'=1 / (2 * sin({Angle}))',
                 alias=NormalizationFactor)
        ],
        [
            Cell('AxisX',
                 styles=[Style.BOLD]),
            Cell('AxisY',
                 styles=[Style.BOLD]),
            Cell('AxisZ',
                 styles=[Style.BOLD])
        ],
        [
            Cell(f'={U11} * {NormalizationFactor}',
                 alias=alias('AxisX')),
            Cell(f'={U12} * {NormalizationFactor}',
                 alias=alias('AxisY')),
            Cell(f'={U13} * {NormalizationFactor}',
                 alias=alias('AxisZ'))
        ]
    ]
