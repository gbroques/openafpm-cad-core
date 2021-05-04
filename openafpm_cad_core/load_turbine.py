from pathlib import Path

import FreeCAD as App

from .create_spreadsheet_document import create_spreadsheet_document
from .gui_document import get_gui_document_by_path, write_gui_documents
from .wind_turbine import WindTurbine

__all__ = ['load_turbine']


def load_turbine(magnafpm_parameters: dict,
                 furling_parameters: dict,
                 user_parameters: dict):
    spreadsheet_document = create_spreadsheet_document(
        magnafpm_parameters, furling_parameters, user_parameters)
    package_path = Path(__file__).parent.absolute()
    documents_path = package_path.joinpath('documents')
    gui_document_by_path = get_gui_document_by_path(documents_path)
    spreadsheet_document_path = documents_path.joinpath(
        'Master of Puppets.FCStd')
    spreadsheet_document.saveAs(str(spreadsheet_document_path))
    alternator_document_path = documents_path.joinpath('Alternator.FCStd')
    alternator_document = App.openDocument(str(alternator_document_path))
    for obj in spreadsheet_document.Objects:
        obj.recompute()
    spreadsheet_document.recompute(None, True, True)
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = document_by_name.values()
    for document in documents:
        for obj in document.Objects:
            obj.recompute()
        document.recompute(None, True, True)
        document.save()
    write_gui_documents(gui_document_by_path)
    return WindTurbine(alternator_document)
