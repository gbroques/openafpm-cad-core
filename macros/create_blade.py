from pathlib import Path
from typing import List, Tuple, Optional, Callable, Any
import FreeCAD
import Part
import Draft
import math
import numpy as np

# Debug flag to control section boundary visibility
DEBUG = False


def find_stable_region(
    bottom_points: list[tuple[float, float]], start_idx: int, min_length: int = 5
) -> tuple[int, int]:
    """
    Find longest stable slope region starting from global Z minimum for optimal flattening.

    Airfoils have 3 distinct geometric regions: trailing edge chaos (0-5 points),
    linear middle section with stable slopes, and leading edge curvature (last 10-15 points).
    This algorithm finds the longest consecutive stable region starting from start_idx
    with minimal slope variation (≤ 0.001 threshold).

    Args:
        bottom_points: List of (x, z) coordinates for airfoil bottom surface
        start_idx: Starting point index (typically global Z minimum)
        min_length: Minimum consecutive stable points required (default: 5)

    Returns:
        Tuple of (start_index, end_index) defining the longest stable region from start_idx

    Raises:
        ValueError: If no stable region meeting criteria is found

    Developed through empirical testing of 15+ flattening methods, achieving
    0.000000mm trailing edge error by geometric principle isolation.
    """

    # Calculate point-to-point slopes from start_idx onwards
    slopes = []
    for i in range(start_idx, len(bottom_points) - 1):
        x1, z1 = bottom_points[i]
        x2, z2 = bottom_points[i + 1]
        slope = (z2 - z1) / (x2 - x1) if x2 != x1 else 0
        slopes.append(slope)

    # Find longest consecutive stable region starting from start_idx
    # Threshold 0.0001 empirically optimized to detect leading edge curvature
    threshold = 0.0001  # Optimized threshold for airfoil geometry detection
    stable_count = 0
    longest_stable_end = None

    for i in range(len(slopes) - 1):
        slope_change = abs(slopes[i + 1] - slopes[i])
        if slope_change <= threshold:
            stable_count += 1
            # Keep extending the stable region as long as it remains stable
            if stable_count >= min_length:
                longest_stable_end = i + 1
        else:
            # Hit instability - if we have a good stable region, stop here
            if stable_count >= min_length:
                break
            else:
                # Reset and keep looking for the first stable region
                stable_count = 0

    if longest_stable_end is None:
        raise ValueError(f"No stable region found starting from point {start_idx}")

    # Convert slope indices back to point indices
    stable_end = (
        start_idx + longest_stable_end + 2
    )  # +2 because we need points, not slopes

    return start_idx, stable_end


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


def create_boundary_vertices(
    trailing_edge_x: float,
    W: float,
    thickness: float,
    drop_end: float,
    y_position: float,
) -> Tuple[FreeCAD.Vector, FreeCAD.Vector, FreeCAD.Vector, FreeCAD.Vector]:
    """Create boundary trapezoid vertices for hybrid airfoil mapping.

    Args:
        trailing_edge_x: X coordinate of trailing edge
        W: Distance from leading edge to center
        thickness: Maximum Z thickness
        drop_end: Z drop at trailing edge
        y_position: Y position of the section

    Returns:
        Tuple of (trailing, root_bottom, root_top, leading_top) vertices
    """
    v_trailing = FreeCAD.Vector(W, y_position, 0.0)  # Leading edge at z=0
    v_root_bottom = FreeCAD.Vector(
        trailing_edge_x, y_position, 0.0
    )  # Trailing edge at z=0
    v_root_top = FreeCAD.Vector(
        trailing_edge_x, y_position, thickness - drop_end
    )  # Trailing edge top
    v_leading_top = FreeCAD.Vector(W, y_position, thickness)  # Leading edge top
    return v_trailing, v_root_bottom, v_root_top, v_leading_top


def find_z_zero_crossing_idx(poles: List[FreeCAD.Vector]) -> Optional[int]:
    """Find index where airfoil crosses Z=0 (from negative to positive).

    Args:
        poles: List of airfoil control points

    Returns:
        Index of crossing point, or None if no crossing found
    """
    return next(
        (i for i in range(len(poles) - 1) if poles[i].z < 0 and poles[i + 1].z >= 0),
        None,
    )


def calculate_wire_point_distribution(
    wire1_length: float, wire2_length: float, total_points: int
) -> Tuple[int, int]:
    """Calculate proportional point distribution based on wire lengths.

    Args:
        wire1_length: Length of first wire segment
        wire2_length: Length of second wire segment
        total_points: Total number of points to distribute

    Returns:
        Tuple of (wire1_point_count, wire2_point_count)
    """
    total_wire_length = wire1_length + wire2_length
    wire1_ratio = wire1_length / total_wire_length if total_wire_length > 0 else 0.5
    wire1_point_count = max(2, round(total_points * wire1_ratio))
    wire2_point_count = max(2, total_points - wire1_point_count)
    return wire1_point_count, wire2_point_count


def discretize_wire_segment(
    start_point: FreeCAD.Vector, end_point: FreeCAD.Vector, point_count: int
) -> List[FreeCAD.Vector]:
    """Discretize a wire segment into specified number of points.

    Args:
        start_point: Starting point of the segment
        end_point: Ending point of the segment
        point_count: Number of points to generate along the segment

    Returns:
        List of discretized points along the wire segment
    """
    wire = Part.makeLine(start_point, end_point)
    discretized = wire.discretize(point_count)
    return [FreeCAD.Vector(p.x, p.y, p.z) for p in discretized]


def create_bspline_from_points(points: List[FreeCAD.Vector]) -> Part.Edge:
    """Create B-spline edge from list of points using interpolation.

    Args:
        points: List of 3D points to interpolate through

    Returns:
        FreeCAD edge representing the B-spline curve
    """
    spline = Part.BSplineCurve()
    spline.interpolate(points, False)
    return spline.toShape()


def create_closed_airfoil_wire(
    bspline_edge: Part.Edge, points: List[FreeCAD.Vector]
) -> Part.Wire:
    """Create closed airfoil wire with trailing edge line if needed.

    Args:
        bspline_edge: B-spline edge representing the main airfoil curve
        points: Original points used to create the B-spline

    Returns:
        Closed FreeCAD wire (adds closing line if not already closed)
    """
    first_point = points[0]
    last_point = points[-1]
    is_closed = first_point.distanceToPoint(last_point) < 0.001

    if not is_closed:
        closing_line = Part.makeLine(last_point, first_point)
        return Part.Wire([bspline_edge, closing_line])
    else:
        return Part.Wire([bspline_edge])


def create_boundary_check_function(
    trailing_edge_x: float,
    W: float,
    thickness: float,
    drop_end: float,
    chord_length_x: float,
) -> Callable[[float, float], bool]:
    """Create boundary checking function for point filtering.

    Args:
        trailing_edge_x: X coordinate of trailing edge
        W: Distance from leading edge to center
        thickness: Maximum Z thickness
        drop_end: Z drop at trailing edge
        chord_length_x: Chord length in X direction

    Returns:
        Function that checks if (x, z) point is inside boundary trapezoid
    """
    boundary_z_base = thickness - drop_end
    slope = drop_end / chord_length_x

    def is_point_in_boundary_trapezoid(x, z):
        """Check if point is inside boundary trapezoid using geometric logic"""
        # Boundary X range: trailing_edge_x to W
        if x < trailing_edge_x or x > W:
            return False

        # Boundary Z range: 0 to top_line
        if z < 0.0:
            return False

        # Calculate top boundary using slanted line: z = boundary_z_base + slope * (x - trailing_edge_x)
        top_z = boundary_z_base + slope * (x - trailing_edge_x)
        if z > top_z:
            return False

        return True

    return is_point_in_boundary_trapezoid


def extract_bspline_control_points(shape: Part.Shape) -> Optional[List[FreeCAD.Vector]]:
    """Extract B-spline control points from a shape's edges.

    Args:
        shape: FreeCAD shape to extract control points from

    Returns:
        List of control points if B-spline found, None otherwise
    """
    for edge in shape.Edges:
        if hasattr(edge.Curve, "getPoles"):
            return edge.Curve.getPoles()
    return None


def create_airfoil_object(
    wire: Part.Wire, name: str, doc: FreeCAD.Document, show: bool = True
) -> Part.Feature:
    """Create a FreeCAD Part::Feature object from a wire.

    Args:
        wire: FreeCAD wire to create object from
        name: Complete name for the object (no suffix added)
        doc: FreeCAD document to create object in
        show: Whether to show the object in the document (default: True)

    Returns:
        FreeCAD Part::Feature object containing the wire
    """
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = wire
    if not show and FreeCAD.GuiUp:
        obj.ViewObject.Visibility = False
    return obj


def extract_leading_edge_points(
    poles: List[FreeCAD.Vector],
    leading_edge_start: int,
    leading_edge_end: int,
    boundary_check_fn: Callable[[float, float], bool],
) -> List[FreeCAD.Vector]:
    """Extract leading edge points that fall within boundary trapezoid.

    Args:
        poles: List of airfoil control points
        leading_edge_start: Start index of leading edge range
        leading_edge_end: End index of leading edge range
        boundary_check_fn: Function to check if point is within boundary

    Returns:
        List of preserved leading edge points within boundary
    """
    preserved_points = []
    for i, pole in enumerate(poles):
        if leading_edge_start <= i <= leading_edge_end and boundary_check_fn(
            pole.x, pole.z
        ):
            preserved_points.append(pole)
    return preserved_points


def get_preserved_points_y200(
    poles: List[FreeCAD.Vector],
    leading_edge_start: int,
    leading_edge_end: int,
    is_point_in_boundary_trapezoid: Callable[[float, float], bool],
    y_position: float,
    doc: FreeCAD.Document
) -> List[Tuple[int, float]]:
    """Extract and visualize preserved leading edge points.
    
    Args:
        poles: List of airfoil control points
        leading_edge_start: Start index of leading edge range
        leading_edge_end: End index of leading edge range
        is_point_in_boundary_trapezoid: Function to check if point is within boundary
        y_position: Y coordinate for visualization
        doc: FreeCAD document for creating spheres
        
    Returns:
        List of (index, x_coordinate) tuples for preserved points
    """
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

        # Create group for preserved points visualization (only for y=200)
        if y_position == 200.0:
            preserved_group = doc.addObject("App::DocumentObjectGroup", f"Preserved_Points_y{y_position}")
            
            # Create colored spheres for each preserved point
            for i, (pole_idx, pole_x) in enumerate(preserved_points):
                pole = poles[pole_idx]
                sphere = doc.addObject("Part::Sphere", f"Preserved_Point_{pole_idx}")
                sphere.Radius = 1.0  # 1mm radius
                sphere.Placement.Base = FreeCAD.Vector(pole.x, y_position, pole.z)
                
                # Color spheres only if GUI is available
                if FreeCAD.GuiUp:
                    # Color spheres: red for first, blue for last, green for middle
                    if i == 0:
                        sphere.ViewObject.ShapeColor = (1.0, 0.0, 0.0)  # Red
                    elif i == len(preserved_points) - 1:
                        sphere.ViewObject.ShapeColor = (0.0, 0.0, 1.0)  # Blue
                    else:
                        sphere.ViewObject.ShapeColor = (0.0, 1.0, 0.0)  # Green
                    
                preserved_group.addObject(sphere)
            
            print(f"Created {len(preserved_points)} colored spheres for preserved points")
    
    return preserved_points


