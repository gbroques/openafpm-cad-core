"""
Module to create a document with a spreadsheet that controls other spreadsheets.
"""
import FreeCAD as App
import Spreadsheet

__all__ = ['create_master_of_puppets']


def create_master_of_puppets(document_name,
                             imported_spreadsheet_name,
                             master_spreadsheet_name,
                             magn_afpm_parameters,
                             user_parameters,
                             furling_tool_parameters):
    document = App.newDocument(document_name)
    # TODO: Get rid of MechanicalClearance pop hack.
    magn_afpm_parameters_copy = magn_afpm_parameters.copy()
    magn_afpm_parameters_copy.pop('MechanicalClearance')
    _create_imported_sheet(document,
                           imported_spreadsheet_name,
                           magn_afpm_parameters_copy,
                           user_parameters,
                           furling_tool_parameters)
    document.recompute()
    _create_master_sheet(document, master_spreadsheet_name,
                         imported_spreadsheet_name)
    return document


def _create_imported_sheet(document,
                           name,
                           magn_afpm_parameters,
                           user_parameters,
                           furling_tool_parameters):
    sheet = document.addObject('Spreadsheet::Sheet', name)
    magn_afpm_cells = _dict_to_cells(magn_afpm_parameters)
    user_cells = _dict_to_cells(user_parameters)
    furling_tool_cells = _dict_to_cells(furling_tool_parameters)
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


def _create_master_sheet(document, name, imported_spreadsheet_name):
    sheet = document.addObject(
        'Spreadsheet::Sheet', name)

    cells = [
        ['Inputs', ''],
        ['Holes', '=' + imported_spreadsheet_name + '.B28'],
        ['RotorRadius', '=' + imported_spreadsheet_name + '.B3'],
        ['DiskThickness', '=' + imported_spreadsheet_name + '.B4'],
        ['MagnetLength', '=' + imported_spreadsheet_name + '.B5'],
        ['MagnetWidth', '=' + imported_spreadsheet_name + '.B6'],
        ['MagnetThickness', '=' + imported_spreadsheet_name + '.B7'],
        ['NumberMagnet', '=' + imported_spreadsheet_name + '.B8'],
        ['HubHolesPlacement', '=' + imported_spreadsheet_name + '.B26'],
        ['RotorInnerCircle', '=' + imported_spreadsheet_name + '.B27'],
        ['StatorThickness', '=' + imported_spreadsheet_name + '.B9'],
        ['CoilLegWidth', '=' + imported_spreadsheet_name + '.B10'],
        ['CoilInnerWidth1', '=' + imported_spreadsheet_name + '.B11'],
        ['CoilInnerWidth2', '=' + imported_spreadsheet_name + '.B12'],
        ['Angle', '=' + imported_spreadsheet_name + '.B14'],
        ['Offset', '=' + imported_spreadsheet_name + '.B24'],
        ['ResineRotorMargin', '=' + imported_spreadsheet_name + '.B34'],
        ['CharacteristicsOfMetalParts', ''],
        ['MetalThicknessL', '=' + imported_spreadsheet_name + '.B30'],
        ['MetalLengthL', '=' + imported_spreadsheet_name + '.B29'],
        ['OuterRadiusYawPipe', '=' + imported_spreadsheet_name + '.B32'],
        ['PipesThickness', '=' + imported_spreadsheet_name + '.B33'],
        ['FlatMetalThickness', '=' + imported_spreadsheet_name + '.B31'],
        ['HingeInnerBodyOuterRadius',
            '=RotorRadius < 187.5 ? 24.15 : RotorRadius < 275 ? 38 : 50.8'],
        ['HubHoles', '=' + imported_spreadsheet_name + '.B35'],
        ['VariableInterParts', ''],
        ['ResineStatorOuterRadius', '=RotorRadius + CoilLegWidth + 20'],
        ['CharacteristicsOfFurling', ''],
        ['BracketLength', '=' + imported_spreadsheet_name + '.B15'],
        ['BracketWidth', '=' + imported_spreadsheet_name + '.B16'],
        ['BracketThickness', '=' + imported_spreadsheet_name + '.B17'],
        ['BoomLength', '=' + imported_spreadsheet_name + '.B18'],
        ['VaneThickness', '=' + imported_spreadsheet_name + '.B21'],
        ['VaneLength', '=' + imported_spreadsheet_name + '.B22'],
        ['VaneWidth', '=' + imported_spreadsheet_name + '.B23'],
        ['BoomPipeRadius', '=' + imported_spreadsheet_name + '.B19'],
        ['BoomPipeThickness', '=' + imported_spreadsheet_name + '.B20']
    ]

    _populate_sheet(sheet, cells)
    return sheet


def _populate_sheet(sheet, cells):
    for i, (key, value) in enumerate(cells):
        number = i + 1
        sheet.set('A' + str(number), key)
        sheet.set('B' + str(number), str(value))
        if value:
            sheet.setAlias('B' + str(number), key)
