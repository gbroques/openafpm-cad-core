from typing import List, Tuple

from .cell import Cell, Style


def create_euler_to_axis_angle_cells(alias_namespace: str,
                                     euler_angles: Tuple[str, str, str]) -> List[List[Cell]]:
    x, y, z = euler_angles
    def alias(a): return alias_namespace + a
    # Euler Angles
    Z = alias('Z')
    Y = alias('Y')
    X = alias('X')
    # Quaternion
    C1 = alias('C1')
    C2 = alias('C2')
    C3 = alias('C3')
    S1 = alias('S1')
    S2 = alias('S2')
    S3 = alias('S3')
    Qx = alias('Qx')
    Qy = alias('Qy')
    Qz = alias('Qz')
    Qw = alias('Qw')
    # Axis-angle
    ScalingFactor = alias('ScalingFactor')
    NormalizationFactor = alias('NormalizationFactor')
    return [
        [
            Cell(alias_namespace, styles=[Style.UNDERLINE, Style.BOLD]),
        ],
        # Euler Angles
        [
            Cell('Euler Angles', styles=[Style.UNDERLINE]),
            Cell('Rotation order is Z, Y, X')
        ],
        [
            Cell('Z'), Cell('Y'), Cell('X')
        ],
        [
            Cell(z, alias=Z),
            Cell(y, alias=Y),
            Cell(x, alias=X)
        ],
        # Quaternion
        [
            Cell('Quaternion', styles=[Style.UNDERLINE])
        ],
        [
            Cell('C1'), Cell('C2'), Cell('C3')
        ],
        [
            Cell(f'=cos({Z} / 2.0)', alias=C1),
            Cell(f'=cos({Y} / 2.0)', alias=C2),
            Cell(f'=cos({X} / 2.0)', alias=C3)
        ],
        [
            Cell('S1'), Cell('S2'), Cell('S3')
        ],
        [
            Cell(f'=sin({Z} / 2.0)', alias=S1),
            Cell(f'=sin({Y} / 2.0)', alias=S2),
            Cell(f'=sin({X} / 2.0)', alias=S3)
        ],
        [
            Cell('Qx'), Cell('Qy'), Cell('Qz')
        ],
        [
            Cell(f'={C1}*{C2}*{S3} - {S1}*{S2}*{C3}', alias=Qx),
            Cell(f'={C1}*{S2}*{C3} + {S1}*{C2}*{S3}', alias=Qy),
            Cell(f'={S1}*{C2}*{C3} - {C1}*{S2}*{S3}', alias=Qz)
        ],
        [
            Cell('Qw')
        ],
        [
            Cell(f'={C1}*{C2}*{C3} + {S1}*{S2}*{S3}', alias=Qw),
        ],
        # Axis-angle
        [
            Cell('Axis-angle', styles=[Style.UNDERLINE])
        ],
        [
            Cell('ScalingFactor'),
            Cell('NormalizationFactor'),
            Cell(alias('Angle'), styles=[Style.BOLD])
        ],
        [
            Cell(f'=sqrt(1 - {Qw} ^ 2)',
                 alias=ScalingFactor),
            Cell(f'={ScalingFactor} < 0.001 ? 1 : {ScalingFactor}',
                 alias=NormalizationFactor),
            Cell(f'=2 * acos({Qw})',
                 alias=alias('Angle'))
        ],
        [
            Cell(alias('AxisX'), styles=[Style.BOLD]),
            Cell(alias('AxisY'), styles=[Style.BOLD]),
            Cell(alias('AxisZ'), styles=[Style.BOLD])
        ],
        [
            Cell(f'={Qx} / {NormalizationFactor}',
                 alias=alias('AxisX')),
            Cell(f'={Qy} / {NormalizationFactor}',
                 alias=alias('AxisY')),
            Cell(f'={Qz} / {NormalizationFactor}',
                 alias=alias('AxisZ'))
        ]
    ]
