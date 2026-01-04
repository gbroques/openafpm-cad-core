"""
Wind Turbine Twisted Tapered Plank Generator

Creates a parameterized wind turbine blade with flat-bottom sections and leading edge transitions.
Supports 45° ramp cutting and 120° root cut for proper turbine mounting.

Usage:
    python create_twisted_tapered_plank.py

The script generates:
- Root sections (Root_a, Root_b) with flat bottoms
- Blade sections (Section_5, Section_4a/4b, Section_3, Section_2, Section_1)
- Leading edge wedge cutters for smooth transitions
- 45° ramp and 120° root cuts for mounting
"""

import FreeCAD
import Part
from FreeCAD import Vector
import FreeCADGui as Gui
import math
from typing import Dict, Any, Tuple

# Debug flag to control visualization objects
DEBUG = False

def validate_geometry(obj: Any, name: str) -> None:
    """Validate FreeCAD geometry object."""
    if hasattr(obj, 'Shape') and not obj.Shape.isValid():
        print(f"Warning: {name} geometry may be invalid")

# Turbine configuration
config = {
    # 2400mm turbine blade root parameters
    'W': 50,  # tip width, also distance from leading edge to center
    'X': 87,  # 120° root cut dimension
    'R2': 125,  # radius of flat circular area on back
    'wood_width': 200,  # x dimension
    'thickness': 40,  # z dimension
    
    # Blade parameters
    'blade_radius': 1200,  # mm
    'num_sections': 6,
    
    # Drop values for 2400mm turbine (controls trailing edge angle)
    # drops[0] reduced from 40 to 38.8 to create 1.2mm minimum trailing edge thickness
    'drops': [38.8, 32, 15, 7, 3, 1],  # mm
    
    # Thickness values for 2400mm turbine (at leading edge)
    'thicknesses': [27, 27, 19, 14, 9, 6],  # mm
}

def setup_document() -> Tuple[Any, Any]:
    """Setup FreeCAD document and create main container.
    
    Returns:
        Tuple[FreeCAD.Document, FreeCAD.DocumentObject]: Document and blade container
    """
    if not FreeCAD.ActiveDocument:
        FreeCAD.newDocument()
    
    doc = FreeCAD.ActiveDocument
    blade_container = doc.addObject("App::Part", "TwistedTaperedPlank")
    return doc, blade_container

def create_wedge_cutter(config: Dict[str, Any]) -> Any:
    """Create tetrahedral wedge for 45° ramp cutting.
    
    Args:
        config: Turbine configuration dictionary containing:
            - W: tip width (mm)
            - wood_width: maximum blade width (mm) 
            - thickness: blade thickness (mm)
            - blade_radius: total blade radius (mm)
            - num_sections: number of blade sections
    
    Returns:
        FreeCAD.DocumentObject: Tetrahedral wedge cutter for 45° ramp
    """
    W = config['W']
    wood_width = config['wood_width']
    thickness = config['thickness']
    blade_radius = config['blade_radius']
    num_sections = config['num_sections']
    section_length = blade_radius / num_sections
    
    root_width_front = wood_width
    root_width_rear = wood_width - (wood_width - W) * (section_length / blade_radius)

    v1 = Vector(W, section_length, thickness)
    v2 = Vector(W - root_width_front, 0, thickness)
    v3 = Vector(W - root_width_rear, section_length, thickness - config['drops'][0])  # Respect drops[0] value
    v4 = Vector(W - root_width_rear, section_length, thickness)

    face1 = Part.Face(Part.makePolygon([v1, v2, v4, v1]))
    face2 = Part.Face(Part.makePolygon([v1, v2, v3, v1]))
    face3 = Part.Face(Part.makePolygon([v1, v3, v4, v1]))
    face4 = Part.Face(Part.makePolygon([v2, v3, v4, v2]))

    shell = Part.Shell([face1, face2, face3, face4])
    wedge = Part.Solid(shell)
    wedge_obj = Part.show(wedge, "Wedge_cutter")
    validate_geometry(wedge_obj, "Wedge_cutter")
    return wedge_obj

