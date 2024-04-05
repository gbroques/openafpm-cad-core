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
        parameters['furling'],
        parameters['user'])
    filepath = turbine_dir.joinpath(f'{slugify_enum(assembly)}.obj')
    with open(filepath, 'w') as f:
        f.write(obj_file_contents)
        return str(filepath.resolve())


def slugify_enum(enum: Union[Assembly, WindTurbine]) -> str:
    return enum.value.lower().replace(' ', '-')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Export wind turbine(s) to .obj using default values.')
    parser.add_argument('path',
                        metavar='<path>',
                        type=str,
                        help='Output path.')
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        choices=['t', 'h', 'star', 't2f', 'all'],
                        required=False,
                        default='all',
                        help='Type of turbine to visualize. Defaults to all.')
    args = parser.parse_args()
    if args.type == 'all':
        turbines = (
            WindTurbine.T_SHAPE,
            WindTurbine.H_SHAPE,
            WindTurbine.STAR_SHAPE,
            WindTurbine.T_SHAPE_2F)
    else:
        turbine = {
            't': WindTurbine.T_SHAPE,
            'h': WindTurbine.H_SHAPE,
            'star': WindTurbine.STAR_SHAPE,
            't2f': WindTurbine.T_SHAPE_2F
        }[args.type]
        turbines = (turbine,)
    assemblies = (
        Assembly.WIND_TURBINE,
        Assembly.STATOR_MOLD,
        Assembly.ROTOR_MOLD,
        Assembly.MAGNET_JIG,
        Assembly.COIL_WINDER,
        Assembly.BLADE_TEMPLATE)
    path = Path(args.path)
    triples = [(turbine, assembly, path)
               for turbine in turbines for assembly in assemblies]

    with Pool(len(triples)) as p:
        filepaths = p.map(write_obj_file, triples)
        print('\n'.join(filepaths))
