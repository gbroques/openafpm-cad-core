
from multiprocessing import Pool

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
    turbines = (
        WindTurbine.T_SHAPE,
        WindTurbine.H_SHAPE,
        WindTurbine.STAR_SHAPE,
        WindTurbine.T_SHAPE_2F)
    with Pool(len(turbines)) as p:
        filepaths = p.map(write_to_svg, turbines)
        print('\n'.join(filepaths))
