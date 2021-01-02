import FreeCAD as App
import FreeCADGui as Gui
import Draft
import os

__all__ = ['make_alternator']


def make_alternator(base_path,
                    has_separate_master_files,
                    document,
                    rotor_disc1_name,
                    coil_inner_width_1,
                    disk_thickness,
                    magnet_thickness):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    stator_path = os.path.join(base_path, 'Stator')
    if not has_separate_master_files:
        _open_master(base_path)
    if has_separate_master_files:
        _open_stator_master(stator_path)
    _merge_stator_resin_cast(document, stator_path)

    rotor_path = os.path.join(base_path, 'Rotor')
    if has_separate_master_files:
        _open_rotor_master(rotor_path)
    if hasattr(Gui, 'setActiveDocument') and hasattr(Gui, 'SendMsgToActiveView'):
        Gui.setActiveDocument(document.Name)
        Gui.SendMsgToActiveView('ViewFit')
    rotor_name = 'Rotor'
    rotor = _assemble_rotor(document, rotor_path, rotor_name, rotor_disc1_name)
    document.recompute()
    App.setActiveDocument(document.Name)
    top_rotor = Draft.clone(rotor)
    _position_top_rotor(top_rotor, coil_inner_width_1,
                        disk_thickness, magnet_thickness)
    _move_rotor(rotor, coil_inner_width_1, disk_thickness, magnet_thickness)


def _open_master(base_path):
    App.openDocument(os.path.join(
        base_path, 'MasterBigWindturbine.FCStd'))


def _open_stator_master(stator_path):
    App.openDocument(os.path.join(stator_path, 'MasterStator.FCStd'))


def _merge_stator_resin_cast(document, stator_path):
    document.mergeProject(
        os.path.join(stator_path, 'StatorResinCast.FCStd'))
    _enforce_recompute_last_spreadsheet(document)


def _open_rotor_master(rotor_path):
    App.openDocument(os.path.join(rotor_path, 'Master.FCStd'))


def _assemble_rotor(document, rotor_path, rotor_name, rotor_disc1_name):
    _merge_rotor_resin_cast(document, rotor_path)
    _merge_rotor_disc1(document, rotor_path)
    rotor = document.addObject('Part::Compound', rotor_name)
    rotor.Links = [
        document.getObject('PocketBody'),  # rotor_resin_cast_name
        document.getObject(rotor_disc1_name)
    ]
    return rotor


def _merge_rotor_resin_cast(document, rotor_path):
    document.mergeProject(
        os.path.join(rotor_path, 'RotorResinCast.FCStd'))
    _enforce_recompute_last_spreadsheet(document)


def _merge_rotor_disc1(document, rotor_path):
    document.mergeProject(
        os.path.join(rotor_path, 'Disc1.FCStd'))
    _enforce_recompute_last_spreadsheet(document)


def _enforce_recompute_last_spreadsheet(document):
    sheets = document.findObjects('Spreadsheet::Sheet')
    last_sheet = sheets[len(sheets) - 1]
    last_sheet.enforceRecompute()


def _move_rotor(rotor, coil_inner_width_1,  disk_thickness, magnet_thickness):
    placement = App.Placement()
    z = _calculate_rotor_z_offset(
        coil_inner_width_1,  disk_thickness, magnet_thickness)
    placement.move(App.Vector(0, 0, -z))
    rotor.Placement = placement


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
