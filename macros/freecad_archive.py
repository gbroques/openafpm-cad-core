from openafpm_cad_core.app import (WindTurbineShape, load_freecad_archive,
                                   exec_turbine_function,
                                   get_default_parameters)


def write_archive(turbine_shape: WindTurbineShape) -> str:
    parameters = get_default_parameters(turbine_shape)

    zip_bytes = load_freecad_archive(
        parameters['magnafpm'],
        parameters['furling'],
        parameters['user'])

    name = turbine_shape.value.lower().replace(' ', '-')
    filename = f'{name}.zip'
    with open(filename, 'wb') as zip_file:
        zip_file.write(zip_bytes)
    return filename


if __name__ == '__main__':
    exec_turbine_function(
        'Create archive containing FreeCAD documents using default values.', write_archive)
