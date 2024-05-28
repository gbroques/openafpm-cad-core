from argparse import ArgumentParser
from multiprocessing import Pool
from typing import Callable

import FreeCAD as App
from FreeCAD import Console

from .wind_turbine_shape import WindTurbineShape

__all__ = ['exec_turbine_function']


def exec_turbine_function(
        description: str,
        turbine_function: Callable[[WindTurbineShape], str]) -> None:
    parser = ArgumentParser(description=description)
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        choices=['t', 'h', 'star', 'all'],
                        required=False,
                        default='t',
                        help='Type of turbine. Defaults to t.')
    args = parser.parse_args()
    turbines: tuple = ()
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
    if App.GuiUp == 1:
        Console.PrintWarning(f'FreeCAD Gui is up. Defaulting to {turbines[0]}\n')
        print(turbine_function(turbines[0]))
    else:
        with Pool(len(turbines)) as p:
            filepaths = p.map(turbine_function, turbines)
            print('\n'.join(filepaths))
