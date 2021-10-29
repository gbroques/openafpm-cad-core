"""
FreeCAD macro to create wind turbine document
with spreadsheet containing input parameters.
"""
from typing import Any, Callable

import FreeCADGui as Gui
from PySide import QtGui
import FreeCAD as App
import os
import tempfile
from pathlib import Path
from .get_default_parameters import get_default_parameters
from .wind_turbine import WindTurbine

__all__ = ['CreateSpreadsheetTaskPanel']


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

        # Row 3
        row3 = QtGui.QHBoxLayout()
        save_as_label = QtGui.QLabel(
            '<strong>Save As:</strong>', self.form)
        row3.addWidget(save_as_label)
        layout.addLayout(row3)

        # Row 4
        row4 = QtGui.QHBoxLayout()
        self.save_as_location_label = QtGui.QLabel('', self.form)
        self.tempfile = tempfile.tempdir + os.path.sep + 'freecad-last-save-location'
        if os.path.exists(self.tempfile):
            with open(self.tempfile) as f:
                self.save_as = f.read()
                self.set_save_as_location_label()
        row4.addWidget(self.save_as_location_label)
        layout.addLayout(row4)

        # Row 5
        row5 = QtGui.QHBoxLayout()
        save_as_button = QtGui.QPushButton(
            'Save As')
        save_as_button.clicked.connect(self.handle_save_as)
        row5.addWidget(save_as_button)

        layout.addLayout(row5)

    def handle_save_as(self):
        save_as = QtGui.QFileDialog.getSaveFileName(
            None,
            'Save As',
            App.ConfigGet('UserAppData') + os.path.sep + 'Mod',
            'FreeCAD Document (*.FCStd)')
        path, pattern = save_as
        self.save_as = path
        self.set_save_as_location_label()
        with open(self.tempfile, 'w') as f:
            f.write(self.save_as)

    def set_save_as_location_label(self):
        label = self.save_as.replace(str(Path.home()), '~')

        path_parts = label.split(os.path.sep)
        middle_parts = list(map(lambda _: '..', path_parts[1:-2]))
        truncated_path_parts = [path_parts[0]] + middle_parts + path_parts[-2:]
        truncated_path = os.path.sep.join(truncated_path_parts)

        self.save_as_location_label.setText(truncated_path)
        self.save_as_location_label.setToolTip(label)

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

    def handle_combo_box_activated(self, selected_variant: str):
        selected_wind_turbine = WindTurbine(selected_variant)
        selected_rotor_disk_radius = get_rotor_disk_radius(
            selected_wind_turbine)
        self.rotor_disk_radius_value.setText(selected_rotor_disk_radius)

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        variant = WindTurbine(self.combo_box.currentText())
        parameters = get_default_parameters(variant)
        if self.on_close:
            document = self.on_close(parameters['magnafpm'],
                                     parameters['furling'],
                                     parameters['user'])
            if hasattr(self, 'save_as') and self.save_as:
                document.saveAs(self.save_as)
                App.Console.PrintMessage(f'Saved document as {self.save_as}')
        Gui.Control.closeDialog()


def get_rotor_disk_radius(variant: WindTurbine):
    parameters = get_default_parameters(variant)
    return str(parameters['magnafpm']['RotorDiskRadius'])
