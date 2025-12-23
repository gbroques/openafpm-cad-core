from pathlib import Path
from typing import List, Tuple
import FreeCAD
import Part


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


def create_airfoil_wire(coordinates: List[Tuple[float, float]]) -> Part.Wire:
    """Create FreeCAD Wire from airfoil coordinates"""
    points = [FreeCAD.Vector(x, 0, y) for x, y in coordinates]

    # Check if airfoil is closed (first and last points match)
    first_point = points[0]
    last_point = points[-1]
    is_closed = first_point.distanceToPoint(last_point) < 0.001

    # Create BSpline curve (not closed to preserve sharp trailing edge)
    spline = Part.BSplineCurve()
    spline.interpolate(points, False)  # False to avoid smoothing trailing edge
    edge = spline.toShape()

    if not is_closed:
        # Add sharp closing line from last point to first point
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
) -> Part.Feature:
    # Calculate z positions internally
    z_top_end = thickness - drop_end
    z_bottom_right_end = max(0, z_top_end - thick_end)
    
    chord_length = wood_width - (wood_width - W) * (y_end / blade_radius)
    z_bottom_end = thickness - thick_end

    # Only create the 4 vertices needed for the cross-section wire at y_end
    v1 = FreeCAD.Vector(
        W - chord_length, y_end, z_bottom_right_end
    )  # Trailing edge bottom
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)  # Leading edge bottom
    v3 = FreeCAD.Vector(W, y_end, thickness)  # Leading edge top
    v4 = FreeCAD.Vector(W - chord_length, y_end, z_top_end)  # Trailing edge top

    # Create cross-section wire
    back_wire = Part.makePolygon([v2, v1, v4, v3, v2])
    return Part.show(back_wire, name)


# Load airfoil coordinates and create wire
# USNPS4 airfoil: http://airfoiltools.com/airfoil/details?airfoil=usnps4-il
W = 50  # Distance from leading edge to center
coordinates = load_airfoil_coordinates(Path(__file__).parent / "USNPS4.dat")
reflected_coordinates = flip_airfoil_coordinates_vertically(coordinates)
flipped_coordinates = flip_airfoil_coordinates_horizontally(reflected_coordinates)
scaled_coordinates = scale_airfoil_coordinates(
    flipped_coordinates, 100.0
)  # 100mm chord
translated_coordinates = translate_airfoil_coordinates(scaled_coordinates, W)
wire = create_airfoil_wire(translated_coordinates)

# Show in FreeCAD
if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

Part.show(wire, "USNPS4_Airfoil")
print(
    f"Created airfoil wire with {len(translated_coordinates)} coordinates, chord length: 100mm"
)

# Copy blade section creation logic from create_root.py
blade_radius = 1200  # mm
wood_width = 200  # root width
thickness = 40  # z dimension
num_sections = 6
section_length = blade_radius / num_sections
drops = [40, 32, 15, 7, 3, 1]  # mm
thicknesses = [27, 27, 19, 14, 9, 6]  # mm

# Create blade sections from station 5 to tip (y=400 to y=1200)
section_names = ["Section_5", "Section_4", "Section_3", "Section_2", "Tip"]

for i in range(1, num_sections):  # i=1,2,3,4,5 (y=200,400,600,800,1000,1200)
    y_end = (i + 1) * section_length
    thick_end = thicknesses[i]
    drop_end = drops[i]

    # Create cross-section at y_end
    create_section(
        y_end,
        thick_end,
        drop_end,
        section_names[i - 1],
        W,
        wood_width,
        blade_radius,
        thickness,
    )

print("Created blade section wires from station 5 to tip")
