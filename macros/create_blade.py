from pathlib import Path
from typing import List, Tuple, Optional
import FreeCAD
import Part
import Draft
import math


def calculate_chord_length(
    wood_width: float, W: float, y_position: float, blade_radius: float
) -> float:
    """Calculate chord length at given y position using linear taper"""
    return wood_width - (wood_width - W) * (y_position / blade_radius)


def calculate_station_position(station_number: int, section_length: float) -> float:
    """Calculate y position for given station number"""
    return station_number * section_length


def calculate_trailing_edge_x(W: float, chord_length: float) -> float:
    """Calculate trailing edge x position"""
    return W - chord_length


def create_boundary_vertices(trailing_edge_x: float, W: float, thickness: float, drop_end: float, y_position: float) -> Tuple[FreeCAD.Vector, FreeCAD.Vector, FreeCAD.Vector, FreeCAD.Vector]:
    """Create boundary trapezoid vertices for hybrid airfoil mapping"""
    v_trailing = FreeCAD.Vector(W, y_position, 0.0)  # Leading edge at z=0
    v_root_bottom = FreeCAD.Vector(trailing_edge_x, y_position, 0.0)  # Trailing edge at z=0
    v_root_top = FreeCAD.Vector(trailing_edge_x, y_position, thickness - drop_end)  # Trailing edge top
    v_leading_top = FreeCAD.Vector(W, y_position, thickness)  # Leading edge top
    return v_trailing, v_root_bottom, v_root_top, v_leading_top


def find_z_zero_crossing_idx(poles: List) -> Optional[int]:
    """Find index where airfoil crosses Z=0 (from negative to positive)"""
    return next(
        (i for i in range(len(poles) - 1) if poles[i].z < 0 and poles[i + 1].z >= 0),
        None,
    )


