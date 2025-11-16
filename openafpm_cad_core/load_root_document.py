from pathlib import Path
from typing import Callable, List, Tuple

import FreeCAD as App
from FreeCAD import Document

from .get_documents_path import get_documents_path
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .upsert_spreadsheet_document import upsert_spreadsheet_document

__all__ = ['load_root_document', 'load_root_documents', 'load_document']


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
    set_preferences()
    spreadsheet_document_name = 'Master_of_Puppets'

    documents_path = get_documents_path()

    spreadsheet_document_path = documents_path.joinpath(f'{spreadsheet_document_name}.FCStd')
    spreadsheet_document = upsert_spreadsheet_document(spreadsheet_document_path,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    root_documents = []
    for get_root_document_path in get_root_document_paths:
        document = load_document(get_root_document_path)
        root_documents.append(document)

    recompute_all_documents()

    return root_documents, spreadsheet_document


def load_document(get_root_document_path: Callable[[Path], Path], recompute = False, recompute_all: bool = False) -> Document:
    documents_path = get_documents_path()
    document = App.openDocument(str(get_root_document_path(documents_path)))
    if recompute:
        recompute_document(document)
    if recompute_all:
        recompute_all_documents()
    return document


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


def set_preferences():
    # fix error with stator coil not being properly linked to by coil winder
    # because it's opened earlier in a partial state.
    document_preferences = App.ParamGet(
        'User parameter:BaseApp/Preferences/Document')
    document_preferences.SetBool('NoPartialLoading', True)
    # Avoid creating redundant .FCStd1 backup files.
    document_preferences.SetInt('CountBackupFiles', 0)
