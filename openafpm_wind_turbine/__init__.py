import os
from abc import ABC, abstractmethod

import Draft
import FreeCAD as App
import importWebGL
import Part
from FreeCAD import Placement, Rotation, Vector

from .alternator import make_alternator
from .common import make_compound
from .frame import make_frame
from .h_shape_frame import (assemble_h_shape_frame,
                            calculate_h_channel_section_height)
from .hub import make_hub
from .hub_threads import make_hub_threads
from .master_of_puppets import create_master_of_puppets
from .t_shape_frame import (assemble_t_shape_frame,
                            calculate_t_channel_section_height)

# T Shape
# =======
rotor_radius = 130
rotor_inner_circle = 32.5
hub_holes_placement = 50
magnet_length = 46
hub_holes = 6
holes = 6
hub_rod_length = 330
metal_length_l = 50
metal_thickness_l = 6
yaw_pipe_radius = 30.15

# H Shape
# =======
# rotor_radius = 230
# rotor_inner_circle = 47.5
# hub_holes_placement = 65
# magnet_length = 46
# hub_holes = 7
# holes = 6
# hub_rod_length = 250
# metal_length_l = 50
# metal_thickness_l = 6
# yaw_pipe_radius = 44.5

# Star Shape
# ==========
# rotor_radius = 349
# rotor_inner_circle = 81.5
# hub_holes_placement = 102.5
# magnet_length = 58
# hub_holes = 8
# holes = 7
# hub_rod_length = 270
# metal_length_l = 65
# metal_thickness_l = 8
# yaw_pipe_radius = 57.15

"""
T Shape Frame

  A
BC BC
  D
"""

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
    'MetalLengthL': metal_length_l,
    'MetalThicknessL': metal_thickness_l,
    'FlatMetalThickness': 10,
    'YawPipeRadius': yaw_pipe_radius,
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

    wind_turbine = create_wind_turbine(
        magn_afpm_parameters, user_parameters, furling_tool_parameters)
    wind_turbine.render()


class WindTurbine(ABC):
    def __init__(self,
                 magn_afpm_parameters,
                 user_parameters,
                 furling_tool_parameters,
                 base_dir,
                 has_separate_master_files,
                 distance_between_stator_and_rotor,
                 flange_bottom_pad_length,
                 flange_top_pad_length,
                 number_of_hub_holes,
                 assemble_frame):
        self.magn_afpm_parameters = magn_afpm_parameters
        self.user_parameters = user_parameters
        self.furling_tool_parameters = furling_tool_parameters
        self.has_separate_master_files = has_separate_master_files
        self.distance_between_stator_and_rotor = distance_between_stator_and_rotor
        self.flange_bottom_pad_length = flange_bottom_pad_length
        self.flange_top_pad_length = flange_top_pad_length
        self.number_of_hub_holes = number_of_hub_holes
        self.assemble_frame = assemble_frame

        self.base_path = os.path.join(
            os.path.dirname(__file__), 'documents', base_dir)
        self.doc = App.newDocument('WindTurbine')

    def render(self):
        if not self.has_separate_master_files:
            _open_master(self.base_path)

        # alternator_name = 'Alternator'
        # alternator = make_alternator(
        #     self.base_path,
        #     self.has_separate_master_files,
        #     self.doc,
        #     alternator_name,
        #     self.magn_afpm_parameters['CoilInnerWidth1'],
        #     self.magn_afpm_parameters['DiskThickness'],
        #     self.magn_afpm_parameters['MagnetThickness'],
        #     self.distance_between_stator_and_rotor)

        # hub_name = 'Hub'
        # hub = make_hub(
        #     self.base_path,
        #     self.doc,
        #     hub_name,
        #     self.flange_top_pad_length)
        # self._move_hub(hub)
        # hub_z_offset = self.calculate_hub_z_offset()
        # middle_flange_pad_thickness = 15
        # thread_z_offset = hub_z_offset + middle_flange_pad_thickness
        # threads_name = 'Threads'
        # threads = make_hub_threads(self.doc,
        #                            threads_name,
        #                            self.user_parameters['HubHoles'],
        #                            hub_rod_length,
        #                            self.number_of_hub_holes,
        #                            self.user_parameters['HubHolesPlacement'],
        #                            thread_z_offset)
        frame = make_frame(
            self.base_path,
            self.has_separate_master_files,
            self.doc,
            self.assemble_frame,
            self.user_parameters['MetalLengthL'],
            self.calculate_channel_section_height())
        self.doc.recompute()
        # objects = [
        #     alternator,
        #     hub,
        #     threads
        # ]
        # importWebGL.export(objects, 'wind-turbine-webgl.html')

    def _move_hub(self, hub):
        hub_z_offset = self.calculate_hub_z_offset()
        placement = Placement()
        placement.move(Vector(0, 0, hub_z_offset))
        hub.Placement = placement

    @abstractmethod
    def calculate_hub_z_offset(self):
        raise NotImplementedError(
            'Sub class must implement calculate_hub_z_offset.')

    @abstractmethod
    def calculate_channel_section_height(self):
        raise NotImplementedError(
            'Sub class must implement calculate_channel_section_height.')