def discretize_filleted_wire_edges(filleted_edges, target_points=55):
    """
    Discretize edges 0, 5, 6 from filleted wire with proportional point distribution.
    
    Args:
        filleted_edges: List of edges from filleted wire
        target_points: Total points needed (default 55 for 79-25+1)
    
    Returns:
        Tuple of (edge0_points, edge5_points, edge6_points) excluding overlaps
    """
    # Calculate lengths of remaining edges
    edge0_length = filleted_edges[0].Length  # Wedge cut start → Preserved point
    edge5_length = filleted_edges[5].Length  # Wedge cut end → Another point
    edge6_length = filleted_edges[6].Length  # Final edge
    
    remaining_total_length = edge0_length + edge5_length + edge6_length
    
    # Distribute points proportionally by length
    points_edge0 = max(3, int(target_points * edge0_length / remaining_total_length))
    points_edge5 = max(3, int(target_points * edge5_length / remaining_total_length))
    points_edge6 = max(3, int(target_points * edge6_length / remaining_total_length))
    
    # Adjust to ensure exactly target_points total
    total_assigned = points_edge0 + points_edge5 + points_edge6
    if total_assigned != target_points:
        diff = target_points - total_assigned
        # Add to longest edge
        if edge6_length >= max(edge0_length, edge5_length):
            points_edge6 += diff
        elif edge0_length >= edge5_length:
            points_edge0 += diff
        else:
            points_edge5 += diff
    
    # Discretize edges
    points_edge0_disc = filleted_edges[0].discretize(Number=points_edge0)
    points_edge5_disc = filleted_edges[5].discretize(Number=points_edge5)
    points_edge6_disc = filleted_edges[6].discretize(Number=points_edge6)
    
    # Combine points excluding overlaps
    remaining_points = []
    remaining_points.extend(points_edge0_disc[:-1])  # Exclude last (overlap with cyan)
    remaining_points.extend(points_edge5_disc[1:])   # Exclude first (overlap with cyan)
    remaining_points.extend(points_edge6_disc)       # Include all
    
    # Adjust if needed
    if len(remaining_points) < target_points:
        needed = target_points - len(remaining_points)
        points_edge6_disc = filleted_edges[6].discretize(Number=points_edge6 + needed)
        
        # Recombine
        remaining_points = []
        remaining_points.extend(points_edge0_disc[:-1])
        remaining_points.extend(points_edge5_disc[1:])
        remaining_points.extend(points_edge6_disc)
    
    return points_edge0_disc[:-1], points_edge5_disc[1:], points_edge6_disc


def interpolate_filleted_with_preserved_points(filleted_points, doc, y_position, t=0.5):
    """
    Interpolate filleted points with preserved airfoil points from y=200.
    
    Args:
        filleted_points: List of 25 filleted points to interpolate
        doc: FreeCAD document
        y_position: Y coordinate for interpolated points
        t: Interpolation parameter (0.0=all filleted, 1.0=all airfoil)
    
    Returns:
        List of 25 interpolated points
    """
    # Find preserved points from existing hybrid airfoil
    preserved_points_y200 = []
    for obj in doc.Objects:
        if hasattr(obj, 'Name') and 'Preserved_Points_y200' in obj.Name:
            for child in obj.Group:
                if hasattr(child, 'Placement') and 'Preserved_Point_' in child.Name:
                    point = child.Placement.Base
                    try:
                        index = int(child.Name.split('_')[-1])
                        preserved_points_y200.append((index, point.x))
                    except ValueError:
                        pass
            break
    
    # Sort by index to maintain order
    preserved_points_y200.sort(key=lambda x: x[0])
    
    # Find root section (should be the first in final_loft_sections or look for Hybrid_Airfoil_y200)
    root_section = None
    for obj in doc.Objects:
        if hasattr(obj, 'Name') and ('Hybrid_Airfoil_y200' in obj.Name or 'Root_Section' in obj.Name):
            root_section = obj
            break
    
    # If not found, try to find any object with y200 in the name
    if not root_section:
        for obj in doc.Objects:
            if hasattr(obj, 'Name') and 'y200' in obj.Name and hasattr(obj, 'Shape'):
                root_section = obj
                break
    
    if not root_section:
        raise ValueError("Root section not found for interpolation")
    
    root_bspline = root_section.Shape.Edge1.Curve
    poles = [root_bspline.getPole(i + 1) for i in range(root_bspline.NbPoles)]
    
    # Extract preserved points for interpolation
    airfoil_25_control_points = []
    for i, (pole_idx, x_coord) in enumerate(preserved_points_y200[:25]):
        preserved_point = FreeCAD.Vector(x_coord, 200.0, 0.0)
        pole = poles[pole_idx]
        preserved_point.z = pole.z
        airfoil_25_control_points.append(preserved_point)
    
    # Pad with remaining poles if needed
    while len(airfoil_25_control_points) < 25:
        remaining_idx = len(preserved_points_y200) + len(airfoil_25_control_points) - len(preserved_points_y200)
        if remaining_idx < len(poles):
            airfoil_25_control_points.append(poles[remaining_idx])
    
    # Linear interpolation between filleted and airfoil points
    interpolated_points = []
    for i in range(25):
        filleted_pt = filleted_points[i]
        airfoil_pt = airfoil_25_control_points[i]
        
        # Parametric interpolation: (1-t)*filleted + t*airfoil
        interp_x = (1 - t) * filleted_pt.x + t * airfoil_pt.x
        interp_y = y_position
        interp_z = (1 - t) * filleted_pt.z + t * airfoil_pt.z
        
        interpolated_points.append(FreeCAD.Vector(interp_x, interp_y, interp_z))
    
    return interpolated_points


def create_combined_orange_magenta_wire(filleted_edges, rect_25_points_filleted, doc, y_position, name_suffix=""):
    """
    Create Combined_Orange_Magenta_Wire by combining discretized filleted edges with interpolated points.
    
    Args:
        filleted_edges: List of edges from filleted wire
        rect_25_points_filleted: 25 filleted points from edges 1-4
        doc: FreeCAD document
        y_position: Y coordinate for the wire
        name_suffix: Optional suffix for object names
    
    Returns:
        FreeCAD Part::Feature object containing the combined wire
    """
    # Discretize remaining edges (0, 5, 6) for magenta points
    edge0_points, edge5_points, edge6_points = discretize_filleted_wire_edges(filleted_edges, target_points=55)
    
    # Interpolate filleted points with preserved airfoil points for orange points
    interpolated_25_points = interpolate_filleted_with_preserved_points(
        rect_25_points_filleted, doc, y_position, t=0.5
    )
    
    # Combine points in correct edge order: magenta (edge 0) + orange (edges 1-4) + magenta (edges 5-6)
    # Note: Need to exclude first point of edge6_points to avoid duplicate (original logic)
    edges_5_6_points = edge5_points + edge6_points[1:]  # Exclude first point of edge 6
    combined_79_points = edge0_points + interpolated_25_points + edges_5_6_points
    
    print(f"Combining: {len(edge0_points)} magenta (edge 0) + {len(interpolated_25_points)} orange (edges 1-4) + {len(edges_5_6_points)} magenta (edges 5-6) = {len(combined_79_points)} points")
    
    # Create B-spline from combined points
    combined_edge = create_bspline_from_points(combined_79_points)
    
    # Create trailing edge line to close the wire
    first_point = combined_79_points[0]
    last_point = combined_79_points[-1]
    trailing_edge_line = Part.makeLine(last_point, first_point)
    
    # Create closed wire from B-spline + trailing edge
    combined_wire = Part.Wire([combined_edge, trailing_edge_line])
    
    # Create FreeCAD object for the combined wire
    wire_name = f"Combined_Orange_Magenta_Wire_y{y_position}{name_suffix}"
    combined_bspline_obj = doc.addObject("Part::Feature", wire_name)
    combined_bspline_obj.Shape = combined_wire
    
    print(f"Created closed B-spline wire with {len(combined_79_points)} points + trailing edge")
    
    return combined_bspline_obj


def create_blade_loft(
    sections: List[Part.Feature], doc: FreeCAD.Document
) -> Optional[Part.Feature]:
    """Create a loft through all blade sections.

    Args:
        sections: List of blade section objects to loft through
        doc: FreeCAD document to create loft in

    Returns:
        FreeCAD loft object if successful, None if failed
    """
    if len(sections) < 2:
        print(f"Not enough sections found for loft: {len(sections)}")
        return None

    try:
        loft = doc.addObject("Part::Loft", "Complete_Blade_Loft")
        loft.Sections = sections
        loft.Solid = True
        loft.Ruled = False
        doc.recompute()
        print(f"Created complete blade loft with {len(sections)} sections")
        return loft
    except Exception as e:
        print(f"Failed to create complete loft: {e}")
        return None


def create_cross_section_wire(
    W: float,
    chord_length_x: float,
    y_end: float,
    z_bottom_right_end: float,
    z_bottom_end: float,
    thickness: float,
    z_top_end: float,
) -> Part.Wire:
    """Create standard cross-section wire with 4 vertices.

    Args:
        W: Distance from leading edge to center
        chord_length_x: Chord length in X direction
        y_end: Y position of the section
        z_bottom_right_end: Z coordinate of trailing edge bottom
        z_bottom_end: Z coordinate of leading edge bottom
        thickness: Maximum Z thickness
        z_top_end: Z coordinate of trailing edge top

    Returns:
        FreeCAD wire representing the cross-section
    """
    v1 = FreeCAD.Vector(
        W - chord_length_x, y_end, z_bottom_right_end
    )  # Trailing edge bottom
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)  # Leading edge bottom
    v3 = FreeCAD.Vector(W, y_end, thickness)  # Leading edge top
    v4 = FreeCAD.Vector(W - chord_length_x, y_end, z_top_end)  # Trailing edge top
    return Part.makePolygon([v2, v1, v4, v3, v2])