def find_crossing_indices(poles: List, boundary_z_base: float, slope: float, trailing_edge_x: float) -> Tuple[Optional[int], Optional[int]]:
    """Find Z=0 crossing and boundary crossing indices in airfoil poles"""
    # Find Z=0 crossing
    z_crossing_idx = None
    for i in range(len(poles) - 1):
        if poles[i].z < 0 and poles[i + 1].z >= 0:
            z_crossing_idx = i
            break
    
    # Find boundary crossing using slanted line equation
    boundary_crossing_idx = None
    for i in range(len(poles) - 1):
        current_z = boundary_z_base + slope * (poles[i].x - trailing_edge_x)
        next_z = boundary_z_base + slope * (poles[i + 1].x - trailing_edge_x)
        
        if poles[i].z < current_z and poles[i + 1].z >= next_z:
            boundary_crossing_idx = i
            break
    
    return z_crossing_idx, boundary_crossing_idx


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
    # Step 1: Scale first (before flattening)
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Step 2: Flatten using all bottom points on scaled airfoil
    # Find all bottom surface points from trailing edge to end
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    all_bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Use NumPy for linear regression on all bottom points
    import numpy as np

    x_coords = [x for x, z in all_bottom_points]
    z_coords = [z for x, z in all_bottom_points]
    slope, intercept = np.polyfit(x_coords, z_coords, 1)
    flatten_angle = -math.degrees(math.atan(slope))

    bottom_most_point = min(scaled_coordinates, key=lambda p: p[1])

    # Use airfoil centroid as rotation center
    centroid_x = sum(x for x, z in scaled_coordinates) / len(scaled_coordinates)
    centroid_z = sum(z for x, z in scaled_coordinates) / len(scaled_coordinates)

    flattened_coordinates = rotate_airfoil_coordinates_about_point(
        scaled_coordinates, centroid_x, centroid_z, flatten_angle
    )

    # Recalculate z_shift after rotation to fix vertical positioning
    rotated_min_z = min(z for x, z in flattened_coordinates)
    z_shift = -rotated_min_z
    bottom_aligned_coordinates = [(x, z + z_shift) for x, z in flattened_coordinates]

    # Step 3: Apply flips
    reflected_coordinates = flip_airfoil_coordinates_vertically(
        bottom_aligned_coordinates
    )
    final_coordinates = flip_airfoil_coordinates_horizontally(reflected_coordinates)
    x_translated_coordinates = translate_airfoil_coordinates(
        final_coordinates, x_offset
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
    section_length: float,
    station4_drop: Optional[float] = None,
    station4_thick: Optional[float] = None,
) -> Part.Feature:
    # Calculate z positions internally
    z_top_end = thickness - drop_end
    z_bottom_right_end = max(0, z_top_end - thick_end)

    chord_length_x = calculate_chord_length(wood_width, W, y_end, blade_radius)
    z_bottom_end = thickness - thick_end

    # Calculate actual chord length accounting for z-drop (hypotenuse)
    chord_length = math.sqrt(chord_length_x**2 + drop_end**2)

    # Create airfoil wire
    rotation_angle = math.degrees(math.atan(drop_end / chord_length))

    airfoil_wire = create_airfoil_wire_at_section(
        airfoil_coordinates,
        chord_length,  # Use 3D chord length
        y_end,
        W,
        thickness,
        rotation_angle,
        W,
        thickness,
    )
    # Store wire directly without creating FreeCAD object
    doc = FreeCAD.ActiveDocument
    obj = doc.addObject("Part::Feature", f"{name}_Airfoil")
    obj.Shape = airfoil_wire

    # Check Section_5_Airfoil control points for consistency
    if name == "Section_5":
        # Check B-spline control points
        for edge in airfoil_wire.Edges:
            if hasattr(edge.Curve, "getPoles"):
                poles = edge.Curve.getPoles()
                print(f"Section_5_Airfoil B-spline has {len(poles)} control points")
                break

    # Only create the 4 vertices needed for the cross-section wire at y_end
    v1 = FreeCAD.Vector(
        W - chord_length_x, y_end, z_bottom_right_end
    )  # Trailing edge bottom
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)  # Leading edge bottom
    v3 = FreeCAD.Vector(W, y_end, thickness)  # Leading edge top
    v4 = FreeCAD.Vector(W - chord_length_x, y_end, z_top_end)  # Trailing edge top

    # Create cross-section wire
    back_wire = Part.makePolygon([v2, v1, v4, v3, v2])

    # Root_triangle has an extra vertex for wedge cut
    station_6_y = 1 * section_length  # Station 6 (Root_triangle)
    if y_end == station_6_y:  # First section (Root_triangle)
        # Calculate station positions from blade parameters
        station_5_y = calculate_station_position(
            2, section_length
        )  # Station 5 (section 2)
        station_4_y = calculate_station_position(
            3, section_length
        )  # Station 4 (section 3)
        w5 = calculate_chord_length(wood_width, W, station_5_y, blade_radius)
        w4 = calculate_chord_length(wood_width, W, station_4_y, blade_radius)

        z5_unclamped = (thickness - drop_end) - thick_end
        z4 = (thickness - station4_drop) - station4_thick
        t_term = -z5_unclamped / (z4 - z5_unclamped)
        y_term = station_5_y + t_term * (station_4_y - station_5_y)
        x_term_width = w5 + t_term * (w4 - w5)
        # Calculate wedge cut using connection line intersection logic from twisted tapered plank
        # This is where the wedge connection line intersects at y=200
        y_split = math.sqrt(R2**2 - W**2)  # Cylinder intersection with leading edge
        x_term = W - x_term_width  # Termination x-coordinate
        t_end = (y_end - y_split) / (y_term - y_split) if y_term != y_split else 0
        t_end = max(0, min(1, t_end))
        wedge_cut_x = W + t_end * (x_term - W)  # This gives ~24.41

        v_wedge = FreeCAD.Vector(wedge_cut_x, y_end, 0)  # Wedge cut vertex at z=0

        # Create Root_triangle wire: v2 -> v_wedge -> v1 -> v4 -> v3 -> v2
        # This connects: leading_edge_bottom -> wedge_cut -> root_cut_bottom -> trailing_edge_top -> leading_edge_top -> back
        back_wire = Part.makePolygon([v2, v_wedge, v1, v4, v3, v2])

    Part.show(back_wire, name)
    return obj  # Return the airfoil object


