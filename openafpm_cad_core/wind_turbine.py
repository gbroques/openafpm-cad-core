import os
from abc import ABC, abstractmethod

import Draft
import FreeCAD as App
import Part
from FreeCAD import Placement, Rotation, Vector

from . import importObj as importOBJ
from .alternator import make_alternator
from .coil import make_coils
from .common import make_compound
from .frame import make_frame
from .h_shape_frame import (assemble_h_shape_frame,
                            calculate_h_channel_section_height)
from .hub import make_hub
from .hub_threads import make_hub_threads
from .magnet import make_rotor_magnets
from .star_shape_frame import (assemble_star_shape_frame,
                               calculate_star_channel_section_height)
from .t_shape_frame import (
    assemble_t_shape_frame, calculate_t_channel_section_height,
    distance_between_stub_axle_shaft_and_tail_hinge_end_bracket)

__all__ = ['create_wind_turbine']


def create_wind_turbine(magnafpm_parameters, user_parameters, furling_parameters):
    rotor_radius = magnafpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(
            magnafpm_parameters, user_parameters, furling_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(
            magnafpm_parameters, user_parameters, furling_parameters)
    else:
        return StarShapeWindTurbine(
            magnafpm_parameters, user_parameters, furling_parameters)


class WindTurbine(ABC):
    def __init__(self,
                 magnafpm_parameters,
                 user_parameters,
                 furling_parameters,
                 base_dir,
                 has_separate_master_files,
                 flange_top_pad_length,
                 flange_bottom_pad_length,
                 number_of_hub_holes,
                 assemble_frame,
                 hub_rod_length):
        self.magnafpm_parameters = magnafpm_parameters
        self.user_parameters = user_parameters
        self.furling_parameters = furling_parameters
        self.has_separate_master_files = has_separate_master_files
        self.flange_top_pad_length = flange_top_pad_length
        self.flange_bottom_pad_length = flange_bottom_pad_length
        self.number_of_hub_holes = number_of_hub_holes
        self.assemble_frame = assemble_frame
        self.hub_rod_length = hub_rod_length

        documents_path = os.path.join(
            os.path.dirname(__file__), 'documents')
        self.common_path = os.path.join(documents_path, 'common')
        self.base_path = os.path.join(documents_path, base_dir)
        self.doc = App.newDocument('WindTurbine')

    def to_obj(self):
        if not self.has_separate_master_files:
            _open_master(self.base_path)

        App.setActiveDocument(self.doc.Name)
        magnets = make_rotor_magnets(
            self.doc,
            self.magnafpm_parameters['MagnetLength'],
            self.magnafpm_parameters['MagnetWidth'],
            self.magnafpm_parameters['MagnetThickness'],
            self.magnafpm_parameters['NumberMagnet'],
            self.magnafpm_parameters['RotorDiskRadius'])

        alternator_name = 'Alternator'
        # T Shape, number of coils = RotorRadius <= 125 ? 6 : 9
        number_of_coils = round(
            self.magnafpm_parameters['NumberMagnet'] * 0.75)
        inner_stator_hole_radius = (
            self.magnafpm_parameters['RotorDiskRadius'] -
            self.magnafpm_parameters['MagnetLength'] -
            self.magnafpm_parameters['CoilLegWidth']
        )
        coils = make_coils(self.common_path, self.doc,
                           number_of_coils, inner_stator_hole_radius)
        alternator = make_alternator(
            self.base_path,
            self.has_separate_master_files,
            self.doc,
            alternator_name,
            self.magnafpm_parameters['StatorThickness'],
            self.magnafpm_parameters['DiskThickness'],
            self.magnafpm_parameters['MagnetThickness'],
            self.magnafpm_parameters['MechanicalClearance'],
            magnets,
            coils)

        flange_cover_thickness = 10
        middle_flange_pad_thickness = 16

        hub_name = 'Hub'
        stub_axle_shaft_z_offset = (
            self.flange_top_pad_length +
            self.flange_bottom_pad_length +
            middle_flange_pad_thickness +
            flange_cover_thickness
        )
        hub = make_hub(
            self.base_path,
            self.doc,
            hub_name,
            stub_axle_shaft_z_offset)
        self._place_hub(hub)
        hub_z_offset = self.calculate_hub_z_offset()
        thread_z_offset = hub_z_offset + middle_flange_pad_thickness
        threads_name = 'Threads'
        threads = make_hub_threads(self.doc,
                                   threads_name,
                                   self.user_parameters['HubHoles'],
                                   self.hub_rod_length,
                                   self.number_of_hub_holes,
                                   self.user_parameters['HubHolesPlacement'],
                                   thread_z_offset)
        frame = make_frame(
            self.base_path,
            self.has_separate_master_files,
            self.doc,
            self.assemble_frame,
            self.user_parameters['MetalLengthL'],
            self.calculate_channel_section_height())
        # TODO: Should "place_frame" be encapsulated by "make_frame"?
        self.place_frame(frame)

        self.doc.recompute()
        objects = [
            alternator,
            hub,
            threads,
            frame
        ]
        # Rotate model for Three.js
        pl = Placement(Vector(), Rotation(-90, -180, -270))
        place_objects(objects, pl)
        ungrouped = ungroup_objects(objects)
        obj_file_contents = importOBJ.export(ungrouped)
        return obj_file_contents

    def _place_hub(self, hub):
        hub_z_offset = self.calculate_hub_z_offset()
        placement = Placement()
        placement.move(Vector(0, 0, hub_z_offset))
        place_objects(hub.Group, placement)

    @abstractmethod
    def calculate_hub_z_offset(self):
        # TODO: This no longer differs for each subclass
        raise NotImplementedError(
            'Sub class must implement calculate_hub_z_offset.')

    @abstractmethod
    def calculate_channel_section_height(self):
        raise NotImplementedError(
            'Sub class must implement calculate_channel_section_height.')

    @abstractmethod
    def place_frame(self, frame):
        raise NotImplementedError(
            'Sub class must implement place_frame.')


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magnafpm_parameters, user_parameters, furling_parameters):
        super().__init__(magnafpm_parameters,
                         user_parameters,
                         furling_parameters,
                         base_dir='t_shape',
                         has_separate_master_files=True,
                         flange_top_pad_length=40,
                         flange_bottom_pad_length=45,
                         number_of_hub_holes=4,
                         assemble_frame=assemble_t_shape_frame,
                         hub_rod_length=330)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magnafpm_parameters['StatorThickness'],
            self.magnafpm_parameters['DiskThickness'],
            self.magnafpm_parameters['MagnetThickness'],
            self.magnafpm_parameters['MechanicalClearance']
        )

    def calculate_channel_section_height(self):
        return calculate_t_channel_section_height(
            self.magnafpm_parameters['RotorDiskRadius'],
            self.magnafpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalThicknessL'],
            self.user_parameters['YawPipeRadius'],
            self.furling_parameters['Offset']
        )

    def calculate_frame_y_offset(self):
        return -distance_between_stub_axle_shaft_and_tail_hinge_end_bracket(
            self.magnafpm_parameters['RotorDiskRadius'],
            self.user_parameters['MetalThicknessL'],
            self.user_parameters['YawPipeRadius'],
            self.furling_parameters['Offset']
        )

    def place_frame(self, frame):
        x = frame.Placement.Base.x
        y = self.calculate_frame_y_offset()
        z = calculate_frame_z_offset(
            self.calculate_hub_z_offset(),
            self.user_parameters['MetalLengthL'],
            self.user_parameters['MetalThicknessL'])
        vector = Vector(x, -y, z)
        frame.Placement = Placement(vector, Rotation(-180, 0, -90))


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magnafpm_parameters, user_parameters, furling_parameters):
        super().__init__(magnafpm_parameters,
                         user_parameters,
                         furling_parameters,
                         base_dir='h_shape',
                         has_separate_master_files=True,
                         flange_top_pad_length=40,
                         flange_bottom_pad_length=45,
                         number_of_hub_holes=5,
                         assemble_frame=assemble_h_shape_frame,
                         hub_rod_length=250)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magnafpm_parameters['StatorThickness'],
            self.magnafpm_parameters['DiskThickness'],
            self.magnafpm_parameters['MagnetThickness'],
            self.magnafpm_parameters['MechanicalClearance']
        )

    def calculate_channel_section_height(self):
        return calculate_h_channel_section_height(
            self.magnafpm_parameters['RotorDiskRadius'],
            self.magnafpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalLengthL'],
        )

    def place_frame(self, frame):
        x = frame.Placement.Base.x
        y = self.calculate_frame_y_offset()
        z = calculate_frame_z_offset(
            self.calculate_hub_z_offset(),
            self.user_parameters['MetalLengthL'],
            self.user_parameters['MetalThicknessL'])
        vector = Vector(x, y, z)
        frame.Placement = Placement(vector, Rotation(0, 0, -90))

    def calculate_frame_y_offset(self):
        return -self.calculate_channel_section_height() / 2


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magnafpm_parameters, user_parameters, furling_parameters):
        super().__init__(magnafpm_parameters,
                         user_parameters,
                         furling_parameters,
                         base_dir='star_shape',
                         has_separate_master_files=False,
                         flange_top_pad_length=75,
                         flange_bottom_pad_length=85,
                         number_of_hub_holes=6,
                         assemble_frame=assemble_star_shape_frame,
                         hub_rod_length=270)

    def calculate_hub_z_offset(self):
        return calculate_hub_z_offset(
            self.magnafpm_parameters['StatorThickness'],
            self.magnafpm_parameters['DiskThickness'],
            self.magnafpm_parameters['MagnetThickness'],
            self.magnafpm_parameters['MechanicalClearance']
        )

    def calculate_channel_section_height(self):
        return calculate_star_channel_section_height(
            self.magnafpm_parameters['RotorDiskRadius'],
            self.magnafpm_parameters['CoilLegWidth'],
            self.user_parameters['MetalLengthL'],
        )

    def place_frame(self, frame):
        x = frame.Placement.Base.x
        y = self.calculate_frame_y_offset()
        z = calculate_frame_z_offset(
            self.calculate_hub_z_offset(),
            self.user_parameters['MetalLengthL'],
            self.user_parameters['MetalThicknessL'])
        vector = Vector(x, y, z)
        frame.Placement = Placement(vector, Rotation(0, 0, -90))

    def calculate_frame_y_offset(self):
        return -self.calculate_channel_section_height() / 2


