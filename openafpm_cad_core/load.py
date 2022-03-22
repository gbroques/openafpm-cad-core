from enum import Enum, unique
from pathlib import Path
from typing import List, Tuple

from FreeCAD import Document

from .load_root_document import load_root_document, load_root_documents
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_model import WindTurbineModel

__all__ = [
    'load_all',
    'load_turbine',
    'load_assembly',
    'Assembly'
]


@unique
class Assembly(Enum):
    WindTurbine = 'Wind Turbine'
    StatorMold = 'Stator Mold'
    RotorMold = 'Rotor Mold'
    CoilWinder = 'Coil Winder'


def load_assembly(assembly: Assembly,
                  magnafpm_parameters: MagnafpmParameters,
                  furling_parameters: FurlingParameters,
                  user_parameters: UserParameters):
    load_function_by_assembly = {
        Assembly.WindTurbine: load_turbine,
        Assembly.StatorMold: load_stator_mold,
        Assembly.RotorMold: load_rotor_mold,
        Assembly.CoilWinder: load_coil_winder_mold
    }
    load_function = load_function_by_assembly[assembly]
    return load_function(magnafpm_parameters, furling_parameters, user_parameters)


def load_all(magnafpm_parameters: MagnafpmParameters,
             furling_parameters: FurlingParameters,
             user_parameters: UserParameters) -> Tuple[List[Document], Document]:
    return load_root_documents(
        [
            get_wind_turbine_document_path,
            get_stator_mold_assembly_document_path,
            get_rotor_mold_assembly_document_path
        ],
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )


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


def get_wind_turbine_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath('WindTurbine.FCStd')


def load_stator_mold(magnafpm_parameters: MagnafpmParameters,
                     furling_parameters: FurlingParameters,
                     user_parameters: UserParameters) -> Tuple[Document, Document]:
    return load_root_document(
        get_stator_mold_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )


def get_stator_mold_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        'Alternator', 'Stator', 'Mold', 'Stator_Mold_Assembly.FCStd')


def load_coil_winder_mold(magnafpm_parameters: MagnafpmParameters,
                          furling_parameters: FurlingParameters,
                          user_parameters: UserParameters) -> Tuple[Document, Document]:
    return load_root_document(
        get_coil_winder_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )


def get_coil_winder_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        'Alternator', 'Stator', 'CoilWinder', 'Stator_CoilWinder_Assembly.FCStd')


def load_rotor_mold(magnafpm_parameters: MagnafpmParameters,
                    furling_parameters: FurlingParameters,
                    user_parameters: UserParameters) -> Tuple[Document, Document]:
    return load_root_document(
        get_rotor_mold_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters
    )


def get_rotor_mold_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        'Alternator', 'Rotor', 'Mold', 'Rotor_Mold_Assembly.FCStd')
