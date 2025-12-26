from pathlib import Path
from typing import List, Tuple, Optional
import FreeCAD
import Part
import Draft
import math


def load_airfoil_coordinates(filepath: Path) -> List[Tuple[float, float]]:
    """Load airfoil coordinates from .dat file

    Coordinates follow counterclockwise convention:
    - Starts at upper surface trailing edge (x=1.0, y>0)
    - Goes to leading edge (x=0.0)
    - Continues to lower surface trailing edge (x=1.0, y<0)

    See: https://m-selig.ae.illinois.edu/ads/coord_seligFmt_fig/airfoilCoordinatesSm.png
    """
    coordinates = []
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    x, y = float(parts[0]), float(parts[1])
                    coordinates.append((x, y))
                except ValueError:
                    continue
    return coordinates


def scale_airfoil_coordinates(
    coordinates: List[Tuple[float, float]], chord_length: float
) -> List[Tuple[float, float]]:
    """Scale airfoil coordinates by chord length"""
    return [(x * chord_length, y * chord_length) for x, y in coordinates]


def flip_airfoil_coordinates_vertically(
    coordinates: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """Flip airfoil coordinates vertically (negate y-values)"""
    return [(x, -y) for x, y in coordinates]


def flip_airfoil_coordinates_horizontally(
    coordinates: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """Flip airfoil coordinates horizontally (negate x-values)"""
    return [(-x, y) for x, y in coordinates]


def translate_airfoil_coordinates(
    coordinates: List[Tuple[float, float]], x_offset: float
) -> List[Tuple[float, float]]:
    """Translate airfoil coordinates along x-axis"""
    return [(x + x_offset, y) for x, y in coordinates]


def rotate_airfoil_coordinates_about_point(
    coordinates: List[Tuple[float, float]],
    center_x: float,
    center_z: float,
    angle_deg: float,
) -> List[Tuple[float, float]]:
    """Rotate airfoil coordinates about a specific point in x-z plane"""
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated = []
    for x, z in coordinates:
        # Translate to origin
        x_rel = x - center_x
        z_rel = z - center_z

        # Rotate (positive angle rotates counterclockwise)
        x_rot = x_rel * cos_a - z_rel * sin_a
        z_rot = x_rel * sin_a + z_rel * cos_a

        # Translate back
        x_new = x_rot + center_x
        z_new = z_rot + center_z
        rotated.append((x_new, z_new))

    return rotated


def create_airfoil_wire_at_section(
    coordinates: List[Tuple[float, float]],
    chord_length: float,
    y_position: float,
    x_offset: float,
    z_offset: float,
    rotation_angle: float = 0.0,
    rotation_center_x: Optional[float] = None,
    rotation_center_z: Optional[float] = None,
) -> Part.Wire:
    """Create airfoil wire at specified blade section

    Args:
        coordinates: Raw airfoil coordinates from .dat file
        chord_length: Desired chord length (mm)
        y_position: Y position along blade (mm)
        x_offset: X translation (mm)
        z_offset: Z translation (mm)
        rotation_angle: Additional rotation angle (degrees)
        rotation_center_x: X center for rotation (defaults to x_offset)
        rotation_center_z: Z center for rotation (defaults to z_offset)
    """
    # Step 1: Flatten using linear regression
    min_z = min(z for _, z in coordinates)
    tolerance = 0.010
    bottom_points = [(x, z) for x, z in coordinates if abs(z - min_z) < tolerance]

    n = len(bottom_points)
    sum_x = sum(x for x, _ in bottom_points)
    sum_z = sum(z for _, z in bottom_points)
    sum_xz = sum(x * z for x, z in bottom_points)
    sum_x2 = sum(x * x for x, _ in bottom_points)

    denominator = n * sum_x2 - sum_x * sum_x
    slope = (n * sum_xz - sum_x * sum_z) / denominator
    flatten_angle = -math.degrees(math.atan(slope))

    bottom_most_point = min(coordinates, key=lambda p: p[1])
    flattened_coordinates = rotate_airfoil_coordinates_about_point(
        coordinates, bottom_most_point[0], bottom_most_point[1], flatten_angle
    )

    z_shift = -bottom_most_point[1]
    bottom_aligned_coordinates = [(x, z + z_shift) for x, z in flattened_coordinates]

    # Step 2: Apply flips
    reflected_coordinates = flip_airfoil_coordinates_vertically(
        bottom_aligned_coordinates
    )
    flipped_coordinates = flip_airfoil_coordinates_horizontally(reflected_coordinates)

    # Step 3: Scale and position
    scaled_coordinates = scale_airfoil_coordinates(flipped_coordinates, chord_length)
    x_translated_coordinates = translate_airfoil_coordinates(
        scaled_coordinates, x_offset
    )

    # Step 4: Convert to 3D and apply z_offset
    xyz_coordinates = [
        (x, y_position, z + z_offset) for x, z in x_translated_coordinates
    ]

    # Step 5: Apply additional rotation if specified
    if rotation_angle != 0.0:
        center_x = rotation_center_x if rotation_center_x is not None else x_offset
        center_z = rotation_center_z if rotation_center_z is not None else z_offset
        # Convert back to 2D for rotation, then back to 3D
        xz_coordinates = [(x, z) for x, _, z in xyz_coordinates]
        rotated_coordinates = rotate_airfoil_coordinates_about_point(
            xz_coordinates, center_x, center_z, rotation_angle
        )
        xyz_coordinates = [(x, y_position, z) for x, z in rotated_coordinates]

    # Step 6: Create wire and measure leading edge overshoot
    points = [FreeCAD.Vector(x, y, z) for x, y, z in xyz_coordinates]
    spline = Part.BSplineCurve()
    spline.interpolate(points, False)
    temp_wire = Part.Wire([spline.toShape()])

    # Measure leading edge overshoot
    actual_leading_x = temp_wire.BoundBox.XMax
    leading_overshoot = actual_leading_x - x_offset

    # Shift all coordinates back by the overshoot amount
    if leading_overshoot > 0:
        xyz_coordinates = [(x - leading_overshoot, y, z) for x, y, z in xyz_coordinates]

    # Create final wire with corrected coordinates
    points = [FreeCAD.Vector(x, y, z) for x, y, z in xyz_coordinates]
    spline = Part.BSplineCurve()
    spline.interpolate(points, False)
    edge = spline.toShape()

    first_point = points[0]
    last_point = points[-1]
    is_closed = first_point.distanceToPoint(last_point) < 0.001

    if not is_closed:
        closing_line = Part.makeLine(last_point, first_point)
        return Part.Wire([edge, closing_line])
    else:
        return Part.Wire([edge])


def create_discretized_root_triangle(
    y_end,
    name,
    W,
    chord_length_x,
    z_top_end,
    z_bottom_right_end,
    thickness,
    thick_end,
    num_discretization_points,
    duplicate_end_point_offset=0.001,
):
    """Create discretized root triangle with 79 points + 2 duplicate endpoints = 81 points"""

    print(
        f"Root triangle parameters: z_top_end={z_top_end}, z_bottom_right_end={z_bottom_right_end}"
    )

    # Define the 4 quadrilateral vertices (same as cross-section wire)
    z_bottom_end = thickness - thick_end
    v1 = FreeCAD.Vector(
        W - chord_length_x, y_end, z_bottom_right_end
    )  # Trailing edge bottom
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)  # Leading edge bottom
    v3 = FreeCAD.Vector(W, y_end, thickness)  # Leading edge top
    v4 = FreeCAD.Vector(W - chord_length_x, y_end, z_top_end)  # Trailing edge top

    print(f"Quadrilateral vertices: v1={v1}, v2={v2}, v3={v3}, v4={v4}")

    # Create wire with Draft.make_fillet for rounded corners
    # Create FreeCAD objects for the edges (will be deleted)
    edge1_obj = Part.show(Part.makeLine(v1, v2), f"{name}_Edge1")
    edge2_obj = Part.show(Part.makeLine(v2, v3), f"{name}_Edge2")
    edge3_obj = Part.show(Part.makeLine(v3, v4), f"{name}_Edge3")

    fillet_radius = 8.0

    # First fillet: bottom corner
    filleted_corner1 = Draft.make_fillet(
        [edge1_obj, edge2_obj], radius=fillet_radius, delete=False
    )

    # Fillet produces 3 edges: [trimmed_edge1, rounded_corner, trimmed_edge2]
    # The last edge (index 2) connects to v3
    connecting_edge = filleted_corner1.Shape.Edges[2]

    # Second fillet: top corner (delete intermediate objects automatically)
    connecting_edge_obj = Part.show(connecting_edge, f"{name}_ConnectingEdge")
    filleted_corner2 = Draft.make_fillet(
        [connecting_edge_obj, edge3_obj], radius=fillet_radius, delete=True
    )

    # Combine edges: first two edges from corner1 + all edges from corner2
    complete_edges = []
    complete_edges.extend(filleted_corner1.Shape.Edges[:2])  # First two edges (exclude connecting edge)
    complete_edges.extend(filleted_corner2.Shape.Edges)      # All edges from second fillet

    # Create and show the final discretization wire
    open_filleted_wire = Part.Wire(complete_edges)
    Part.show(open_filleted_wire, f"{name}_Discretization_Wire")
    print(
        f"Created filleted discretization wire: {len(open_filleted_wire.Edges)} edges"
    )

    # Discretize the filleted wire into points matching airfoil coordinate count
    discretized_points = open_filleted_wire.discretize(num_discretization_points)

    # Convert to FreeCAD Vectors
    points = [FreeCAD.Vector(p.x, p.y, p.z) for p in discretized_points]

    print(f"Discretized {len(points)} points from open wire")

    # Add duplicate endpoints with small offset
    first_point = points[0]
    second_point = points[1]
    last_point = points[-1]
    second_last_point = points[-2]

    # Create duplicate first point slightly between first and second
    duplicate_first = first_point + duplicate_end_point_offset * (second_point - first_point)

    # Create duplicate last point slightly between last and second-to-last
    duplicate_last = last_point + duplicate_end_point_offset * (second_last_point - last_point)

    # Final 81 points: first + duplicate_first + middle points + duplicate_last + last
    final_points = (
        [points[0]] + [duplicate_first] + points[1:-1] + [duplicate_last] + [points[-1]]
    )

    # Create B-spline interpolation from the 81 points at same y position
    # Create B-spline curve through the points using interpolation
    try:
        bspline = Part.BSplineCurve()
        bspline.interpolate(final_points)
        bspline_edge = Part.Edge(bspline)

        # Add closing line from last point to first point (trailing edge)
        first_point = final_points[0]
        last_point = final_points[-1]
        closing_line = Part.makeLine(last_point, first_point)

        # Create closed wire
        bspline_wire = Part.Wire([bspline_edge, closing_line])
        Part.show(bspline_wire, f"{name}_BSpline_Closed")
        print(f"Created closed B-spline wire from {len(final_points)} points at y=200")

        # Delete intermediate objects
        doc = FreeCAD.ActiveDocument
        for obj_name in [
            f"{name}_Edge1",
            f"{name}_Edge2",
            name,
        ]:
            try:
                obj = doc.getObject(obj_name)
                if obj:
                    doc.removeObject(obj_name)
            except:
                pass

        try:
            if filleted_corner1:
                doc.removeObject(filleted_corner1.Name)
            if filleted_corner2:
                doc.removeObject(filleted_corner2.Name)
        except:
            pass

    except Exception as e:
        print(f"Failed to create B-spline: {e}")

    print(
        f"Created discretized {name} with {len(final_points)} points ({num_discretization_points} + 2 duplicates)"
    )
    return final_points


def create_section(
    y_end: float,
    thick_end: float,
    drop_end: float,
    name: str,
    W: float,
    wood_width: float,
    blade_radius: float,
    thickness: float,
    airfoil_coordinates: List[Tuple[float, float]],
) -> Part.Feature:
    # Calculate z positions internally
    z_top_end = thickness - drop_end
    z_bottom_right_end = max(0, z_top_end - thick_end)

    chord_length_x = wood_width - (wood_width - W) * (y_end / blade_radius)
    z_bottom_end = thickness - thick_end

    # Calculate actual chord length accounting for z-drop (hypotenuse)
    chord_length = math.sqrt(chord_length_x**2 + drop_end**2)

    # Create airfoil wire
    rotation_angle = math.degrees(math.atan(drop_end / chord_length))

    # Skip airfoil creation for root triangle (y=200)
    if y_end != 200:
        airfoil_wire = create_airfoil_wire_at_section(
            airfoil_coordinates,
            chord_length,
            y_end,
            W,
            thickness,
            rotation_angle,
            W,
            thickness,
        )
        Part.show(airfoil_wire, f"{name}_Airfoil")
    else:
        # Create discretized root triangle with points matching airfoil + 2 duplicates
        create_discretized_root_triangle(
            y_end,
            name,
            W,
            chord_length_x,
            z_top_end,
            z_bottom_right_end,
            thickness,
            thick_end,
            len(airfoil_coordinates),
        )

    # Only create the 4 vertices needed for the cross-section wire at y_end
    v1 = FreeCAD.Vector(
        W - chord_length_x, y_end, z_bottom_right_end
    )  # Trailing edge bottom
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)  # Leading edge bottom
    v3 = FreeCAD.Vector(W, y_end, thickness)  # Leading edge top
    v4 = FreeCAD.Vector(W - chord_length_x, y_end, z_top_end)  # Trailing edge top

    # Create cross-section wire
    back_wire = Part.makePolygon([v2, v1, v4, v3, v2])
    return Part.show(back_wire, name)


