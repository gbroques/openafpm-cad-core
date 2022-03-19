"""
FreeCAD macro to load wind turbine and related assemblies.
"""
import FreeCADGui as Gui
from openafpm_cad_core.gui import CreateSpreadsheetTaskPanel

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Load Assembly')
Gui.Control.showDialog(panel)
