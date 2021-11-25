from pathlib import Path

import FreeCAD as App
from FreeCAD import Document

from .create_spreadsheet_document import create_spreadsheet_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_model import WindTurbineModel

__all__ = ['load_turbine']


def load_turbine(magnafpm_parameters: MagnafpmParameters,
                 furling_parameters: FurlingParameters,
                 user_parameters: UserParameters) -> WindTurbineModel:
    spreadsheet_document_name = 'Master_of_Puppets'
    spreadsheet_document = create_spreadsheet_document(spreadsheet_document_name,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    documents_path = get_documents_path()

    save_document(spreadsheet_document,
                  documents_path,
                  spreadsheet_document_name)

    root_document_name = 'WindTurbine'
    root_document = open_document(documents_path, root_document_name)
    recompute_document(spreadsheet_document)

    recompute_all_documents()

    return WindTurbineModel(root_document, spreadsheet_document)


def get_documents_path() -> Path:
    package_path = Path(__file__).parent.absolute()
    return package_path.joinpath('documents')


def open_document(path: Path, document_name: str) -> Document:
    document_path = path.joinpath(f'{document_name}.FCStd')
    return App.openDocument(str(document_path))


def save_document(document: Document, path: Path, document_name: str):
    document_path = path.joinpath(f'{document_name}.FCStd')
    document.saveAs(str(document_path))


def recompute_all_documents() -> None:
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = document_by_name.values()
    for document in documents:
        recompute_document(document)


def recompute_document(document: Document) -> None:
    for obj in document.Objects:
        obj.recompute()
    document.recompute(None, True, True)
