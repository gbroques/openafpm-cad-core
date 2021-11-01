"""
FreeCAD macro to visualize wind turbines using default values.
"""
from argparse import ArgumentParser
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path
from typing import Tuple

from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   visualize)


def write_obj_file(path_turbine_pair: Tuple[Path, WindTurbine]) -> str:
    path, turbine = path_turbine_pair
    parameters = get_default_parameters(turbine)

    wind_turbine_model = visualize(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'])

    obj_file_contents = wind_turbine_model.to_obj()

    filename = turbine.value.lower().replace(' ', '-')
    filepath = path.joinpath(f'{filename}.obj')
    with open(filepath, 'w') as f:
        f.write(obj_file_contents)
        return str(filepath.resolve())


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
        WindTurbine.STAR_SHAPE)

    paths = repeat(Path(args.path), len(turbines))
    pairs = tuple(zip(paths, turbines))
    with Pool(3) as p:
        filepaths = p.map(write_obj_file, pairs)
        print('Created')
        print('\n'.join(filepaths))
