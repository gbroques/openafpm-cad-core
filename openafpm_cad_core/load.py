from enum import Enum, unique
from pathlib import Path
from typing import List, Tuple

import FreeCAD as App
from FreeCAD import Document

from .load_root_document import load_document, load_root_document, load_root_documents
from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters

__all__ = ["load_all", "load_turbine", "load_alernator", "load_assembly", "Assembly"]


@unique
class Assembly(Enum):
    WIND_TURBINE = "Wind Turbine"
    STATOR_MOLD = "Stator Mold"
    ROTOR_MOLD = "Rotor Mold"
    MAGNET_JIG = "Magnet Jig"
    COIL_WINDER = "Coil Winder"
    BLADE_TEMPLATE = "Blade Template"


def load_assembly(
    assembly: Assembly,
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
):
    load_function_by_assembly = {
        Assembly.WIND_TURBINE: load_turbine,
        Assembly.STATOR_MOLD: load_stator_mold,
        Assembly.ROTOR_MOLD: load_rotor_mold,
        Assembly.MAGNET_JIG: load_magnet_jig,
        Assembly.COIL_WINDER: load_coil_winder,
        Assembly.BLADE_TEMPLATE: load_blade_template,
    }
    load_function = load_function_by_assembly[assembly]
    return load_function(magnafpm_parameters, furling_parameters, user_parameters)


def load_all(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
    progress_callback=None,
    progress_range=(0, 100),
    cancel_event=None,
) -> Tuple[List[Document], Document]:
    """Load all wind turbine CAD documents with optional progress reporting.
    
    Loads the complete set of OpenAFPM wind turbine documents including:
    - Wind Turbine assembly
    - Stator Mold, Rotor Mold assemblies  
    - Magnet Jig, Coil Winder assemblies
    - Blade Template
    
    Args:
        magnafpm_parameters: Generator/alternator parameters from MagnAFPM tool
        furling_parameters: Tail and furling mechanism parameters
        user_parameters: User-defined construction parameters
        progress_callback: Optional callback function(stage_name: str, percent: int)
        progress_range: Tuple of (start_percent, end_percent) for progress scaling
        cancel_event: Optional threading.Event to signal cancellation
        
    Returns:
        Tuple of (root_documents, spreadsheet_document)
        - root_documents: List of 6 loaded FreeCAD Document objects (root of document hierarchy)
        - spreadsheet_document: Master parameter spreadsheet Document
        
    Example:
        >>> def progress_handler(stage, percent):
        ...     print(f"[{percent}%] {stage}")
        >>> 
        >>> params = get_default_parameters("T Shape")
        >>> root_docs, sheet = load_all(
        ...     params['magnafpm'], 
        ...     params['furling'], 
        ...     params['user'],
        ...     progress_callback=progress_handler,
        ...     progress_range=(0, 80)  # Reserve 80-100% for other operations
        ... )
        
    Note:
        Loading typically takes 50+ seconds due to document recomputation.
        Progress callback provides detailed feedback during this process.
    """
    return load_root_documents(
        [
            get_wind_turbine_document_path,
            get_stator_mold_assembly_document_path,
            get_rotor_mold_assembly_document_path,
            get_magnet_jig_assembly_document_path,
            get_coil_winder_assembly_document_path,
            get_blade_template_document_path,
        ],
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
        progress_callback,
        progress_range,
        cancel_event,
    )


def load_turbine(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_wind_turbine_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_wind_turbine_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath("WindTurbine.FCStd")


def load_stator_mold(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_stator_mold_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_stator_mold_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        "Alternator", "Stator", "Mold", "Stator_Mold_Assembly.FCStd"
    )


def load_rotor_mold(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_rotor_mold_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_rotor_mold_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        "Alternator", "Rotor", "Mold", "Rotor_Mold_Assembly.FCStd"
    )


def load_magnet_jig(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_magnet_jig_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_magnet_jig_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        "Alternator", "Rotor", "MagnetJig", "Rotor_MagnetJig_Assembly.FCStd"
    )


def load_coil_winder(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_coil_winder_assembly_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_coil_winder_assembly_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath(
        "Alternator", "Stator", "CoilWinder", "Stator_CoilWinder_Assembly.FCStd"
    )


def load_blade_template(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Tuple[Document, Document]:
    return load_root_document(
        get_blade_template_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
    )


def get_blade_template_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath("Blades", "Blade_Template.FCStd")


def load_alernator(recompute_all=False) -> Document:
    return load_document(get_alternator_document_path, recompute_all=recompute_all)


def get_alternator_document_path(documents_path: Path) -> Path:
    return documents_path.joinpath("Alternator", "Alternator.FCStd")
