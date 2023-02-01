"""
FreeCAD macro to visualize wind turbines using default values.
"""
from argparse import ArgumentParser
from multiprocessing import Pool
from pathlib import Path
from typing import Tuple, Union

from openafpm_cad_core.app import (Assembly, WindTurbine, assembly_to_obj,
                                   get_default_parameters)


def write_obj_file(turbine_assembly_path_triple: Tuple[WindTurbine, Assembly, Path]) -> str:
    turbine, assembly, path = turbine_assembly_path_triple
    parameters = get_default_parameters(turbine)

    turbine_dir = path.joinpath(slugify_enum(turbine))
    turbine_dir.mkdir(exist_ok=True)

    obj_file_contents = assembly_to_obj(
        assembly,
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'],
        save_spreadsheet_document=True)
    filepath = turbine_dir.joinpath(f'{slugify_enum(assembly)}.obj')
    with open(filepath, 'w') as f:
        f.write(obj_file_contents)
        return str(filepath.resolve())


def slugify_enum(enum: Union[Assembly, WindTurbine]) -> str:
    return enum.value.lower().replace(' ', '-')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Export wind turbines to .obj using default values.')
    parser.add_argument('path',
                        metavar='<path>',
                        type=str,
                        help='Output path.')

    args = parser.parse_args()

    turbines = (
        WindTurbine.T_SHAPE,
        WindTurbine.H_SHAPE,
        WindTurbine.STAR_SHAPE,
        WindTurbine.T_SHAPE_2F)
    assemblies = (
        Assembly.WIND_TURBINE,
        Assembly.STATOR_MOLD,
        Assembly.ROTOR_MOLD,
        Assembly.MAGNET_JIG,
        Assembly.COIL_WINDER)
    path = Path(args.path)
    triples = [(turbine, assembly, path)
                for turbine in turbines for assembly in assemblies]

    with Pool(len(triples)) as p:
        filepaths = p.map(write_obj_file, triples)
        print('Created')
        print('\n'.join(filepaths))