# Main execution
if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

# Load airfoil coordinates
# USNPS4 airfoil: http://airfoiltools.com/airfoil/details?airfoil=usnps4-il
coordinates = load_airfoil_coordinates(Path(__file__).parent / "USNPS4.dat")

# Blade parameters
W = 50  # Distance from leading edge to center
blade_radius = 1200  # mm
wood_width = 200  # root width
thickness = 40  # z dimension
num_sections = 6
section_length = blade_radius / num_sections
minimum_trailing_edge_thickness = 0.1  # mm
drops = [40 - minimum_trailing_edge_thickness, 32, 15, 7, 3, 1]  # mm
thicknesses = [27, 27, 19, 14, 9, 6]  # mm

section_names = [
    "Root_triangle",
    "Section_5",
    "Section_4",
    "Section_3",
    "Section_2",
    "Tip",
]

# Create blade sections from root triangle to tip (y=200 to y=1200)
for i in range(num_sections):  # i=0,1,2,3,4,5 (y=200,400,600,800,1000,1200)
    y_end = (i + 1) * section_length
    thick_end = thicknesses[i]
    drop_end = drops[i]

    create_section(
        y_end,
        thick_end,
        drop_end,
        section_names[i],
        W,
        wood_width,
        blade_radius,
        thickness,
        coordinates,
    )

print("Created blade section wires and airfoils from root triangle to tip")

# Create loft through all sections from root to tip
try:
    doc = FreeCAD.ActiveDocument

    # Collect all sections in order from root to tip
    sections = []
    section_names = [
        "Root_triangle_BSpline_Closed",
        "Section_5_Airfoil",
        "Section_4_Airfoil",
        "Section_3_Airfoil",
        "Section_2_Airfoil",
        "Tip_Airfoil",
    ]

    for section_name in section_names:
        obj = doc.getObject(section_name)
        if obj:
            sections.append(obj)
            print(f"Added {section_name} to loft")
        else:
            print(f"Warning: {section_name} not found")

    if len(sections) >= 2:
        loft = doc.addObject("Part::Loft", "Complete_Blade_Loft")
        loft.Sections = sections
        loft.Solid = True
        loft.Ruled = False
        doc.recompute()
        print(f"Created complete blade loft with {len(sections)} sections")
    else:
        print(f"Not enough sections found for loft: {len(sections)}")

except Exception as e:
    print(f"Failed to create complete loft: {e}")
