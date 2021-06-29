from .create_spreadsheet_document import create_spreadsheet_document
from .load_turbine import load_turbine
from .wind_turbine import WindTurbine

__all__ = [
    'visualize',
    'CreateSpreadsheetTaskPanel'
]


def visualize(magnafpm_parameters: dict,
              user_parameters: dict,
              furling_parameters: dict) -> WindTurbine:
    return load_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
