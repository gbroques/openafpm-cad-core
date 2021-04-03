"""
FreeCAD macro to create WindTurbine document
with spreadsheet containing input parameters.
"""

from enum import Enum, unique

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui

DEFAULT_SPREADSHEET_NAME = 'Master of Puppets'


@unique
class WindTurbine(Enum):
    T_SHAPE = 'T Shape'
    H_SHAPE = 'H Shape'
    STAR_SHAPE = 'Star Shape'


parameters_by_variant = {
    WindTurbine.T_SHAPE: {
        'MagnAFPM': {
            'RotorDiskRadius': 150,
            'DiskThickness': 10,
            'MagnetLength': 46,
            'MagnetWidth': 30,
            'MagnetThickness': 10,
            'NumberMagnet': 12,
            'StatorThickness': 13,
            'CoilLegWidth': 22.5,
            'CoilInnerWidth1': 30,
            'CoilInnerWidth2': 30,
            'MechanicalClearance': 3
        },
        'OpenFurl': {
            'Angle': 20,
            'BracketLength': 300,
            'BracketWidth': 30,
            'BracketThickness': 5,
            'BoomLength': 1000,
            'BoomPipeRadius': 24.15,
            'BoomPipeThickness': 5,
            'VaneThickness': 6,
            'VaneLength': 1200,
            'VaneWidth': 500,
            'Offset': 125
        },
        'User': {
            'HubHolesPlacement': 50,
            'RotorInnerCircle': 32.5,
            'Holes': 6,
            'MetalLengthL': 50,
            'MetalThicknessL': 6,
            'FlatMetalThickness': 10,
            'YawPipeRadius': 30.15,
            'PipeThickness': 5,
            'ResineRotorMargin': 5,
            'HubHoles': 6
        }
    },
    WindTurbine.H_SHAPE: {
        'MagnAFPM': {
            'RotorDiskRadius': 230,
            'DiskThickness': 10,
            'MagnetLength': 46,
            'MagnetWidth': 30,
            'MagnetThickness': 10,
            'NumberMagnet': 16,
            'StatorThickness': 13,
            'CoilLegWidth': 22.5,
            'CoilInnerWidth1': 30,
            'CoilInnerWidth2': 30,
            'MechanicalClearance': 3
        },
        'OpenFurl': {
            'Angle': 20,
            'BracketLength': 300,
            'BracketWidth': 30,
            'BracketThickness': 5,
            'BoomLength': 1000,
            'BoomPipeRadius': 24.15,
            'BoomPipeThickness': 5,
            'VaneThickness': 6,
            'VaneLength': 1200,
            'VaneWidth': 500,
            'Offset': 125
        },
        'User': {
            'HubHolesPlacement': 65,
            'RotorInnerCircle': 47.5,
            'Holes': 6,
            'MetalLengthL': 50,
            'MetalThicknessL': 6,
            'FlatMetalThickness': 10,
            'YawPipeRadius': 44.5,
            'PipeThickness': 5,
            'ResineRotorMargin': 5,
            'HubHoles': 7
        }
    },
    WindTurbine.STAR_SHAPE: {
        'MagnAFPM': {
            'RotorDiskRadius': 349,
            'DiskThickness': 10,
            'MagnetLength': 58,
            'MagnetWidth': 30,
            'MagnetThickness': 10,
            'NumberMagnet': 32,
            'StatorThickness': 15,
            'CoilLegWidth': 22.5,
            'CoilInnerWidth1': 30,
            'CoilInnerWidth2': 30,
            'MechanicalClearance': 3
        },
        'OpenFurl': {
            'Angle': 20,
            'BracketLength': 300,
            'BracketWidth': 30,
            'BracketThickness': 5,
            'BoomLength': 1000,
            'BoomPipeRadius': 24.15,
            'BoomPipeThickness': 5,
            'VaneThickness': 6,
            'VaneLength': 1200,
            'VaneWidth': 500,
            'Offset': 125
        },
        'User': {
            'HubHolesPlacement': 102.5,
            'RotorInnerCircle': 81.5,
            'Holes': 7,
            'MetalLengthL': 65,
            'MetalThicknessL': 8,
            'FlatMetalThickness': 10,
            'YawPipeRadius': 57.15,
            'PipeThickness': 5,
            'ResineRotorMargin': 5,
            'HubHoles': 8
        }
    }
}


