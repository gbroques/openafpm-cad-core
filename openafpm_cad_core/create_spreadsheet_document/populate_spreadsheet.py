from typing import List

from .cell import Cell
from .column_number_mappers import map_number_to_column

__all__ = ['populate_spreadsheet']


def populate_spreadsheet(spreadsheet: object, cells: List[List[Cell]]) -> None:
    """Populates a spreadsheet object with the given cells.

    .. code-block:: python

        spreadsheet = document.addObject('Spreadsheet::Sheet', name)
        populate_spreadsheet(spreadsheet, cells)

    """
    for row_index in range(len(cells)):
        for col_index in range(len(cells[row_index])):
            cell_address = get_cell_address(row_index, col_index)
            cell = cells[row_index][col_index]
            populate_spreadsheet_with_cell(spreadsheet, cell_address, cell)


def get_cell_address(row_index: int, col_index: int) -> str:
    row_num = row_index + 1
    col_num = col_index + 1
    column = map_number_to_column(col_num)
    cell_address = column + str(row_num)
    return cell_address


def populate_spreadsheet_with_cell(spreadsheet: object,
                                   cell_address: str,
                                   cell: Cell) -> None:
    spreadsheet.set(cell_address, cell.content)
    spreadsheet.setAlias(cell_address, cell.alias)
    spreadsheet.setStyle(cell_address, cell.style)
    spreadsheet.setAlignment(cell_address, cell.alignment)
    spreadsheet.setBackground(cell_address, cell.background)
    spreadsheet.setForeground(cell_address, cell.foreground)
