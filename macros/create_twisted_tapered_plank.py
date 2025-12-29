import FreeCAD
import Part
from FreeCAD import Vector
import FreeCADGui as Gui
import math

# 2400mm turbine blade root parameters
W = 50  # tip width, also distance from leading edge to center
X = 87  # 120° root cut dimension
R2 = 125  # radius of flat circular area on back
wood_width = 200  # x dimension
thickness = 40  # z dimension

# Blade parameters
blade_radius = 1200  # mm
num_sections = 6
section_length = blade_radius / num_sections

# Drop values for 2400mm turbine (controls trailing edge angle)
drops = [40, 32, 15, 7, 3, 1]  # mm

# Thickness values for 2400mm turbine (at leading edge)
thicknesses = [27, 27, 19, 14, 9, 6]  # mm

# Calculate root split point where cylinder intersects leading edge
y_split = math.sqrt(R2**2 - W**2)

if not FreeCAD.ActiveDocument:
    FreeCAD.newDocument()

doc = FreeCAD.ActiveDocument
blade_container = doc.addObject("App::Part", "TwistedTaperedPlank")

# Calculate termination point where trailing edge bottom reaches z=0
y5 = 400
y4 = 600
w5 = wood_width - (wood_width - W) * (y5 / blade_radius)
w4 = wood_width - (wood_width - W) * (y4 / blade_radius)
z5_unclamped = (thickness - drops[1]) - thicknesses[1]
z4 = (thickness - drops[2]) - thicknesses[2]
t_term = -z5_unclamped / (z4 - z5_unclamped)
y_term = y5 + t_term * (y4 - y5)
x_term_width = w5 + t_term * (w4 - w5)
x_term = W - x_term_width

def create_section(y_start, y_end, thick_start, thick_end, drop_start, drop_end, z_top_start, z_top_end, z_bottom_right_start, z_bottom_right_end, name):
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

# Create blade sections
blocks = []

for i in range(num_sections):
    y_start = i * section_length
    y_end = (i + 1) * section_length
    
    thick_start = thicknesses[i - 1] if i > 0 else thickness
    thick_end = thicknesses[i]
    
    if i == 0:
        # Root_a: y=0 to y=y_split, flat bottom
        root_a = create_section(0, y_split, thickness, thickness, 0, 0,
                               thickness, thickness, 0, 0, "Root_a")
        blocks.append(root_a)
        
        # Root_b: y=y_split to y=section_length, flat bottom
        width_start = wood_width - (wood_width - W) * (y_split / blade_radius)
        width_end = wood_width - (wood_width - W) * (section_length / blade_radius)
        
        v1 = Vector(W, y_split, 0)
        v2 = Vector(W - width_start, y_split, 0)
        v3 = Vector(W - width_end, section_length, 0)
        v4 = Vector(W, section_length, 0)
        v5 = Vector(W, y_split, thickness)
        v6 = Vector(W - width_start, y_split, thickness)
        v7 = Vector(W - width_end, section_length, thickness)
        v8 = Vector(W, section_length, thickness)
        
        front = Part.Face(Part.makePolygon([v1, v2, v6, v5, v1]))
        back = Part.Face(Part.makePolygon([v4, v3, v7, v8, v4]))
        bottom = Part.makeRuledSurface(Part.makeLine(v1, v2), Part.makeLine(v4, v3))
        left = Part.makeRuledSurface(Part.makeLine(v1, v4), Part.makeLine(v5, v8))
        top = Part.makeRuledSurface(Part.makeLine(v5, v6), Part.makeLine(v8, v7))
        right = Part.makeRuledSurface(Part.makeLine(v2, v3), Part.makeLine(v6, v7))
        
        shell_rb = Part.Shell([bottom, top, front, back, left, right])
        root_b_solid = Part.Solid(shell_rb)
        root_b = Part.show(root_b_solid, "Root_b")
        blocks.append(root_b)
        continue
    
    drop_start = drops[i - 1] if i > 0 else 0
    drop_end = drops[i]
    z_top_start = thickness - drop_start
    z_top_end = thickness - drop_end
    z_bottom_right_start = max(0, z_top_start - thick_start)
    z_bottom_right_end = max(0, z_top_end - thick_end)
    
    if i == 1:  # Section_5: flat bottom
        section_obj = create_section(y_start, y_end, thick_start, thick_end, 0, 0,
                                    z_top_start, z_top_end, 0, 0, "Section_5")
        blocks.append(section_obj)
    elif i == 2:  # Section_4: split at termination point
        thick_term = thicknesses[1] + t_term * (thicknesses[2] - thicknesses[1])
        drop_term = drops[1] + t_term * (drops[2] - drops[1])
        z_top_term = thickness - drop_term
        
        section_4a = create_section(y_start, y_term, thick_start, thick_term, drops[1], drop_term, 
                                   z_top_start, z_top_term, 0, 0, "Section_4a")
        blocks.append(section_4a)
        
        section_4b = create_section(y_term, y_end, thick_term, thick_end, drop_term, drops[2],
                                   z_top_term, z_top_end, 0, z_bottom_right_end, "Section_4b")
        blocks.append(section_4b)
    else:
        section_obj = create_section(y_start, y_end, thick_start, thick_end, 0, 0,
                                    z_top_start, z_top_end, z_bottom_right_start, z_bottom_right_end, f"Section_{7-i}")
        blocks.append(section_obj)

