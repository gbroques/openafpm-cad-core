import time
from typing import Dict, List
import zipfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

__all__ = ['get_gui_document_by_path',
           'rekey_gui_document_by_path',
           'write_gui_documents']


def get_gui_document_by_path(document_paths: List[Path]) -> Dict[str, bytes]:
    gui_document_by_path = {}
    for path in document_paths:
        with ZipFile(path, 'r') as fcstd:
            try:
                with fcstd.open('GuiDocument.xml') as gui_document:
                    gui_document_contents = gui_document.read()
                    gui_document_by_path[str(path)] = gui_document_contents
            except KeyError as key_error:
                print(f'No GuiDocument.xml in Document ${path}')
                # TODO: Replace print statement with add_note feature available in Python 3.11
                # see https://peps.python.org/pep-0678/
                # key_error.add_note(f'No GuiDocument.xml in Document ${path}')
                raise
    return gui_document_by_path


def rekey_gui_document_by_path(gui_document_by_source: Dict[str, bytes],
                               destination_by_source: Dict[str, str]) -> Dict[str, str]:
    gui_document_by_new_path = {}
    for source, gui_document_contents in gui_document_by_source.items():
        destination = destination_by_source[source]
        gui_document_by_new_path[destination] = gui_document_contents
    return gui_document_by_new_path


def write_gui_documents(gui_document_by_path: Dict[str, bytes]) -> None:
    for path, gui_document_contents in gui_document_by_path.items():
        gui_document_path = zipfile.Path(path, at='GuiDocument.xml')
        if gui_document_path.exists():
            continue
        with ZipFile(path, 'a', ZIP_DEFLATED) as fcstd:
            member = ZipInfo('GuiDocument.xml', time.localtime()[:6])
            member.compress_type = ZIP_DEFLATED
            fcstd.writestr(member, gui_document_contents)
