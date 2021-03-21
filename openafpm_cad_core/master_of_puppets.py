"""
Module to create a document with a spreadsheet that controls other spreadsheets.
"""
import FreeCAD as App
import Spreadsheet

__all__ = ['create_master_of_puppets']


def create_master_of_puppets(document_name,
                             master_spreadsheet_name,
                             magnafpm_parameters,
                             user_parameters,
                             furling_parameters):
    document = App.newDocument(document_name)
    _create_master_spreadsheet(document,
                               master_spreadsheet_name,
                               magnafpm_parameters,
                               user_parameters,
                               furling_parameters)
    document.recompute()
    return document


def _create_master_spreadsheet(document,
                               name,
                               magnafpm_parameters,
                               user_parameters,
                               furling_parameters):
    sheet = document.addObject('Spreadsheet::Sheet', name)
    magn_afpm_cells = _dict_to_cells(magnafpm_parameters)
    user_cells = _dict_to_cells(user_parameters)
    furling_tool_cells = _dict_to_cells(furling_parameters)
    cells = [
        ['Inputs', 'Value'],

        # MagnAFPM
        # --------
        ['MagnAFPM', ''],
        *magn_afpm_cells,

        # FurlingTool
        # -----------
        ['FurlingTool', ''],
        *furling_tool_cells,

        # User
        # ----
        ['User', ''],
        *user_cells
    ]

    _populate_sheet(sheet, cells)
    return sheet


def _dict_to_cells(dictionary):
    return [[key, value] for key, value in dictionary.items()]


def _populate_sheet(sheet, cells):
    for i, (key, value) in enumerate(cells):
        number = i + 1
        sheet.set('A' + str(number), key)
        sheet.set('B' + str(number), str(value))
        if value:
            sheet.setAlias('B' + str(number), key)