# Main execution
if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

# Load airfoil coordinates
# USNPS4 airfoil: http://airfoiltools.com/airfoil/details?airfoil=usnps4-il
coordinates = load_airfoil_coordinates(Path(__file__).parent / "USNPS4.dat")


# Create hybrid airfoil using distance-based mapping
def create_hybrid_airfoil_section_6b(
    y_position: float,
    thick_end: float,
    drop_end: float,
    W: float,
    wood_width: float,
    blade_radius: float,
    thickness: float,
    airfoil_coordinates: List[Tuple[float, float]],
    root_airfoil: Part.Feature,
):
    """Create hybrid airfoil: leading edge from airfoil, rest mapped to Section_6b wire"""
    fitted_airfoil = root_airfoil

    # Calculate chord length at this y position
    chord_length_x = calculate_chord_length(wood_width, W, y_position, blade_radius)
    trailing_edge_x = calculate_trailing_edge_x(W, chord_length_x)

    # Create boundary vertices for bounds checking
    v_trailing, v_root_bottom, v_root_top, v_leading_top = create_boundary_vertices(
        trailing_edge_x, W, thickness, drop_end, y_position
    )

    # Create closed wire for face
    closed_wire_for_face = Part.makePolygon(
        [v_trailing, v_root_bottom, v_root_top, v_leading_top, v_trailing]
    )

    # Get airfoil control points
    bspline_edge = None
    for edge in fitted_airfoil.Shape.Edges:
        if hasattr(edge.Curve, "getPoles"):
            bspline_edge = edge
            break

    if not bspline_edge:
        print("No B-spline found in airfoil")
        return

    poles = bspline_edge.Curve.getPoles()

    # Create hybrid points
    hybrid_points = []
    leading_edge_preserved = 0
    mapped_points = 0

    # First, create the discretized wires for mapping
    # Calculate where airfoil crosses Z=0 by finding the crossing point dynamically
    crossing_idx = find_z_zero_crossing_idx(poles)

    if crossing_idx is not None:
        p_before, p_after = poles[crossing_idx], poles[crossing_idx + 1]
        t = (
            -p_before.z / (p_after.z - p_before.z)
            if abs(p_after.z - p_before.z) > 1e-10
            else 0
        )
        x_at_z0 = p_before.x + t * (p_after.x - p_before.x)
    else:
        x_at_z0 = 0

    # Calculate where points cross the slanted boundary line dynamically
    trailing_edge_x = W - chord_length_x  # Calculate -125 equivalent
    boundary_z_base = thickness - drop_end  # Z-height at trailing edge
    slope = drop_end / chord_length_x  # Calculate slope from actual parameters

    # Find crossing with slanted boundary: z = boundary_z_base + slope * (x - trailing_edge_x)
    boundary_crossing_idx = next(
        (
            i
            for i in range(len(poles) - 1)
            if (poles[i].z - (boundary_z_base + slope * (poles[i].x - trailing_edge_x)))
            * (
                poles[i + 1].z
                - (boundary_z_base + slope * (poles[i + 1].x - trailing_edge_x))
            )
            < 0
        ),
        None,
    )

    if boundary_crossing_idx is not None:
        p_before, p_after = (
            poles[boundary_crossing_idx],
            poles[boundary_crossing_idx + 1],
        )
        boundary_z_before = boundary_z_base + slope * (p_before.x - trailing_edge_x)
        boundary_z_after = boundary_z_base + slope * (p_after.x - trailing_edge_x)

        if (
            abs((p_after.z - boundary_z_after) - (p_before.z - boundary_z_before))
            > 1e-10
        ):
            t_cross = (p_before.z - boundary_z_before) / (
                (p_before.z - boundary_z_before) - (p_after.z - boundary_z_after)
            )
            x_cross = p_before.x + t_cross * (p_after.x - p_before.x)
            z_cross = p_before.z + t_cross * (p_after.z - p_before.z)
        else:
            x_cross = p_before.x
    else:
        x_cross = trailing_edge_x

    # Create split points
    split1_point = FreeCAD.Vector(x_at_z0, y_position, 0.0)
    split2_point = FreeCAD.Vector(x_cross, y_position, z_cross)

    # Use dynamically found crossing indices as leading edge range
    leading_edge_start = crossing_idx
    leading_edge_end = boundary_crossing_idx

    # Calculate how many points will be preserved (leading edge points in boundary)
    preserved_points = 0
    for i, pole in enumerate(poles):
        if leading_edge_start <= i <= leading_edge_end:  # Use dynamic range
            # Check if point would be in boundary trapezoid
            x, z = pole.x, pole.z
            # Same boundary check logic as below
            if (
                trailing_edge_x <= x <= W and 0 <= z <= thickness
            ):  # Allow full thickness range for preserved points
                preserved_points += 1

    # Calculate discretization to get exactly 81 B-spline control points
    # B-spline interpolation: N input points → N+2 control points
    # We want 81 control points, so we need 79 input points (79 + 2 = 81)
    total_target = len(airfoil_coordinates)  # 79 points for B-spline input
    mapped_points = total_target - preserved_points

    # Calculate wire lengths for proportional distribution
    wire1_start = FreeCAD.Vector(
        trailing_edge_x, y_position, 0.0
    )  # Use calculated trailing edge
    wire1_end = split1_point  # Z=0 crossing point
    wire2_start = split2_point  # Boundary crossing point
    wire2_end = FreeCAD.Vector(
        trailing_edge_x, y_position, thickness - drop_end
    )  # Trailing edge thickness

    wire1_length = wire1_start.distanceToPoint(wire1_end)
    wire2_length = wire2_start.distanceToPoint(wire2_end)
    total_wire_length = wire1_length + wire2_length

    # Distribute mapped points proportionally based on wire lengths
    wire1_ratio = wire1_length / total_wire_length if total_wire_length > 0 else 0.5
    wire1_point_count = max(2, round(mapped_points * wire1_ratio))
    wire2_point_count = max(2, mapped_points - wire1_point_count)

    # Create and discretize Wire 1: from trailing edge bottom to split1_point
    wire1_points = []
    for i in range(wire1_point_count):
        t = i / (wire1_point_count - 1) if wire1_point_count > 1 else 0
        point = wire1_start + t * (wire1_end - wire1_start)
        wire1_points.append(point)

    # Create and discretize Wire 2: from split2_point to trailing edge top
    wire2_points = []
    for i in range(wire2_point_count):
        t = i / (wire2_point_count - 1) if wire2_point_count > 1 else 0
        point = wire2_start + t * (wire2_end - wire2_start)
        wire2_points.append(point)

    # Use geometric bounds checking instead of isInside() function
    def is_point_in_boundary_trapezoid(x, z):
        """Check if point is inside boundary trapezoid using geometric logic"""
        # Boundary X range: trailing_edge_x to W
        if x < trailing_edge_x or x > W:
            return False

        # Boundary Z range: 0 to top_line
        if z < 0.0:
            return False

        # Top boundary line: Z = trailing_edge_z + slope * (X - trailing_edge_x)
        # Calculate slope from trailing edge to leading top
        trailing_edge_z = thickness - drop_end  # Actual trailing edge height
        leading_top_z = thickness
        slope = (leading_top_z - trailing_edge_z) / (W - trailing_edge_x)
        top_z = trailing_edge_z + slope * (x - trailing_edge_x)
        if z > top_z:
            return False

        return True

    for i, pole in enumerate(poles):
        if (
            leading_edge_start <= i <= leading_edge_end
            and is_point_in_boundary_trapezoid(pole.x, pole.z)
        ):
            # Keep leading edge points (blue ones)
            hybrid_points.append(FreeCAD.Vector(pole.x, y_position, pole.z))
            leading_edge_preserved += 1
        else:
            # Map to our new discretized split wires with adjusted mapping
            if i < len(wire1_points):  # Map to Wire1 points
                # Points 0-(wire1_count-1) map directly to Wire1 points
                hybrid_points.append(wire1_points[i])
                mapped_points += 1
            elif i < leading_edge_start:
                # Points 15-18 skip mapping to reduce total count
                pass
            else:
                # Points after leading edge map to Wire2
                post_preserved_index = i - (leading_edge_end + 1)
                if post_preserved_index >= 0 and post_preserved_index < len(
                    wire2_points
                ):
                    hybrid_points.append(wire2_points[post_preserved_index])
                    mapped_points += 1

    # Find X boundaries of preserved leading edge points
    preserved_points = []
    for i, pole in enumerate(poles):
        if (
            leading_edge_start <= i <= leading_edge_end
            and is_point_in_boundary_trapezoid(pole.x, pole.z)
        ):
            preserved_points.append((i, pole.x))

    if preserved_points:
        first_point = preserved_points[0]
        last_point = preserved_points[-1]
        min_x = min(x for _, x in preserved_points)
        max_x = max(x for _, x in preserved_points)
        print(f"Leading edge preserved points:")
        print(f"  First point: index {first_point[0]}, X = {first_point[1]:.3f}")
        print(f"  Last point: index {last_point[0]}, X = {last_point[1]:.3f}")
        print(f"  X range: {min_x:.3f} to {max_x:.3f} (span: {max_x - min_x:.3f}mm)")

    print(
        f"Leading edge preserved: {leading_edge_preserved}, Mapped points: {mapped_points}"
    )

    # No duplicate removal needed since wire2 ends at exact trailing edge
    print(f"Using {len(hybrid_points)} points for B-spline creation")

    # Create hybrid airfoil wire
    # Create B-spline interpolation through points
    spline = Part.BSplineCurve()
    spline.interpolate(hybrid_points, False)
    edge = spline.toShape()

    # Close the trailing edge with a line (like other airfoils)
    first_point = hybrid_points[0]
    last_point = hybrid_points[-1]
    is_closed = first_point.distanceToPoint(last_point) < 0.001

    if not is_closed:
        closing_line = Part.makeLine(last_point, first_point)
        hybrid_wire = Part.Wire([edge, closing_line])
    else:
        hybrid_wire = Part.Wire([edge])

    Part.show(hybrid_wire, f"Hybrid_Airfoil_y{int(y_position)}")
    print(
        f"Created smooth hybrid airfoil B-spline at y={y_position} with {len(hybrid_points)} points (closed with trailing edge line)"
    )
    print(
        f"  Leading edge preserved: {leading_edge_preserved}, Mapped points: {mapped_points}"
    )
    print(f"  Chord length: {chord_length_x:.1f}mm")

    # Check B-spline control points
    for edge in hybrid_wire.Edges:
        if hasattr(edge.Curve, "getPoles"):
            poles = edge.Curve.getPoles()
            print(
                f"Hybrid_Airfoil_y{int(y_position)} B-spline has {len(poles)} control points"
            )
            break


