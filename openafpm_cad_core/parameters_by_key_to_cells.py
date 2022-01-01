from typing import Any, Dict, List

from .spreadsheet import Cell, Style

__all__ = ['parameters_by_key_to_cells']


def parameters_by_key_to_cells(parameters_by_key: Dict[str, Dict[str, Any]]) -> List[List[Cell]]:
    cells = []
    for key, parameters in parameters_by_key.items():
        cells.append([Cell(key, styles=[Style.UNDERLINE])])
        cells.extend(_dict_to_cells(parameters))
    return cells


def _dict_to_cells(dictionary: Dict[str, Any]) -> List[List[Cell]]:
    return [
        [Cell(key), Cell(str(value), alias=key)]
        for key, value in dictionary.items()
    ]