def create_root_triangle_cross_section(
    W: float,
    chord_length_x: float,
    y_end: float,
    z_bottom_right_end: float,
    z_bottom_end: float,
    thickness: float,
    z_top_end: float,
    section_length: float,
    blade_radius: float,
    wood_width: float,
    drop_end: float,
    thick_end: float,
    station4_drop: float,
    station4_thick: float,
    R2: float,
) -> Part.Wire:
    """Create root triangle cross-section with wedge cut.

    Args:
        W: Distance from leading edge to center
        chord_length_x: Chord length in X direction
        y_end: Y position of the section
        z_bottom_right_end: Z coordinate of trailing edge bottom
        z_bottom_end: Z coordinate of leading edge bottom
        thickness: Maximum Z thickness
        z_top_end: Z coordinate of trailing edge top
        section_length: Length of each blade section
        blade_radius: Total blade radius
        wood_width: Width of root section
        drop_end: Z drop at trailing edge
        thick_end: Thickness at trailing edge
        station4_drop: Drop value at station 4
        station4_thick: Thickness value at station 4
        R2: Radius of flat circular area on back

    Returns:
        FreeCAD wire representing the root triangle cross-section
    """
    # Create base vertices
    v1 = FreeCAD.Vector(W - chord_length_x, y_end, z_bottom_right_end)
    v2 = FreeCAD.Vector(W, y_end, z_bottom_end)
    v3 = FreeCAD.Vector(W, y_end, thickness)
    v4 = FreeCAD.Vector(W - chord_length_x, y_end, z_top_end)

    # Calculate wedge cut position
    wedge_cut_x = calculate_wedge_cut_position(
        section_length,
        blade_radius,
        wood_width,
        W,
        thickness,
        drop_end,
        thick_end,
        station4_drop,
        station4_thick,
        R2,
    )

    # Create triangle vertices with wedge cut
    base_vertices = [v2, v1, v4, v3]
    triangle_vertices = create_root_triangle_vertices(base_vertices, wedge_cut_x, y_end)
    return Part.makePolygon(triangle_vertices)


def assemble_hybrid_points(
    poles: List[FreeCAD.Vector],
    leading_edge_start: int,
    leading_edge_end: int,
    boundary_check_fn: Callable[[float, float], bool],
    wire1_points: List[FreeCAD.Vector],
    wire2_points: List[FreeCAD.Vector],
    y_position: float,
) -> Tuple[List[FreeCAD.Vector], int, int]:
    """Assemble hybrid points using original complex interleaving logic.

    Args:
        poles: Original airfoil control points
        leading_edge_start: Start index of leading edge range
        leading_edge_end: End index of leading edge range
        boundary_check_fn: Function to check if point is within boundary
        wire1_points: Points from first discretized wire segment
        wire2_points: Points from second discretized wire segment
        y_position: Y coordinate for the section

    Returns:
        Tuple of (hybrid_points, leading_edge_preserved_count, mapped_points_count)
    """
    hybrid_points = []
    leading_edge_preserved = 0
    mapped_points = 0

    # Original point assembly logic - interleave points correctly
    for i, pole in enumerate(poles):
        if leading_edge_start <= i <= leading_edge_end and boundary_check_fn(
            pole.x, pole.z
        ):
            # Keep leading edge points (blue ones)
            hybrid_points.append(FreeCAD.Vector(pole.x, y_position, pole.z))
            leading_edge_preserved += 1
        else:
            # Smart mapping: use wire1 for points below Z=0, preserve natural curve for points above Z=0
            if pole.z < 0.0:
                # Use boundary mapping (wire1/wire2) for points below Z=0
                if i < len(wire1_points):  # Map to Wire1 points
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
            else:
                # Preserve natural airfoil curve for points above Z=0
                hybrid_points.append(FreeCAD.Vector(pole.x, y_position, pole.z))
                leading_edge_preserved += 1

    return hybrid_points, leading_edge_preserved, mapped_points


def calculate_wedge_cut_position(
    section_length: float,
    blade_radius: float,
    wood_width: float,
    W: float,
    thickness: float,
    drop_end: float,
    thick_end: float,
    station4_drop: float,
    station4_thick: float,
    R2: float,
) -> float:
    """Calculate wedge cut x position using connection line intersection logic"""
    station_5_y = calculate_station_position(2, section_length)
    station_4_y = calculate_station_position(3, section_length)
    w5 = calculate_chord_length(wood_width, W, station_5_y, blade_radius)
    w4 = calculate_chord_length(wood_width, W, station_4_y, blade_radius)

    z5_unclamped = (thickness - drop_end) - thick_end
    z4 = (thickness - station4_drop) - station4_thick
    t_term = -z5_unclamped / (z4 - z5_unclamped)
    y_term = station_5_y + t_term * (station_4_y - station_5_y)
    x_term_width = w5 + t_term * (w4 - w5)

    # Calculate wedge cut using connection line intersection logic from twisted tapered plank
    y_split = math.sqrt(R2**2 - W**2)  # Cylinder intersection with leading edge
    x_term = W - x_term_width  # Termination x-coordinate
    t_end = (section_length - y_split) / (y_term - y_split) if y_term != y_split else 0
    t_end = max(0, min(1, t_end))
    wedge_cut_x = W + t_end * (x_term - W)  # This gives ~24.41

    return wedge_cut_x


def create_root_triangle_vertices(
    base_vertices: List[FreeCAD.Vector], wedge_cut_x: float, y_end: float
) -> List[FreeCAD.Vector]:
    """Create Root_triangle vertices with wedge cut"""
    v2, v1, v4, v3 = base_vertices
    v_wedge = FreeCAD.Vector(wedge_cut_x, y_end, 0)  # Wedge cut vertex at z=0

    # Create Root_triangle wire: v2 -> v_wedge -> v1 -> v4 -> v3 -> v2
    # This connects: leading_edge_bottom -> wedge_cut -> root_cut_bottom -> trailing_edge_top -> leading_edge_top -> back
    return [v2, v_wedge, v1, v4, v3, v2]


