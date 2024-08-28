"""
FreeCAD macro to view magnets aligning with coil holes.

See 'Winding Type' section at https://www.openafpm.net/design-tips for details.
"""
import FreeCAD as App
import FreeCADGui as Gui

from openafpm_cad_core.app import find_object_by_label


def find_descendent_by_label(obj, label: str):
    if obj.Label == label:
        return obj
    elif obj.TypeId == 'App::Link':
        return find_descendent_by_label(obj.LinkedObject, label)
    elif is_link_array(obj):
        return find_descendent_by_label(obj.Base, label)
    elif obj.TypeId == 'App::Part':
        for child in obj.Group:
            grandchild = find_descendent_by_label(child, label)
            if grandchild:
                return grandchild


def is_link_array(obj: object) -> bool:
    return (
        obj.TypeId == 'Part::FeaturePython' and
        hasattr(obj, 'ArrayType')
    )


documents_by_name = App.listDocuments()
if not App.GuiUp:
    message = 'Gui must be up to run this macro.'
    App.Console.PrintWarning(message)
    raise SystemExit(message)
elif 'Alternator' not in documents_by_name:
    App.Console.PrintWarning('Alternator document must be open.')
else:
    alternator_document = documents_by_name['Alternator']
    App.setActiveDocument(alternator_document.Name)
    alternator_document.openTransaction('view_coil_magnet_alignment')

    parts_to_hide = [
        ('Blade_Assembly_FrontTriangle', None),
        ('Blade_Assembly_BackDisk', None),
        ('Rotor_Front', None),
        ('Stator', 'ResinCast'),
        ('Rotor_Back', 'Rotor_ResinCast')
    ]

    for part, descendent in parts_to_hide:
        obj_to_hide = find_object_by_label(alternator_document, part)
        if descendent:
            obj_to_hide = find_descendent_by_label(obj_to_hide, descendent)
        obj_to_hide.ViewObject.Visibility = False

    stator = find_object_by_label(alternator_document, 'Stator')
    coil = find_descendent_by_label(stator, 'Coil')
    coil.ViewObject.Transparency = 80

    Gui.runCommand('Std_ViewRight')
    Gui.runCommand('Std_ViewRotateLeft')

    alternator_document.commitTransaction()