def create_section(y_start: float, y_end: float, thick_start: float, thick_end: float, 
                  drop_start: float, drop_end: float, z_top_start: float, z_top_end: float, 
                  z_bottom_right_start: float, z_bottom_right_end: float, name: str, 
                  config: Dict[str, Any]) -> Any:
    """Create a blade section with specified parameters.
    
    Args:
        y_start: Starting Y position along blade (mm)
        y_end: Ending Y position along blade (mm)
        thick_start: Leading edge thickness at start (mm)
        thick_end: Leading edge thickness at end (mm)
        drop_start: Trailing edge drop at start (mm)
        drop_end: Trailing edge drop at end (mm)
        z_top_start: Top surface Z at trailing edge start (mm)
        z_top_end: Top surface Z at trailing edge end (mm)
        z_bottom_right_start: Bottom surface Z at trailing edge start (mm)
        z_bottom_right_end: Bottom surface Z at trailing edge end (mm)
        name: Section name for FreeCAD object
        config: Turbine configuration dictionary
    
    Returns:
        FreeCAD.DocumentObject: Blade section solid
    """
    W = config['W']
    wood_width = config['wood_width']
    thickness = config['thickness']
    blade_radius = config['blade_radius']
    
    width_start = wood_width - (wood_width - W) * (y_start / blade_radius)
    width_end = wood_width - (wood_width - W) * (y_end / blade_radius)
    
    flat_bottom = (z_bottom_right_start == 0 and z_bottom_right_end == 0)
    
    if flat_bottom:
        z_bottom_start = 0
        z_bottom_end = 0
    else:
        z_bottom_start = thickness - thick_start
        z_bottom_end = thickness - thick_end
    
    v1 = Vector(W, y_start, z_bottom_start)
    v2 = Vector(W - width_start, y_start, z_bottom_right_start)
    v3 = Vector(W - width_end, y_end, z_bottom_right_end)
    v4 = Vector(W, y_end, z_bottom_end)
    v5 = Vector(W, y_start, thickness)
    v6 = Vector(W - width_start, y_start, z_top_start)
    v7 = Vector(W - width_end, y_end, z_top_end)
    v8 = Vector(W, y_end, thickness)
    
    front = Part.Face(Part.makePolygon([v1, v2, v6, v5, v1]))
    back = Part.Face(Part.makePolygon([v4, v3, v7, v8, v4]))
    bottom = Part.makeRuledSurface(Part.makeLine(v1, v2), Part.makeLine(v4, v3))
    left = Part.makeRuledSurface(Part.makeLine(v1, v4), Part.makeLine(v5, v8))
    top = Part.makeRuledSurface(Part.makeLine(v5, v6), Part.makeLine(v8, v7))
    right = Part.makeRuledSurface(Part.makeLine(v2, v3), Part.makeLine(v6, v7))
    
    shell = Part.Shell([bottom, top, front, back, left, right])
    section = Part.Solid(shell)
    return Part.show(section, name)

