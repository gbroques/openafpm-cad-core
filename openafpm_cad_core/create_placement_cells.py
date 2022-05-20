from typing import List, Tuple

from .spreadsheet import Alignment, Cell, Style

__all__ = ['create_placement_cells']


def create_placement_cells(name: str,
                           base: Tuple[str, str, str],
                           axis: Tuple[str, str, str],
                           angle: str) -> List[List[Cell]]:
    def namespace(s): return name + s
    x, y, z = base
    X, Y, Z = namespace('X'), namespace('Y'), namespace('Z')
    Base = namespace('Base')
    Ax, Ay, Az = axis
    Axis = namespace('Axis')
    Angle = namespace('Angle')
    Rotation = namespace('Rotation')
    Placement = namespace('Placement')
    return [
        [
            Cell(name, styles=[Style.UNDERLINE])
        ],
        [
            Cell('x', horizontal_alignment=Alignment.RIGHT),
            Cell('y', horizontal_alignment=Alignment.RIGHT),
            Cell('z', horizontal_alignment=Alignment.RIGHT)
        ],
        [
            Cell(x, alias=X),
            Cell(y, alias=Y),
            Cell(z, alias=Z),
        ],
        [
            Cell('Base'),
            Cell('Axis'),
            Cell('Angle')
        ],
        [
            Cell(f'=create(<<vector>>; {X}; {Y}; {Z})',
                 alias=Base),
            Cell(f'=create(<<vector>>; {Ax}; {Ay}; {Az})', alias=Axis),
            Cell(angle, alias=Angle)
        ],
        [
            Cell('Rotation'),
            Cell('Placement')
        ],
        [
            Cell(f'=create(<<rotation>>; {Axis}; {Angle})', alias=Rotation),
            Cell(
                f'=create(<<placement>>; {Base}; {Rotation})', alias=Placement)
        ]
    ]