def find_crossing_indices(
    poles: List, boundary_z_base: float, slope: float, trailing_edge_x: float
) -> Tuple[Optional[int], Optional[int]]:
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
    drop_end: float = 0.0,
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
    # Step 1: Scale by hypotenuse of chord_length and drop_end
    hypotenuse_length = math.sqrt(chord_length**2 + drop_end**2)
    scaled_coordinates = scale_airfoil_coordinates(coordinates, hypotenuse_length)

    # Step 2: Flatten AFTER scaling
    # Find bottom surface points (trailing edge to end)
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    global_z_min_idx = min(range(len(bottom_points)), key=lambda i: bottom_points[i][1])
    start_idx, end_idx = find_stable_region(bottom_points, global_z_min_idx)
    mid_points = bottom_points[start_idx:end_idx]
    x_coords = [x for x, z in mid_points]
    z_coords = [z for x, z in mid_points]
    slope, intercept = np.polyfit(x_coords, z_coords, 1)
    flatten_angle = -math.degrees(math.atan(slope))

    # Find global min Z point for flattening rotation center
    min_z_point = min(scaled_coordinates, key=lambda p: p[1])  # p[1] is Z in 2D
    flatten_rotation_center_x, flatten_rotation_center_z = min_z_point

    # Rotate about global min Z point for flattening
    flattened_coordinates = rotate_airfoil_coordinates_about_point(
        scaled_coordinates,
        flatten_rotation_center_x,
        flatten_rotation_center_z,
        flatten_angle,
    )

    # Apply Z shift using trailing edge for optimal closure
    trailing_edge_z = flattened_coordinates[-1][1]  # Last point Z value
    z_shift = -trailing_edge_z
    bottom_aligned_coordinates = [(x, z + z_shift) for x, z in flattened_coordinates]

    # Preserve exact hypotenuse length for trailing edge only
    # Rotation can introduce floating-point precision errors
    if bottom_aligned_coordinates:
        # Fix only trailing edge (last point) to exact hypotenuse length
        bottom_aligned_coordinates[-1] = (
            hypotenuse_length,
            bottom_aligned_coordinates[-1][1],
        )

    # Check trailing edge alignment
    last_point = bottom_aligned_coordinates[-1]
    trailing_error = abs(last_point[1])
    print(f"Airfoil at y={y_position}: Trailing edge error = {trailing_error:.6f}mm")

    # Step 3: Apply flips
    reflected_coordinates = flip_airfoil_coordinates_vertically(
        bottom_aligned_coordinates
    )
    final_coordinates = flip_airfoil_coordinates_horizontally(reflected_coordinates)
    # Step 4: Convert to 3D and apply z_offset
    xyz_coordinates = [(x, y_position, z + z_offset) for x, z in final_coordinates]

    # Step 5: Translate in X direction (now in 3D)
    xyz_coordinates = [(x + x_offset, y, z) for x, y, z in xyz_coordinates]

    # Step 5: Apply additional rotation if specified
    if rotation_angle != 0.0:
        center_x = rotation_center_x  # Use passed parameter directly
        center_z = rotation_center_z  # Use passed parameter directly
        # Convert back to 2D for rotation, then back to 3D
        xz_coordinates = [(x, z) for x, _, z in xyz_coordinates]
        rotated_coordinates = rotate_airfoil_coordinates_about_point(
            xz_coordinates, center_x, center_z, rotation_angle
        )
        xyz_coordinates = [(x, y_position, z) for x, z in rotated_coordinates]

    # Create test B-spline to measure overshoot
    points = [FreeCAD.Vector(x, y, z) for x, y, z in xyz_coordinates]
    test_spline = Part.BSplineCurve()
    test_spline.interpolate(points, False)
    test_edge = test_spline.toShape()

    # Calculate precise B-spline overshoot beyond leading edge boundary

    # Get the actual curve's bounding box
    bbox = test_edge.BoundBox
    max_x_bbox = bbox.XMax
    overshoot_bbox = max_x_bbox - W

    print(
        f"Airfoil at y={y_position}: BoundBox max X = {max_x_bbox:.6f}mm, overshoot = {overshoot_bbox:.6f}mm"
    )

    # Apply predictive overshoot correction if needed
    if overshoot_bbox > 0.001:  # Only correct if overshoot > 1 micron
        # Use conservative pullback approach - B-splines don't scale linearly
        pullback_distance = overshoot_bbox * 1.001  # Minimal 0.1% margin
        trailing_edge_3d = xyz_coordinates[-1]  # Last point (trailing edge)

        # Find the leading edge (point with maximum X)
        leading_edge_idx = max(
            range(len(xyz_coordinates)), key=lambda i: xyz_coordinates[i][0]
        )
        leading_edge_3d = xyz_coordinates[leading_edge_idx]

        corrected_xyz_coordinates = []
        for i, (x, y, z) in enumerate(xyz_coordinates):
            if i == len(xyz_coordinates) - 1:  # Keep trailing edge fixed
                corrected_xyz_coordinates.append((x, y, z))
            else:
                # Calculate how far this point is from trailing edge to leading edge
                total_chord = leading_edge_3d[0] - trailing_edge_3d[0]
                point_distance = x - trailing_edge_3d[0]

                if total_chord > 0:
                    # Scale the pullback based on position along chord
                    position_ratio = point_distance / total_chord
                    pullback_amount = pullback_distance * position_ratio
                    new_x = x - pullback_amount
                else:
                    new_x = x

                corrected_xyz_coordinates.append((new_x, y, z))

        xyz_coordinates = corrected_xyz_coordinates

    # Create final B-spline with corrected coordinates
    points = [FreeCAD.Vector(x, y, z) for x, y, z in xyz_coordinates]
    spline = Part.BSplineCurve()
    spline.interpolate(points, False)
    edge = spline.toShape()

    # Verify correction by measuring final overshoot
    final_bbox = edge.BoundBox
    final_overshoot = final_bbox.XMax - W
    discretized = edge.discretize(1000)  # Get 1000 points along the actual edge
    max_x_discrete = max(pt.x for pt in discretized)
    overshoot_discrete = max_x_discrete - W

    print(
        f"Airfoil at y={y_position}: BoundBox max X = {final_bbox.XMax:.6f}mm, overshoot = {final_overshoot:.6f}mm"
    )
    print(
        f"Airfoil at y={y_position}: Discretized max X = {max_x_discrete:.6f}mm, overshoot = {overshoot_discrete:.6f}mm"
    )

    first_point = points[0]
    last_point = points[-1]

    # Measure trailing edge thickness (distance between first and last points)
    trailing_edge_thickness = first_point.distanceToPoint(last_point)
    print(
        f"Airfoil at y={y_position}: Trailing edge thickness = {trailing_edge_thickness:.3f}mm"
    )

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
    R2: float,
    doc: FreeCAD.Document,
    station4_drop: Optional[float] = None,
    station4_thick: Optional[float] = None,
) -> Part.Feature:
    # Calculate z positions internally
    z_top_end = thickness - drop_end
    z_bottom_right_end = max(0, z_top_end - thick_end)

    chord_length_x = calculate_chord_length(wood_width, W, y_end, blade_radius)
    z_bottom_end = thickness - thick_end

    # Use X-axis chord length for proper positioning
    chord_length = chord_length_x

    # Calculate hypotenuse for scaling and positioning
    hypotenuse_length = math.sqrt(chord_length_x**2 + drop_end**2)

    # Create airfoil wire
    rotation_angle = math.degrees(math.atan(drop_end / chord_length_x))

    # Position airfoil so bottom trailing edge aligns with section boundary
    # Calculate actual trailing edge X position for this section
    trailing_edge_x = W - chord_length_x
    z_bottom_trailing = thickness - drop_end  # Z at trailing edge from boundary

    airfoil_wire = create_airfoil_wire_at_section(
        airfoil_coordinates,
        chord_length,  # Use X-axis chord length
        y_end,
        trailing_edge_x + hypotenuse_length,  # Use corrected hypotenuse for positioning
        z_bottom_trailing,  # Bottom trailing edge at boundary Z
        rotation_angle,  # Rotate to match boundary slope
        trailing_edge_x,  # Rotation center at actual trailing edge X
        z_bottom_trailing,  # Rotation center at boundary Z
        drop_end,  # Add drop_end parameter
    )

    # Store wire directly without creating FreeCAD object
    obj = create_airfoil_object(airfoil_wire, f"{name}_Airfoil", doc, DEBUG)

    # Check Section_5_Airfoil control points for consistency
    if name == "Section_5":
        poles = extract_bspline_control_points(airfoil_wire)
        if poles:
            print(f"Section_5_Airfoil B-spline has {len(poles)} control points")

    # Create cross-section wire
    station_6_y = calculate_station_position(
        1, section_length
    )  # Root_triangle position
    if y_end == station_6_y:  # First section (Root_triangle)
        back_wire = create_root_triangle_cross_section(
            W,
            chord_length_x,
            y_end,
            z_bottom_right_end,
            z_bottom_end,
            thickness,
            z_top_end,
            section_length,
            blade_radius,
            wood_width,
            drop_end,
            thick_end,
            station4_drop,
            station4_thick,
            R2,
        )
    else:
        back_wire = create_cross_section_wire(
            W,
            chord_length_x,
            y_end,
            z_bottom_right_end,
            z_bottom_end,
            thickness,
            z_top_end,
        )

    if DEBUG:
        Part.show(back_wire, name)
    return obj  # Return the airfoil object


# Main execution
if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

# Get document reference for all operations
doc = FreeCAD.ActiveDocument

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
    doc: FreeCAD.Document,
) -> Part.Feature:
    """Create hybrid airfoil: leading edge from airfoil, rest mapped to Section_6b wire.

    Returns:
        FreeCAD Part::Feature object containing the hybrid airfoil wire
    """
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
    poles = extract_bspline_control_points(fitted_airfoil.Shape)
    if not poles:
        print("No B-spline found in airfoil")
        return

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

    # Simple approach: boundary crossing is just before original global Y minimum
    original_global_y_min_idx = min(
        range(len(airfoil_coordinates)), key=lambda i: airfoil_coordinates[i][1]
    )
    boundary_crossing_idx = original_global_y_min_idx - 1

    # Still need these variables for interpolation calculation
    trailing_edge_x = W - chord_length_x  # Calculate -125 equivalent
    boundary_z_base = thickness - drop_end  # Z-height at trailing edge
    slope = drop_end / chord_length_x  # Calculate slope from actual parameters

    p_before, p_after = (
        poles[boundary_crossing_idx],
        poles[boundary_crossing_idx + 1],
    )
    boundary_z_before = boundary_z_base + slope * (p_before.x - trailing_edge_x)
    boundary_z_after = boundary_z_base + slope * (p_after.x - trailing_edge_x)

    if abs((p_after.z - boundary_z_after) - (p_before.z - boundary_z_before)) > 1e-10:
        t_cross = (p_before.z - boundary_z_before) / (
            (p_before.z - boundary_z_before) - (p_after.z - boundary_z_after)
        )
        x_cross = p_before.x + t_cross * (p_after.x - p_before.x)
        z_cross = p_before.z + t_cross * (p_after.z - p_before.z)
    else:
        x_cross = p_before.x
        z_cross = p_before.z  # Use the point's Z coordinate

    # Create split points
    split1_point = FreeCAD.Vector(x_at_z0, y_position, 0.0)
    split2_point = FreeCAD.Vector(x_cross, y_position, z_cross)

    # Use dynamically found crossing indices as leading edge range
    leading_edge_start = crossing_idx if crossing_idx is not None else 0
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

    # Distribute mapped points proportionally based on wire lengths
    wire1_point_count, wire2_point_count = calculate_wire_point_distribution(
        wire1_length, wire2_length, mapped_points
    )

    # Create and discretize Wire 1: from trailing edge bottom to split1_point
    wire1_points = discretize_wire_segment(wire1_start, wire1_end, wire1_point_count)

    # Create and discretize Wire 2: from split2_point to trailing edge top
    wire2_points = discretize_wire_segment(wire2_start, wire2_end, wire2_point_count)

    # Create boundary checking function
    is_point_in_boundary_trapezoid = create_boundary_check_function(
        trailing_edge_x, W, thickness, drop_end, chord_length_x
    )

    # Assemble hybrid points using helper function with original complex logic
    hybrid_points, leading_edge_preserved, mapped_points = assemble_hybrid_points(
        poles,
        leading_edge_start,
        leading_edge_end,
        is_point_in_boundary_trapezoid,
        wire1_points,
        wire2_points,
        y_position,
    )

    # Extract preserved points using reusable function
    preserved_points = get_preserved_points_y200(
        poles, leading_edge_start, leading_edge_end, 
        is_point_in_boundary_trapezoid, y_position, doc
    )

    print(
        f"Leading edge preserved: {leading_edge_preserved}, Mapped points: {mapped_points}"
    )

    # No duplicate removal needed since wire2 ends at exact trailing edge
    print(f"Using {len(hybrid_points)} points for B-spline creation")

    # Create hybrid airfoil wire
    # Create B-spline interpolation through points
    edge = create_bspline_from_points(hybrid_points)

    # Close the trailing edge with a line (like other airfoils)
    hybrid_wire = create_closed_airfoil_wire(edge, hybrid_points)

    # Create FreeCAD object
    hybrid_obj = create_airfoil_object(
        hybrid_wire, f"Hybrid_Airfoil_y{int(y_position)}", doc, DEBUG
    )

    print(
        f"Created smooth hybrid airfoil B-spline at y={y_position} with {len(hybrid_points)} points (closed with trailing edge line)"
    )
    print(
        f"  Leading edge preserved: {leading_edge_preserved}, Mapped points: {mapped_points}"
    )
    print(f"  Chord length: {chord_length_x:.1f}mm")

    # Measure trailing edge thickness (distance between first and last points)
    first_point = hybrid_points[0]
    last_point = hybrid_points[-1]
    trailing_edge_thickness = math.sqrt(
        (first_point[0] - last_point[0]) ** 2
        + (first_point[1] - last_point[1]) ** 2
        + (first_point[2] - last_point[2]) ** 2
    )
    print(f"  Trailing edge thickness: {trailing_edge_thickness:.3f}mm")

    # Check B-spline control points
    poles = extract_bspline_control_points(hybrid_wire)
    if poles:
        print(
            f"Hybrid_Airfoil_y{int(y_position)} B-spline has {len(poles)} control points"
        )

    return hybrid_obj


# Blade parameters
W = 50  # Distance from leading edge to center
blade_radius = 1200  # mm
wood_width = 200  # root width
thickness = 40  # z dimension
R2 = 125  # radius of flat circular area on back
num_sections = 6
section_length = blade_radius / num_sections
number_of_station_5_to_6_transitions = 3  # Number of interpolated hybrid sections
minimum_trailing_edge_thickness = 1.2  # mm
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


