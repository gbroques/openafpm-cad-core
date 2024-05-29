"""
FreeCAD macro to create wind turbine document
with spreadsheet containing input parameters.
"""
import FreeCADGui as Gui
from PySide import QtGui

from ..get_default_parameters import get_default_parameters, get_presets
from ..load import Assembly, load_all, load_assembly
from ..wind_turbine_shape import WindTurbineShape

__all__ = ['CreateSpreadsheetTaskPanel']

ALL = 'All'


class CreateSpreadsheetTaskPanel:
    def __init__(self, title: str):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.selected_assembly = Assembly.WIND_TURBINE

        layout = QtGui.QVBoxLayout(self.form)

        # Row 1
        row1 = QtGui.QHBoxLayout()

        preset_label = QtGui.QLabel('<strong>Preset:</strong>', self.form)
        self.preset_combo_box = self.create_preset_combo_box()

        row1.addWidget(preset_label)
        row1.addWidget(self.preset_combo_box)

        layout.addLayout(row1)

        # Row 2
        row2 = QtGui.QHBoxLayout()

        load_label = QtGui.QLabel('<strong>Load:</strong>', self.form)
        self.load_combo_box = self.create_load_combo_box()

        row2.addWidget(load_label)
        row2.addWidget(self.load_combo_box)

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
        default_preset = WindTurbineShape.T.value
        default_rotor_disk_radius = get_rotor_disk_radius(default_preset)
        return QtGui.QLabel(default_rotor_disk_radius, self.form)

    def create_preset_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        items = get_presets()
        combo_box.addItems(items)
        combo_box.activated[str].connect(
            self.handle_preset_combo_box_activated)
        return combo_box

    def handle_preset_combo_box_activated(self, selected_preset: str):
        selected_rotor_disk_radius = get_rotor_disk_radius(
            selected_preset)
        self.rotor_disk_radius_value.setText(selected_rotor_disk_radius)

    def create_load_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        items = [assembly.value for assembly in list(Assembly)]
        items.append(ALL)
        combo_box.addItems(items)
        return combo_box

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        preset = self.preset_combo_box.currentText()
        parameters = get_default_parameters(preset)
        assembly_text = self.load_combo_box.currentText()
        if assembly_text == ALL:
            load_all(parameters['magnafpm'],
                     parameters['furling'],
                     parameters['user'])
        else:
            assembly = Assembly(assembly_text)
            load_assembly(assembly,
                          parameters['magnafpm'],
                          parameters['furling'],
                          parameters['user'])
        Gui.Control.closeDialog()


def get_rotor_disk_radius(preset: str) -> str:
    parameters = get_default_parameters(preset)
    return str(parameters['magnafpm']['RotorDiskRadius'])
