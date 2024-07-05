from typing import Union

from openafpm_cad_core.app import (WindTurbineShape, exec_turbine_function,
                                   export_to_dxf, get_default_parameters)


def write_dxf_zip(turbine_shape: Union[WindTurbineShape, str]) -> str:
    parameters = get_default_parameters(turbine_shape)

    zip_bytes = export_to_dxf(
        parameters['magnafpm'],
        parameters['furling'],
        parameters['user'])

    shape = turbine_shape if isinstance(turbine_shape, str) else turbine_shape.value
    name = shape.lower().replace(' ', '-')
    filename = f'{name}-dxf.zip'
    with open(filename, 'wb') as zip_file:
        zip_file.write(zip_bytes)
    return filename


if __name__ == '__main__':
    exec_turbine_function(
        'Export flat parts to DXF using default values.', write_dxf_zip)