# Blade parameters
W = 50  # Distance from leading edge to center
blade_radius = 1200  # mm
wood_width = 200  # root width
thickness = 40  # z dimension
R2 = 125  # radius of flat circular area on back
num_sections = 6
section_length = blade_radius / num_sections
number_of_station_5_to_6_transitions = 3  # Number of interpolated hybrid sections
minimum_trailing_edge_thickness = 1  # mm
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

    section_obj = create_section(
        y_end,
        thick_end,
        drop_end,
        section_names[i],
        W,
        wood_width,
        blade_radius,
        thickness,
        coordinates,
        section_length,
        drops[2] if i == 0 else None,  # Station 4 drop for Root_triangle
        thicknesses[2] if i == 0 else None,  # Station 4 thickness for Root_triangle
    )

    # Create hybrid airfoil for Root_triangle section
    if i == 0:  # Root_triangle section at y=200
        create_hybrid_airfoil_section_6b(
            y_end,
            thick_end,
            drop_end,
            W,
            wood_width,
            blade_radius,
            thickness,
            coordinates,
            section_obj,  # Pass the airfoil object directly
        )

print("Created blade section wires and airfoils from root triangle to tip")


def create_interpolated_hybrid_section(
    y_position, hybrid_control_points, section5_control_points, section_length
):
    """Create hybrid section by linear interpolation between control points"""
    # Calculate station positions from section_length
    station_6_y = 1 * section_length  # y=200 (Root_triangle/hybrid)
    station_5_y = 2 * section_length  # y=400 (Section_5)

    # station_6_y → weight=1.0 (full hybrid)
    # station_5_y → weight=0.0 (full Section_5)
    weight = (station_5_y - y_position) / (station_5_y - station_6_y)

    interpolated_points = []
    for i in range(len(hybrid_control_points)):
        hybrid_pt = hybrid_control_points[i]
        section5_pt = section5_control_points[i]

        interp_pt = FreeCAD.Vector(
            hybrid_pt.x * weight + section5_pt.x * (1 - weight),
            y_position,  # Y is fixed
            hybrid_pt.z * weight + section5_pt.z * (1 - weight),
        )
        interpolated_points.append(interp_pt)

    # Create B-spline from interpolated points
    spline = Part.BSplineCurve()
    spline.interpolate(interpolated_points, False)
    edge = spline.toShape()

    # Close with trailing edge line
    first_point = interpolated_points[0]
    last_point = interpolated_points[-1]
    closing_line = Part.makeLine(last_point, first_point)
    wire = Part.Wire([edge, closing_line])

    Part.show(wire, f"Hybrid_Airfoil_y{int(y_position)}")
    print(f"Created interpolated hybrid at y={y_position} (weight={weight:.3f})")
    return wire


