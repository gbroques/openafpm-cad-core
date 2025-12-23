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
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    x, y = float(parts[0]), float(parts[1])
                    coordinates.append((x, y))
                except ValueError:
                    continue
    return coordinates

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

# Load airfoil coordinates and create wire
# USNPS4 airfoil: http://airfoiltools.com/airfoil/details?airfoil=usnps4-il
coordinates = load_airfoil_coordinates(Path(__file__).parent / 'USNPS4.dat')
wire = create_airfoil_wire(coordinates)

# Show in FreeCAD
if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

Part.show(wire, "USNPS4_Airfoil")
print(f"Created airfoil wire with {len(coordinates)} coordinates")
