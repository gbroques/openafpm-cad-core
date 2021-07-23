from .create_spreadsheet_document import create_spreadsheet_document
from .get_default_parameters import get_default_parameters
from .load_turbine import load_turbine
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine import WindTurbine
from .wind_turbine_model import WindTurbineModel

__all__ = [
    'create_spreadsheet_document',
    'get_default_parameters',
    'visualize',
    'WindTurbine'
]


def visualize(magnafpm_parameters: MagnafpmParameters,
              user_parameters: UserParameters,
              furling_parameters: FurlingParameters) -> WindTurbineModel:
    return load_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
