"""
FreeCAD macro to calculate global placement of a selected child object.
"""
from FreeCAD import Console, Placement
from FreeCADGui import Selection


def calculate_global_placement(child: object, placements: Placement = []) -> Placement:
    placements.append(child.Placement)
    in_list = child.InList
    num_in = len(in_list)
    if len(in_list) == 0:
        global_placement = Placement()
        placements.reverse()  # Reverse list in order of parent to child.
        for placement in placements:
            global_placement *= placement
        return global_placement
    if num_in > 1:
        Console.PrintWarning(
            f'{child.Label} has more than 1 parent. Choosing 1st.\n')
    parent = in_list[0]
    Console.PrintMessage(f'{parent.Label} ({parent.TypeId})\n')
    return calculate_global_placement(
        parent, placements
    )


selection = Selection.getSelection()

if len(selection) == 0:
    Console.PrintWarning(f'Must select at least 1 object.')
else:
    if len(selection) > 1:
        Console.PrintWarning(f'Selected more than 1 object. Choosing 1st.')

    selected = selection[0]
    global_placement = calculate_global_placement(selected)
    Console.PrintMessage(f'{selected.Label} Global Placement\n')
    Console.PrintMessage(global_placement)
