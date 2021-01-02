import os

import Draft
import FreeCAD as App
import FreeCADGui as Gui

from .common import enforce_recompute_last_spreadsheet, make_compound

__all__ = ['make_rotors']


def make_rotors(base_path,
                has_separate_master_files,
                document,
                rotor_disc1_name,
                coil_inner_width_1,
                disk_thickness,
                magnet_thickness):
    rotor_path = os.path.join(base_path, 'Rotor')
    if has_separate_master_files:
        _open_rotor_master(rotor_path)
    if hasattr(Gui, 'setActiveDocument') and hasattr(Gui, 'SendMsgToActiveView'):
        Gui.setActiveDocument(document.Name)
        Gui.SendMsgToActiveView('ViewFit')
    bottom_rotor = _assemble_bottom_rotor(
        document, rotor_path, rotor_disc1_name)
    document.recompute()
    App.setActiveDocument(document.Name)
    top_rotor = Draft.clone(bottom_rotor)
    _position_top_rotor(top_rotor, coil_inner_width_1,
                        disk_thickness, magnet_thickness)
    _move_bottom_rotor(bottom_rotor, coil_inner_width_1,
                       disk_thickness, magnet_thickness)
    return bottom_rotor, top_rotor


def _open_rotor_master(rotor_path):
    App.openDocument(os.path.join(rotor_path, 'Master.FCStd'))


def _assemble_bottom_rotor(document, rotor_path, rotor_disc1_name):
    _merge_rotor_resin_cast(document, rotor_path)
    _merge_rotor_disc1(document, rotor_path)
    rotor = make_compound(document, 'BottomRotor', [
        document.getObject('PocketBody'),  # rotor_resin_cast_name
        document.getObject(rotor_disc1_name)
    ])
    return rotor


def _merge_rotor_resin_cast(document, rotor_path):
    document.mergeProject(
        os.path.join(rotor_path, 'RotorResinCast.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def _merge_rotor_disc1(document, rotor_path):
    document.mergeProject(
        os.path.join(rotor_path, 'Disc1.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def _move_bottom_rotor(rotor, coil_inner_width_1, disk_thickness, magnet_thickness):
    z = _calculate_rotor_z_offset(
        coil_inner_width_1,  disk_thickness, magnet_thickness)
    Draft.move(rotor, App.Vector(0, 0, -z))


def _position_top_rotor(top_rotor, coil_inner_width_1, disk_thickness, magnet_thickness):
    App.DraftWorkingPlane.alignToPointAndAxis(
        App.Vector(0, 0, 0), App.Vector(1, 0, 0), 0)
    Draft.rotate([top_rotor], 180.0, App.Vector(0.0, 0.0, 0.0),
                 axis=App.Vector(1.0, 0.0, 0.0), copy=False)
    z = _calculate_rotor_z_offset(
        coil_inner_width_1,  disk_thickness, magnet_thickness)
    Draft.move(top_rotor, App.Vector(0, 0, z))


def _calculate_rotor_z_offset(coil_inner_width_1, disk_thickness, magnet_thickness):
    stator_thickness = coil_inner_width_1
    distance_of_rotor_from_stator = 30
    rotor_thickness = _calculate_rotor_thickness(
        disk_thickness, magnet_thickness)
    return (
        distance_of_rotor_from_stator +
        (stator_thickness / 2) +
        rotor_thickness
    )


def _calculate_rotor_thickness(disk_thickness, magnet_thickness):
    return disk_thickness + magnet_thickness
