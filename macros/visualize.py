"""
FreeCAD macro to visualize wind turbines using default values.
"""
from argparse import ArgumentParser
from multiprocessing import Pool
from pathlib import Path
from typing import Tuple, Union

from openafpm_cad_core.app import (Assembly, WindTurbineShape, load_assembly_to_obj,
                                   get_default_parameters)


def write_obj_file(shape_assembly_path_triple: Tuple[WindTurbineShape, Assembly, Path]) -> str:
    shape, assembly, path = shape_assembly_path_triple
    parameters = get_default_parameters(shape)

    turbine_dir = path.joinpath(slugify_enum(shape))
    turbine_dir.mkdir(exist_ok=True)

    obj_file_contents = load_assembly_to_obj(
        assembly,
        parameters['magnafpm'],
        parameters['furling'],
        parameters['user'])
    filepath = turbine_dir.joinpath(f'{slugify_enum(assembly)}.obj')
    with open(filepath, 'w') as f:
        f.write(obj_file_contents)
        return str(filepath.resolve())


def slugify_enum(enum: Union[Assembly, WindTurbineShape]) -> str:
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
                        choices=['t', 'h', 'star', 'all'],
                        required=False,
                        default='all',
                        help='Type of turbine to visualize. Defaults to all.')
    args = parser.parse_args()
    if args.type == 'all':
        turbines = (
            WindTurbineShape.T,
            WindTurbineShape.H,
            WindTurbineShape.STAR)
    else:
        turbine = {
            't': WindTurbineShape.T,
            'h': WindTurbineShape.H,
            'star': WindTurbineShape.STAR
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
