"""
FreeCAD macro to create spreadsheet controlling Wind Turbine model.
"""
import FreeCADGui as Gui
from openafpm_cad_core.app import create_spreadsheet_document
from openafpm_cad_core.gui import CreateSpreadsheetTaskPanel


def on_close(magnafpm_parameters,
             furling_parameters,
             user_parameters):
    return create_spreadsheet_document(
        'Master_of_Puppets',
        magnafpm_parameters,
        furling_parameters,
        user_parameters)


Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel(
    'Select Wind Turbine Variant', on_close)
Gui.Control.showDialog(panel)
