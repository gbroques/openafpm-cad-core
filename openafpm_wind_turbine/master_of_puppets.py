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
    _create_imported_sheet(document,
                           imported_spreadsheet_name,
                           magn_afpm_parameters,
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

    cell_alias_map = get_master_sheet_cell_alias_map()

    def build_expression(field_name):
        return '=' + imported_spreadsheet_name + '.' + field_name

    cells = [
        ['Inputs', ''],
        ['Holes', build_expression(cell_alias_map['Holes'])],
        ['RotorRadius', build_expression(cell_alias_map['RotorRadius'])],
        ['DiskThickness', build_expression(cell_alias_map['DiskThickness'])],
        ['MagnetLength', build_expression(cell_alias_map['MagnetLength'])],
        ['MagnetWidth', build_expression(cell_alias_map['MagnetWidth'])],
        ['MagnetThickness', build_expression(
            cell_alias_map['MagnetThickness'])],
        ['NumberMagnet', build_expression(cell_alias_map['NumberMagnet'])],
        ['HubHolesPlacement', build_expression(
            cell_alias_map['HubHolesPlacement'])],
        ['RotorInnerCircle', build_expression(
            cell_alias_map['RotorInnerCircle'])],
        ['StatorThickness', build_expression(
            cell_alias_map['StatorThickness'])],
        ['CoilLegWidth', build_expression(cell_alias_map['CoilLegWidth'])],
        ['CoilInnerWidth1', build_expression(
            cell_alias_map['CoilInnerWidth1'])],
        ['CoilInnerWidth2', build_expression(
            cell_alias_map['CoilInnerWidth2'])],
        ['Angle', build_expression(cell_alias_map['Angle'])],
        ['Offset', build_expression(cell_alias_map['Offset'])],
        ['ResineRotorMargin', build_expression(
            cell_alias_map['ResineRotorMargin'])],
        ['CharacteristicsOfMetalParts', ''],
        ['MetalThicknessL', build_expression(
            cell_alias_map['MetalThicknessL'])],
        ['MetalLengthL', build_expression(cell_alias_map['MetalLengthL'])],
        ['OuterRadiusYawPipe', build_expression(
            cell_alias_map['OuterRadiusYawPipe'])],
        ['PipesThickness', build_expression(cell_alias_map['PipesThickness'])],
        ['FlatMetalThickness', build_expression(
            cell_alias_map['FlatMetalThickness'])],
        ['HingeInnerBodyOuterRadius',
            '=RotorRadius < 187.5 ? 24.15 : RotorRadius < 275 ? 38 : 50.8'],
        ['HubHoles', build_expression(cell_alias_map['HubHoles'])],
        ['VariableInterParts', ''],
        ['ResineStatorOuterRadius', '=RotorRadius + CoilLegWidth + 20'],
        ['CharacteristicsOfFurling', ''],
        ['BracketLength', build_expression(cell_alias_map['BracketLength'])],
        ['BracketWidth', build_expression(cell_alias_map['BracketWidth'])],
        ['BracketThickness', build_expression(
            cell_alias_map['BracketThickness'])],
        ['BoomLength', build_expression(cell_alias_map['BoomLength'])],
        ['VaneThickness', build_expression(cell_alias_map['VaneThickness'])],
        ['VaneLength', build_expression(cell_alias_map['VaneLength'])],
        ['VaneWidth', build_expression(cell_alias_map['VaneWidth'])],
        ['BoomPipeRadius', build_expression(cell_alias_map['BoomPipeRadius'])],
        ['BoomPipeThickness', build_expression(
            cell_alias_map['BoomPipeThickness'])]
    ]

    _populate_sheet(sheet, cells)
    return sheet


def get_master_sheet_cell_alias_map():
    # TODO: Get rid of this mapping by making all 'DIFFERENT!' fields the same.
    return {
        'Holes': 'Holes',
        'RotorRadius': 'RotorDiskRadius',  # DIFFERENT!
        'DiskThickness': 'DiskThickness',
        'MagnetLength': 'MagnetLength',
        'MagnetWidth': 'MagnetWidth',
        'MagnetThickness': 'MagnetThickness',
        'NumberMagnet': 'NumberMagnet',
        'HubHolesPlacement': 'HubHolesPlacement',
        'RotorInnerCircle': 'RotorInnerCircle',
        'StatorThickness': 'StatorThickness',
        'CoilLegWidth': 'CoilLegWidth',
        'CoilInnerWidth1': 'CoilInnerWidth1',
        'CoilInnerWidth2': 'CoilInnerWidth2',
        'Angle': 'Angle',
        'Offset': 'Offset',
        'ResineRotorMargin': 'ResineRotorMargin',
        'MetalThicknessL': 'MetalThicknessL',
        'MetalLengthL': 'MetalLengthL',
        'OuterRadiusYawPipe': 'YawPipeRadius',  # DIFFERENT!
        'PipesThickness': 'PipeThickness',  # DIFFERENT!
        'FlatMetalThickness': 'FlatMetalThickness',
        'HubHoles': 'HubHoles',
        'BracketLength': 'BracketLength',
        'BracketWidth': 'BracketWidth',
        'BracketThickness': 'BracketThickness',
        'BoomLength': 'BoomLength',
        'VaneThickness': 'VaneThickness',
        'VaneLength': 'VaneLength',
        'VaneWidth': 'VaneWidth',
        'BoomPipeRadius': 'BoomPipeRadius',
        'BoomPipeThickness': 'BoomPipeThickness'
    }


def _populate_sheet(sheet, cells):
    for i, (key, value) in enumerate(cells):
        number = i + 1
        sheet.set('A' + str(number), key)
        sheet.set('B' + str(number), str(value))
        if value:
            sheet.setAlias('B' + str(number), key)