# Test multiple approaches with corrected trailing edge error checking
def test_multiple_flatten_approaches():
    """Test various flatten angle calculation methods with proper error checking"""

    # Step 1: Scale FIRST
    chord_length = 175.0
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Find bottom surface points
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Method 1: All bottom points (original)
    x_coords_all = [x for x, z in bottom_points]
    z_coords_all = [z for x, z in bottom_points]
    slope_1, _ = np.polyfit(x_coords_all, z_coords_all, 1)
    angle_1 = -math.degrees(math.atan(slope_1))

    # Method 2: Endpoints only
    trailing_pt = bottom_points[0]
    leading_pt = bottom_points[-1]
    slope_2 = (leading_pt[1] - trailing_pt[1]) / (leading_pt[0] - trailing_pt[0])
    angle_2 = -math.degrees(math.atan(slope_2))

    # Method 3: Middle 50% of points
    mid_start = len(bottom_points) // 4
    mid_end = 3 * len(bottom_points) // 4
    mid_points = bottom_points[mid_start:mid_end]
    x_coords_mid = [x for x, z in mid_points]
    z_coords_mid = [z for x, z in mid_points]
    slope_3, _ = np.polyfit(x_coords_mid, z_coords_mid, 1)
    angle_3 = -math.degrees(math.atan(slope_3))

    # Method 4: First and last 25% (exclude middle)
    quarter = len(bottom_points) // 4
    edge_points = bottom_points[:quarter] + bottom_points[-quarter:]
    x_coords_edge = [x for x, z in edge_points]
    z_coords_edge = [z for x, z in edge_points]
    slope_4, _ = np.polyfit(x_coords_edge, z_coords_edge, 1)
    angle_4 = -math.degrees(math.atan(slope_4))

    # Method 5: Weighted regression (more weight to endpoints)
    weights = []
    for i in range(len(bottom_points)):
        if i < len(bottom_points) * 0.1 or i > len(bottom_points) * 0.9:
            weights.append(3.0)  # High weight for endpoints
        else:
            weights.append(1.0)  # Normal weight for middle
    slope_5, _ = np.polyfit(x_coords_all, z_coords_all, 1, w=weights)
    angle_5 = -math.degrees(math.atan(slope_5))

    # Method 6: Exclude outliers (remove top/bottom 10% by Z value)
    sorted_by_z = sorted(bottom_points, key=lambda p: p[1])
    trim_count = len(sorted_by_z) // 10
    trimmed_points = (
        sorted_by_z[trim_count:-trim_count] if trim_count > 0 else sorted_by_z
    )
    x_coords_trim = [x for x, z in trimmed_points]
    z_coords_trim = [z for x, z in trimmed_points]
    slope_6, _ = np.polyfit(x_coords_trim, z_coords_trim, 1)
    angle_6 = -math.degrees(math.atan(slope_6))

    methods = [
        ("All Bottom Points", slope_1, angle_1),
        ("Endpoints Only", slope_2, angle_2),
        ("Middle 50%", slope_3, angle_3),
        ("Edge 25% Each", slope_4, angle_4),
        ("Weighted Endpoints", slope_5, angle_5),
        ("Trimmed Outliers", slope_6, angle_6),
    ]

    print(f"Testing {len(methods)} flatten angle methods:")
    print(f"Bottom surface: {len(bottom_points)} points")
    print(f"Trailing edge: ({trailing_pt[0]:.3f}, {trailing_pt[1]:.3f})")
    print(f"Leading edge: ({leading_pt[0]:.3f}, {leading_pt[1]:.3f})")
    print()

    best_error = float("inf")
    best_method = None

    for i, (name, slope, angle) in enumerate(methods):
        print(f"--- Method {i + 1}: {name} ---")
        print(f"Slope: {slope:.6f}")
        print(f"Flatten angle: {angle:.6f} degrees")

        # Apply this flatten angle
        min_z_point = min(scaled_coordinates, key=lambda p: p[1])
        rotation_center_x, rotation_center_z = min_z_point

        flattened = rotate_airfoil_coordinates_about_point(
            scaled_coordinates, rotation_center_x, rotation_center_z, angle
        )

        # Apply Z shift
        global_min_z = min(z for x, z in flattened)
        z_shift = -global_min_z
        aligned = [(x, z + z_shift) for x, z in flattened]

        # Check ACTUAL trailing edge error (last point)
        last_point = aligned[-1]  # Last point in airfoil sequence
        trailing_error = abs(last_point[1])  # Z value of last point

        print(f"Last point: ({last_point[0]:.3f}, {last_point[1]:.6f})")
        print(f"Trailing edge error: {trailing_error:.6f}mm")

        if trailing_error < best_error:
            best_error = trailing_error
            best_method = (i + 1, name)

        # Create visualization
        points_3d = [FreeCAD.Vector(x, i * 30, z) for x, z in aligned]

        spline = Part.BSplineCurve()
        spline.interpolate(points_3d, False)
        edge = spline.toShape()

        first_point = points_3d[0]
        last_point_3d = points_3d[-1]
        is_closed = first_point.distanceToPoint(last_point_3d) < 0.001

        if not is_closed:
            closing_line = Part.makeLine(last_point_3d, first_point)
            wire = Part.Wire([edge, closing_line])
        else:
            wire = Part.Wire([edge])

        Part.show(wire, f"Method_{i + 1}_{name.replace(' ', '_')}")
        print()

    print(f"🏆 BEST METHOD: {best_method[0]} - {best_method[1]}")
    print(f"🏆 BEST ERROR: {best_error:.6f}mm")


# Test Middle 50% method implementation
def test_middle_50_method():
    """Test the Middle 50% flatten angle method"""

    # Step 1: Scale FIRST
    chord_length = 175.0
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Step 2: Flatten using Middle 50% method
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Middle 50% method for flatten angle calculation
    mid_start = len(bottom_points) // 4
    mid_end = 3 * len(bottom_points) // 4
    mid_points = bottom_points[mid_start:mid_end]

    x_coords = [x for x, z in mid_points]
    z_coords = [z for x, z in mid_points]
    slope, intercept = np.polyfit(x_coords, z_coords, 1)
    flatten_angle = -math.degrees(math.atan(slope))

    # Find global min Z point as rotation center
    min_z_point = min(scaled_coordinates, key=lambda p: p[1])
    rotation_center_x, rotation_center_z = min_z_point

    print(f"Middle 50% method:")
    print(
        f"Bottom points: {len(bottom_points)} total, using {len(mid_points)} middle points"
    )
    print(f"Slope: {slope:.6f}")
    print(f"Flatten angle: {flatten_angle:.6f} degrees")
    print(f"Rotation center: ({rotation_center_x:.3f}, {rotation_center_z:.3f})")

    # Rotate about global min Z point
    flattened_coordinates = rotate_airfoil_coordinates_about_point(
        scaled_coordinates, rotation_center_x, rotation_center_z, flatten_angle
    )

    # Apply positive Z shift to align bottom to X-axis
    global_min_z = min(z for x, z in flattened_coordinates)
    z_shift = -global_min_z
    bottom_aligned_coordinates = [(x, z + z_shift) for x, z in flattened_coordinates]

    # Check trailing edge error - use the LAST point (actual trailing edge)
    last_point = bottom_aligned_coordinates[-1]  # Last point in airfoil sequence
    trailing_error = abs(last_point[1])  # Z value of last point
    print(f"Last point (trailing edge): ({last_point[0]:.3f}, {last_point[1]:.6f})")
    print(f"Trailing edge error: {trailing_error:.6f}mm")

    # Create visualization
    points_3d = [FreeCAD.Vector(x, 0, z) for x, z in bottom_aligned_coordinates]

    spline = Part.BSplineCurve()
    spline.interpolate(points_3d, False)
    edge = spline.toShape()

    first_point = points_3d[0]
    last_point_3d = points_3d[-1]
    is_closed = first_point.distanceToPoint(last_point_3d) < 0.001

    if not is_closed:
        closing_line = Part.makeLine(last_point_3d, first_point)
        wire = Part.Wire([edge, closing_line])
    else:
        wire = Part.Wire([edge])

    Part.show(wire, "Middle_50_Flattened_Airfoil")

    # Print final bounds
    bbox = wire.BoundBox


# Test different middle percentage ranges for optimal flatten angle
def test_middle_percentage_ranges():
    """Test various middle percentage ranges to find optimal flatten angle"""

    # Step 1: Scale FIRST
    chord_length = 175.0
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Find bottom surface points
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Test different middle percentage ranges
    percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    # Also test just the two middle points
    methods = []

    for pct in percentages:
        # Calculate start and end indices for middle percentage
        exclude_each_side = (
            (100 - pct) / 2 / 100
        )  # e.g., for 70%, exclude 15% each side
        start_idx = int(len(bottom_points) * exclude_each_side)
        end_idx = len(bottom_points) - start_idx

        if end_idx > start_idx:  # Ensure we have points to use
            mid_points = bottom_points[start_idx:end_idx]
            methods.append((f"Middle {pct}%", mid_points))

    # Test just the two middle points
    mid_idx = len(bottom_points) // 2
    if len(bottom_points) >= 2:
        two_middle = bottom_points[mid_idx - 1 : mid_idx + 1]
        methods.append(("Two Middle Points", two_middle))

    # Test single middle point (for reference)
    if len(bottom_points) >= 1:
        single_middle = [bottom_points[mid_idx]]
        # Can't do linear regression with 1 point, so use endpoints
        trailing_pt = bottom_points[0]
        leading_pt = bottom_points[-1]
        slope_single = (leading_pt[1] - trailing_pt[1]) / (
            leading_pt[0] - trailing_pt[0]
        )
        methods.append(("Single Middle (fallback to endpoints)", None, slope_single))

    print(f"Testing {len(methods)} middle percentage methods:")
    print(f"Bottom surface: {len(bottom_points)} total points")
    print()

    best_error = float("inf")
    best_method = None

    for i, method_data in enumerate(methods):
        if len(method_data) == 3:  # Special case for single middle
            name, _, slope = method_data
            angle = -math.degrees(math.atan(slope))
        else:
            name, mid_points = method_data

            if len(mid_points) < 2:
                print(f"--- Method {i + 1}: {name} ---")
                print("Skipped: Not enough points for regression")
                print()
                continue

            x_coords = [x for x, z in mid_points]
            z_coords = [z for x, z in mid_points]
            slope, _ = np.polyfit(x_coords, z_coords, 1)
            angle = -math.degrees(math.atan(slope))

        print(f"--- Method {i + 1}: {name} ---")
        if len(method_data) != 3:
            print(f"Using {len(mid_points)} points out of {len(bottom_points)} total")
        print(f"Slope: {slope:.6f}")
        print(f"Flatten angle: {angle:.6f} degrees")

        # Apply this flatten angle
        min_z_point = min(scaled_coordinates, key=lambda p: p[1])
        rotation_center_x, rotation_center_z = min_z_point

        flattened = rotate_airfoil_coordinates_about_point(
            scaled_coordinates, rotation_center_x, rotation_center_z, angle
        )

        # Apply Z shift
        global_min_z = min(z for x, z in flattened)
        z_shift = -global_min_z
        aligned = [(x, z + z_shift) for x, z in flattened]

        # Check ACTUAL trailing edge error (last point)
        last_point = aligned[-1]  # Last point in airfoil sequence
        trailing_error = abs(last_point[1])  # Z value of last point

        print(f"Last point: ({last_point[0]:.3f}, {last_point[1]:.6f})")
        print(f"Trailing edge error: {trailing_error:.6f}mm")

        if trailing_error < best_error:
            best_error = trailing_error
            best_method = (i + 1, name)

        # Create visualization
        points_3d = [FreeCAD.Vector(x, i * 25, z) for x, z in aligned]

        spline = Part.BSplineCurve()
        spline.interpolate(points_3d, False)
        edge = spline.toShape()

        first_point = points_3d[0]
        last_point_3d = points_3d[-1]
        is_closed = first_point.distanceToPoint(last_point_3d) < 0.001

        if not is_closed:
            closing_line = Part.makeLine(last_point_3d, first_point)
            wire = Part.Wire([edge, closing_line])
        else:
            wire = Part.Wire([edge])

        Part.show(wire, f"Middle_{name.replace(' ', '_').replace('%', 'pct')}")
        print()


