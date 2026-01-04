#!/usr/bin/env python3
"""Visualize airfoil with bottom points highlighted"""

import FreeCAD
import Part
import math

# Load airfoil coordinates (skip header line)
coordinates = []
with open('macros/USNPS4.dat', 'r') as f:
    lines = f.readlines()[1:]  # Skip header
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) >= 2:
                x, z = float(parts[0]), float(parts[1])
                coordinates.append((x, z))

print(f'Loaded {len(coordinates)} airfoil points')

# Create airfoil wire from raw coordinates
points_3d = [FreeCAD.Vector(x, 0.0, z) for x, z in coordinates]
spline = Part.BSplineCurve()
spline.interpolate(points_3d, False)
airfoil_wire = Part.Wire([spline.toShape()])
Part.show(airfoil_wire, "Raw_Airfoil_Wire")

# Identify bottom points
min_z = min(z for _, z in coordinates)
tolerance = 0.010
bottom_points = [(x, z) for x, z in coordinates if abs(z - min_z) < tolerance]

print(f'Bottom points (within {tolerance} of min_z={min_z:.3f}): {len(bottom_points)}')

# Create group for bottom point spheres
doc = FreeCAD.ActiveDocument
bottom_points_group = doc.addObject("App::DocumentObjectGroup", "Bottom_Points")

# Draw bottom points as spheres
for i, (x, z) in enumerate(bottom_points):
    sphere = Part.makeSphere(0.01, FreeCAD.Vector(x, 0.0, z))  # radius 0.01 (10mm at scale)
    sphere_obj = Part.show(sphere, f"Bottom_Point_{i:02d}")
    bottom_points_group.addObject(sphere_obj)
    
    # Color spheres red
    if FreeCAD.GuiUp:
        sphere_obj.ViewObject.ShapeColor = (1.0, 0.0, 0.0)  # Red

print(f"Created {len(bottom_points)} bottom point spheres")
print(f"Added to group: {bottom_points_group.Name}")
