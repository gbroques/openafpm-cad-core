from typing import Iterable, List, Tuple

from ..close_all_documents import close_all_documents
from .cell import Cell
from .column_number_mappers import map_number_to_column

__all__ = ['populate_spreadsheet']


def populate_spreadsheet(spreadsheet: object, cells: List[List[Cell]], cancel_event=None) -> None:
    """Populates a spreadsheet object with the given cells.

    .. code-block:: python

        spreadsheet = document.addObject('Spreadsheet::Sheet', name)
        populate_spreadsheet(spreadsheet, cells)

    """
    for cell_address, cell in enumerate_cells(cells):
        if cancel_event is not None and cancel_event.is_set():
            close_all_documents()
            raise InterruptedError("Operation was cancelled")
        populate_spreadsheet_with_cell(spreadsheet, cell_address, cell, cancel_event)


def enumerate_cells(cells: List[List[Cell]]) -> Iterable[Tuple[str, Cell]]:
    for row_index in range(len(cells)):
        for col_index in range(len(cells[row_index])):
            cell_address = get_cell_address(row_index, col_index)
            cell = cells[row_index][col_index]
            yield cell_address, cell


def get_cell_address(row_index: int, col_index: int) -> str:
    row_num = row_index + 1
    col_num = col_index + 1
    column = map_number_to_column(col_num)
    cell_address = column + str(row_num)
    return cell_address


def populate_spreadsheet_with_cell(spreadsheet: object,
                                   cell_address: str,
                                   cell: Cell,
                                   cancel_event=None) -> None:
    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")
        
    spreadsheet.set(cell_address, cell.content)
    if spreadsheet.getCellFromAlias(cell.alias) is not None:
        raise ValueError(f'Alias "{cell.alias}" already defined')
    spreadsheet.setAlias(cell_address, cell.alias)
    spreadsheet.setStyle(cell_address, cell.style)
    spreadsheet.setAlignment(cell_address, cell.alignment)
    spreadsheet.setBackground(cell_address, cell.background)
    spreadsheet.setForeground(cell_address, cell.foreground)
