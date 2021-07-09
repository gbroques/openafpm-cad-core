"""
FreeCAD macro to create wind turbine document
with spreadsheet containing input parameters.
"""

from enum import Enum, unique
from typing import Any, Callable

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui

__all__ = ['CreateSpreadsheetTaskPanel']


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
            'VerticalPlaneAngle': 20,
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
            'HubHoles': 6,
            'HorizontalPlaneAngle': 55
        }
    },
    WindTurbine.H_SHAPE: {
        'MagnAFPM': {
            'RotorDiskRadius': 225,
            'DiskThickness': 10,
            'MagnetLength': 46,
            'MagnetWidth': 30,
            'MagnetThickness': 10,
            'NumberMagnet': 16,
            'StatorThickness': 13,
            'CoilLegWidth': 32,
            'CoilInnerWidth1': 30,
            'CoilInnerWidth2': 30,
            'MechanicalClearance': 3
        },
        'OpenFurl': {
            'VerticalPlaneAngle': 15,
            'BracketLength': 600,
            'BracketWidth': 50,
            'BracketThickness': 6,
            'BoomLength': 1800,
            'BoomPipeRadius': 24.15,
            'BoomPipeThickness': 5,
            'VaneThickness': 9,
            'VaneLength': 1200,
            'VaneWidth': 900,
            'Offset': 250
        },
        'User': {
            'HubHolesPlacement': 65,
            'RotorInnerCircle': 47.5,
            'Holes': 7,
            'MetalLengthL': 50,
            'MetalThicknessL': 6,
            'FlatMetalThickness': 10,
            'YawPipeRadius': 44.5,
            'PipeThickness': 5,
            'ResineRotorMargin': 5,
            'HubHoles': 7,
            'HorizontalPlaneAngle': 55
        }
    },
    WindTurbine.STAR_SHAPE: {
        'MagnAFPM': {
            'RotorDiskRadius': 350,
            'DiskThickness': 10,
            'MagnetLength': 58,
            'MagnetWidth': 27,
            'MagnetThickness': 10,
            'NumberMagnet': 32,
            'StatorThickness': 15,
            'CoilLegWidth': 22.4,
            'CoilInnerWidth1': 40,
            'CoilInnerWidth2': 27,
            'MechanicalClearance': 3
        },
        'OpenFurl': {
            'VerticalPlaneAngle': 15,
            'BracketLength': 600,
            'BracketWidth': 50,
            'BracketThickness': 6,
            'BoomLength': 1800,
            'BoomPipeRadius': 24.15,
            'BoomPipeThickness': 5,
            'VaneThickness': 9,
            'VaneLength': 1200,
            'VaneWidth': 900,
            'Offset': 500
        },
        'User': {
            'HubHolesPlacement': 102.5,
            'RotorInnerCircle': 81.5,
            'Holes': 7,
            'MetalLengthL': 65,
            'MetalThicknessL': 8,
            'FlatMetalThickness': 10,
            'YawPipeRadius': 57.15,
            'PipeThickness': 6,
            'ResineRotorMargin': 5,
            'HubHoles': 8,
            'HorizontalPlaneAngle': 55
        }
    }
}


class CreateSpreadsheetTaskPanel:
    def __init__(self,
                 title: str,
                 on_close: Callable[[dict, dict, dict], Any] = None):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.on_close = on_close

        layout = QtGui.QVBoxLayout(self.form)

        # Row 1
        row1 = QtGui.QHBoxLayout()

        label = QtGui.QLabel('<strong>Variant:</strong>', self.form)
        self.combo_box = self.create_combo_box()

        row1.addWidget(label)
        row1.addWidget(self.combo_box)

        layout.addLayout(row1)

        # Row 2
        row2 = QtGui.QHBoxLayout()

        rotor_disk_radius_label = QtGui.QLabel(
            '<strong>Rotor Disk Radius:</strong>', self.form)
        self.rotor_disk_radius_value = self.create_rotor_disk_radius_value()

        row2.addWidget(rotor_disk_radius_label)
        row2.addWidget(self.rotor_disk_radius_value)

        layout.addLayout(row2)

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
        if self.on_close:
            self.on_close(parameters['MagnAFPM'],
                          parameters['OpenFurl'],
                          parameters['User'])
        Gui.Control.closeDialog()


def get_rotor_disk_radius(variant):
    return str(parameters_by_variant[variant]['MagnAFPM']['RotorDiskRadius'])
