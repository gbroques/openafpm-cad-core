import os
import shutil
from pathlib import Path
from tempfile import gettempdir
from typing import Dict, List
from uuid import uuid1

import FreeCAD as App
from FreeCAD import Document

from .gui_document import (get_gui_document_by_path,
                           rekey_gui_document_by_path, write_gui_documents)
from .load import load_all
from .make_archive import make_archive
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['create_archive']


def create_archive(magnafpm_parameters: MagnafpmParameters,
                   furling_parameters: FurlingParameters,
                   user_parameters: UserParameters) -> bytes:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters,
        furling_parameters,
        user_parameters)
    wind_turbine_document = root_documents[0]
    document_source = Path(wind_turbine_document.FileName).parent
    archive_source = Path(gettempdir()).joinpath(
        str(uuid1())).joinpath('WindTurbine')
    archive_source.mkdir(parents=True)

    # Save documents to where the archive will be created from first.
    save_documents(
        root_documents,
        spreadsheet_document.Name,
        source=document_source,
        destination=archive_source)

    archive_destination = Path(archive_source).joinpath('WindTurbine.zip')
    bytes_content = make_archive(
        str(archive_source), str(archive_destination))
    # Delete the directory the archive was created from.
    shutil.rmtree(archive_source)
    return bytes_content


def save_documents(root_documents: List[Document],
                   spreadsheet_document_name: str,
                   source: Path,
                   destination: Path) -> None:
    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)

    spreadsheet_document_path = save_and_close_spreadsheet_document(
        spreadsheet_document_name, destination)

    part_documents = get_part_documents(spreadsheet_document_name)
    source_paths = get_paths(part_documents)

    root_document_filenames = [d.FileName for d in root_documents]
    destination_by_source = save_document_copies_and_close(
        source, destination, part_documents)

    App.openDocument(spreadsheet_document_path)
    reopen_and_save_documents(
        source, destination, root_document_filenames)

    gui_document_by_source = get_gui_document_by_path(source_paths)

    gui_document_by_destination = rekey_gui_document_by_path(
        gui_document_by_source, destination_by_source)

    write_gui_documents(gui_document_by_destination)


def get_paths(documents: List[Document]) -> List[Path]:
    return [Path(d.FileName) for d in documents]


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


def save_and_close_spreadsheet_document(spreadsheet_document_name: str, destination: Path) -> str:
    spreadsheet_document = App.listDocuments()[spreadsheet_document_name]
    spreadsheet_document_filename = f'{spreadsheet_document_name}.FCStd'
    spreadsheet_document_path = destination.joinpath(
        spreadsheet_document_filename)
    spreadsheet_document.saveAs(str(spreadsheet_document_path))
    App.closeDocument(spreadsheet_document_name)
    return str(spreadsheet_document_path)


def reopen_and_save_documents(source: Path, destination: Path, root_document_filenames: List[str]) -> List[Document]:
    for root_document_filename in root_document_filenames:
        root_document_path = get_destination_path(
            root_document_filename, source, destination)
        App.openDocument(str(root_document_path))
    documents = get_open_documents()
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
    documents = get_open_documents()
    return [
        d for d in documents
        if d.Name != spreadsheet_document_name
    ]


def get_open_documents() -> List[Document]:
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    return document_by_name.values()
