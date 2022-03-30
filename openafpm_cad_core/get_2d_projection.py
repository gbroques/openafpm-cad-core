import Draft
import FreeCAD as App
from FreeCAD import Placement, Vector

__all__ = ['get_2d_projection']


def get_2d_projection(obj: object) -> object:
    # Reset Placement of object,
    # as objects not aligned with the XY plane are exported to DXF incorrectly.
    # See Also: https://forum.freecadweb.org/viewtopic.php?p=539543
    original_placement = obj.Placement
    obj.Placement = Placement()
    projection = None
    if obj.Label == 'Tail_Stop_HighEnd':
        projection = get_2d_high_end_stop_projection(obj)
    else:
        projection = get_2d_projection_on_xy_plane(obj)
    obj.Placement = original_placement
    return projection


def get_2d_projection_on_xy_plane(obj: object) -> object:
    """Create a 2D projection of the object via the Draft workbench.

    Assumes the flat face of the object is aligned with the XY plane,
    along the z-axis.

    See Also:
        https://wiki.freecadweb.org/Draft_Shape2DView
    """
    document = obj.Document
    App.setActiveDocument(document.Name)
    shape = Draft.makeShape2DView(obj, Vector(0, 0, 1))
    document.recompute()
    return shape


def get_2d_high_end_stop_projection(obj: object) -> object:
    """The High End Stop requires special care when exporting to DXF.
    Create a 2D projection of the second to largest face via the Draft workbench.

    See Also:
        https://wiki.freecadweb.org/Draft_Shape2DView
    """
    document = obj.Document
    faces = obj.Shape.Faces
    App.setActiveDocument(document.Name)
    second_to_largest_face = sorted(
        faces, key=lambda f: f.Area, reverse=True)[1]
    index = None
    for i, face in enumerate(faces, start=1):
        if face.isEqual(second_to_largest_face):
            index = i
            break
    shape = Draft.makeShape2DView(
        obj, Vector(1, 0, 0), facenumbers=[index - 1])
    shape.ProjectionMode = 'Individual Faces'
    document.recompute()
    return shape
