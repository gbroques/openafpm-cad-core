"""
FreeCAD macro to load wind turbine and related tools.
"""
import FreeCADGui as Gui
from openafpm_cad_core.gui import LoadAssemblyTaskPanel

Gui.Control.closeDialog()
panel = LoadAssemblyTaskPanel('Load Assembly')
Gui.Control.showDialog(panel)
