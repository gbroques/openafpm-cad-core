from openafpm_cad_core.app import (WindTurbine, exec_turbine_function,
                                   get_default_parameters, preview_dxf_as_svg)


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
    exec_turbine_function(
        'Preview flat parts as SVG using default values.', write_to_svg)
