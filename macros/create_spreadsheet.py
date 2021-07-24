"""
FreeCAD macro to create spreadsheet that drives wind turbine model.
"""
import FreeCADGui as Gui
from openafpm_cad_core.app import create_spreadsheet_document
from openafpm_cad_core.gui import CreateSpreadsheetTaskPanel

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel(
    'Select Wind Turbine Variant', create_spreadsheet_document)
Gui.Control.showDialog(panel)
