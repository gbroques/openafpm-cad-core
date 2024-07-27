"""Module for loading spreadsheet document."""

from FreeCAD import Document

from .get_documents_path import get_documents_path
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .upsert_spreadsheet_document import upsert_spreadsheet_document

__all__ = ['load_spreadsheet_document']


def load_spreadsheet_document(magnafpm_parameters: MagnafpmParameters,
                              furling_parameters: FurlingParameters,
                              user_parameters: UserParameters) -> Document:
    name = 'Master_of_Puppets'
    documents_path = get_documents_path()
    spreadsheet_document_path = documents_path.joinpath(f'{name}.FCStd')
    return upsert_spreadsheet_document(spreadsheet_document_path,
                                       magnafpm_parameters,
                                       furling_parameters,
                                       user_parameters)
