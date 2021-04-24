from pathlib import Path

import FreeCAD as App

from .create_spreadsheet_document import create_spreadsheet_document

__all__ = ['load_turbine']


def load_turbine(magnafpm_parameters: dict,
                 furling_parameters: dict,
                 user_parameters: dict):
    spreadsheet_document = create_spreadsheet_document(
        magnafpm_parameters, furling_parameters, user_parameters)
    package_path = Path(__file__).parent.absolute()
    documents_path = package_path.joinpath('documents', 'common')
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
    for doc in documents:
        for obj in doc.Objects:
            obj.recompute()
        doc.recompute(None, True, True)
