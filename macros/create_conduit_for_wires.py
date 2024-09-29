"""
Creates a cylinder representing electrical conduit,
a tube used to protect and route the wires for the Stator Coils.

Use this when the Stator Mold is loaded.

The tube will be smaller than the notch for the resin to
flow out and support it's connection to the stator.

The resin around the tube could collide with the resin on the magnet disk.
Thus, this macro also loads the rotor resin cast.
"""
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core.app import find_object_by_label


def recompute_document(document):
    for obj in document.Objects:
        obj.touch()
        obj.recompute()
    document.recompute(None, True, True)


documents_by_name = App.listDocuments()
if not App.GuiUp:
    message = 'Gui must be up to run this macro.'
    App.Console.PrintWarning(message)
    raise SystemExit(message)
elif 'Stator_Mold_Assembly' not in documents_by_name:
    App.Console.PrintWarning('Stator_Mold_Assembly document must be open.')
else:
    main_document = documents_by_name['Master_of_Puppets']
    stator_mold_assembly_document = documents_by_name['Stator_Mold_Assembly']
    stator_mold_lid_document = documents_by_name['Stator_Mold_Lid']

    stator_mold_assembly_path = Path(stator_mold_assembly_document.FileName)
    rotor_resin_cast_path = str(
        stator_mold_assembly_path.parents[2].joinpath('Rotor/Rotor_ResinCast.FCStd'))
    rotor_resin_cast_document = App.open(rotor_resin_cast_path)
    recompute_document(rotor_resin_cast_document)
    App.setActiveDocument(stator_mold_assembly_document.Name)
    stator_mold_assembly_document.openTransaction('conduit_for_wires')

    rotor_resin_cast = find_object_by_label(
        rotor_resin_cast_document, 'Rotor_ResinCast')
    rotor_resin_cast_link = stator_mold_assembly_document.addObject(
        'App::Link', 'Rotor_ResinCast_Link')
    rotor_resin_cast_link.setLink(rotor_resin_cast)

    height = stator_mold_lid_document.Spreadsheet.StatorThickness
    x = -stator_mold_lid_document.Spreadsheet.PocketX
    y = -stator_mold_lid_document.Spreadsheet.PocketY
    z = stator_mold_assembly_document.Spreadsheet.LidZ
    distance_between_layers = stator_mold_assembly_document.Spreadsheet.DistanceBetweenLayers

    rotor_resin_cast_link.Placement.Base.z = z - distance_between_layers * 0.5
    rotor_resin_cast_link.recompute()

    tube = stator_mold_assembly_document.addObject('Part::Cylinder', 'Tube')
    tube_diameter = main_document.Alternator.WireTubeDiameter
    tube.Radius = tube_diameter / 2
    tube.Height = height
    tube.Placement.Base.x = x
    tube.Placement.Base.y = y
    tube.Placement.Base.z = z
    tube.ViewObject.ShapeColor = (1.0, 1.0, 1.0, 0.0)

    stator_mold_lid = find_object_by_label(
        stator_mold_assembly_document, 'Stator_Mold_Lid')
    stator_mold_lid.ViewObject.Transparency = 100

    stator_mold_assembly_document.recompute()

    Gui.ActiveDocument.ActiveView.viewTop()
    stator_mold_assembly_document.commitTransaction()
