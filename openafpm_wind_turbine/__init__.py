import FreeCAD as App
import FreeCADGui as Gui
from .master_of_puppets import create_master_of_puppets
import os
import importWebGL
from abc import ABC

t_shape_rotor_radius = 150
h_shape_rotor_radius = 250
star_shape_rotor_radius = 300

magn_afpm_parameters = {
    'RotorDiskRadius': star_shape_rotor_radius,
    'DiskThickness': 10,
    'MagnetLength': 58,
    'MagnetWidth': 30,
    'MagnetThickness': 10,
    'NumberMagnet': 12,
    'StatorThickness': 13,
    'CoilLegWidth': 23.26,
    'CoilInnerWidth1': 30,
    'CoilInnerWidth2': 30
}


def main():
    master_of_puppets_doc_name = 'Master of Puppets'
    imported_spreadsheet_name = 'Spreadsheet001'
    master_spreadsheet_name = 'Spreadsheet'
    master_of_puppets_doc = create_master_of_puppets(
        master_of_puppets_doc_name,
        imported_spreadsheet_name,
        master_spreadsheet_name,
        magn_afpm_parameters)
    master_of_puppets_doc.recompute()

    wind_turbine = create_wind_turbine(magn_afpm_parameters)
    wind_turbine.render()
    wind_turbine.export_to_webgl()


class WindTurbine(ABC):
    def __init__(self,
                 magn_afpm_parameters,
                 base_dir,
                 has_separate_master_files,
                 stator_resin_cast_name):
        self.magn_afpm_parameters = magn_afpm_parameters
        self.has_separate_master_files = has_separate_master_files
        self.stator_resin_cast_name = stator_resin_cast_name
        self.rotor_resin_cast_name = 'PocketBody'

        self.base_path = os.path.join(
            os.path.dirname(__file__), 'documents', base_dir)
        self.doc = App.newDocument('WindTurbine')

    def render(self):
        stator_path = os.path.join(self.base_path, 'Stator')
        if not self.has_separate_master_files:
            self._open_master()
        if self.has_separate_master_files:
            self._open_stator_master(stator_path)
        self._merge_stator_resin_cast(stator_path)

        rotor_path = os.path.join(self.base_path, 'Rotor')
        if self.has_separate_master_files:
            self._open_rotor_master(rotor_path)
        self._merge_rotor_resin_cast(rotor_path)
        self._move_rotor_resin_cast()
        self.doc.recompute()

    def _open_master(self):
        App.openDocument(os.path.join(
            self.base_path, 'MasterBigWindturbine.FCStd'))

    def _open_stator_master(self, stator_path):
        App.openDocument(os.path.join(stator_path, 'MasterStator.FCStd'))

    def _merge_stator_resin_cast(self, stator_path):
        self.doc.mergeProject(
            os.path.join(stator_path, 'StatorResinCast.FCStd'))
        self.doc.Spreadsheet.enforceRecompute()

        if hasattr(Gui, 'setActiveDocument') and hasattr(Gui, 'SendMsgToActiveView'):
            Gui.setActiveDocument(self.doc.Name)
            Gui.SendMsgToActiveView('ViewFit')

    def _open_rotor_master(self, rotor_path):
        App.openDocument(os.path.join(rotor_path, 'Master.FCStd'))

    def _merge_rotor_resin_cast(self, rotor_path):
        self.doc.mergeProject(
            os.path.join(rotor_path, 'RotorResinCast.FCStd'))
        self.doc.Spreadsheet001.enforceRecompute()

        if hasattr(Gui, 'setActiveDocument') and hasattr(Gui, 'SendMsgToActiveView'):
            Gui.setActiveDocument(self.doc.Name)
            Gui.SendMsgToActiveView('ViewFit')

    def _move_rotor_resin_cast(self):
        placement = App.Placement()
        stator_thickness = magn_afpm_parameters['CoilInnerWidth1']
        distance_from_stator = 30
        z = distance_from_stator + (stator_thickness / 2)
        placement.move(App.Vector(0, 0, z))
        self.doc.getObject(self.rotor_resin_cast_name).Placement = placement

    def export_to_webgl(self):
        objects = [
            self.doc.getObject(self.stator_resin_cast_name),
            self.doc.getObject(self.rotor_resin_cast_name)
        ]
        importWebGL.export(objects, 'wind-turbine-webgl.html')


class TShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters, 't_shape', True, 'Pad')


class HShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters, 'h_shape', True, 'Pad')


class StarShapeWindTurbine(WindTurbine):
    def __init__(self, magn_afpm_parameters):
        super().__init__(magn_afpm_parameters, 'star_shape', False, 'Body')


def create_wind_turbine(magn_afpm_parameters):
    rotor_radius = magn_afpm_parameters['RotorDiskRadius']
    if 0 <= rotor_radius < 187.5:
        return TShapeWindTurbine(magn_afpm_parameters)
    elif 187.5 <= rotor_radius <= 275:
        return HShapeWindTurbine(magn_afpm_parameters)
    else:
        return StarShapeWindTurbine(magn_afpm_parameters)
