import os
from abc import ABC, abstractmethod

import Draft
import FreeCAD as App
import importWebGL
import Part
from FreeCAD import Placement, Vector, Rotation

from .alternator import make_alternator
from .hub import make_hub
from .master_of_puppets import create_master_of_puppets
from .common import make_compound

# T Shape
# =======
rotor_radius = 130
rotor_inner_circle = 32.5
hub_holes_placement = 50
magnet_length = 46
hub_holes = 6
holes = 6
hub_rod_length = 330

# H Shape
# =======
# rotor_radius = 230
# rotor_inner_circle = 47.5
# hub_holes_placement = 65
# magnet_length = 46
# hub_holes = 7
# holes = 6
# hub_rod_length = 250

# Star Shape
# ==========
# rotor_radius = 349
# rotor_inner_circle = 81.5
# hub_holes_placement = 102.5
# magnet_length = 58
# hub_holes = 8
# holes = 7
# hub_rod_length = 270

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
    # Distance between center of hub hole and center of alternator
    'HubHolesPlacement': hub_holes_placement,
    'RotorInnerCircle': rotor_inner_circle,
    'Holes': holes,  # Radius of outer holes on stator
    'MetalLengthL': 80,
    'MetalThicknessL': 8,
    'FlatMetalThickness': 10,
    'YawPipeRadius': 58.15,
    'PipeThickness': 6,
    'ResineRotorMargin': 5,
    'HubHoles': hub_holes  # Radius of hub holes
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

    wind_turbine = create_wind_turbine(magn_afpm_parameters, user_parameters)
    wind_turbine.render()


class WindTurbine(ABC):
    def __init__(self,
                 magn_afpm_parameters,
                 user_parameters,
                 base_dir,
                 has_separate_master_files,
                 distance_between_stator_and_rotor,
                 flange_bottom_pad_length,
                 flange_top_pad_length,
                 number_of_hub_holes):
        self.magn_afpm_parameters = magn_afpm_parameters
        self.user_parameters = user_parameters
        self.has_separate_master_files = has_separate_master_files
        self.distance_between_stator_and_rotor = distance_between_stator_and_rotor
        self.flange_bottom_pad_length = flange_bottom_pad_length
        self.flange_top_pad_length = flange_top_pad_length
        self.number_of_hub_holes = number_of_hub_holes

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
        hub = make_hub(
            self.base_path,
            self.doc,
            hub_name,
            self.flange_top_pad_length)
        self._move_hub(hub)
        hub_z_offset = self.calculate_hub_z_offset()
        middle_flange_pad_thickness = 15
        thread_z_offset = hub_z_offset + middle_flange_pad_thickness
        threads = create_threads(self.doc,
                                 self.user_parameters['HubHoles'],
                                 hub_rod_length,
                                 self.number_of_hub_holes,
                                 self.user_parameters['HubHolesPlacement'],
                                 thread_z_offset)
        thread_compound = make_compound(self.doc, 'Threads', threads)
        self.doc.recompute()
        objects = [
            alternator,
            hub,
            thread_compound
        ]
        importWebGL.export(objects, 'wind-turbine-webgl.html')

    def _move_hub(self, hub):
        hub_z_offset = self.calculate_hub_z_offset()
        placement = Placement()
        placement.move(Vector(0, 0, hub_z_offset))
        hub.Placement = placement

    @abstractmethod
    def calculate_hub_z_offset(self):
        raise NotImplementedError(
            'Sub class must implement calculate_hub_z_offset.')


def _open_master(base_path):
    App.openDocument(os.path.join(
        base_path, 'MasterBigWindturbine.FCStd'))


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         base_dir='t_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=30,
                         flange_bottom_pad_length=30,
                         flange_top_pad_length=30,
                         number_of_hub_holes=4)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magn_afpm_parameters['CoilInnerWidth1'],
            self.magn_afpm_parameters['DiskThickness'],
            self.magn_afpm_parameters['MagnetThickness'],
            self.flange_bottom_pad_length,
            self.distance_between_stator_and_rotor
        )


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         base_dir='h_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=36,
                         flange_bottom_pad_length=15,
                         flange_top_pad_length=30,
                         number_of_hub_holes=5)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magn_afpm_parameters['CoilInnerWidth1'],
            self.magn_afpm_parameters['DiskThickness'],
            self.magn_afpm_parameters['MagnetThickness'],
            self.flange_bottom_pad_length,
            self.distance_between_stator_and_rotor
        )


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         base_dir='star_shape',
                         has_separate_master_files=False,
                         distance_between_stator_and_rotor=45,
                         flange_bottom_pad_length=45,
                         flange_top_pad_length=40,
                         number_of_hub_holes=6)

    def calculate_hub_z_offset(self):
        stator_thickness = self.magn_afpm_parameters['CoilInnerWidth1']
        return (
            (stator_thickness / 2) +
            self.flange_bottom_pad_length +
            self.distance_between_stator_and_rotor
        )


def create_wind_turbine(magn_afpm_parameters, user_parameters):
    rotor_radius = magn_afpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(magn_afpm_parameters, user_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(magn_afpm_parameters, user_parameters)
    else:
        return StarShapeWindTurbine(magn_afpm_parameters, user_parameters)


def calculate_hub_z_offset(coil_inner_width1,
                           disk_thickness,
                           magnet_thickness,
                           flange_bottom_pad_length,
                           distance_between_stator_and_rotor):
    stator_thickness = coil_inner_width1
    rotor_resin_cast_thickness = (
        disk_thickness +
        magnet_thickness
    )
    return (
        (stator_thickness / 2) +
        flange_bottom_pad_length +
        rotor_resin_cast_thickness +
        distance_between_stator_and_rotor
    )


def create_threads(document, radius, length, n, hub_holes_placement, z_offset):
    thread = document.addObject('Part::Cylinder', 'Thread')
    thread.Placement = Placement(
        Vector(0, 0, z_offset), Rotation(Vector(0, 1, 0), 180))
    thread.Radius = radius
    thread.Height = length
    return create_polar_array(thread, n, hub_holes_placement)


def create_polar_array(part, n, y_offset):
    array = [part]
    Draft.move(part, Vector(0, y_offset, 0))
    exterior_angle = calculate_exterior_angle(n)
    App.DraftWorkingPlane.alignToPointAndAxis(
        Vector(0, 0, 0), Vector(0, 0, 1), 0)
    previous = part
    for i in range(n - 1):
        clone = Draft.clone(previous)
        Draft.rotate(clone, exterior_angle, Vector(
            0, 0, 0), axis=Vector(0, 0, 1), copy=False)
        array.append(clone)
        previous = clone
    return array


def calculate_exterior_angle(n):
    """
    Calculate exterior angle for an "n" sided regular polygon.

    Reference:
    https://www.mathsisfun.com/geometry/regular-polygons.html
    """
    return 360 / n
