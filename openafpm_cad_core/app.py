from .create_spreadsheet_document import create_spreadsheet_document
from .export_to_dxf import export_to_dxf
from .get_default_parameters import get_default_parameters
from .load import load_turbine
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .preview_dxf_as_svg import preview_dxf_as_svg
from .wind_turbine import WindTurbine
from .wind_turbine_model import WindTurbineModel

__all__ = [
    'create_spreadsheet_document',
    'export_to_dxf'
    'get_default_parameters',
    'preview_dxf_as_svg',
    'visualize',
    'WindTurbine',
]


def visualize(magnafpm_parameters: MagnafpmParameters,
              user_parameters: UserParameters,
              furling_parameters: FurlingParameters) -> WindTurbineModel:
    return load_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