def _open_master(base_path):
    App.openDocument(os.path.join(
        base_path, 'MasterBigWindturbine.FCStd'))


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters, furling_tool_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         furling_tool_parameters,
                         base_dir='t_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=30,
                         flange_bottom_pad_length=30,
                         flange_top_pad_length=30,
                         number_of_hub_holes=4,
                         assemble_frame=assemble_t_shape_frame)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magn_afpm_parameters['CoilInnerWidth1'],
            self.magn_afpm_parameters['DiskThickness'],
            self.magn_afpm_parameters['MagnetThickness'],
            self.flange_bottom_pad_length,
            self.distance_between_stator_and_rotor
        )

    def calculate_channel_section_height(self):
        return calculate_t_channel_section_height(
            self.magn_afpm_parameters['RotorDiskRadius'],
            self.magn_afpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalThicknessL'],
            self.user_parameters['YawPipeRadius'],
            self.furling_tool_parameters['Offset']
        )


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters, furling_tool_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         furling_tool_parameters,
                         base_dir='h_shape',
                         has_separate_master_files=True,
                         distance_between_stator_and_rotor=36,
                         flange_bottom_pad_length=15,
                         flange_top_pad_length=30,
                         number_of_hub_holes=5,
                         assemble_frame=assemble_h_shape_frame)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magn_afpm_parameters['CoilInnerWidth1'],
            self.magn_afpm_parameters['DiskThickness'],
            self.magn_afpm_parameters['MagnetThickness'],
            self.flange_bottom_pad_length,
            self.distance_between_stator_and_rotor
        )

    def calculate_channel_section_height(self):
        return calculate_h_channel_section_height(
            self.magn_afpm_parameters['RotorDiskRadius'],
            self.magn_afpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalLengthL'],
        )


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters, user_parameters, furling_tool_parameters):
        super().__init__(magn_afpm_parameters,
                         user_parameters,
                         furling_tool_parameters,
                         base_dir='star_shape',
                         has_separate_master_files=False,
                         distance_between_stator_and_rotor=45,
                         flange_bottom_pad_length=45,
                         flange_top_pad_length=40,
                         number_of_hub_holes=6,
                         assemble_frame=assemble_t_shape_frame)

    def calculate_hub_z_offset(self):
        stator_thickness = self.magn_afpm_parameters['CoilInnerWidth1']
        return (
            (stator_thickness / 2) +
            self.flange_bottom_pad_length +
            self.distance_between_stator_and_rotor
        )

    def calculate_channel_section_height(self):
        return calculate_h_channel_section_height(
            self.magn_afpm_parameters['RotorDiskRadius'],
            self.magn_afpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalLengthL'],
        )


def create_wind_turbine(magn_afpm_parameters, user_parameters, furling_tool_parameters):
    rotor_radius = magn_afpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(
            magn_afpm_parameters, user_parameters, furling_tool_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(
            magn_afpm_parameters, user_parameters, furling_tool_parameters)
    else:
        return StarShapeWindTurbine(
            magn_afpm_parameters, user_parameters, furling_tool_parameters)


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
