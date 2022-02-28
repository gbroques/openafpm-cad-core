from pathlib import Path

from .load_root_document import load_root_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_model import WindTurbineModel

__all__ = ['load_turbine', 'load_stator_mold']


def load_turbine(magnafpm_parameters: MagnafpmParameters,
                 furling_parameters: FurlingParameters,
                 user_parameters: UserParameters) -> WindTurbineModel:
    root_document, spreadsheet_document = load_root_document(
        get_wind_turbine_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )

    return WindTurbineModel(root_document, spreadsheet_document)


def load_stator_mold(magnafpm_parameters: MagnafpmParameters,
                     furling_parameters: FurlingParameters,
                     user_parameters: UserParameters) -> None:
    root_document, spreadsheet_document = load_root_document(
        get_stator_mold_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )
    return None


def get_wind_turbine_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath('WindTurbine.FCStd')


def get_stator_mold_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        'Alternator', 'Stator', 'Mold', 'Stator_Mold_Assembly.FCStd')
