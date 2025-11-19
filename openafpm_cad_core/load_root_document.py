from pathlib import Path
from typing import Callable, List, Tuple, Optional
import re

import FreeCAD as App
from FreeCAD import Document

from .close_all_documents import close_all_documents
from .get_documents_path import get_documents_path
from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters
from .upsert_spreadsheet_document import upsert_spreadsheet_document

__all__ = ["load_root_document", "load_root_documents", "load_document"]


def load_root_document(
    get_root_document_path: Callable[[Path], Path],
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
    progress_callback=None,
) -> Tuple[List[Document], Document]:
    root_documents, spreadsheet_document = load_root_documents(
        [get_root_document_path],
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
        progress_callback,
    )
    return root_documents[0], spreadsheet_document


def load_root_documents(
    get_root_document_paths: List[Callable[[Path], Path]],
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
    progress_callback=None,
    progress_range=(0, 100),
    cancel_event=None,
) -> Tuple[List[Document], Document]:
    
    scaled_callback = create_scaled_progress_callback(progress_callback, progress_range)
    
    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")
    
    if scaled_callback:
        scaled_callback("Initializing", 0)

    set_preferences()
    spreadsheet_document_name = "Master_of_Puppets"

    documents_path = get_documents_path()

    if scaled_callback:
        scaled_callback("Creating spreadsheet", 5)
    spreadsheet_document_path = documents_path.joinpath(
        f"{spreadsheet_document_name}.FCStd"
    )
    spreadsheet_document = upsert_spreadsheet_document(
        spreadsheet_document_path,
        magnafpm_parameters,
        furling_parameters,
        user_parameters,
        cancel_event,
    )

    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")

    root_documents = []
    total_docs = len(get_root_document_paths)
    for i, get_root_document_path in enumerate(get_root_document_paths):
        if cancel_event is not None and cancel_event.is_set():
            close_all_documents()
            raise InterruptedError("Operation was cancelled")
            
        if scaled_callback:
            progress = 10 + (i * 60 // total_docs)
            doc_name = get_document_name_from_path_function(get_root_document_path)
            scaled_callback(f"Opening documents for {doc_name}", progress)
        document = load_document(get_root_document_path)
        root_documents.append(document)

    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")

    if scaled_callback:
        scaled_callback("Recomputing documents", 70)
    recompute_all_documents(scaled_callback, cancel_event)

    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")

    if scaled_callback:
        scaled_callback("Complete", 100)
    return root_documents, spreadsheet_document


def load_document(
    get_root_document_path: Callable[[Path], Path],
    recompute: bool = False,
    recompute_all: bool = False,
) -> Document:
    documents_path = get_documents_path()
    document = App.openDocument(str(get_root_document_path(documents_path)))
    if recompute:
        recompute_document(document)
    if recompute_all:
        recompute_all_documents()
    return document


def save_document(document: Document, path: Path, document_name: str) -> None:
    document_path = path.joinpath(f"{document_name}.FCStd")
    document.saveAs(str(document_path))


def recompute_all_documents(progress_callback=None, cancel_event=None) -> None:
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = list(document_by_name.values())
    total_docs = len(documents)

    for i, document in enumerate(documents):
        if cancel_event is not None and cancel_event.is_set():
            close_all_documents()
            raise InterruptedError("Operation was cancelled")
            
        if progress_callback:
            progress = 70 + int((i / total_docs) * 25)  # 70-95% range
            progress_callback(f"Recomputing {document.Name}", progress)
        recompute_document(document, cancel_event)


def recompute_document(document: Document, cancel_event=None) -> None:
    for obj in document.Objects:
        if cancel_event is not None and cancel_event.is_set():
            close_all_documents()
            raise InterruptedError("Operation was cancelled")
        obj.recompute()
    
    if cancel_event is not None and cancel_event.is_set():
        close_all_documents()
        raise InterruptedError("Operation was cancelled")
    document.recompute(None, True, True)


def set_preferences():
    # fix error with stator coil not being properly linked to by coil winder
    # because it's opened earlier in a partial state.
    document_preferences = App.ParamGet("User parameter:BaseApp/Preferences/Document")
    document_preferences.SetBool("NoPartialLoading", True)
    # Avoid creating redundant .FCStd1 backup files.
    document_preferences.SetInt("CountBackupFiles", 0)


def get_document_name_from_path_function(get_path_func: Callable[[Path], Path]) -> str:
    """Derive a readable document name from the path function"""
    path = get_path_func(get_documents_path())
    name = path.stem.replace("_", " ")
    # Add spaces before uppercase letters that follow lowercase letters
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", name)


def create_scaled_progress_callback(
    progress_callback: Optional[Callable[[str, int], None]], 
    progress_range: Tuple[int, int]
) -> Optional[Callable[[str, int], None]]:
    """Create a progress callback that scales progress to the given range"""
    if not progress_callback:
        return None
    
    def scaled_callback(stage: str, percent: int) -> None:
        start, end = progress_range
        scaled_percent = start + (percent * (end - start) // 100)
        progress_callback(stage, scaled_percent)
    
    return scaled_callback
