import os
from abc import ABC

import FreeCAD as App
import importWebGL

from .make_alternator import make_alternator
from .master_of_puppets import create_master_of_puppets

# T Shape
# =======
# rotor_radius = 130
# rotor_inner_circle = 25
# hub_holes_placement = 44
# magnet_length = 46

# H Shape
# =======
rotor_radius = 230
rotor_inner_circle = 47.5
hub_holes_placement = 78
magnet_length = 46

# Star Shape
# ==========
# rotor_radius = 349
# rotor_inner_circle = 81.5
# hub_holes_placement = 102.5
# magnet_length = 58

magn_afpm_parameters = {
    'RotorDiskRadius': rotor_radius,
    'DiskThickness': 10,
    'MagnetLength': magnet_length,
    'MagnetWidth': 30,
    'MagnetThickness': 10,
    'NumberMagnet': 12,
    'StatorThickness': 13,
    'CoilLegWidth': 23.26,
    'CoilInnerWidth1': 30,
    'CoilInnerWidth2': 30
}

user_parameters = {
    # Distance of holes from center
    'HubHolesPlacement': hub_holes_placement,
    'RotorInnerCircle': rotor_inner_circle,
    'Holes': 7,
    'MetalLengthL': 80,
    'MetalThicknessL': 8,
    'FlatMetalThickness': 10,
    'YawPipeRadius': 58.15,
    'PipeThickness': 6,
    'ResineRotorMargin': 5,
    'HubHoles': 10
}


def main():
    master_of_puppets_doc_name = 'Master of Puppets'
    imported_spreadsheet_name = 'Spreadsheet001'
    master_spreadsheet_name = 'Spreadsheet'
    master_of_puppets_doc = create_master_of_puppets(
        master_of_puppets_doc_name,
        imported_spreadsheet_name,
        master_spreadsheet_name,
        magn_afpm_parameters,
        user_parameters)
    master_of_puppets_doc.recompute()

    wind_turbine = create_wind_turbine(magn_afpm_parameters)
    wind_turbine.render()


class WindTurbine(ABC):
    def __init__(self,
                 magn_afpm_parameters,
                 base_dir,
                 has_separate_master_files,
                 stator_resin_cast_name,
                 rotor_disc1_name):
        self.magn_afpm_parameters = magn_afpm_parameters
        self.has_separate_master_files = has_separate_master_files
        self.stator_resin_cast_name = stator_resin_cast_name
        self.rotor_disc1_name = rotor_disc1_name

        self.base_path = os.path.join(
            os.path.dirname(__file__), 'documents', base_dir)
        self.doc = App.newDocument('WindTurbine')

    def render(self):
        alternator_name = 'Alternator'
        make_alternator(self.base_path,
                        self.has_separate_master_files,
                        self.doc,
                        alternator_name,
                        self.stator_resin_cast_name,
                        self.rotor_disc1_name,
                        magn_afpm_parameters['CoilInnerWidth1'],
                        magn_afpm_parameters['DiskThickness'],
                        magn_afpm_parameters['MagnetThickness'])
        self.doc.recompute()
        self._export_to_webgl(alternator_name)

    def _export_to_webgl(self, alternator_name):
        objects = [
            self.doc.getObject(alternator_name),
        ]
        importWebGL.export(objects, 'wind-turbine-webgl.html')


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         't_shape',
                         True,
                         'Pad',
                         'Pocket001Body')


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         'h_shape',
                         True,
                         'Pad',
                         'Pocket001Body')


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         'star_shape',
                         False,
                         'Body',
                         'Body001')


def create_wind_turbine(magn_afpm_parameters):
    rotor_radius = magn_afpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(magn_afpm_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(magn_afpm_parameters)
    else:
        return StarShapeWindTurbine(magn_afpm_parameters)
