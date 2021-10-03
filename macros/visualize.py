"""
FreeCAD macro to visualize wind turbine using default values.
"""
from argparse import ArgumentParser

from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   visualize)


def create_obj_file(turbine: WindTurbine):
    parameters = get_default_parameters(turbine)

    wind_turbine_model = visualize(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'])

    obj_file_contents = wind_turbine_model.to_obj()

    filename = turbine.value.lower().replace(' ', '-')
    with open(f'{filename}.obj', 'w') as f:
        f.write(obj_file_contents)
        print(f'{filename}.obj created.')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Export wind turbine to .obj using default values.')
    parser.add_argument('variant',
                        metavar='<variant>',
                        type=str,
                        choices={'t', 'h', 'star'},
                        help='Type of wind turbine, T, H, or Star Shape.')

    args = parser.parse_args()

    variant_by_choice = {
        't': WindTurbine.T_SHAPE,
        'h': WindTurbine.H_SHAPE,
        'star': WindTurbine.STAR_SHAPE
    }

    turbine = variant_by_choice[args.variant]
    create_obj_file(turbine)
