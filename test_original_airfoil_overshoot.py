#!/usr/bin/env python3
"""Test original airfoil coordinates for B-spline overshoot beyond length 1.0"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

import FreeCAD
import Part
from macros.create_blade import load_airfoil_coordinates

def test_original_airfoil_overshoot():
    """Test if original airfoil coordinates create B-spline overshoot beyond 1.0"""
    
    # Load original airfoil coordinates
    airfoil_path = Path(__file__).parent / "macros" / "USNPS4.dat"
    coordinates = load_airfoil_coordinates(airfoil_path)
    
    print(f"Loaded {len(coordinates)} airfoil coordinates")
    print(f"X range: {min(x for x, y in coordinates):.10f} to {max(x for x, y in coordinates):.10f}")
    print(f"Y range: {min(y for x, y in coordinates):.10f} to {max(y for x, y in coordinates):.10f}")
    
    # Create 3D points at y=0 for B-spline creation
    points_3d = [FreeCAD.Vector(x, 0.0, y) for x, y in coordinates]
    
    # Create B-spline curve
    bspline = Part.BSplineCurve()
    bspline.interpolate(points_3d, False)
    edge = bspline.toShape()
    
    # Get bounding box with high precision
    bbox = edge.BoundBox
    
    print(f"\nB-spline Bounding Box Analysis:")
    print(f"X Min: {bbox.XMin:.15f}")
    print(f"X Max: {bbox.XMax:.15f}")
    print(f"Y Min: {bbox.YMin:.15f}")
    print(f"Y Max: {bbox.YMax:.15f}")
    print(f"Z Min: {bbox.ZMin:.15f}")
    print(f"Z Max: {bbox.ZMax:.15f}")
    
    # Check overshoot beyond 1.0 in X direction
    x_overshoot = bbox.XMax - 1.0
    print(f"\nOvershoot Analysis:")
    print(f"X Max - 1.0 = {x_overshoot:.15f}")
    
    if x_overshoot > 0:
        print(f"✅ OVERSHOOT DETECTED: {x_overshoot:.15f} units beyond 1.0")
    else:
        print(f"❌ No overshoot detected (within 1.0 boundary)")
    
    # Also check by discretizing the curve for comparison
    discretized_points = edge.discretize(10000)  # Very high resolution
    max_x_discrete = max(pt.x for pt in discretized_points)
    discrete_overshoot = max_x_discrete - 1.0
    
    print(f"\nDiscretized Analysis (10000 points):")
    print(f"Max X (discretized): {max_x_discrete:.15f}")
    print(f"Discrete overshoot: {discrete_overshoot:.15f}")
    
    # Find the control points for reference
    poles = []
    try:
        # Try to get control points
        for i in range(bspline.NbPoles):
            pole = bspline.getPole(i + 1)  # FreeCAD uses 1-based indexing
            poles.append(pole)
        
        max_control_x = max(pole.x for pole in poles)
        print(f"\nControl Points Analysis:")
        print(f"Number of control points: {len(poles)}")
        print(f"Max control point X: {max_control_x:.15f}")
        print(f"Control point overshoot: {max_control_x - 1.0:.15f}")
        
    except Exception as e:
        print(f"Could not extract control points: {e}")
    
    return x_overshoot > 0

if __name__ == "__main__":
    # Create a temporary FreeCAD document
    if not FreeCAD.ActiveDocument:
        FreeCAD.newDocument()
    
    has_overshoot = test_original_airfoil_overshoot()
    
    if has_overshoot:
        print(f"\n🎯 CONCLUSION: Original airfoil coordinates DO create B-spline overshoot!")
    else:
        print(f"\n📏 CONCLUSION: Original airfoil coordinates stay within 1.0 boundary")