# Create tetrahedral wedge for 45° ramp
root_width_front = wood_width
root_width_rear = wood_width - (wood_width - W) * (section_length / blade_radius)

v1 = Vector(W, section_length, thickness)
v2 = Vector(W - root_width_front, 0, thickness)
v3 = Vector(W - root_width_rear, section_length, 0)
v4 = Vector(W - root_width_rear, section_length, thickness)

face1 = Part.Face(Part.makePolygon([v1, v2, v4, v1]))
face2 = Part.Face(Part.makePolygon([v1, v2, v3, v1]))
face3 = Part.Face(Part.makePolygon([v1, v3, v4, v1]))
face4 = Part.Face(Part.makePolygon([v2, v3, v4, v2]))

shell = Part.Shell([face1, face2, face3, face4])
wedge = Part.Solid(shell)
wedge_obj = Part.show(wedge, "Wedge_cutter")

def create_leading_edge_wedge(y_start, y_end, z_top_start, z_top_end, name):
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
        # 4-faced pyramid wedge
        v1 = Vector(W, y_start, 0)
        v2 = Vector(W, y_end, 0)
        v3 = Vector(x_end, y_end, 0)
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

# Create wedges
drop_at_term = drops[1] + t_term * (drops[2] - drops[1])
root_b_wedge = create_leading_edge_wedge(y_split, section_length, thickness, thickness, "Root_b_wedge")
section_5_wedge = create_leading_edge_wedge(200, 400, thickness - drops[0], thickness - drops[1], "Section_5_wedge")
section_4a_wedge = create_leading_edge_wedge(400, y_term, thickness - drops[1], thickness - drop_at_term, "Section_4a_wedge")

# Cut operations
root_a_cut = doc.addObject("Part::Cut", "Root_a_cut")
root_a_cut.Base = blocks[0]
root_a_cut.Tool = wedge_obj
if FreeCAD.GuiUp:
    root_a_cut.ViewObject.Visibility = False

# Two-step Root_b cutting
root_b_step1 = doc.addObject("Part::Cut", "Root_b_step1")
root_b_step1.Base = blocks[1]
root_b_step1.Tool = wedge_obj

root_b_cut = doc.addObject("Part::Cut", "Root_b_cut")
root_b_cut.Base = root_b_step1
root_b_cut.Tool = root_b_wedge

# Cut Section_5 and Section_4a
section_5_cut = doc.addObject("Part::Cut", "Section_5_cut")
section_5_cut.Base = blocks[2]
section_5_cut.Tool = section_5_wedge

section_4a_cut = doc.addObject("Part::Cut", "Section_4a_cut")
section_4a_cut.Base = blocks[3]
section_4a_cut.Tool = section_4a_wedge

# Create 120° root cut
tri_pts = [Vector(W, 0, 0), Vector(0, 0, 0), Vector(W, X, 0), Vector(W, 0, 0)]
tri_face = Part.Face(Part.makePolygon(tri_pts))
root_wedge = tri_face.extrude(Vector(0, 0, thickness))
root_wedge_obj = Part.show(root_wedge, "Root_120_cutter")
if FreeCAD.GuiUp:
    root_wedge_obj.ViewObject.Visibility = False

final_root = doc.addObject("Part::Cut", "Final_root")
final_root.Base = root_a_cut
final_root.Tool = root_wedge_obj

# Add R2 cylinder visualization
cyl_obj = doc.addObject("Part::Cylinder", "R2_flat_area")
cyl_obj.Radius = R2
cyl_obj.Height = thickness
cyl_obj.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(Vector(0,0,1), 0))

doc.recompute()

# Add parts to container
for section in blocks[1:]:
    blade_container.addObject(section)

if FreeCAD.GuiUp:
    Gui.SendMsgToActiveView("ViewFit")

print(f"✓ Root created with 45° ramp and 120° root cut")
print(f"  W={W}mm, X={X}mm, R2={R2}mm")
