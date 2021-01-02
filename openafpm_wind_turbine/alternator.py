from .common import enforce_recompute_last_spreadsheet, make_compound
from .rotor import make_rotors
from .stator import load_stator

__all__ = ['make_alternator']


def make_alternator(base_path,
                    has_separate_master_files,
                    document,
                    name,
                    stator_resin_cast_name,
                    rotor_disc1_name,
                    coil_inner_width_1,
                    disk_thickness,
                    magnet_thickness):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    load_stator(base_path, has_separate_master_files, document)

    bottom_rotor, top_rotor = make_rotors(
        base_path,
        has_separate_master_files,
        document,
        rotor_disc1_name,
        coil_inner_width_1,
        disk_thickness,
        magnet_thickness)
    return make_compound(document, name, [
        document.getObject(stator_resin_cast_name),
        bottom_rotor,
        top_rotor
    ])
