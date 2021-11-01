from pathlib import Path

import FreeCAD as App

from .create_spreadsheet_document import create_spreadsheet_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_model import WindTurbineModel

__all__ = ['load_turbine']


def load_turbine(magnafpm_parameters: MagnafpmParameters,
                 furling_parameters: FurlingParameters,
                 user_parameters: UserParameters) -> WindTurbineModel:
    spreadsheet_document_name = 'Master_of_Puppets'
    spreadsheet_document = create_spreadsheet_document(spreadsheet_document_name,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    package_path = Path(__file__).parent.absolute()
    documents_path = package_path.joinpath('documents')

    spreadsheet_document_path = documents_path.joinpath(
        f'{spreadsheet_document_name}.FCStd')
    # TODO: Saving the spreadsheet document might create a race condition
    #       in a multi-user or concurrent environment.
    #       In practice, this doesn't seem to be causing issues.
    #       If it does present a problem, one solution would be to remove
    #       all XLinks to the Master_of_Puppets document, and remove the saveAs below.
    #       FreeCAD then throws errors that the "Linked document is not saved".
    #       These errors are neglible, and everything still works correctly.
    #       To get rid of the errors, we could make the Spreadsheet document a temporary document,
    #       but temporary documents don't show up in the Tree view.
    spreadsheet_document.saveAs(str(spreadsheet_document_path))

    root_document_name = 'WindTurbine'
    root_document_path = documents_path.joinpath(f'{root_document_name}.FCStd')
    root_document = App.openDocument(str(root_document_path))
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

    return WindTurbineModel(root_document, spreadsheet_document)