class TaskPanel:
    def __init__(self, title):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)

        layout = QtGui.QVBoxLayout(self.form)

        # Row 1
        row1 = QtGui.QHBoxLayout()

        label = QtGui.QLabel('<strong>Document Name:</strong>', self.form)
        self.line_edit = QtGui.QLineEdit(self.form)
        self.line_edit.setText(DEFAULT_SPREADSHEET_NAME)

        row1.addWidget(label)
        row1.addWidget(self.line_edit)

        layout.addLayout(row1)

        # Row 2
        row2 = QtGui.QHBoxLayout()

        label = QtGui.QLabel('<strong>Variant:</strong>', self.form)
        self.combo_box = self.create_combo_box()

        row2.addWidget(label)
        row2.addWidget(self.combo_box)

        layout.addLayout(row2)

        # Row 3
        row3 = QtGui.QHBoxLayout()

        rotor_disk_radius_label = QtGui.QLabel(
            '<strong>Rotor Disk Radius:</strong>', self.form)
        self.rotor_disk_radius_value = self.create_rotor_disk_radius_value()

        row3.addWidget(rotor_disk_radius_label)
        row3.addWidget(self.rotor_disk_radius_value)

        layout.addLayout(row3)

    def create_rotor_disk_radius_value(self):
        default_variant = WindTurbine.T_SHAPE
        default_rotor_disk_radius = get_rotor_disk_radius(default_variant)
        return QtGui.QLabel(default_rotor_disk_radius, self.form)

    def create_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        items = [variant.value for variant in list(WindTurbine)]
        combo_box.addItems(items)
        combo_box.activated[str].connect(self.handle_combo_box_activated)
        return combo_box

    def handle_combo_box_activated(self, selected_text):
        selected_variant = WindTurbine(selected_text)
        selected_rotor_disk_radius = get_rotor_disk_radius(selected_variant)
        self.rotor_disk_radius_value.setText(selected_rotor_disk_radius)

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        current_text = self.combo_box.currentText()
        variant = WindTurbine(current_text)
        parameters = parameters_by_variant[variant]
        create_spreadsheet_document(self.line_edit.text(), parameters)
        Gui.Control.closeDialog()


def get_rotor_disk_radius(variant):
    return str(parameters_by_variant[variant]['MagnAFPM']['RotorDiskRadius'])


def create_spreadsheet_document(document_name, parameters_by_key):
    document = App.newDocument(document_name)
    sheet_name = 'Spreadsheet'
    sheet = document.addObject('Spreadsheet::Sheet', sheet_name)
    cells = _buid_cells(parameters_by_key)

    _populate_spreadsheet(sheet, cells)
    document.recompute()
    return document


def _buid_cells(parameters_by_key):
    cells = []
    for key, parameters in parameters_by_key.items():
        cells.append([key, ''])
        cells.extend(_dict_to_cells(parameters))
    return cells


def _dict_to_cells(dictionary):
    return [[key, value] for key, value in dictionary.items()]


def _populate_spreadsheet(spreadsheet, cells):
    for i, (key, value) in enumerate(cells):
        number = str(i + 1)
        key_cell = 'A' + number
        value_cell = 'B' + number
        spreadsheet.set(key_cell, key)
        spreadsheet.set(value_cell, str(value))
        if value:
            spreadsheet.setAlias(value_cell, key)
        else:
            spreadsheet.setStyle(key_cell, 'bold')


Gui.Control.closeDialog()
panel = TaskPanel('Select Wind Turbine Variant')
Gui.Control.showDialog(panel)
