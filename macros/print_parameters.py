from argparse import ArgumentParser, Namespace
from operator import attrgetter

from openafpm_cad_core.app import (WindTurbineShape, exec_turbine_function,
                                   get_default_parameters,
                                   load_spreadsheet_document)


def get_parameter(turbine_shape: WindTurbineShape, args: Namespace) -> str:
    parameters = get_default_parameters(turbine_shape)

    spreadsheet_document = load_spreadsheet_document(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'])

    def get_attr(attr: str) -> str:
        return f'{turbine_shape.name} {attr} {attrgetter(attr)(spreadsheet_document)}'
    return '\n'.join(map(get_attr, args.attrs))


if __name__ == '__main__':
    def argument_parser_customizer(argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('attrs', nargs='+')
    exec_turbine_function(
        'Print parameter values for wind turbine(s) using presets.',
        get_parameter,
        argument_parser_customizer)
