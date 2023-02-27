"""
FreeCAD macro to visualize wind turbines using default values.
"""
import pstats
import cProfile

from openafpm_cad_core.app import (Assembly, WindTurbine, assembly_to_obj,
                                   get_default_parameters)


def visualize() -> str:
    parameters = get_default_parameters(WindTurbine.T_SHAPE)

    obj_file_contents = assembly_to_obj(
        Assembly.STATOR_MOLD,
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'],
        save_spreadsheet_document=False)


if __name__ == '__main__':
    with cProfile.Profile() as profile:
        visualize()
    
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
    results.dump_stats('t-shape-stator-mold-after.prof')
