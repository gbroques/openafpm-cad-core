# Postpone evalutation of annotations.
# TODO: Remove in Python 3.10 or greater.
# See:
#   https://stackoverflow.com/a/42845998
from __future__ import annotations

from enum import Enum, unique
from typing import List, Tuple

__all__ = [
    'Cell',
    'Style',
    'Alignment',
    'Color'
]


@unique
class Style(Enum):
    """Enumeration of cell styles.

    `See also, FreeCAD source code`__.

    __ https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/Gui/PropertiesDialog.cpp#L161-L181
    """
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'

    @classmethod
    def encode(cls, styles: List[Style]) -> str:
        """Encode a set of styles as a string.

        `See also, FreeCAD source code`__.

        __ https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/Cell.cpp#L960-L983
        """
        return '|'.join(map(lambda s: s.value, styles))


@unique
class Alignment(Enum):
    """Enumeration of cell alignment.

    `See also, FreeCAD source code`__.

    __ https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/SheetPyImp.cpp#L695-L706

    """
    LEFT = 'left'
    HORIZONTAL_CENTER = 'center'
    RIGHT = 'right'
    TOP = 'top'
    VERTICAL_CENTER = 'vcenter'
    BOTTOM = 'bottom'

    @classmethod
    def encode(cls, alignments: Tuple[Alignment, Alignment]) -> str:
        """Encode horizontal and vertical alignment as a string.

        `See also, FreeCAD source code`__.

        __ https://github.com/FreeCAD/FreeCAD/blob/0.19.2/src/Mod/Spreadsheet/App/Cell.cpp#L901-L936
        """
        return '|'.join(map(lambda a: a.value, alignments))


@unique
class Color(Enum):
    """Enumeration of default background and foreground colors in the form (r, g, b, a).

    Where (r, g, b, a) are float values in the range 0 to 1 inclusive:

    * r = red
    * g = green
    * b = blue
    * a = alpha (opacity)
    """
    WHITE = (1.0, 1.0, 1.0, 1.0)
    BLACK = (0.0, 0.0, 0.0, 1.0)


class Cell:
    """Represents a cell in a FreeCAD spreadsheet."""

    def __init__(self,
                 content: str = '',
                 alias: str = '',
                 styles: List[Style] = [],
                 horizontal_alignment: Alignment = Alignment.LEFT,
                 vertical_alignment: Alignment = Alignment.VERTICAL_CENTER,
                 background: Tuple[float, float,
                                   float, float] = Color.WHITE.value,
                 foreground: Tuple[float, float, float, float] = Color.BLACK.value) -> None:
        self.content = content
        self.alias = alias
        self.styles = styles
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment
        self.background = background
        self.foreground = foreground

    @property
    def style(self) -> str:
        return Style.encode(self.styles)

    @property
    def alignment(self) -> str:
        return Alignment.encode((self.horizontal_alignment, self.vertical_alignment))

    def __repr__(self) -> str:
        return self.content
