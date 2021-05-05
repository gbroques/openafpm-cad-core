"""
FreeCAD macro to load wind turbine.
"""

import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core import CreateSpreadsheetTaskPanel, load_turbine

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant', load_turbine)
Gui.Control.showDialog(panel)
