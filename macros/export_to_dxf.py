
from multiprocessing import Pool

from openafpm_cad_core.app import (WindTurbine, export_to_dxf,
                                   get_default_parameters)


def export(turbine: WindTurbine) -> str:
    parameters = get_default_parameters(turbine)

    zip_bytes = export_to_dxf(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'])

    name = turbine.value.lower().replace(' ', '-')
    filename = f'{name}-dxf.zip'
    with open(filename, 'wb') as zip_file:
        zip_file.write(zip_bytes)
    return filename


if __name__ == '__main__':
    turbines = (
        WindTurbine.T_SHAPE,
        WindTurbine.H_SHAPE,
        WindTurbine.STAR_SHAPE)
    with Pool(3) as p:
        filepaths = p.map(export, turbines)
        print('Created')
        print('\n'.join(filepaths))