def _open_master(base_path):
    App.openDocument(os.path.join(
        base_path, 'MasterBigWindturbine.FCStd'))


def calculate_hub_z_offset(stator_thickness,
                           disk_thickness,
                           magnet_thickness,
                           distance_between_stator_and_rotor):
    rotor_resin_cast_thickness = (
        disk_thickness +
        magnet_thickness
    )
    return (
        (stator_thickness / 2) +
        rotor_resin_cast_thickness +
        distance_between_stator_and_rotor
    )


def calculate_frame_z_offset(hub_z_offset,
                             metal_length_l,
                             metal_thickness_l):
    stub_axle_shaft_top = 14
    return (
        hub_z_offset +
        stub_axle_shaft_top +
        metal_length_l +
        metal_thickness_l
    )


def place_objects(objects, placement):
    for obj in objects:
        if is_object_group(obj):
            place_objects(obj.Group, placement)
        else:
            obj.Placement = placement.multiply(obj.Placement)


def ungroup_objects(objects):
    ungrouped = []
    for obj in objects:
        if is_object_group(obj):
            objs = ungroup_objects(obj.Group)
            ungrouped.extend(objs)
        else:
            ungrouped.append(obj)
    return ungrouped


def is_object_group(obj):
    return obj.TypeId == 'App::DocumentObjectGroup'
