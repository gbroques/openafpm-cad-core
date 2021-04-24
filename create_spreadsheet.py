"""
FreeCAD macro to create document with
spreadsheet containing input parameters.
"""

import FreeCADGui as Gui

from openafpm_cad_core import CreateSpreadsheetTaskPanel

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant')
Gui.Control.showDialog(panel)
