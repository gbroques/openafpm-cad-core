from .common import (enforce_recompute_last_spreadsheet, find_object_by_label,
                     make_compound)
from .rotor import make_rotors
from .stator import make_stator

__all__ = ['make_alternator']


def make_alternator(base_path,
                    has_separate_master_files,
                    document,
                    name,
                    stator_thickness,
                    disk_thickness,
                    magnet_thickness,
                    distance_between_stator_and_rotor,
                    magnets,
                    coils):
    """
    The alternator consists of the stator,
    sandwiched by two rotors.
    """
    stator_name = 'Stator'
    stator = make_stator(base_path,
                         document,
                         stator_name,
                         coils)

    bottom_rotor, top_rotor = make_rotors(
        base_path,
        has_separate_master_files,
        document,
        stator_thickness,
        disk_thickness,
        magnet_thickness,
        distance_between_stator_and_rotor,
        magnets)
    alternator = document.addObject('App::DocumentObjectGroup', name)

    alternator.addObjects([
        stator,
        bottom_rotor,
        top_rotor
    ])
    return alternator
