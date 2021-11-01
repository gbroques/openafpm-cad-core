import os
from pathlib import Path
from typing import Dict, List

import FreeCAD as App
from FreeCAD import Document

from .gui_document import (get_gui_document_by_path,
                           rekey_gui_document_by_path, write_gui_documents)

__all__ = ['save_documents']


def save_documents(root_document_name: str,
                   spreadsheet_document_name: str,
                   source: Path,
                   destination: Path) -> None:
    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)

    save_and_reopen_spreadsheet_document(
        spreadsheet_document_name, destination)

    documents = get_part_documents(spreadsheet_document_name)

    destination_by_source = save_document_copies_and_close(
        source, destination, documents)

    reopen_and_save_documents(root_document_name, destination)

    source_paths = get_part_document_paths(
        source, spreadsheet_document_name)

    gui_document_by_source = get_gui_document_by_path(source_paths)

    gui_document_by_destination = rekey_gui_document_by_path(
        gui_document_by_source, destination_by_source)

    write_gui_documents(gui_document_by_destination)


def save_document_copies_and_close(source: Path,
                                   destination: Path,
                                   documents: List[Document]) -> Dict[str, str]:
    destination_by_source = {}
    for document in documents:
        document_source = document.FileName
        document_destination = get_destination_path(
            document_source, source, destination)
        if not document_destination.parent.exists():
            document_destination.parent.mkdir(parents=True, exist_ok=True)
        document.saveCopy(str(document_destination))
        destination_by_source[document_source] = str(document_destination)
        App.closeDocument(document.Name)
    return destination_by_source


def save_and_reopen_spreadsheet_document(spreadsheet_document_name: str, destination: Path) -> Document:
    spreadsheet_document = App.listDocuments()[spreadsheet_document_name]
    spreadsheet_document_filename = f'{spreadsheet_document_name}.FCStd'
    spreadsheet_document_path = destination.joinpath(
        spreadsheet_document_filename)
    spreadsheet_document.saveAs(str(spreadsheet_document_path))
    App.closeDocument(spreadsheet_document_name)
    spreadsheet_document = App.openDocument(str(spreadsheet_document_path))
    return spreadsheet_document


def reopen_and_save_documents(root_document_name: str, destination: Path) -> List[Document]:
    root_document = str(destination.joinpath(f'{root_document_name}.FCStd'))
    App.openDocument(root_document)
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = document_by_name.values()
    for document in documents:
        document.save()
    return documents


def get_destination_path(document_source: str,
                         source: Path,
                         destination: Path) -> Path:
    ending_path = str(document_source).replace(
        str(source) + os.path.sep, '')
    return destination.joinpath(ending_path)


def get_part_documents(spreadsheet_document_name: str) -> List[Document]:
    """Part documents are any document containing parts (i.e. not the main spreadsheet document)."""
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = document_by_name.values()
    return [
        d for d in documents
        if d.Name != spreadsheet_document_name
    ]


def get_part_document_paths(base_path: Path,
                            spreadsheet_document_name: str) -> List[Path]:
    """Part documents are any document containing parts (i.e. not the main spreadsheet document)."""
    return [
        p for p in list(base_path.glob('**/*.FCStd'))
        if p.stem != spreadsheet_document_name
    ]
