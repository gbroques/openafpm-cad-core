import time
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

__all__ = ['get_gui_document_by_path', 'write_gui_documents']


def get_gui_document_by_path(base_path: Path) -> dict:
    document_paths = list(base_path.glob('**/*.FCStd'))

    gui_document_by_path = {}
    for path in document_paths:
        with ZipFile(path, 'r') as fcstd:
            with fcstd.open('GuiDocument.xml') as gui_document:
                gui_document_contents = gui_document.read()
                gui_document_by_path[path] = gui_document_contents
    return gui_document_by_path


def write_gui_documents(gui_document_by_path: dict) -> None:
    for path, gui_document_contents in gui_document_by_path.items():
        with ZipFile(path, 'a', ZIP_DEFLATED) as fcstd:
            member = ZipInfo('GuiDocument.xml', time.localtime()[:6])
            member.compress_type = ZIP_DEFLATED
            fcstd.writestr(member, gui_document_contents)