def create_leading_edge_wedge(y_start: float, y_end: float, z_top_start: float, z_top_end: float, 
                             name: str, y_split: float, y_term: float, x_term: float, 
                             t_term: float, config: Dict[str, Any]) -> Any:
    """Create leading edge wedge cutter for smooth transitions.
    
    Creates either a 4-faced pyramid wedge (for Root_b) or 5-faced tapered wedge
    (for other sections) to cut leading edge transitions from thick to flat bottom.
    
    Args:
        y_start: Starting Y position (mm)
        y_end: Ending Y position (mm)
        z_top_start: Top surface Z at start (mm)
        z_top_end: Top surface Z at end (mm)
        name: Wedge name for FreeCAD object
        y_split: Y position where root splits (mm)
        y_term: Y position where trailing edge reaches z=0 (mm)
        x_term: X position of termination point (mm)
        t_term: Interpolation parameter for termination
        config: Turbine configuration dictionary
    
    Returns:
        FreeCAD.DocumentObject: Leading edge wedge cutter
    """
    W = config['W']
    thickness = config['thickness']
    thicknesses = config['thicknesses']
    
    t_start = (y_start - y_split) / (y_term - y_split) if y_term != y_split else 0
    t_end = (y_end - y_split) / (y_term - y_split) if y_term != y_split else 0
    t_start = max(0, min(1, t_start))
    t_end = max(0, min(1, t_end))
    
    x_start = W + t_start * (x_term - W)
    x_end = W + t_end * (x_term - W)
    
    if name == "Root_b_wedge":
        z_leading_start = 0
        z_leading_end = 0
    elif "Section_5" in name:
        z_leading_start = thickness - thicknesses[0]
        z_leading_end = thickness - thicknesses[1]
    else:  # Section_4a
        thick_term = thicknesses[1] + t_term * (thicknesses[2] - thicknesses[1])
        z_leading_start = thickness - thicknesses[1]
        z_leading_end = thickness - thick_term
    
    if "Root_b" in name and abs(z_leading_start) < 0.1 and abs(z_leading_end) < 0.1:
        # 4-faced pyramid wedge with 1mm minimum thickness respect
        v1 = Vector(W, y_start, 0)
        v2 = Vector(W, y_end, 0)
        v3 = Vector(x_end, y_end, 0)  # Bottom vertex at z=0
        v4 = Vector(x_start, y_start, 0)
        v5 = Vector(W, y_end, thickness - thicknesses[0])
        
        faces = [
            Part.Face(Part.makePolygon([v1, v2, v3, v4, v1])),
            Part.Face(Part.makePolygon([v1, v2, v5, v1])),
            Part.Face(Part.makePolygon([v2, v3, v5, v2])),
            Part.Face(Part.makePolygon([v3, v4, v5, v3]))
        ]
        
        shell = Part.Shell(faces)
        wedge_solid = Part.Solid(shell)
        return Part.show(wedge_solid, name)
    else:
        # 5-faced wedge
        v1 = Vector(W, y_start, 0)
        v2 = Vector(W, y_end, 0)
        v3 = Vector(x_end, y_end, 0)
        v4 = Vector(x_start, y_start, 0)
        v5 = Vector(W, y_start, z_leading_start)
        v6 = Vector(W, y_end, z_leading_end)
        
        faces = [
            Part.Face(Part.makePolygon([v1, v2, v3, v4, v1])),
            Part.Face(Part.makePolygon([v1, v2, v6, v5, v1])),
            Part.Face(Part.makePolygon([v2, v3, v6, v2])),
            Part.Face(Part.makePolygon([v4, v1, v5, v4]))
        ]
        
        # Top slanted face
        edges = [Part.makeLine(v5, v6), Part.makeLine(v6, v3), 
                Part.makeLine(v3, v4), Part.makeLine(v4, v5)]
        wire = Part.Wire(edges)
        face = Part.makeFilledFace([wire])
        faces.append(face)
        
        shell = Part.Shell(faces)
        wedge_solid = Part.Solid(shell)
        return Part.show(wedge_solid, name)

# Main execution
doc, blade_container = setup_document()

# Extract commonly used values
W = config['W']
X = config['X']
R2 = config['R2']
wood_width = config['wood_width']
thickness = config['thickness']
blade_radius = config['blade_radius']
num_sections = config['num_sections']
drops = config['drops']
thicknesses = config['thicknesses']
section_length = blade_radius / num_sections

# Calculate root split point where cylinder intersects leading edge
y_split = math.sqrt(R2**2 - W**2)

# Calculate termination point where trailing edge bottom reaches z=0
# Between Station 5 (y=400) and Station 4 (y=600)
station_5_y = 400
station_4_y = 600
w5 = wood_width - (wood_width - W) * (station_5_y / blade_radius)
w4 = wood_width - (wood_width - W) * (station_4_y / blade_radius)
z5_unclamped = (thickness - drops[1]) - thicknesses[1]
z4 = (thickness - drops[2]) - thicknesses[2]
t_term = -z5_unclamped / (z4 - z5_unclamped)
y_term = station_5_y + t_term * (station_4_y - station_5_y)
x_term_width = w5 + t_term * (w4 - w5)
x_term = W - x_term_width

