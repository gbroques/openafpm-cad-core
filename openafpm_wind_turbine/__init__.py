import os
from abc import ABC

import FreeCAD as App
from FreeCAD import Vector, Placement
import importWebGL

from .alternator import make_alternator
from .hub import make_hub
from .master_of_puppets import create_master_of_puppets

# T Shape
# =======
rotor_radius = 130
rotor_inner_circle = 25
hub_holes_placement = 44
magnet_length = 46

# H Shape
# =======
# rotor_radius = 230
# rotor_inner_circle = 47.5
# hub_holes_placement = 78
# magnet_length = 46

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

furling_tool_parameters = {
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
    'Offset': 400,
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
        user_parameters,
        furling_tool_parameters)
    master_of_puppets_doc.recompute()

    wind_turbine = create_wind_turbine(magn_afpm_parameters)
    wind_turbine.render()


class WindTurbine(ABC):
    def __init__(self,
                 magn_afpm_parameters,
                 base_dir,
                 has_separate_master_files,
                 distance_between_stator_and_rotor):
        self.magn_afpm_parameters = magn_afpm_parameters
        self.has_separate_master_files = has_separate_master_files
        self.distance_between_stator_and_rotor = distance_between_stator_and_rotor

        self.base_path = os.path.join(
            os.path.dirname(__file__), 'documents', base_dir)
        self.doc = App.newDocument('WindTurbine')

    def render(self):
        if not self.has_separate_master_files:
            _open_master(self.base_path)

        alternator_name = 'Alternator'
        alternator = make_alternator(
            self.base_path,
            self.has_separate_master_files,
            self.doc,
            alternator_name,
            self.magn_afpm_parameters['CoilInnerWidth1'],
            self.magn_afpm_parameters['DiskThickness'],
            self.magn_afpm_parameters['MagnetThickness'],
            self.distance_between_stator_and_rotor)

        hub_name = 'Hub'
        hub = make_hub(self.base_path, self.doc, hub_name)
        stator_thickness = self.magn_afpm_parameters['CoilInnerWidth1']
        flange_bottom_pad_length = 30
        stator_resin_cast_thickness = (
            self.magn_afpm_parameters['DiskThickness'] +
            self.magn_afpm_parameters['MagnetThickness']
        )
        hub_z_offset = (
            (stator_thickness / 2) +
            flange_bottom_pad_length +
            stator_resin_cast_thickness +
            self.distance_between_stator_and_rotor
        )
        placement = Placement()
        placement.move(Vector(0, 0, hub_z_offset))
        hub.Placement = placement

        self.doc.recompute()
        objects = [
            alternator,
            hub
        ]
        importWebGL.export(objects, 'wind-turbine-webgl.html')


def _open_master(base_path):
    App.openDocument(os.path.join(
        base_path, 'MasterBigWindturbine.FCStd'))


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         base_dir='t_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=30)


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         base_dir='h_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=36)


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters,
                         base_dir='star_shape',
                         has_separate_master_files=False,
                         distance_between_stator_and_rotor=45)


def create_wind_turbine(magn_afpm_parameters):
    rotor_radius = magn_afpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(magn_afpm_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(magn_afpm_parameters)
    else:
        return StarShapeWindTurbine(magn_afpm_parameters)
