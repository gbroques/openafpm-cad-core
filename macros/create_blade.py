from pathlib import Path
from typing import List, Tuple, Optional
import FreeCAD
import Part
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

    # Step 6: Create wire
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
        Part.show(
            create_airfoil_wire_at_section(
                airfoil_coordinates,
                chord_length,
                y_end,
                W,
                thickness,
                rotation_angle,
                W,
                thickness,
            ),
            f"{name}_Airfoil",
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
drops = [40, 32, 15, 7, 3, 1]  # mm
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