# Create blade sections
blocks = []

for i in range(num_sections):
    y_start = i * section_length
    y_end = (i + 1) * section_length
    
    thick_start = thicknesses[i - 1] if i > 0 else thickness
    thick_end = thicknesses[i]
    
    # Create sections with consistent naming
    section_names = ["Section_6a_block", "Section_6b_block", "Section_5_block", "Section_4a_block", "Section_4b", "Section_3", "Section_2", "Section_1"]
    
    if i == 0:
        # Section_6a: y=0 to y=y_split, flat bottom
        root_a = create_section(0, y_split, thickness, thickness, 0, 0,
                               thickness, thickness, 0, 0, "Section_6a_block", config)
        blocks.append(root_a)
        
        # Root_b: y=y_split to y=section_length, flat bottom with 1mm trailing edge
        width_start = wood_width - (wood_width - W) * (y_split / blade_radius)
        width_end = wood_width - (wood_width - W) * (section_length / blade_radius)
        
        v1 = Vector(W, y_split, 0)
        v2 = Vector(W - width_start, y_split, 0)
        v3 = Vector(W - width_end, section_length, 0)  # Trailing edge bottom stays at z=0
        v4 = Vector(W, section_length, 0)
        v5 = Vector(W, y_split, thickness)
        v6 = Vector(W - width_start, y_split, thickness)
        v7 = Vector(W - width_end, section_length, thickness)  # Trailing edge top at original height
        v8 = Vector(W, section_length, thickness)
        
        front = Part.Face(Part.makePolygon([v1, v2, v6, v5, v1]))
        back = Part.Face(Part.makePolygon([v4, v3, v7, v8, v4]))
        bottom = Part.makeRuledSurface(Part.makeLine(v1, v2), Part.makeLine(v4, v3))
        left = Part.makeRuledSurface(Part.makeLine(v1, v4), Part.makeLine(v5, v8))
        top = Part.makeRuledSurface(Part.makeLine(v5, v6), Part.makeLine(v8, v7))
        right = Part.makeRuledSurface(Part.makeLine(v2, v3), Part.makeLine(v6, v7))
        
        shell_rb = Part.Shell([bottom, top, front, back, left, right])
        root_b_solid = Part.Solid(shell_rb)
        root_b = Part.show(root_b_solid, "Section_6b_block")
        blocks.append(root_b)
        continue
    
    drop_start = drops[i - 1] if i > 0 else 0
    drop_end = drops[i]
    z_top_start = thickness - drop_start
    z_top_end = thickness - drop_end
    z_bottom_right_start = max(0, z_top_start - thick_start)
    z_bottom_right_end = max(0, z_top_end - thick_end)
    
    if i == 1:  # Section_5: use standard create_section with natural 1mm thickness
        section_obj = create_section(y_start, y_end, thick_start, thick_end, 0, 0,
                                    z_top_start, z_top_end, z_bottom_right_start, z_bottom_right_end, section_names[2], config)
        blocks.append(section_obj)
    elif i == 2:  # Section_4: split at termination point
        thick_term = thicknesses[1] + t_term * (thicknesses[2] - thicknesses[1])
        drop_term = drops[1] + t_term * (drops[2] - drops[1])
        z_top_term = thickness - drop_term
        
        section_4a = create_section(y_start, y_term, thick_start, thick_term, drops[1], drop_term, 
                                   z_top_start, z_top_term, 0, 0, section_names[3], config)
        blocks.append(section_4a)
        
        section_4b = create_section(y_term, y_end, thick_term, thick_end, drop_term, drops[2],
                                   z_top_term, z_top_end, 0, z_bottom_right_end, section_names[4], config)
        blocks.append(section_4b)
    else:
        # Use proper section index (i+2 accounts for Root_a, Root_b offset)
        section_name = section_names[min(i+2, len(section_names)-1)]
        section_obj = create_section(y_start, y_end, thick_start, thick_end, 0, 0,
                                    z_top_start, z_top_end, z_bottom_right_start, z_bottom_right_end, section_name, config)
        blocks.append(section_obj)

