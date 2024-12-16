"""
Task panel to load wind turbine or related tools based on preset values.
"""
import json
from typing import Tuple

import FreeCADGui as Gui
from PySide import QtCore, QtGui

from ..get_default_parameters import get_default_parameters, get_presets
from ..load import Assembly, load_all, load_assembly
from ..loadmat import loadmat
from ..map_magnafpm_parameters import map_magnafpm_parameters
from ..wind_turbine_shape import (WindTurbineShape,
                                  map_rotor_disk_radius_to_wind_turbine_shape)

__all__ = ['LoadAssemblyTaskPanel']

ALL = 'All'
DEFAULT_PRESET = WindTurbineShape.T.value


class QHLine(QtGui.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class LoadAssemblyTaskPanel:
    def __init__(self, title: str):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.selected_assembly = Assembly.WIND_TURBINE

        layout = QtGui.QVBoxLayout(self.form)

        rows = [
            {
                'label': '<strong>Assembly:</strong>',
                'value': self.create_assembly_combo_box(),
                'value_field_name': 'assembly_combo_box'
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

        divider_layout = QtGui.QHBoxLayout()
        h_line = QHLine()
        divider_layout.addWidget(h_line)
        layout.addLayout(divider_layout)

        simulation_label_layout = QtGui.QHBoxLayout()
        simulation_label = QtGui.QLabel('<strong>Simulation:</strong>', self.form)
        self.simulation_value = QtGui.QLabel('', self.form)
        self.simulation_value.setAlignment(QtCore.Qt.AlignVCenter)
        self.simulation_value.setWordWrap(True)
        simulation_label_layout.addWidget(simulation_label)
        simulation_label_layout.addWidget(self.simulation_value)
        layout.addLayout(simulation_label_layout)

        select_button_description_label_layout = QtGui.QHBoxLayout()
        select_button_description_label = QtGui.QLabel(
            'Optionally select a MagnAFPM simulation file (.mat) to be merged into selected preset or JSON file.', self.form)
        select_button_description_label.setWordWrap(True)
        select_button_description_label_layout.addWidget(select_button_description_label)
        layout.addLayout(select_button_description_label_layout)

        simulation_button_layout = QtGui.QHBoxLayout()
        self.simulation_button_label = 'Select'
        self.simulation_button = QtGui.QPushButton(self.simulation_button_label)
        self.simulation_button.clicked.connect(self.select_simulation_file)
        simulation_button_layout.addWidget(self.simulation_button)
        layout.addLayout(simulation_button_layout)

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
        combo_box.currentTextChanged[str].connect(
            self.handle_preset_combo_box_current_text_changed)
        return combo_box

    def handle_preset_combo_box_current_text_changed(self, selected_preset: str):
        turbine_value_text = get_turbine_value_text(selected_preset)
        description = get_description(selected_preset)
        self.turbine_value.setText(turbine_value_text)
        self.description_value.setText(description)

    def create_assembly_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        items = [assembly.value for assembly in list(Assembly)]
        items.append(ALL)
        combo_box.addItems(items)
        return combo_box

    def select_simulation_file(self):
        if self.simulation_value.text() == '':
            filepath, _ = QtGui.QFileDialog.getOpenFileName(
                self.form, 'Open file', '', 'MagnAFPM simulation or JSON file (*.mat *.json)')
            self.simulation_value.setText(filepath)
            if filepath.endswith('.json'):
                with open(filepath) as f:
                    parameters = json.load(f)
                    preset = parameters['preset']
                    self.preset_combo_box.setCurrentIndex(self.preset_combo_box.findText(preset))
            self.simulation_button.setText('Clear')
        else:
            self.simulation_value.setText('')
            self.simulation_button.setText(self.simulation_button_label)

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        preset = self.preset_combo_box.currentText()
        parameters = get_default_parameters(preset)
        assembly_text = self.assembly_combo_box.currentText()
        magnafpm_parameters = parameters['magnafpm']
        furling_parameters = parameters['furling']
        user_parameters = parameters['user']
        simulation_filepath = self.simulation_value.text()
        if simulation_filepath != '':
            if simulation_filepath.endswith('.mat'):
                magnafpm_parameters = map_magnafpm_parameters(loadmat(simulation_filepath))
            else: # .json
                with open(simulation_filepath) as f:
                    parameters = json.load(f)
                    magnafpm_parameters = parameters['magnafpm']
                    furling_parameters = parameters['furling']
                    user_parameters = parameters['user']

        if assembly_text == ALL:
            load_all(magnafpm_parameters,
                     furling_parameters,
                     user_parameters)
        else:
            assembly = Assembly(assembly_text)
            load_assembly(assembly,
                          magnafpm_parameters,
                          furling_parameters,
                          user_parameters)
        Gui.Control.closeDialog()


def get_turbine_value_text(preset: str) -> str:
    rotor_diameter, rotor_disk_radius = get_rotor_diameter_and_rotor_disk_radius(
        preset)
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    return f'{rotor_diameter / 1000:g}m diameter {wind_turbine_shape.value}'


def get_rotor_diameter_and_rotor_disk_radius(preset: str) -> Tuple[float, float]:
    parameters = get_default_parameters(preset)
    magnafpm = parameters['magnafpm']
    return magnafpm['RotorDiameter'], magnafpm['RotorDiskRadius']


def get_description(preset: str) -> str:
    parameters = get_default_parameters(preset)
    return parameters['description']