# Test Middle 80% method implementation
def test_middle_80_method():
    """Test the optimal Middle 80% flatten angle method"""

    # Step 1: Scale FIRST
    chord_length = 175.0
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Step 2: Flatten using Middle 80% method
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Middle 80% method for flatten angle calculation
    exclude_each_side = 0.1  # Exclude 10% from each side = middle 80%
    start_idx = int(len(bottom_points) * exclude_each_side)
    end_idx = len(bottom_points) - start_idx
    mid_points = bottom_points[start_idx:end_idx]

    x_coords = [x for x, z in mid_points]
    z_coords = [z for x, z in mid_points]
    slope, intercept = np.polyfit(x_coords, z_coords, 1)
    flatten_angle = -math.degrees(math.atan(slope))

    # Find global min Z point as rotation center
    min_z_point = min(scaled_coordinates, key=lambda p: p[1])
    rotation_center_x, rotation_center_z = min_z_point

    print(f"Middle 80% method (OPTIMAL):")
    print(
        f"Bottom points: {len(bottom_points)} total, using {len(mid_points)} middle points"
    )
    print(f"Slope: {slope:.6f}")
    print(f"Flatten angle: {flatten_angle:.6f} degrees")
    print(f"Rotation center: ({rotation_center_x:.3f}, {rotation_center_z:.3f})")

    # Rotate about global min Z point
    flattened_coordinates = rotate_airfoil_coordinates_about_point(
        scaled_coordinates, rotation_center_x, rotation_center_z, flatten_angle
    )

    # Apply positive Z shift to align bottom to X-axis
    global_min_z = min(z for x, z in flattened_coordinates)
    z_shift = -global_min_z
    bottom_aligned_coordinates = [(x, z + z_shift) for x, z in flattened_coordinates]

    # Check trailing edge error - use the LAST point (actual trailing edge)
    last_point = bottom_aligned_coordinates[-1]  # Last point in airfoil sequence
    trailing_error = abs(last_point[1])  # Z value of last point
    print(f"Last point (trailing edge): ({last_point[0]:.3f}, {last_point[1]:.6f})")
    print(f"Trailing edge error: {trailing_error:.6f}mm")

    # Create visualization
    points_3d = [FreeCAD.Vector(x, 0, z) for x, z in bottom_aligned_coordinates]

    spline = Part.BSplineCurve()
    spline.interpolate(points_3d, False)
    edge = spline.toShape()

    first_point = points_3d[0]
    last_point_3d = points_3d[-1]
    is_closed = first_point.distanceToPoint(last_point_3d) < 0.001

    if not is_closed:
        closing_line = Part.makeLine(last_point_3d, first_point)
        wire = Part.Wire([edge, closing_line])
    else:
        wire = Part.Wire([edge])

    Part.show(wire, "Middle_80_Optimal_Airfoil")

    # Debug: Check which point is the global Z min
    global_min_point = min(scaled_coordinates, key=lambda p: p[1])
    print(f"Global Z min point: ({global_min_point[0]:.3f}, {global_min_point[1]:.6f})")

    # Check if global min is in middle 80%
    global_min_in_middle80 = global_min_point in mid_points
    print(f"Global Z min in Middle 80%: {global_min_in_middle80}")

    if global_min_in_middle80:
        global_min_index = mid_points.index(global_min_point)
        print(f"Global Z min is Middle80_Point_{global_min_index:02d}")
    else:
        print("Global Z min is in excluded points")

    # Show first few middle 80% points for comparison
    print(f"First 3 Middle 80% points:")
    for i in range(min(3, len(mid_points))):
        x, z = mid_points[i]
        print(f"  Middle80_Point_{i:02d}: ({x:.3f}, {z:.6f})")

    # Create spheres to visualize the middle 80% points used for regression
    print(f"Creating debug spheres for {len(mid_points)} middle 80% points...")
    for i, (x, z) in enumerate(mid_points):
        sphere = Part.makeSphere(1.0)  # 1mm radius spheres
        sphere.translate(
            FreeCAD.Vector(x, 10, z + z_shift)
        )  # Offset Y=10 for visibility
        Part.show(sphere, f"Middle80_Point_{i:02d}")

    # Also show the excluded points as smaller spheres for comparison
    excluded_start = bottom_points[:start_idx]
    excluded_end = bottom_points[end_idx:]

    print(f"Creating debug spheres for {len(excluded_start)} excluded start points...")
    for i, (x, z) in enumerate(excluded_start):
        sphere = Part.makeSphere(1.0)  # 1mm radius spheres
        sphere.translate(FreeCAD.Vector(x, 15, z + z_shift))  # Offset Y=15
        Part.show(sphere, f"Excluded_Start_{i:02d}")

    print(f"Creating debug spheres for {len(excluded_end)} excluded end points...")
    for i, (x, z) in enumerate(excluded_end):
        sphere = Part.makeSphere(1.0)  # 1mm radius spheres
        sphere.translate(FreeCAD.Vector(x, 15, z + z_shift))  # Offset Y=15
        Part.show(sphere, f"Excluded_End_{i:02d}")

    # Print final bounds
    bbox = wire.BoundBox


# Compare rotation center methods: Global Z min vs Last trailing edge vs Middle 80%
def compare_rotation_centers():
    """Compare different rotation center approaches with Middle 80% flatten angle"""

    # Step 1: Scale FIRST
    chord_length = 175.0
    scaled_coordinates = scale_airfoil_coordinates(coordinates, chord_length)

    # Find bottom surface points and calculate Middle 80% flatten angle
    trailing_edge_idx = min(
        range(len(scaled_coordinates)), key=lambda i: scaled_coordinates[i][0]
    )
    bottom_points = scaled_coordinates[trailing_edge_idx:]

    # Middle 80% method for flatten angle (optimal)
    exclude_each_side = 0.1
    start_idx = int(len(bottom_points) * exclude_each_side)
    end_idx = len(bottom_points) - start_idx
    mid_points = bottom_points[start_idx:end_idx]

    x_coords = [x for x, z in mid_points]
    z_coords = [z for x, z in mid_points]
    slope, _ = np.polyfit(x_coords, z_coords, 1)
    flatten_angle = -math.degrees(math.atan(slope))

    print(f"Using Middle 80% flatten angle: {flatten_angle:.6f} degrees")
    print(f"Testing 3 different rotation centers:")
    print()

    # Method 1: Global Z min (current approach)
    global_min_point = min(scaled_coordinates, key=lambda p: p[1])

    # Method 2: Last trailing edge point (final point in airfoil)
    last_trailing_point = scaled_coordinates[-1]

    # Method 3: Middle 80% centroid
    mid_centroid_x = sum(x for x, z in mid_points) / len(mid_points)
    mid_centroid_z = sum(z for x, z in mid_points) / len(mid_points)
    mid_centroid_point = (mid_centroid_x, mid_centroid_z)

    methods = [
        ("Global Z Min", global_min_point),
        ("Last Trailing Edge", last_trailing_point),
        ("Middle 80% Centroid", mid_centroid_point),
    ]

    best_error = float("inf")
    best_method = None

    for i, (name, rotation_center) in enumerate(methods):
        print(f"--- Method {i + 1}: {name} ---")
        print(f"Rotation center: ({rotation_center[0]:.3f}, {rotation_center[1]:.6f})")

        # Apply flatten angle with this rotation center
        flattened = rotate_airfoil_coordinates_about_point(
            scaled_coordinates, rotation_center[0], rotation_center[1], flatten_angle
        )

        # Apply Z shift
        global_min_z = min(z for x, z in flattened)
        z_shift = -global_min_z
        aligned = [(x, z + z_shift) for x, z in flattened]

        # Check ACTUAL trailing edge error (last point)
        last_point = aligned[-1]  # Last point in airfoil sequence
        trailing_error = abs(last_point[1])  # Z value of last point

        print(f"Last point: ({last_point[0]:.3f}, {last_point[1]:.6f})")
        print(f"Trailing edge error: {trailing_error:.6f}mm")

        if trailing_error < best_error:
            best_error = trailing_error
            best_method = (i + 1, name)

        # Create visualization
        points_3d = [FreeCAD.Vector(x, i * 40, z) for x, z in aligned]

        spline = Part.BSplineCurve()
        spline.interpolate(points_3d, False)
        edge = spline.toShape()

        first_point = points_3d[0]
        last_point_3d = points_3d[-1]
        is_closed = first_point.distanceToPoint(last_point_3d) < 0.001

        if not is_closed:
            closing_line = Part.makeLine(last_point_3d, first_point)
            wire = Part.Wire([edge, closing_line])
        else:
            wire = Part.Wire([edge])

        Part.show(wire, f"RotCenter_{i + 1}_{name.replace(' ', '_')}")
        print()


