"""
Task panel to load wind turbine or related tools based on preset values.
"""
from typing import Tuple

import FreeCADGui as Gui
from PySide import QtCore, QtGui

from ..get_default_parameters import get_default_parameters, get_presets
from ..load import Assembly, load_all, load_assembly
from ..wind_turbine_shape import (WindTurbineShape,
                                  map_rotor_disk_radius_to_wind_turbine_shape)

__all__ = ['LoadAssemblyTaskPanel']

ALL = 'All'
DEFAULT_PRESET = WindTurbineShape.T.value


class LoadAssemblyTaskPanel:
    def __init__(self, title: str):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.selected_assembly = Assembly.WIND_TURBINE

        layout = QtGui.QVBoxLayout(self.form)

        rows = [
            {
                'label': '<strong>Load:</strong>',
                'value': self.create_load_combo_box(),
                'value_field_name': 'load_combo_box'
            },
            {
                'label': '<strong>Preset:</strong>',
                'value': self.create_preset_combo_box(),
                'value_field_name': 'preset_combo_box'
            },
            {
                'label': '<strong>Turbine:</strong>',
                'value': self.create_turbine_value(),
                'value_field_name': 'turbine_value'
            }
        ]

        for row in rows:
            horizontal_layout = QtGui.QHBoxLayout()

            label = QtGui.QLabel(row['label'], self.form)
            setattr(self, row['value_field_name'], row['value'])

            horizontal_layout.addWidget(label)
            horizontal_layout.addWidget(row['value'])

            layout.addLayout(horizontal_layout)

        description_label_layout = QtGui.QHBoxLayout()
        description_label = QtGui.QLabel('<strong>Description:</strong>', self.form)
        description_label_layout.addWidget(description_label)
        layout.addLayout(description_label_layout)

        description_value_layout = QtGui.QHBoxLayout()
        self.description_value = self.create_description_value()
        description_value_layout.addWidget(self.description_value)
        layout.addLayout(description_value_layout)

    def create_turbine_value(self):
        default_text = get_turbine_value_text(DEFAULT_PRESET)
        label = QtGui.QLabel(default_text, self.form)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return label

    def create_description_value(self):
        description = get_description(DEFAULT_PRESET)
        label = QtGui.QLabel(description, self.form)
        label.setWordWrap(True)
        return label

    def create_preset_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        items = get_presets()
        combo_box.addItems(items)
        combo_box.activated[str].connect(
            self.handle_preset_combo_box_activated)
        return combo_box

    def handle_preset_combo_box_activated(self, selected_preset: str):
        turbine_value_text = get_turbine_value_text(selected_preset)
        description = get_description(selected_preset)
        self.turbine_value.setText(turbine_value_text)
        self.description_value.setText(description)

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


def get_turbine_value_text(preset: str) -> str:
    rotor_diameter, rotor_disk_radius = get_rotor_diameter_and_rotor_disk_radius(
        preset)
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    return f'{rotor_diameter / 1000}m diameter {wind_turbine_shape.value}'


def get_rotor_diameter_and_rotor_disk_radius(preset: str) -> Tuple[float, float]:
    parameters = get_default_parameters(preset)
    magnafpm = parameters['magnafpm']
    return magnafpm['RotorDiameter'], magnafpm['RotorDiskRadius']


def get_description(preset: str) -> str:
    parameters = get_default_parameters(preset)
    return parameters['description']
