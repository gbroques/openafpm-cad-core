
from multiprocessing import Pool
from argparse import ArgumentParser

from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   preview_dxf_as_svg)


def write_to_svg(turbine: WindTurbine) -> str:
    parameters = get_default_parameters(turbine)

    svg = preview_dxf_as_svg(
        parameters['magnafpm'],
        parameters['furling'],
        parameters['user'])

    name = turbine.value.lower().replace(' ', '-')
    filename = f'{name}-dxf-overview.svg'
    with open(filename, 'w') as svg_file:
        svg_file.write(svg)
    return filename


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Preview flat parts as SVG using default values.')
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
        filepaths = p.map(write_to_svg, turbines)
        print('\n'.join(filepaths))
