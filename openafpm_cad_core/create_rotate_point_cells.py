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
            Cell('Point', styles=[Style.ITALIC])
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
            Cell('Center', styles=[Style.ITALIC]),
            Cell('to Rotate Around')
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
        [
            Cell('V = P  - C', styles=[Style.ITALIC])
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
            Cell('R = C + Prime', styles=[Style.ITALIC])
        ],
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
            Cell('Vector', styles=[Style.ITALIC]),
            Cell('to Rotate')
        ],
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
        *create_rotation_matrix_cells(
            (
                (R11, R12, R13),
                (R21, R22, R23),
                (R31, R32, R33)
            ),
            (aX, aY, aZ),
            (Ax, Ay, Az),
            rotation_angle,
            Angle
        ),
        [
            Cell('Rotation Matrix * V',
                 styles=[Style.ITALIC])
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


def create_multiply_rotation_cells(alias_namespace: str,
                                   rotation_axis_a: Tuple[str, str, str],
                                   rotation_angle_a: str,
                                   rotation_axis_b: Tuple[str, str, str],
                                   rotation_angle_b: str) -> List[List[Cell]]:
    """
    Multiplies two 3x3 rotation matrices together.

    Equivalent FreeCAD Python code:

    ::

        rotation_c = rotation_a.multiply(rotation_b)

    """
    def alias(a): return alias_namespace + a

    # Rotation Axis & Angle for A
    aX, aY, aZ = rotation_axis_a
    Ax, Ay, Az = alias('Ax'), alias('Ay'), alias('Az')
    AngleA = alias('AngleA')

    # Rotation Axis & Angle for B
    bX, bY, bZ = rotation_axis_b
    Bx, By, Bz = alias('Bx'), alias('By'), alias('Bz')
    AngleB = alias('AngleB')

    # Rotation Matrix A
    A11, A12, A13 = alias('A11'), alias('A12'), alias('A13')
    A21, A22, A23 = alias('A21'), alias('A22'), alias('A23')
    A31, A32, A33 = alias('A31'), alias('A32'), alias('A33')

    # Rotation Matrix B
    B11, B12, B13 = alias('B11'), alias('B12'), alias('B13')
    B21, B22, B23 = alias('B21'), alias('B22'), alias('B23')
    B31, B32, B33 = alias('B31'), alias('B32'), alias('B33')

    # Rotation Matrix C
    C11, C12, C13 = alias('11'), alias('12'), alias('13')
    C21, C22, C23 = alias('21'), alias('22'), alias('23')
    C31, C32, C33 = alias('31'), alias('32'), alias('33')
    return [
        *create_rotation_matrix_cells(
            (
                (A11, A12, A13),
                (A21, A22, A23),
                (A31, A32, A33)
            ),
            (aX, aY, aZ),
            (Ax, Ay, Az),
            rotation_angle_a,
            AngleA
        ),
        *create_rotation_matrix_cells(
            (
                (B11, B12, B13),
                (B21, B22, B23),
                (B31, B32, B33)
            ),
            (bX, bY, bZ),
            (Bx, By, Bz),
            rotation_angle_b,
            AngleB
        ),
        [
            Cell('Rotate A & B',
                 styles=[Style.ITALIC])
        ],
        [
            Cell(C11, styles=[Style.UNDERLINE]),
            Cell(C12, styles=[Style.UNDERLINE]),
            Cell(C13, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'=({A11} * {B11}) + ({A12} * {B21}) + ({A13} * {B31})',
                 alias=C11),
            Cell(f'=({A11} * {B12}) + ({A12} * {B22}) + ({A13} * {B32})',
                 alias=C12),
            Cell(f'=({A11} * {B13}) + ({A12} * {B23}) + ({A13} * {B33})',
                 alias=C13)
        ],
        [
            Cell(C21, styles=[Style.UNDERLINE]),
            Cell(C22, styles=[Style.UNDERLINE]),
            Cell(C23, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'=({A21} * {B11}) + ({A22} * {B21}) + ({A23} * {B31})',
                 alias=C21),
            Cell(f'=({A21} * {B12}) + ({A22} * {B22}) + ({A23} * {B32})',
                 alias=C22),
            Cell(f'=({A21} * {B13}) + ({A22} * {B23}) + ({A23} * {B33})',
                 alias=C23)
        ],
        [
            Cell(C31, styles=[Style.UNDERLINE]),
            Cell(C32, styles=[Style.UNDERLINE]),
            Cell(C33, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'=({A31} * {B11}) + ({A32} * {B21}) + ({A33} * {B31})',
                 alias=C31),
            Cell(f'=({A31} * {B12}) + ({A32} * {B22}) + ({A33} * {B32})',
                 alias=C32),
            Cell(f'=({A31} * {B13}) + ({A32} * {B23}) + ({A33} * {B33})',
                 alias=C33)
        ]
    ]


MatrixType = Tuple[Tuple[str, str, str],
                   Tuple[str, str, str],
                   Tuple[str, str, str]]


def create_rotation_matrix_cells(Matrix: MatrixType,
                                 Axis: Tuple[str, str, str],
                                 AxisAliases: Tuple[str, str, str],
                                 rotation_angle: str,
                                 Angle: str):
    # Matrix
    Row1, Row2, Row3 = Matrix
    R11, R12, R13 = Row1
    R21, R22, R23 = Row2
    R31, R32, R33 = Row3

    # Axis
    aX, aY, aZ = Axis
    Ax, Ay, Az = AxisAliases
    return [
        [
            Cell('Rotation Axis', styles=[Style.ITALIC])
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
                 styles=[Style.ITALIC]),
            Cell('Formula:', styles=[Style.BOLD]),
            Cell(
                'https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle')
        ],
        [
            Cell(R11, styles=[Style.UNDERLINE]),
            Cell(R12, styles=[Style.UNDERLINE]),
            Cell(R13, styles=[Style.UNDERLINE]),
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
            Cell(R21, styles=[Style.UNDERLINE]),
            Cell(R22, styles=[Style.UNDERLINE]),
            Cell(R23, styles=[Style.UNDERLINE]),
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
            Cell(R31, styles=[Style.UNDERLINE]),
            Cell(R32, styles=[Style.UNDERLINE]),
            Cell(R33, styles=[Style.UNDERLINE]),
        ],
        [
            Cell(f'={Az} * {Ax} * (1 - cos({Angle})) - {Ay} * sin({Angle})',
                 alias=R31),
            Cell(f'={Az} * {Ay} * (1 - cos({Angle})) + {Ax} * sin({Angle})',
                 alias=R32),
            Cell(f'=cos({Angle}) + {Az} ^ 2 * (1 - cos({Angle}))',
                 alias=R33)
        ]
    ]
