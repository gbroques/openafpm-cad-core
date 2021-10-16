from typing import List, Tuple

from .cell import Cell, Style

__all__ = [
    'create_rotate_point_around_cells',
    'create_rotate_vector_cells'
]


def create_rotate_point_around_cells(alias_namespace: str,
                                     point: Tuple[str, str, str],
                                     center: Tuple[str, str, str],
                                     rotation_axis: Tuple[str, str, str],
                                     rotation_angle: str) -> List[List[Cell]]:
    """
    Rotates a point around a center offset from the origin.

    Equivalent FreeCAD Python code:

    ::

        rotated_point = C + rotation.multVec(P - C)

    Where C is the center of rotation, and P is some point.

    See:
        https://forum.freecadweb.org/viewtopic.php?p=503328#p503328

    """
    def alias(a): return alias_namespace + a
    pX, pY, pZ = point
    cX, cY, cZ = center

    # Point and Center
    Px, Py, Pz = alias('Px'), alias('Py'), alias('Pz')
    Cx, Cy, Cz = alias('Cx'), alias('Cy'), alias('Cz')

    # The rotated P - C vector is called "Prime", for lack of a better name.
    prime_alias_prefix = alias_namespace + 'Prime'
    Rx = prime_alias_prefix + 'X'
    Ry = prime_alias_prefix + 'Y'
    Rz = prime_alias_prefix + 'Z'

    # Rotated Point
    RotatedX, RotatedY, RotatedZ = alias('X'), alias('Y'), alias('Z')

    return [
        [
            Cell(alias_namespace, styles=[Style.UNDERLINE, Style.BOLD]),
        ],
        [
            Cell('Px', styles=[Style.UNDERLINE]),
            Cell('Py', styles=[Style.UNDERLINE]),
            Cell('Pz', styles=[Style.UNDERLINE])
        ],
        [
            Cell(pX, alias=Px),
            Cell(pY, alias=Py),
            Cell(pZ, alias=Pz)
        ],
        [
            Cell('Cx', styles=[Style.UNDERLINE]),
            Cell('Cy', styles=[Style.UNDERLINE]),
            Cell('Cz', styles=[Style.UNDERLINE])
        ],
        [
            Cell(cX, alias=Cx),
            Cell(cY, alias=Cy),
            Cell(cZ, alias=Cz)
        ],
        *create_rotate_vector_cells(
            prime_alias_prefix,
            (
                f'={Px} - {Cx}',
                f'={Py} - {Cy}',
                f'={Pz} - {Cz}'
            ),
            rotation_axis,
            rotation_angle
        ),
        [
            Cell(RotatedX, styles=[Style.UNDERLINE]),
            Cell(RotatedY, styles=[Style.UNDERLINE]),
            Cell(RotatedZ, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'={Cx} + {Rx}',
                 alias=RotatedX),
            Cell(f'={Cy} + {Ry}',
                 alias=RotatedY),
            Cell(f'={Cz} + {Rz}',
                 alias=RotatedZ)
        ]
    ]


def create_rotate_vector_cells(alias_namespace: str,
                               vector: Tuple[str, str, str],
                               rotation_axis: Tuple[str, str, str],
                               rotation_angle: str) -> List[List[Cell]]:
    """
    Rotates a vector.

    Equivalent FreeCAD Python code:

    ::

        rotated_point = rotation.multVec(V)

    Where V is some vector.
    """
    def alias(a): return alias_namespace + a
    vX, vY, vZ = vector
    aX, aY, aZ = rotation_axis

    # Vector
    Vx, Vy, Vz = alias('Vx'), alias('Vy'), alias('Vz')

    # Rotation Axis
    Ax, Ay, Az = alias('Ax'), alias('Ay'), alias('Az')

    # Rotation Angle
    Angle = alias('Angle')

    # Rotation Matrix
    R11, R12, R13 = alias('R11'), alias('R12'), alias('R13')
    R21, R22, R23 = alias('R21'), alias('R22'), alias('R23')
    R31, R32, R33 = alias('R31'), alias('R32'), alias('R33')

    # Rotation Matrix * V
    RotatedX, RotatedY, RotatedZ = alias('X'), alias('Y'), alias('Z')
    return [
        [
            Cell('Vx', styles=[Style.UNDERLINE]),
            Cell('Vy', styles=[Style.UNDERLINE]),
            Cell('Vz', styles=[Style.UNDERLINE])
        ],
        [
            Cell(vX, alias=Vx),
            Cell(vY, alias=Vy),
            Cell(vZ, alias=Vz)
        ],
        [
            Cell('Ax', styles=[Style.UNDERLINE]),
            Cell('Ay', styles=[Style.UNDERLINE]),
            Cell('Az', styles=[Style.UNDERLINE])
        ],
        [
            Cell(aX, alias=Ax),
            Cell(aY, alias=Ay),
            Cell(aZ, alias=Az)
        ],
        [
            Cell('Angle', styles=[Style.UNDERLINE])
        ],
        [
            Cell(rotation_angle, alias=Angle)
        ],
        [
            Cell('Rotation Matrix from Axis and Angle',
                 styles=[Style.UNDERLINE]),
            Cell('Formula:'),
            Cell(
                'https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle')
        ],
        [
            Cell('R11', styles=[Style.UNDERLINE]),
            Cell('R12', styles=[Style.UNDERLINE]),
            Cell('R13', styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'=cos({Angle}) + {Ax} ^ 2 * (1 - cos({Angle}))',
                 alias=R11),
            Cell(f'={Ax} * {Ay} * (1 - cos({Angle})) - {Az} * sin({Angle})',
                 alias=R12),
            Cell(f'={Ax} * {Az} * (1 - cos({Angle})) - {Ay} * sin({Angle})',
                 alias=R13)
        ],
        [
            Cell('R21', styles=[Style.UNDERLINE]),
            Cell('R22', styles=[Style.UNDERLINE]),
            Cell('R23', styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'={Ay} * {Ax} * (1 - cos({Angle})) + {Az} * sin({Angle})',
                 alias=R21),
            Cell(f'=cos({Angle}) + {Ay} ^ 2 * (1 - cos({Angle}))',
                 alias=R22),
            Cell(f'={Ay} * {Az} * (1 - cos({Angle})) - {Ax} * sin({Angle})',
                 alias=R23)
        ],
        [
            Cell('R31', styles=[Style.UNDERLINE]),
            Cell('R32', styles=[Style.UNDERLINE]),
            Cell('R33', styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'={Az} * {Ax} * (1 - cos({Angle})) - {Ay} * sin({Angle})',
                 alias=R31),
            Cell(f'={Az} * {Ay} * (1 - cos({Angle})) + {Ax} * sin({Angle})',
                 alias=R32),
            Cell(f'=cos({Angle}) + {Az} ^ 2 * (1 - cos({Angle}))',
                 alias=R33)
        ],
        [
            Cell('Rotation Matrix * V',
                 styles=[Style.UNDERLINE])
        ],
        [
            Cell(RotatedX, styles=[Style.UNDERLINE]),
            Cell(RotatedY, styles=[Style.UNDERLINE]),
            Cell(RotatedZ, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'={R11} * {Vx} + {R12} * {Vy} + {R13} * {Vz}',
                 alias=RotatedX),
            Cell(f'={R21} * {Vx} + {R22} * {Vy} + {R23} * {Vz}',
                 alias=RotatedY),
            Cell(f'={R31} * {Vx} + {R32} * {Vy} + {R33} * {Vz}',
                 alias=RotatedZ)
        ]
    ]
