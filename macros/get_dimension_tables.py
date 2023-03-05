"""
FreeCAD macro to get dimensions for wind turbines using default values.
"""
import json
from argparse import ArgumentParser
from multiprocessing import Pool
from typing import Union

from openafpm_cad_core.app import (Assembly, WindTurbine,
                                   get_default_parameters, get_dimension_tables)


def print_dimension_tables(turbine: WindTurbine) -> str:
    parameters = get_default_parameters(turbine)

    return json.dumps(get_dimension_tables(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling']), indent=2)


def slugify_enum(enum: Union[Assembly, WindTurbine]) -> str:
    return enum.value.lower().replace(' ', '-')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Get dimensions for wind turbine(s) using default values.')
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        choices=['t', 'h', 'star', 't2f', 'all'],
                        required=False,
                        default='all',
                        help='Type of turbine. Defaults to all.')
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

    with Pool(len(turbines)) as p:
        dimension_tables = p.map(print_dimension_tables, turbines)
        print('\n'.join(dimension_tables))
