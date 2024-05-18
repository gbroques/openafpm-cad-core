from argparse import ArgumentParser
from multiprocessing import Pool

import FreeCAD as App
from FreeCAD import Console

from openafpm_cad_core.app import (WindTurbine, export_to_dxf,
                                   get_default_parameters)


def export(turbine: WindTurbine) -> str:
    parameters = get_default_parameters(turbine)

    zip_bytes = export_to_dxf(
        parameters['magnafpm'],
        parameters['furling'],
        parameters['user'])

    name = turbine.value.lower().replace(' ', '-')
    filename = f'{name}-dxf.zip'
    with open(filename, 'wb') as zip_file:
        zip_file.write(zip_bytes)
    return filename


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Export flat parts to DXF using default values.')
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        choices=['t', 'h', 'star', 't2f', 'all'],
                        required=False,
                        default='all',
                        help='Type of turbine. Defaults to all.')
    args = parser.parse_args()
    turbines: tuple = ()
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
    if App.GuiUp == 1:
        Console.PrintWarning(f'FreeCAD Gui is up. Defaulting to {turbines[0]}\n')
        print(export(turbines[0]))
    else:
        with Pool(len(turbines)) as p:
            filepaths = p.map(export, turbines)
            print('\n'.join(filepaths))