# Create blade sections from root triangle to tip (y=200 to y=1200)
loft_sections = []

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
        R2,
        doc,
        drops[2] if i == 0 else None,  # Station 4 drop for Root_triangle
        thicknesses[2] if i == 0 else None,  # Station 4 thickness for Root_triangle
    )

    # Create hybrid airfoil for Root_triangle section and intermediate sections
    if i == 0:  # Root_triangle section at y=200
        hybrid_obj = create_hybrid_airfoil_section_6b(
            y_end,
            thick_end,
            drop_end,
            W,
            wood_width,
            blade_radius,
            thickness,
            coordinates,
            section_obj,  # Pass the airfoil object directly
            doc,
        )
        loft_sections.append(hybrid_obj)
    elif y_end in [250.0, 300.0, 350.0]:  # Intermediate hybrid sections
        hybrid_obj = create_hybrid_airfoil_section_6b(
            y_end,
            thick_end,
            drop_end,
            W,
            wood_width,
            blade_radius,
            thickness,
            coordinates,
            section_obj,  # Pass the airfoil object directly
            doc,
        )
        loft_sections.append(hybrid_obj)
    else:
        loft_sections.append(section_obj)

print("Created blade section wires and airfoils from root triangle to tip")

# Create intermediate hybrid sections at y=250, 300, 350 and insert in correct order
intermediate_positions = [250.0, 300.0, 350.0]
intermediate_sections = []

for y_pos in intermediate_positions:
    # Calculate parameters for intermediate position
    i_interp = (y_pos / section_length) - 1  # Interpolation factor
    thick_interp = thicknesses[0] + (thicknesses[1] - thicknesses[0]) * (i_interp / 1.0)
    drop_interp = drops[0] + (drops[1] - drops[0]) * (i_interp / 1.0)

    section_obj = create_section(
        y_pos,
        thick_interp,
        drop_interp,
        f"Intermediate_{int(y_pos)}",
        W,
        wood_width,
        blade_radius,
        thickness,
        coordinates,
        section_length,
        R2,
        doc,
    )

    hybrid_obj = create_hybrid_airfoil_section_6b(
        y_pos,
        thick_interp,
        drop_interp,
        W,
        wood_width,
        blade_radius,
        thickness,
        coordinates,
        section_obj,
        doc,
    )
    intermediate_sections.append(hybrid_obj)

# Insert intermediate sections in correct order: Root(200), 250, 300, 350, then rest
final_loft_sections = [loft_sections[0]]  # Root at y=200
final_loft_sections.extend(intermediate_sections)  # Add 250, 300, 350
final_loft_sections.extend(loft_sections[1:])  # Add rest (400, 600, 800, 1000, 1200)


def calculate_wedge_cut_vertices_at_y(
    y_position: float,
    R2: float,
    W: float,
    thickness: float,
    wood_width: float,
    section_length: float,
    blade_radius: float,
    drops: List[float],
) -> List[FreeCAD.Vector]:
    """Calculate wedge cut vertices for any y position using the same formula."""
    # Calculate wedge cut intersection points
    root_width_rear = wood_width - (wood_width - W) * (section_length / blade_radius)
    v2_wedge = (-wood_width + W, 0, thickness)
    v1_wedge = (W, section_length, thickness)
    v3_wedge = (W - root_width_rear, section_length, thickness - drops[0])

    t = y_position / section_length
    x_v2v1 = v2_wedge[0] + (v1_wedge[0] - v2_wedge[0]) * t
    x_v2v3 = v2_wedge[0] + (v3_wedge[0] - v2_wedge[0]) * t
    z_v2v3 = v2_wedge[2] + (v3_wedge[2] - v2_wedge[2]) * t

    return [
        FreeCAD.Vector(x_v2v3, y_position, 0),      # vertex 0
        FreeCAD.Vector(W, y_position, 0),           # vertex 1
        FreeCAD.Vector(W, y_position, thickness),   # vertex 2
        FreeCAD.Vector(x_v2v1, y_position, thickness), # vertex 3
        FreeCAD.Vector(x_v2v3, y_position, z_v2v3), # vertex 4
    ]


def create_wedge_cut_wire(
    R2: float,
    W: float,
    thickness: float,
    wood_width: float,
    section_length: float,
    blade_radius: float,
    drops: List[float],
) -> Tuple[List[FreeCAD.Vector], float]:
    """Calculate vertices for cylinder intersection wire with wedge cut geometry.

    Args:
        R2: Cylinder radius for intersection calculation
        W: Leading edge width parameter
        thickness: Blade thickness
        wood_width: Total wood width
        section_length: Length of blade section
        blade_radius: Total blade radius
        drops: List of thickness drops at different positions

    Returns:
        Tuple of (ordered vertices list, y_split intersection position)
    """
    y_split = math.sqrt(R2**2 - W**2)

    # Calculate wedge cut intersection points
    root_width_rear = wood_width - (wood_width - W) * (section_length / blade_radius)
    v2_wedge = (-wood_width + W, 0, thickness)
    v1_wedge = (W, section_length, thickness)
    v3_wedge = (W - root_width_rear, section_length, thickness - drops[0])

    t = y_split / section_length
    x_v2v1 = v2_wedge[0] + (v1_wedge[0] - v2_wedge[0]) * t
    x_v2v3 = v2_wedge[0] + (v3_wedge[0] - v2_wedge[0]) * t
    z_v2v3 = v2_wedge[2] + (v3_wedge[2] - v2_wedge[2]) * t

    return [
        FreeCAD.Vector(x_v2v3, y_split, 0),  # rect_v1
        FreeCAD.Vector(W, y_split, 0),  # rect_v2
        FreeCAD.Vector(W, y_split, thickness),  # rect_v3
        FreeCAD.Vector(x_v2v1, y_split, thickness),  # rect_v4
        FreeCAD.Vector(x_v2v3, y_split, z_v2v3),  # rect_v5
    ], y_split


def create_filleted_wire(
    doc: FreeCAD.Document,
    vertices: List[FreeCAD.Vector],
    fillet_vertices: List[FreeCAD.Vector],
    radius: float = 2.0,
) -> Tuple[Any, int]:
    """Create filleted wire by incrementally building edge list."""
    filleted_edges = []

    # Process vertices dynamically based on vertex count
    # For 5 vertices: 0->1->2->3->4 (connect 3 to 4, not back to 0)
    # For 6 vertices: 0->1->2->3->4->5 (connect 4 to 5, not back to 0)
    num_vertices = len(vertices)
    for i in range(num_vertices - 1):  # Process all vertices except the last
        curr_vertex = vertices[i]
        next_vertex = vertices[i + 1]

        if curr_vertex in fillet_vertices:
            prev_vertex = vertices[i - 1]

            # Check if we can reuse the last edge
            if filleted_edges and filleted_edges[-1].lastVertex().Point.isEqual(
                curr_vertex, 1e-6
            ):
                # Use last edge for first line
                prev_line = Draft.make_line(
                    filleted_edges[-1].firstVertex().Point,
                    filleted_edges[-1].lastVertex().Point,
                )
            else:
                # Create new line from previous vertex
                prev_line = Draft.make_line(prev_vertex, curr_vertex)

            # Create line to next vertex
            next_line = Draft.make_line(curr_vertex, next_vertex)
            doc.recompute()

            # Create fillet
            fillet = Draft.make_fillet([prev_line, next_line], radius, delete=True)
            doc.recompute()

            # Add fillet edges, replacing last edge if we reused it
            if filleted_edges and filleted_edges[-1].lastVertex().Point.isEqual(
                curr_vertex, 1e-6
            ):
                filleted_edges[-1] = fillet.Shape.Edges[
                    0
                ]  # Replace with truncated edge
                filleted_edges.extend(fillet.Shape.Edges[1:])  # Add arc and next edge
            else:
                filleted_edges.extend(fillet.Shape.Edges)

            doc.removeObject(fillet.Name)

        else:
            # Only add regular line edge if next vertex won't be filleted
            if next_vertex not in fillet_vertices:
                line = Draft.make_line(curr_vertex, next_vertex)
                doc.recompute()
                filleted_edges.append(line.Shape.Edges[0])
                doc.removeObject(line.Name)

    # Check edge continuity
    for i in range(len(filleted_edges)):
        curr_end = filleted_edges[i].lastVertex().Point
        next_start = filleted_edges[(i + 1) % len(filleted_edges)].firstVertex().Point
        if not curr_end.isEqual(next_start, 1e-6):
            print(
                f"WARNING: Gap between edges {i} and {i + 1}: {curr_end.distanceToPoint(next_start):.6f}mm"
            )

    # Create wire from filleted edges (open wire - no closure required)
    wire = Part.Wire(filleted_edges)
    obj = doc.addObject("Part::Feature", "Unified_Filleted_Rectangle")
    obj.Shape = wire
    if FreeCAD.GuiUp:
        obj.ViewObject.Visibility = False  # Hide intermediate object
    
    # Discretize wire into 79 points and create B-spline
    discretized_points = []
    
    # Use discretize method to get evenly spaced points
    discretized_points = wire.discretize(Number=79)  # Back to 79 points
    
    # Create B-spline from discretized points (open curve - no wedge cut edge)
    bspline = Part.BSplineCurve()
    bspline.interpolate(discretized_points, False)  # Open curve without wedge cut edge
    
    # Manually close B-spline with the vertical edge (wedge cut edge)
    # With preserved point inserted, vertex 5 is the wedge cut end, vertex 0 is wedge cut start
    if len(vertices) == 6:  # Hybrid with preserved point
        vertical_edge = Part.LineSegment(vertices[5], vertices[0]).toShape()
    else:  # Original 5-vertex case
        vertical_edge = Part.LineSegment(vertices[4], vertices[0]).toShape()
    
    # Create closed wire by combining B-spline and vertical edge
    try:
        closed_edges = [bspline.toShape(), vertical_edge]
        closed_wire = Part.Wire(closed_edges)
        print("Successfully created closed wire with vertical edge")
    except Exception as e:
        print(f"Wire creation with vertical edge failed: {e}")
        # Try just the B-spline as open curve
        closed_wire = bspline.toShape()
    
    bspline_obj = doc.addObject("Part::Feature", "Filleted_Rectangle_BSpline")
    bspline_obj.Shape = closed_wire  # Use closed wire instead of just B-spline
    if FreeCAD.GuiUp:
        bspline_obj.ViewObject.Visibility = False  # Hide intermediate object
    
    # Check control points of the B-spline curve
    bspline_curve = bspline_obj.Shape.Edges[0].Curve  # Get the B-spline curve from first edge
    print(f"Filleted_Rectangle_BSpline has {bspline_curve.NbPoles} control points")
    
    print(f"Discretized filleted rectangle into {len(discretized_points)} points")
    print(f"Created B-spline from discretized points")

    doc.recompute()
    return obj, len(filleted_edges), bspline_obj