# Create root hybrid at y=200


# Get control points from hybrid y=200 and Section_5_Airfoil
doc = FreeCAD.ActiveDocument
hybrid_y200 = doc.getObject("Hybrid_Airfoil_y200")
section5_airfoil = doc.getObject("Section_5_Airfoil")

hybrid_control_points = None
section5_control_points = None

if hybrid_y200:
    for edge in hybrid_y200.Shape.Edges:
        if hasattr(edge.Curve, "getPoles"):
            hybrid_control_points = edge.Curve.getPoles()
            break

if section5_airfoil:
    for edge in section5_airfoil.Shape.Edges:
        if hasattr(edge.Curve, "getPoles"):
            section5_control_points = edge.Curve.getPoles()
            break

# Create interpolated intermediate sections
if hybrid_control_points and section5_control_points:
    if len(hybrid_control_points) == len(section5_control_points):
        # Calculate station positions
        station_6_y = 1 * section_length  # Root_triangle position
        station_5_y = 2 * section_length  # Section_5 position

        # Create parametric number of interpolated sections
        for i in range(1, number_of_station_5_to_6_transitions + 1):
            # Evenly distribute positions between station_6_y and station_5_y
            t = i / (number_of_station_5_to_6_transitions + 1)
            y_position = station_6_y + t * (station_5_y - station_6_y)

            create_interpolated_hybrid_section(
                y_position,
                hybrid_control_points,
                section5_control_points,
                section_length,
            )
        print(
            f"Created interpolated hybrids using {len(hybrid_control_points)} control points"
        )
    else:
        print(
            f"Control point count mismatch: hybrid={len(hybrid_control_points)}, section5={len(section5_control_points)}"
        )
else:
    print("Could not extract control points for interpolation")

# Create loft through all sections from root to tip
try:
    doc = FreeCAD.ActiveDocument

    # Collect all sections in order from root to tip
    sections = []
    section_names = [
        "Hybrid_Airfoil_y200",
        "Hybrid_Airfoil_y250",
        "Hybrid_Airfoil_y300",
        "Hybrid_Airfoil_y350",
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
