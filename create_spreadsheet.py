"""
FreeCAD macro to load wind turbine.
"""

import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core import (CreateSpreadsheetTaskPanel,
                               create_spreadsheet_document)

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant', create_spreadsheet_document)
Gui.Control.showDialog(panel)
