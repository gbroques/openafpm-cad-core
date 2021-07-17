from .create_spreadsheet_document import create_spreadsheet_document
from .get_default_parameters import get_default_parameters
from .load_turbine import load_turbine
from .wind_turbine import WindTurbine

__all__ = [
    'create_spreadsheet_document',
    'get_default_parameters',
    'visualize'
]


def visualize(magnafpm_parameters: dict,
              user_parameters: dict,
              furling_parameters: dict) -> WindTurbine:
    return load_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