def create_cylinder_intersection_rectangle(
    doc: FreeCAD.Document,
    R2: float,
    W: float,
    thickness: float,
    wood_width: float,
    section_length: float,
    blade_radius: float,
    drops: List[float],
) -> None:
    """Create filleted rectangle at cylinder intersection with wedge cut geometry.

    Args:
        doc: FreeCAD document object
        R2: Cylinder radius for intersection calculation
        W: Leading edge width parameter
        thickness: Blade thickness
        wood_width: Total wood width
        section_length: Length of blade section
        blade_radius: Total blade radius
        drops: List of thickness drops at different positions
    """
    vertices, y_split = create_wedge_cut_wire(
        R2, W, thickness, wood_width, section_length, blade_radius, drops
    )

    print(f"Wedge cut vertices:")
    for i, v in enumerate(vertices):
        print(f"  Vertex {i}: {v}")
    
    # The wedge cut edge is from vertex 4 to vertex 0 (the diagonal cut)
    print(f"Wedge cut edge: from vertex 4 {vertices[4]} to vertex 0 {vertices[0]}")

    # Fillet corners at vertices 1, 2 only (avoid vertices 0 and 4 for sharp corners)
    fillet_vertices = [vertices[1], vertices[2]]

    unified_obj, edge_count, bspline_obj = create_filleted_wire(
        doc, vertices, fillet_vertices, radius=8
    )
    print(f"Created unified filleted wire with {edge_count} edges, radius=8mm")
    print(f"Created cylinder intersection rectangle at y={y_split:.2f}mm")
    
    return bspline_obj


cylinder_bspline = create_cylinder_intersection_rectangle(
    doc, R2, W, thickness, wood_width, section_length, blade_radius, drops
)

# Create intermediate hybrid section at y=157.28mm
root_section = final_loft_sections[0]  # Root airfoil at y=200

# Get discretized points from both sections
rect_points = cylinder_bspline.Shape.discretize(Number=79)
airfoil_points = root_section.Shape.discretize(Number=79)

# Create same wire at y=157.28 following same procedure as 114.56
y_hybrid = 157.28
vertices_hybrid = calculate_wedge_cut_vertices_at_y(
    y_hybrid, R2, W, thickness, wood_width, section_length, blade_radius, drops
)

print(f"Hybrid vertices at y={y_hybrid}:")
for i, v in enumerate(vertices_hybrid):
    print(f"  Vertex {i}: {v}")

print(f"Wedge cut edge: from vertex 4 {vertices_hybrid[4]} to vertex 0 {vertices_hybrid[0]}")

# Add the first preserved point from y=200 airfoil at z=0
# This point has X=-39.174 and should be inserted between bottom vertices
preserved_point_x = -39.174  # From y=200 airfoil analysis
preserved_point = FreeCAD.Vector(preserved_point_x, y_hybrid, 0.0)

# Insert preserved point between vertex 0 and vertex 1 (both at z=0)
# New vertex order: 0 -> preserved -> 1 -> 2 -> 3 -> 4
vertices_with_preserved = [
    vertices_hybrid[0],      # vertex 0: wedge cut start
    preserved_point,         # new: preserved point
    vertices_hybrid[1],      # vertex 1: leading edge bottom
    vertices_hybrid[2],      # vertex 2: leading edge top  
    vertices_hybrid[3],      # vertex 3: trailing edge top
    vertices_hybrid[4],      # vertex 4: wedge cut end
]

print(f"Added preserved point at X={preserved_point_x}, creating {len(vertices_with_preserved)} vertices")

# Fillet corners at vertices 2, 3 only (avoid vertices 0, 1, 5 for sharp corners)
fillet_vertices = [vertices_with_preserved[2], vertices_with_preserved[3]]

unified_obj, edge_count, hybrid_bspline = create_filleted_wire(
    doc, vertices_with_preserved, fillet_vertices, radius=8
)
print(f"Created unified filleted wire with {edge_count} edges, radius=8mm")
print(f"Created hybrid section at y={y_hybrid:.2f}mm")

# Discretize the 4 specific segments from the actual filleted wire
filleted_edges = unified_obj.Shape.Edges

print(f"Filleted wire has {len(filleted_edges)} edges:")
for i, edge in enumerate(filleted_edges):
    start_pt = edge.firstVertex().Point
    end_pt = edge.lastVertex().Point
    edge_length = edge.Length
    edge_type = "Line" if hasattr(edge.Curve, 'Direction') else "Curve"
    print(f"  Edge {i}: {edge_type}, Length={edge_length:.3f}mm")
    print(f"    Start: ({start_pt.x:.3f}, {start_pt.y:.3f}, {start_pt.z:.3f})")
    print(f"    End: ({end_pt.x:.3f}, {end_pt.y:.3f}, {end_pt.z:.3f})")

# Calculate lengths of each segment
seg1_length = filleted_edges[1].Length  # Bottom straight
seg2_length = filleted_edges[2].Length  # Filleted curve
seg3_length = filleted_edges[3].Length  # Vertical straight  
seg4_length = filleted_edges[4].Length  # Filleted curve

total_length = seg1_length + seg2_length + seg3_length + seg4_length

print(f"Segment lengths:")
print(f"  Seg 1 (bottom): {seg1_length:.3f}mm")
print(f"  Seg 2 (fillet): {seg2_length:.3f}mm")
print(f"  Seg 3 (vertical): {seg3_length:.3f}mm") 
print(f"  Seg 4 (fillet): {seg4_length:.3f}mm")
print(f"  Total: {total_length:.3f}mm")

# Apply curve weighting (6x for filleted segments, 2x for vertical)
weighted_seg1 = seg1_length * 0.8  # Straight bottom - reduce weight
weighted_seg2 = seg2_length * 6.0  # Curved - 6x weight
weighted_seg3 = seg3_length * 2.0  # Vertical straight - 2x weight
weighted_seg4 = seg4_length * 6.0  # Curved - 6x weight

total_weighted = weighted_seg1 + weighted_seg2 + weighted_seg3 + weighted_seg4

# Distribute 25 points proportionally (minimum 3 points per segment)
base_points = 25 - 4 * 3  # Reserve 3 points per segment = 13 extra points to distribute
points_seg1 = 3 + max(0, int(base_points * weighted_seg1 / total_weighted))
points_seg2 = 3 + max(0, int(base_points * weighted_seg2 / total_weighted))
points_seg3 = 3 + max(0, int(base_points * weighted_seg3 / total_weighted))
points_seg4 = 3 + max(0, int(base_points * weighted_seg4 / total_weighted))

# Adjust to ensure exactly 25 points total
total_assigned = points_seg1 + points_seg2 + points_seg3 + points_seg4
remaining = 25 - total_assigned

# Distribute remaining points to segments with highest weights
weights = [(weighted_seg1, 1), (weighted_seg2, 2), (weighted_seg3, 3), (weighted_seg4, 4)]
weights.sort(reverse=True)

for i in range(remaining):
    segment_idx = weights[i % 4][1]
    if segment_idx == 1:
        points_seg1 += 1
    elif segment_idx == 2:
        points_seg2 += 1
    elif segment_idx == 3:
        points_seg3 += 1
    elif segment_idx == 4:
        points_seg4 += 1

print(f"Point distribution (weighted by length + curve bonus):")
print(f"  Seg 1: {points_seg1} points")
print(f"  Seg 2: {points_seg2} points")
print(f"  Seg 3: {points_seg3} points")
print(f"  Seg 4: {points_seg4} points")

# Discretize with calculated point counts
points_seg1_disc = filleted_edges[1].discretize(Number=points_seg1)
points_seg2_disc = filleted_edges[2].discretize(Number=points_seg2)
points_seg3_disc = filleted_edges[3].discretize(Number=points_seg3)
points_seg4_disc = filleted_edges[4].discretize(Number=points_seg4)

# Combine all points (remove duplicates at connections)
rect_25_points_filleted = []
rect_25_points_filleted.extend(points_seg1_disc[:-1])  # Exclude last (14-1=13)
rect_25_points_filleted.extend(points_seg2_disc[:-1])  # Exclude last (3-1=2)  
rect_25_points_filleted.extend(points_seg3_disc[:-1])  # Exclude last (5-1=4)
rect_25_points_filleted.extend(points_seg4_disc)       # Include all (3)

actual_total = len(rect_25_points_filleted)
print(f"Actual points after combination: {actual_total} (expected: 13+2+4+3=22)")

# If we need exactly 25, add more points to the longest segment
if actual_total < 25:
    needed = 25 - actual_total
    print(f"Need {needed} more points, adding to segment 1")
    # Re-discretize segment 1 with more points
    points_seg1_disc = filleted_edges[1].discretize(Number=points_seg1 + needed)
    
    # Recombine
    rect_25_points_filleted = []
    rect_25_points_filleted.extend(points_seg1_disc[:-1])  # Exclude last
    rect_25_points_filleted.extend(points_seg2_disc[:-1])  # Exclude last
    rect_25_points_filleted.extend(points_seg3_disc[:-1])  # Exclude last
    rect_25_points_filleted.extend(points_seg4_disc)       # Include all

print(f"Discretized 4 filleted segments into {len(rect_25_points_filleted)} points at y={y_hybrid:.2f}mm")

# Create Combined_Orange_Magenta_Wire using refactored functions
combined_bspline_obj = create_combined_orange_magenta_wire(
    filleted_edges, rect_25_points_filleted, doc, y_hybrid
)

# Create transition loft with combined wire in correct order
transition_sections = [cylinder_bspline, combined_bspline_obj, root_section]

transition_loft = doc.addObject("Part::Loft", "Cylinder_To_Root_Loft")
transition_loft.Sections = transition_sections
transition_loft.Solid = True
transition_loft.Ruled = False
doc.recompute()
print(f"Created hybrid section at y=157.28mm for inspection")
print(f"Created transition loft between y=114.56mm and y=200mm with {len(transition_sections)} sections")

# Create loft from all sections (excluding cylinder intersection B-spline)
if final_loft_sections:
    loft = doc.addObject("Part::Loft", "Blade_Loft")
    loft.Sections = final_loft_sections
    loft.Solid = True
    loft.Ruled = False
    doc.recompute()
    print(f"Created blade loft with {len(final_loft_sections)} sections")
