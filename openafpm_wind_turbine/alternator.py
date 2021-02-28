from .common import (enforce_recompute_last_spreadsheet, find_object_by_label,
                     make_compound)
from .rotor import make_rotors
from .stator import load_stator

__all__ = ['make_alternator']


def make_alternator(base_path,
                    has_separate_master_files,
                    document,
                    name,
                    stator_thickness,
                    disk_thickness,
                    magnet_thickness,
                    distance_between_stator_and_rotor):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    stator_resin_cast_label = 'StatorResinCast'
    load_stator(base_path, has_separate_master_files,
                document, stator_resin_cast_label)
    stator_resin_cast = find_object_by_label(document, stator_resin_cast_label)

    bottom_rotor, top_rotor = make_rotors(
        base_path,
        has_separate_master_files,
        document,
        stator_thickness,
        disk_thickness,
        magnet_thickness,
        distance_between_stator_and_rotor)
    alternator = document.addObject('App::DocumentObjectGroup', name)

    alternator.addObjects([
        stator_resin_cast,
        bottom_rotor,
        top_rotor
    ])
    return alternator
