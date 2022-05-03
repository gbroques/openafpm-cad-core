"""
Creates a cylinder representing electrical conduit,
a tube used to protect and route the wires for the Stator Coils.

Use this when the Stator Mold is loaded.

The tube will be smaller than the notch for the resin to
flow out and support it's connection to the stator.

The resin around the tube could collide with the resin on the magnet disk.
"""
import FreeCAD as App

tube_diameter = 20
stator_mold_assembly_document = App.getDocument('Stator_Mold_Assembly')
stator_mold_lid_document = App.getDocument('Stator_Mold_Lid')

height = stator_mold_lid_document.Spreadsheet.StatorThickness
x = -stator_mold_lid_document.Spreadsheet.DistancePocket
y = -stator_mold_lid_document.Spreadsheet.OffsetPocket
z = stator_mold_assembly_document.Spreadsheet.LidZ

tube = stator_mold_assembly_document.addObject('Part::Cylinder', 'Tube')
tube.Radius = tube_diameter / 2
tube.Height = height
tube.Placement.Base.x = x
tube.Placement.Base.y = y
tube.Placement.Base.z = z
tube.ViewObject.ShapeColor = (1.0, 1.0, 1.0, 0.0)
stator_mold_assembly_document.recompute()
