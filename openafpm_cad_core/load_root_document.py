from pathlib import Path
from typing import Callable, List, Tuple

import FreeCAD as App
from FreeCAD import Document

from .create_spreadsheet_document import create_spreadsheet_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['load_root_document', 'load_root_documents']


def load_root_document(get_root_document_path: Callable[[Path], Path],
                       magnafpm_parameters: MagnafpmParameters,
                       furling_parameters: FurlingParameters,
                       user_parameters: UserParameters) -> Tuple[List[Document], Document]:
    root_documents, spreadsheet_document = load_root_documents(
        [get_root_document_path],
        magnafpm_parameters,
        furling_parameters,
        user_parameters)
    return root_documents[0], spreadsheet_document


def load_root_documents(get_root_document_paths: List[Callable[[Path], Path]],
                        magnafpm_parameters: MagnafpmParameters,
                        furling_parameters: FurlingParameters,
                        user_parameters: UserParameters) -> Tuple[List[Document], Document]:
    spreadsheet_document_name = 'Master_of_Puppets'
    spreadsheet_document = create_spreadsheet_document(spreadsheet_document_name,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    documents_path = get_documents_path()

    save_document(spreadsheet_document,
                  documents_path,
                  spreadsheet_document_name)
    root_documents = []
    for get_root_document_path in get_root_document_paths:
        document = load_document(get_root_document_path(documents_path))
        root_documents.append(document)

    recompute_all_documents()

    return root_documents, spreadsheet_document


def load_document(document_path: Path) -> Document:
    document = App.openDocument(str(document_path))
    recompute_document(document)
    return document


def get_documents_path() -> Path:
    package_path = Path(__file__).parent.absolute()
    return package_path.joinpath('documents')


def save_document(document: Document, path: Path, document_name: str) -> None:
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
