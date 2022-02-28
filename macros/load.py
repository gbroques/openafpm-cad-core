"""
FreeCAD macro to load wind turbine.
"""
import FreeCADGui as Gui
from openafpm_cad_core.gui import CreateSpreadsheetTaskPanel

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant')
Gui.Control.showDialog(panel)