wedge_obj = create_wedge_cutter(config)

# Create wedges using named constants
section_5_start = 200
section_5_end = 400
drop_at_term = drops[1] + t_term * (drops[2] - drops[1])
root_b_wedge = create_leading_edge_wedge(y_split, section_length, thickness, thickness, "Root_b_wedge", y_split, y_term, x_term, t_term, config)
section_5_wedge = create_leading_edge_wedge(section_5_start, section_5_end, thickness - drops[0], thickness - drops[1], "Section_5_wedge", y_split, y_term, x_term, t_term, config)
section_4a_wedge = create_leading_edge_wedge(section_5_end, y_term, thickness - drops[1], thickness - drop_at_term, "Section_4a_wedge", y_split, y_term, x_term, t_term, config)

# Cut operations
# Cut operations
Section_6a_intermediate = doc.addObject("Part::Cut", "Section_6a_intermediate")
Section_6a_intermediate.Base = blocks[0]
Section_6a_intermediate.Tool = wedge_obj

# Two-step Section_6b cutting
Section_6b_step1 = doc.addObject("Part::Cut", "Section_6b_step1")
Section_6b_step1.Base = blocks[1]
Section_6b_step1.Tool = wedge_obj

Section_6b = doc.addObject("Part::Cut", "Section_6b")
Section_6b.Base = Section_6b_step1
Section_6b.Tool = root_b_wedge

# Cut Section_5 and Section_4a
Section_5 = doc.addObject("Part::Cut", "Section_5")
Section_5.Base = blocks[2]
Section_5.Tool = section_5_wedge

Section_4a = doc.addObject("Part::Cut", "Section_4a")
Section_4a.Base = blocks[3]
Section_4a.Tool = section_4a_wedge

# Create 120° root cut
tri_pts = [Vector(W, 0, 0), Vector(0, 0, 0), Vector(W, X, 0), Vector(W, 0, 0)]
tri_face = Part.Face(Part.makePolygon(tri_pts))
root_wedge = tri_face.extrude(Vector(0, 0, thickness))
root_wedge_obj = Part.show(root_wedge, "Root_120_cutter")

Section_6a = doc.addObject("Part::Cut", "Section_6a")
Section_6a.Base = Section_6a_intermediate
Section_6a.Tool = root_wedge_obj


# Add R2 cylinder visualization
if DEBUG:
    cyl_obj = doc.addObject("Part::Cylinder", "R2_flat_area")
    cyl_obj.Radius = R2
    cyl_obj.Height = thickness
    cyl_obj.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(Vector(0,0,1), 0))

# Hide intermediate objects and original sections
if FreeCAD.GuiUp:
    # Hide intermediate cuts and tools
    Section_6a_intermediate.ViewObject.Visibility = False
    Section_6b_step1.ViewObject.Visibility = False
    wedge_obj.ViewObject.Visibility = False
    root_wedge_obj.ViewObject.Visibility = False
    
    # Hide original sections that get cut
    for i in [0, 1, 2, 3]:  # Root_a, Root_b, Section_5, Section_4a
        if i < len(blocks) and hasattr(blocks[i], 'ViewObject'):
            blocks[i].ViewObject.Visibility = False
    
    # Hide wedge cutters
    for wedge in [root_b_wedge, section_5_wedge, section_4a_wedge]:
        if wedge and hasattr(wedge, 'ViewObject'):
            wedge.ViewObject.Visibility = False

doc.recompute()

# Add all final objects to container
final_objects = [Section_6a, Section_6b, Section_5, Section_4a]
remaining_sections = blocks[4:]  # Section_4b, Section_3, Section_2, Section_1
for obj in final_objects + remaining_sections + [cyl_obj]:
    if obj:
        blade_container.addObject(obj)

if FreeCAD.GuiUp:
    Gui.SendMsgToActiveView("ViewFit")

print(f"✓ Root created with 45° ramp and 120° root cut")
print(f"  W={W}mm, X={X}mm, R2={R2}mm")
