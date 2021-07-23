"""
FreeCAD macro to load wind turbine.
"""

import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core.app import load_turbine
from openafpm_cad_core.gui import CreateSpreadsheetTaskPanel

Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant', load_turbine)
Gui.Control.showDialog(panel)
