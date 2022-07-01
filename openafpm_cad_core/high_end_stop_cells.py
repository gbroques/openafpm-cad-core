from typing import List, Tuple

from .create_placement_cells import create_placement_cells
from .spreadsheet import Alignment, Cell, Style

__all__ = ['high_end_stop_cells']


def calculate_y_of_ellipse(point_on_plane: Tuple[str, str, str],
                           normal_vector_to_plane: Tuple[str, str, str],
                           center_of_cylinder: Tuple[str, str],
                           radius_of_cylinder: str,
                           angle: str,
                           alias: str) -> Cell:
    Px, Py, Pz = point_on_plane
    Nx, Ny, Nz = normal_vector_to_plane
    Cx, Cz = center_of_cylinder
    r = radius_of_cylinder
    v = angle
    return Cell(f'=({Px} * {Nx} + {Py} * {Ny} + {Pz} * {Nz} - {Cx} * {Nx} - {Cz} * {Nz} - {Nx} * {r} * cos({v}) - {Nz} * {r} * sin({v})) / {Ny}',
                alias=alias)


high_end_stop_cells: List[List[Cell]] = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('FlatMetalThickness'),
        Cell('BoomPipeRadius'),
        Cell('YawPipeDiameter')
    ],
    [
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.BoomPipeRadius',
             alias='BoomPipeRadius'),
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter')
    ],
    [
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle')
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle')
    ],
    [
        Cell('Tail', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('Chamfer'),
        Cell('LowEndStopPlacement'),
        Cell('LowEndStopLengthToYawPipe')
    ],
    [
        Cell('=Tail.TailHingeJunctionChamfer',
             alias='Chamfer'),
        Cell('=Tail.LowEndStopPlacement',
             alias='LowEndStopPlacement'),
        Cell('=Tail.LowEndStopLengthToYawPipe',
             alias='LowEndStopLengthToYawPipe')
    ],
    [
        Cell('WindTurbine', styles=[Style.UNDERLINE])
        # ------------------------------------------
    ],
    [
        Cell('YawBearingPlacement'),
        Cell('TailAssemblyLinkPlacement'),
    ],
    [
        Cell('=WindTurbine.YawBearingPlacement',
             alias='YawBearingPlacement'),
        Cell('=WindTurbine.TailAssemblyLinkPlacement',
             alias='TailAssemblyLinkPlacement')
    ],
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('HighEndStopPlaneLength')
    ],
    [
        Cell('110',  # The exact length of this isn't very important.
             alias='HighEndStopPlaneLength')
    ],
    [
        Cell('FurlAxis'),
        Cell('FurlAngle'),
        Cell('FurlRotation')
    ],
    [
        Cell('=create(<<vector>>; sin(VerticalPlaneAngle); 0; cos(VerticalPlaneAngle))',
             alias='FurlAxis'),
        Cell('=105deg',
             alias='FurlAngle'),
        Cell('=create(<<rotation>>; FurlAxis; FurlAngle)',
             alias='FurlRotation')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
    ],
    # Placement
    # ---------
    [
        Cell('Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    *create_placement_cells(name='TailAssembly',
                            base=(
                                '=Chamfer * cos(180 - HorizontalPlaneAngle)',
                                '=Chamfer * sin(-(180 - HorizontalPlaneAngle))',
                                '0'),
                            axis=('0', '0', '-1'),
                            angle='=180 - HorizontalPlaneAngle'),
    *create_placement_cells(name='OuterTailHinge',
                            base=(
                                '=Tail.OuterTailHingeX',
                                '0',
                                '=Tail.OuterTailHingeZ'),
                            axis=('0', '1', '0'),
                            angle='=VerticalPlaneAngle'),
    # TailBoomVaneAssemblyLink
    *create_placement_cells(name='Tail',
                            base=(
                                '=Tail.TailX',
                                '=Tail.TailY',
                                '=Tail.TailZ'),
                            axis=('0', '0', '1'),
                            angle='=Tail.TailAngle'),
    *create_placement_cells(name='TailBoomVaneAssembly',
                            base=('0', '0', '0'),
                            axis=('0', '1', '0'),
                            angle='90'),
    *create_placement_cells(name='OuterTailHingeHighEndStop',
                            base=(
                                '=FlatMetalThickness / 2',
                                '=BoomPipeRadius',
                                '0'),
                            axis=('0', '1', '0'),
                            angle='-90'),
    [
        Cell('OppositeEnd', styles=[Style.ITALIC]),
    ],
    [
        Cell('x', horizontal_alignment=Alignment.RIGHT),
        Cell('y', horizontal_alignment=Alignment.RIGHT),
        Cell('z', horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('=OuterTailHingeHighEndStopX',
             alias='OuterTailHingeHighEndStopOppositeEndX'),
        Cell('=OuterTailHingeHighEndStopY',
             alias='OuterTailHingeHighEndStopOppositeEndY'),
        Cell('=HighEndStopPlaneLength',
             alias='OuterTailHingeHighEndStopOppositeEndZ'),
    ],
    [
        Cell('Base'),
        Cell('Placement')
    ],
    [
        Cell('=create(<<vector>>; OuterTailHingeHighEndStopOppositeEndX; OuterTailHingeHighEndStopOppositeEndY; OuterTailHingeHighEndStopOppositeEndZ)',
             alias='OuterTailHingeHighEndStopOppositeEndBase'),
        Cell('=create(<<placement>>; OuterTailHingeHighEndStopOppositeEndBase; OuterTailHingeHighEndStopRotation)',
             alias='OuterTailHingeHighEndStopOppositeEndPlacement')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('TailFurlBase'),
        Cell('TailFurlPlacement'),
        Cell('FurledHighEndStopGlobalParentPlacement'),
    ],
    [
        # C - rot.multVec(C)
        Cell('=.OuterTailHingeBase - FurlRotation * .OuterTailHingeBase',
             alias='TailFurlBase'),
        Cell('=create(<<placement>>; TailFurlBase; FurlRotation)',
             alias='TailFurlPlacement'),
        Cell('=TailAssemblyLinkPlacement * TailAssemblyPlacement * TailFurlPlacement * TailPlacement * TailBoomVaneAssemblyPlacement',
             alias='FurledHighEndStopGlobalParentPlacement')
    ],
    [
        Cell('OuterTailHingeHighEndStopFurledPlacement'),
        Cell('OuterTailHingeHighEndStopOppositeEndFurledPlacement')
    ],
    [
        Cell('=FurledHighEndStopGlobalParentPlacement * OuterTailHingeHighEndStopPlacement',
             alias='OuterTailHingeHighEndStopFurledPlacement'),
        Cell('=FurledHighEndStopGlobalParentPlacement * OuterTailHingeHighEndStopOppositeEndPlacement',
             alias='OuterTailHingeHighEndStopOppositeEndFurledPlacement')
    ],
    [
        Cell('OuterTailHingeHighEndStopFurledBase'),
        Cell('OuterTailHingeHighEndStopOppositeEndFurledBase')
    ],
    [
        Cell('=OuterTailHingeHighEndStopFurledPlacement.Base',
             alias='OuterTailHingeHighEndStopFurledBase'),
        Cell('=OuterTailHingeHighEndStopOppositeEndFurledPlacement.Base',
             alias='OuterTailHingeHighEndStopOppositeEndFurledBase')
    ],
    [
        Cell('References', styles=[Style.ITALIC, Style.UNDERLINE])
    ],
    [
        Cell('Finding a point on a 3d line',
             styles=[Style.ITALIC]),
        Cell('What is the equation for a 3D line?',
             styles=[Style.ITALIC]),
    ],
    [
        Cell('https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154'),
        Cell('https://math.stackexchange.com/questions/404440/what-is-the-equation-for-a-3d-line/404446#404446')
    ],
    [
        Cell('Zgiven'),
        # T is a reserved alias since FreeCAD 20.
        Cell('TT'),
        Cell('HighEndStopPointWhereZEqualsZgiven'),
        Cell('HighEndStopWidth', styles=[Style.BOLD, Style.UNDERLINE])
    ],
    [
        # Center of Yaw Bearing
        Cell('=YawBearingPlacement.Base.z', alias='Zgiven'),
        # TT = Zgiven - Az / (Bz - Az)
        # See above "Finding a point on a 3d line" answer.
        Cell('=(Zgiven - .OuterTailHingeHighEndStopFurledBase.z) / (.OuterTailHingeHighEndStopOppositeEndFurledBase.z - .OuterTailHingeHighEndStopFurledBase.z)',
             alias='TT'),
        Cell('=.OuterTailHingeHighEndStopFurledBase + TT * (.OuterTailHingeHighEndStopOppositeEndFurledBase - .OuterTailHingeHighEndStopFurledBase)',
             alias='HighEndStopPointWhereZEqualsZgiven'),
        Cell('=abs(.HighEndStopPointWhereZEqualsZgiven.x) - YawPipeRadius + YawBearingPlacement.Base.x',
             alias='HighEndStopWidth')  # 57.12 desired for T Shape
    ],
    # SafetyCatch
    # -----------
    [
        Cell('SafetyCatch', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('SafetyCatchWidth'),
        Cell('=YawPipeRadius * 1.67',
             alias='SafetyCatchWidth')
    ],
    [
        Cell('SafetyCatchLength'),
        Cell('=YawPipeRadius * 1.33',
             alias='SafetyCatchLength'),
        Cell(),
        # This note applies to entire right column, used to calculate LowerPointWhereZEqualsZgiven.
        Cell('Used in High End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection',
             styles=[Style.ITALIC])
    ],
    # ASCII drawings of high end stop planes for understanding below aliases (e.g. UpperBottomLeftCorner).
    #
    # Upper plane farthest from ground, seen from top view of turbine.
    # Lower plane closest to the ground, seen from bottom view of turbine.
    #
    # ::
    #
    #         Upper
    #     - - - - - - -
    #     | \         | \\
    #     |   \       |   \\
    #     - - - - - - -     \\
    #       \     \     \     \\
    #         \     - - - - - - -
    #           \   |       \   |
    #             \ |         \ |
    #               - - - - - - -
    #                   Lower
    #
    # 3D ASCII Drawing Source: https://1j01.github.io/ascii-hypercube/
    #
    # Both Lower and Upper planes have Top, Left, Right, and Bottom sides.
    # Top is farthest from the hinge, and closest to the vane.
    # Bottom is closest to the hinge, and farthest from the vane.
    # Left is closest to the yaw bearing, and farthest from boom (in furled position).
    # Right is farthest from the yaw bearing, and closest to the boom (in furled position).
    #
    # ::
    #
    #              Top
    #          ┌─────────┐          ^
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #     Left │         │ Right    |  HighEndStopPlaneLength
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          └─────────┘          v
    #            Bottom
    #
    # 2D ASCII Drawing Source: https://asciiflow.com/legacy/
    [
        # of High End Stop
        Cell('UpperBottomLeftCorner'),
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; 0)',
             alias='UpperBottomLeftCorner'),
        Cell('LowerBottomLeftCorner'),
        Cell('=create(<<vector>>; FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; 0)',
             alias='LowerBottomLeftCorner')
    ],
    [
        Cell('UpperBottomLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * UpperBottomLeftCorner',
             alias='UpperBottomLeftCornerGlobal'),
        Cell('UpperBottomLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * LowerBottomLeftCorner',
             alias='LowerBottomLeftCornerGlobal')
    ],
    [
        # of High End Stop
        Cell('UpperTopLeftCorner'),
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; HighEndStopPlaneLength)',
             alias='UpperTopLeftCorner'),
        Cell('LowerTopLeftCorner'),
        Cell('=create(<<vector>>; FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; HighEndStopPlaneLength)',
             alias='LowerTopLeftCorner')
    ],
    [
        Cell('UpperTopLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * UpperTopLeftCorner',
             alias='UpperTopLeftCornerGlobal'),
        Cell('UpperTopLeftCornerGlobal'),
        Cell('=FurledHighEndStopGlobalParentPlacement * LowerTopLeftCorner',
             alias='LowerTopLeftCornerGlobal')
    ],
    [
        # Zgiven
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Zupper'),
        Cell('=YawBearingPlacement.Base.z + (SafetyCatchWidth / 2)',
             alias='Zupper')
    ],
    [
        # T
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Tupper'),
        Cell('=(Zupper - .UpperBottomLeftCornerGlobal.z) / (.UpperTopLeftCornerGlobal.z - .UpperBottomLeftCornerGlobal.z)',
             alias='Tupper'),
        Cell('Tlower'),
        Cell('=(Zgiven - .LowerBottomLeftCornerGlobal.z) / (.LowerTopLeftCornerGlobal.z - .LowerBottomLeftCornerGlobal.z)',
             alias='Tlower')
    ],
    [
        Cell('SafetyCatchPosition'),
        Cell('=.UpperBottomLeftCornerGlobal + Tupper * (UpperTopLeftCornerGlobal - .UpperBottomLeftCornerGlobal)',
             alias='SafetyCatchPosition'),
        Cell('LowerPointWhereZEqualsZgiven'),
        Cell('=.LowerBottomLeftCornerGlobal + Tlower * (.LowerTopLeftCornerGlobal - .LowerBottomLeftCornerGlobal)',
             alias='LowerPointWhereZEqualsZgiven')
    ],
    [
        Cell('SafetyCatchYPadding'),
        Cell('12', alias='SafetyCatchYPadding')
    ],
    [
        # Y position of the safety catch
        # Plus padding for a little extra clearance.
        Cell('SafetyCatchY'),
        Cell('=.SafetyCatchPosition.y + SafetyCatchYPadding',
             alias='SafetyCatchY')
    ],
    # High End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection
    # ------------------------------------------------------------------
    # Calculate an ellipse to make the High End Stop fit the outer pipe of the Yaw Bearing.
    [
        Cell('High End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('InverseFurledHighEndStopGlobalParentPlacement')
    ],
    [
        Cell('=minvert(.FurledHighEndStopGlobalParentPlacement)',
             alias='InverseFurledHighEndStopGlobalParentPlacement')
    ],
    [
        # Calculate two vectors, Va and Vb, on the High End Stop plane.
        Cell('Va'), Cell('Vb')
    ],
    [
        Cell('=OuterTailHingeHighEndStopOppositeEndFurledBase - OuterTailHingeHighEndStopFurledBase',
             alias='Va'),
        Cell('=LowerBottomLeftCornerGlobal - OuterTailHingeHighEndStopFurledBase',
             alias='Vb')
    ],
    [
        # Cross product Va and Vb to find vector perpendicular to the High End Stop plane, Vc.
        # https://en.wikipedia.org/wiki/Cross_product
        Cell('Vc'),
        Cell('Va × Vb')
    ],
    [
        Cell('=create(<<vector>>; .Va.y * .Vb.z - .Va.z * .Vb.y; .Va.z * .Vb.x - .Va.x * .Vb.z; .Va.x * .Vb.y - .Va.y * .Vb.x)',
             alias='Vc'),
        Cell('Cross Product', styles=[Style.ITALIC])
    ],
    [
        # Normalize Vc from step above.
        Cell('Vn'),
        Cell('Normalize Vc')
    ],
    [
        Cell('=Vc / .Vc.Length', alias='Vn')
    ],
    # Relate the equations for a cylinder and plane together,
    # to find the ellipse of intersection.
    #
    # Cylinder Equation (where height is in Y-direction):
    #
    #   (x-h)^2 + (z-k)^2 - r^2 = 0
    #
    #   Where (h, k) is the center of the cylinder,
    #   and r is the radius.
    #
    # Plane Equation:
    #
    #   m * (x - a) + n * (y - b) + o * (z - c) = 0
    #
    #   Where (m, n, o) is a normal vector to the plane (i.e. perpendicular),
    #   and (a, b, c) is a point on the plane.
    #
    # Height of Yaw Bearing cylinder is in Y-direction, so we solve for y.
    #
    # Using WolframAlpha:
    # https://www.wolframalpha.com/input/?i=m+*+%28x+-+a%29+%2B+n+*+%28y+-+b%29+%2B+o+*+%28z+-+c%29+%3D+%28x-h%29%5E2+%2B+%28z-k%29%5E2+-+r%5E2+in+terms+of+y
    #
    # y = (a m + b n + c o + h^2 - 2 h x + k^2 - 2 k z - m x - o z - r^2 + x^2 + z^2) / n and n!=0
    #
    # Next, substitute values for x and z to create a function of v,
    # where v is the angle (in degrees) of a cross-section of the cylinder.
    #
    # See "Curve of Intersection - A Cylinder and a Plane" YouTube video for explanation,
    #     https://www.youtube.com/watch?v=ds3MrMUz3Z0
    #
    # Using WolframAlpha
    # https://www.wolframalpha.com/input/?i=%28a+m+%2B+b+n+%2B+c+o+%2B+h%5E2+-+2+h+x+%2B+k%5E2+-+2+k+z+-+m+x+-+o+z+-+r%5E2+%2B+x%5E2+%2B+z%5E2%29+%2F+n+where+x+%3D+r+cos%28v%29+%2B+h+and+z+%3D+r+sin%28v%29+%2B+k
    #
    # y = (a m + b n + c o - h m - k o - m r cos(v) - o r sin(v)) / n
    #
    #   Used in calculate_y_of_ellipse function above.
    #
    # Setup short aliases for use in equations.
    [
        Cell('(r)adius'),
    ],
    [
        Cell('=YawPipeRadius', alias='r')
    ],
    [
        # Center of Cylinder (h, k)
        # h and k are reserved aliases.
        Cell('Cx'), Cell('Cz'), Cell('(C)enter')
    ],
    [
        Cell('=YawBearingPlacement.Base.x', alias='Cx'),
        Cell('=YawBearingPlacement.Base.z', alias='Cz')
    ],
    [
        Cell('(P)oint, (u)pper plane'),
        Cell('(P)oint, (l)ower plane')
    ],
    [
        Cell('Pu'),
        Cell('Pl')
    ],
    [
        Cell('=UpperBottomLeftCornerGlobal', alias='Pu'),
        Cell('=LowerBottomLeftCornerGlobal', alias='Pl')
    ],
    [
        # Y-value for Upper vertex of ellipse.
        Cell('Yu (upper)'),
        # Y-value for Lower vertex of ellipse.
        Cell('Yl (lower)')
    ],
    [
        calculate_y_of_ellipse(
            ('.Pu.x', '.Pu.y', '.Pu.z'),
            ('.Vn.x', '.Vn.y', '.Vn.z'),
            ('Cx', 'Cz'),
            'r',
            '90',
            'Yu'),
        calculate_y_of_ellipse(
            ('.Pl.x', '.Pl.y', '.Pl.z'),
            ('.Vn.x', '.Vn.y', '.Vn.z'),
            ('Cx', 'Cz'),
            'r',
            '-90',
            'Yl')
    ],
    [
        Cell('3 Points of Ellipse', styles=[Style.ITALIC])
    ],
    [
        Cell('EllipseUpperVertexGlobal'),
        Cell('EllipseLowerVertexGlobal'),
        Cell('EllipseLowerCoVertexGlobal')
    ],
    [
        Cell('=create(<<vector>>; Cx; Yu; Cz + r)',
             alias='EllipseUpperVertexGlobal'),
        Cell('=create(<<vector>>; Cx; Yl; Cz - r)',
             alias='EllipseLowerVertexGlobal'),
        # Point where High End Stop touches Yaw Bearing.
        Cell('=LowerPointWhereZEqualsZgiven',
             alias='EllipseLowerCoVertexGlobal')
    ],
    [
        # Convert to "local" Tail_Stop_HighEnd coordinate system.
        # For use in Sketcher constraints.
        # The lower and upper vertexes (1 and 2) form the major axis.
        # The lower co-vertex (3) forms the minor axis.
        # 1, 2, and 3 numbering correspond to the following description:
        # https://wiki.freecadweb.org/Sketcher_CreateEllipseBy3Points
        #
        # Vertexes denoted by "x".
        #
        #          ^                         , - ~ ~~~ ~ - ,
        #          |                     , '                 ' ,
        #          |                   ,                         ,
        #          |                  ,                           ,
        #          |    Lower Vertex ,                             , Upper Vertex
        #  Y-axis  |            <- - x - - - - - - - - - - - - - - x - ->
        #          |                 ,         Major Axis          ,
        #          |                  ,                           ,
        #          |                   ,                         ,
        #          |                     ,                    , '
        #          |                       ' - , _ _x_ _ ,  '
        #          |
        #          |                          Lower Co-vertex
        #          |
        #          +-------------------------------------------------------------->
        #                                        X-axis
        #
        Cell('EllipseUpperVertexLocal'),
        Cell('EllipseLowerVertexLocal'),
        Cell('EllipseLowerCoVertexLocal')
    ],
    [
        Cell('=InverseFurledHighEndStopGlobalParentPlacement * EllipseUpperVertexGlobal - OuterTailHingeHighEndStopBase',
             alias='EllipseUpperVertexLocal'),
        Cell('=InverseFurledHighEndStopGlobalParentPlacement * EllipseLowerVertexGlobal - OuterTailHingeHighEndStopBase',
             alias='EllipseLowerVertexLocal'),
        Cell('=InverseFurledHighEndStopGlobalParentPlacement * EllipseLowerCoVertexGlobal - OuterTailHingeHighEndStopBase',
             alias='EllipseLowerCoVertexLocal')
    ],
    # Low End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection
    # ------------------------------------------------------------------
    # Calculate an ellipse to make the Low End Stop fit the outer pipe of the Yaw Bearing.
    [
        Cell('Low End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('OuterLowEndStopWidth'),
        Cell('LowEndStopWidth')
    ],
    [
        Cell('=YawPipeRadius * 0.5',
             alias='OuterLowEndStopWidth'),
        Cell('=YawPipeRadius + OuterLowEndStopWidth',
             alias='LowEndStopWidth')
    ],
    [
        Cell('LowEndStopGlobalPlacement'),
        Cell('LowEndStopGlobalBase')
    ],
    [
        Cell('=TailAssemblyLinkPlacement * TailAssemblyPlacement * OuterTailHingePlacement * LowEndStopPlacement',
             alias='LowEndStopGlobalPlacement'),
        Cell('=.LowEndStopGlobalPlacement.Base',
             alias='LowEndStopGlobalBase')
    ],
    [
        # Front, Bottom, Left correspond to X, Y, and Z
        # Relative to Tail_Stop_LowEnd
        Cell('FrontBottomLeftLowEndStopPlanePoint'),
        Cell('FrontBottomLeftLowEndStopPlanePointGlobal')
    ],
    [
        Cell('=create(<<vector>>; 0; -LowEndStopLengthToYawPipe; 0)',
             alias='FrontBottomLeftLowEndStopPlanePoint'),
        Cell('=LowEndStopGlobalPlacement * FrontBottomLeftLowEndStopPlanePoint',
             alias='FrontBottomLeftLowEndStopPlanePointGlobal')
    ],
    [
        # Back, Bottom, Right correspond to X, Y, and Z
        # Relative to Tail_Stop_LowEnd
        Cell('BackBottomRightLowEndStopPlanePoint'),
        Cell('BackBottomRightLowEndStopPlanePointGlobal')
    ],
    [
        Cell('=create(<<vector>>; LowEndStopWidth; 0; 0)',
             alias='BackBottomRightLowEndStopPlanePoint'),
        Cell('=LowEndStopGlobalPlacement * BackBottomRightLowEndStopPlanePoint',
             alias='BackBottomRightLowEndStopPlanePointGlobal')
    ],
    [
        # Calculate two vectors, Vd and Ve, on the Low End Stop plane.
        Cell('Vd'), Cell('Ve')
    ],
    [
        Cell('=FrontBottomLeftLowEndStopPlanePointGlobal - LowEndStopGlobalBase',
             alias='Vd'),
        Cell('=BackBottomRightLowEndStopPlanePointGlobal - LowEndStopGlobalBase',
             alias='Ve')
    ],
    [
        # Cross product Vd and Ve to find vector perpendicular to the Low End Stop plane, Vf.
        # https://en.wikipedia.org/wiki/Cross_product
        Cell('Vf'),
        Cell('Vd × Ve')
    ],
    [
        Cell('=create(<<vector>>; .Vd.y * .Ve.z - .Vd.z * .Ve.y; .Vd.z * .Ve.x - .Vd.x * .Ve.z; .Vd.x * .Ve.y - .Vd.y * .Ve.x)',
             alias='Vf'),
        Cell('Cross Product', styles=[Style.ITALIC])
    ],
    [
        # Normalize Vf from step above.
        Cell('Vo'),
        Cell('Normalize Vf')
    ],
    [
        Cell('=Vf / .Vf.Length', alias='Vo')
    ],
    [
        Cell('Point on Yaw Bearing cylinder where Low End Stop touches it')
    ],
    [
        Cell('=Cx - FrontBottomLeftLowEndStopPlanePointGlobal.x',
             alias='x'),
        Cell('=Cz - FrontBottomLeftLowEndStopPlanePointGlobal.z',
             alias='y')
    ],
    [
        Cell('Theta'),
        Cell('Alpha'),
        Cell('Beta')
    ],
    [
        Cell('=atan2(y; x)',
             alias='Theta'),
        Cell('=Theta + 90deg',
             alias='Alpha'),
        Cell('=Theta - 90deg',
             alias='Beta')
    ],
    [
        # Y-value for Upper vertex of ellipse.
        Cell('Uy (Upper y)'),
        # Y-value for Lower vertex of ellipse.
        Cell('Ly (Lower y)')
    ],
    [
        calculate_y_of_ellipse(
            ('.LowEndStopGlobalBase.x', '.LowEndStopGlobalBase.y',
             '.LowEndStopGlobalBase.z'),
            ('.Vo.x', '.Vo.y', '.Vo.z'),
            ('Cx', 'Cz'),
            'r',
            'Alpha',
            'Uy'),
        calculate_y_of_ellipse(
            ('.LowEndStopGlobalBase.x', '.LowEndStopGlobalBase.y',
             '.LowEndStopGlobalBase.z'),
            ('.Vo.x', '.Vo.y', '.Vo.z'),
            ('Cx', 'Cz'),
            'r',
            'Beta',
            'Ly')
    ],
    [
        Cell('3 Points of Ellipse', styles=[Style.ITALIC])
    ],
    [
        Cell('LowEndStopEllipseUpperVertexGlobal'),
        Cell('LowEndStopEllipseLowerVertexGlobal'),
        Cell('LowEndStopEllipseLowerCoVertexGlobal')
    ],
    [
        Cell('=create(<<vector>>; Cx + r * cos(Alpha); Uy; Cz + r * sin(Alpha))',
             alias='LowEndStopEllipseUpperVertexGlobal'),
        Cell('=create(<<vector>>; Cx + r * cos(Beta); Ly; Cz + r * sin(Beta))',
             alias='LowEndStopEllipseLowerVertexGlobal'),
        # Point where Low End Stop touches Yaw Bearing.
        Cell('=FrontBottomLeftLowEndStopPlanePointGlobal',
             alias='LowEndStopEllipseLowerCoVertexGlobal')
    ],
    [
        Cell('InverseLowEndStopGlobalPlacement')
    ],
    [
        Cell('=minvert(LowEndStopGlobalPlacement)',
             alias='InverseLowEndStopGlobalPlacement')
    ],
    [
        # Convert to "local" Tail_Stop_LowEnd coordinate system.
        # For use in Sketcher constraints.
        # The lower and upper vertexes (1 and 2) form the major axis.
        # The lower co-vertex (3) forms the minor axis.
        # 1, 2, and 3 numbering correspond to the following description:
        # https://wiki.freecadweb.org/Sketcher_CreateEllipseBy3Points
        #
        # Vertexes denoted by "x".
        #
        #          ^                         , - ~ ~~~ ~ - ,
        #          |                     , '                 ' ,
        #          |                   ,                         ,
        #          |                  ,                           ,
        #          |    Lower Vertex ,                             , Upper Vertex
        #  Y-axis  |            <- - x - - - - - - - - - - - - - - x - ->
        #          |                 ,         Major Axis          ,
        #          |                  ,                           ,
        #          |                   ,                         ,
        #          |                     ,                    , '
        #          |                       ' - , _ _x_ _ ,  '
        #          |
        #          |                          Lower Co-vertex
        #          |
        #          +-------------------------------------------------------------->
        #                                        X-axis
        #
        Cell('LowEndStopEllipseUpperVertexLocal'),
        Cell('LowEndStopEllipseLowerVertexLocal'),
        Cell('LowEndStopEllipseLowerCoVertexLocal')
    ],
    [
        Cell('=InverseLowEndStopGlobalPlacement * LowEndStopEllipseUpperVertexGlobal',
             alias='LowEndStopEllipseUpperVertexLocal'),
        Cell('=InverseLowEndStopGlobalPlacement * LowEndStopEllipseLowerVertexGlobal',
             alias='LowEndStopEllipseLowerVertexLocal'),
        Cell('=InverseLowEndStopGlobalPlacement * LowEndStopEllipseLowerCoVertexGlobal',
             alias='LowEndStopEllipseLowerCoVertexLocal')
    ]
]
