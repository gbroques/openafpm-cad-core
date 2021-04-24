"""
FreeCAD macro to create WindTurbine document
with spreadsheet containing input parameters.
"""

import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core import CreateSpreadsheetTaskPanel


def on_close(spreadsheet_document):
    spreadsheet_document.saveAs(
        '/home/g/.FreeCAD/Mod/openafpm-cad-core/openafpm_cad_core/documents/common/Master of Puppets.FCStd')
    alternator_document = App.openDocument(
        '/home/g/.FreeCAD/Mod/openafpm-cad-core/openafpm_cad_core/documents/common/Alternator.FCStd')
    for obj in spreadsheet_document.Objects:
        obj.recompute()
    spreadsheet_document.recompute(None, True, True)
    sort_in_dependency_order = True
    document_by_name = App.listDocuments(sort_in_dependency_order)
    documents = document_by_name.values()
    for doc in documents:
        for obj in doc.Objects:
            obj.recompute()
        doc.recompute(None, True, True)


Gui.Control.closeDialog()
panel = CreateSpreadsheetTaskPanel('Select Wind Turbine Variant', on_close)
Gui.Control.showDialog(panel)
