from typing import List

from .cell import Cell
from .column_number_mappers import map_number_to_column

__all__ = ['populate_spreadsheet']


def populate_spreadsheet(spreadsheet: object, cells: List[List[Cell]]) -> None:
    """
    Populates a spreadsheet object with the given cells.

    ::

        spreadsheet = document.addObject('Spreadsheet::Sheet', name)
        populate_spreadsheet(spreadsheet, cells)

    """
    for row_index in range(len(cells)):
        for col_index in range(len(cells[row_index])):
            row_num = row_index + 1
            col_num = col_index + 1
            column = map_number_to_column(col_num)
            cell_address = column + str(row_num)
            cell = cells[row_index][col_index]
            spreadsheet.set(cell_address, cell.content)
            spreadsheet.setAlias(cell_address, cell.alias)
            spreadsheet.setStyle(cell_address, cell.style)
            spreadsheet.setAlignment(cell_address, cell.alignment)
            spreadsheet.setBackground(cell_address, cell.background)
            spreadsheet.setForeground(cell_address, cell.foreground)
