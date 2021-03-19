import os

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Vector, Placement, Rotation

from .common import (clone_body, enforce_recompute_last_spreadsheet,
                     find_object_by_label, make_compound)

__all__ = ['make_rotors']


def make_rotors(base_path,
                document,
                stator_thickness,
                disk_thickness,
                magnet_thickness,
                distance_between_stator_and_rotor,
                magnets):
    rotor_path = os.path.join(base_path, 'Rotor')
    if hasattr(Gui, 'setActiveDocument') and hasattr(Gui, 'SendMsgToActiveView'):
        Gui.setActiveDocument(document.Name)
        Gui.SendMsgToActiveView('ViewFit')
    bottom_rotor = _assemble_bottom_rotor(
        document, rotor_path, magnets)
    document.recompute()
    App.setActiveDocument(document.Name)
    top_rotor = _make_top_rotor(document,
                                bottom_rotor,
                                stator_thickness,
                                disk_thickness,
                                magnet_thickness,
                                distance_between_stator_and_rotor)
    _move_bottom_rotor(bottom_rotor,
                       stator_thickness,
                       disk_thickness,
                       magnet_thickness,
                       distance_between_stator_and_rotor)
    return bottom_rotor, top_rotor


def _assemble_bottom_rotor(document, rotor_path, magnets):
    rotor_resin_cast_label = 'RotorResinCast'
    _merge_document(document, rotor_path, rotor_resin_cast_label)
    rotor_resin_cast = find_object_by_label(document, rotor_resin_cast_label)
    rotor_resin_cast.Label = 'Bottom' + rotor_resin_cast.Label

    rotor_disc1_label = 'Disc1'
    _merge_document(document, rotor_path, rotor_disc1_label)
    rotor_disc1 = find_object_by_label(document, rotor_disc1_label)
    rotor_disc1.Label = 'Bottom' + rotor_disc1.Label

    magnets.Label = 'Bottom' + magnets.Label

    rotor = document.addObject('App::DocumentObjectGroup', 'BottomRotor')
    rotor.addObjects([
        rotor_resin_cast,
        rotor_disc1,
        magnets
    ])
    return rotor


def _merge_document(document, rotor_path, name):
    document.mergeProject(
        os.path.join(rotor_path, name + '.FCStd'))
    enforce_recompute_last_spreadsheet(document)


def _move_bottom_rotor(bottom_rotor,
                       stator_thickness,
                       disk_thickness,
                       magnet_thickness,
                       distance_between_stator_and_rotor):
    z = _calculate_rotor_z_offset(stator_thickness,
                                  disk_thickness,
                                  magnet_thickness,
                                  distance_between_stator_and_rotor)
    for obj in bottom_rotor.Group:
        obj.Placement = Placement(Vector(0, 0, -z), Rotation())


def _make_top_rotor(document,
                    bottom_rotor,
                    stator_thickness,
                    disk_thickness,
                    magnet_thickness,
                    distance_between_stator_and_rotor):
    z = _calculate_rotor_z_offset(stator_thickness,
                                  disk_thickness,
                                  magnet_thickness,
                                  distance_between_stator_and_rotor)
    clones = []
    for obj in bottom_rotor.Group:
        name = obj.Label.replace('Bottom', 'Top')
        clone = clone_body(document, name, obj)
        clone.Placement = Placement(
            Vector(0, 0, z), Rotation(Vector(0, 1, 0), 180))
        clones.append(clone)

    top_rotor = document.addObject('App::DocumentObjectGroup', 'TopRotor')
    top_rotor.addObjects(clones)
    return top_rotor


def _calculate_rotor_z_offset(stator_thickness,
                              disk_thickness,
                              magnet_thickness,
                              distance_between_stator_and_rotor):
    rotor_thickness = _calculate_rotor_thickness(
        disk_thickness, magnet_thickness)
    return (
        distance_between_stator_and_rotor +
        (stator_thickness / 2) +
        rotor_thickness
    )


def _calculate_rotor_thickness(disk_thickness, magnet_thickness):
    return disk_thickness + magnet_thickness
