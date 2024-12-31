from typing import List, Tuple

from .create_placement_cells import create_placement_cells
from .spreadsheet import Cell, Style

__all__ = ['high_end_stop_cells']


high_end_stop_cells: List[List[Cell]] = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('FlatMetalThickness'),
        Cell('BoomPipeDiameter'),
        Cell('YawPipeDiameter')
    ],
    [
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.BoomPipeDiameter',
             alias='BoomPipeDiameter'),
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter')
    ],
    [
        Cell('VerticalPlaneAngle'),
        Cell('HorizontalPlaneAngle'),
        Cell('BoomLength')
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
        Cell('=Spreadsheet.HorizontalPlaneAngle',
             alias='HorizontalPlaneAngle'),
        Cell('=Spreadsheet.BoomLength',
             alias='BoomLength')
    ],
    [
        Cell('YawBearing', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('YawPipeProjectedLength')
    ],
    [
        Cell('=YawBearing.YawPipeProjectedLength',
             alias='YawPipeProjectedLength')
    ],
    [
        Cell('Tail', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('TailHingeJunctionChamfer'),
        Cell('OuterTailHingeParentPlacement'),
        Cell('TailPlacement')
    ],
    [
        Cell('=Tail.TailHingeJunctionChamfer',
             alias='TailHingeJunctionChamfer'),
        Cell('=Tail.OuterTailHingeParentPlacement',
             alias='OuterTailHingeParentPlacement'),
        Cell('=Tail.TailPlacement',
             alias='TailPlacement')
    ],
    [
        Cell('OuterTailHingeBase'),
        Cell('TailAssemblyPlacement'),
        Cell('HingeOuterPipeDiameter')
    ],
    [
        Cell('=Tail.OuterTailHingeBase',
             alias='OuterTailHingeBase'),
        Cell('=Tail.TailAssemblyPlacement',
             alias='TailAssemblyPlacement'),
        Cell('=Tail.HingeOuterPipeDiameter',
             alias='HingeOuterPipeDiameter')
    ],
    [
        Cell('LowEndStop', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('LeftPerpendicularLowEndStopPlaneNormalVector'),
        Cell('LeftPerpendicularLowEndStopPlaneDistance')
    ],
    [
        Cell('=LowEndStop.LeftPerpendicularLowEndStopPlaneNormalVector',
             alias='LeftPerpendicularLowEndStopPlaneNormalVector'),
        Cell('=LowEndStop.LeftPerpendicularLowEndStopPlaneDistance',
             alias='LeftPerpendicularLowEndStopPlaneDistance')
    ],
    [
        Cell('LowerLowEndStopPlaneNormalVector'),
        Cell('LowerLowEndStopPlaneDistance')
    ],
    [
        Cell('=LowEndStop.LowerLowEndStopPlaneNormalVector',
             alias='LowerLowEndStopPlaneNormalVector'),
        Cell('=LowEndStop.LowerLowEndStopPlaneDistance',
             alias='LowerLowEndStopPlaneDistance')
    ],
    # Static
    # ------
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('FurlAxis')
    ],
    [
        Cell('=vector(sin(VerticalPlaneAngle); 0; cos(VerticalPlaneAngle))',
             alias='FurlAxis')
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius'),
        Cell('BoomPipeRadius')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius'),
        Cell('=BoomPipeDiameter / 2',
             alias='BoomPipeRadius'),
    ],
    # Placement
    # ---------
    [
        Cell('Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    *create_placement_cells(name='TailBoomVaneAssembly',
                            base=('0', '0', '0'),
                            axis=('0', '1', '0'),
                            angle='90'),
    *create_placement_cells(name='HighEndStop',
                            base=(
                                '=FlatMetalThickness / 2',
                                '=BoomPipeRadius',
                                '0'),
                            axis=('0', '1', '0'),
                            angle='-90'),
    *create_placement_cells(name='EndOfBoom',
                            base=(
                                '=0',
                                '=0',
                                '=BoomLength'),
                            axis=('0', '1', '0'),
                            angle='-90'),
    [
        Cell('----------'), Cell('----------'), Cell('----------')
    ],
    # Calculated Placement
    # --------------------
    [
        Cell('Calculated Placement', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('TailBoomVaneAssemblyParentPlacement'),
    ],
    [
        Cell('=TailPlacement * TailBoomVaneAssemblyPlacement',
             alias='TailBoomVaneAssemblyParentPlacement')
    ],
    [
        Cell('----------'), Cell('----------'), Cell('----------')
    ],
    #
    # Maximum Furl Angle
    # ------------------
    # Determine the maximum furl angle for tail before getting too close to the blades.
    # Involves the intersection of two planes, forming a line.
    # Then the intersection of the line with a sphere.
    #
    # The following algorithm is used:
    # 1. Find maximum furl plane.
    # 2. Find plane of rotation for boom.
    # 3. Find sphere containing the plane of rotation for the boom.
    # 4. Find line formed by the intersection of maximum furl plane and plane of rotation for boom.
    # 5. Find intersection point on the line and sphere closest to boom starting point.
    # 6. Calculate angle between boom starting point, center of sphere, and intersection point.
    #
    # See the following 3D plot:
    # https://c3d.libretexts.org/CalcPlot3D/index.html?type=implicit;equation=x%20~%20-11.43y%20-%20914.96;cubes=16;visible=true;fixdomain=false;xmin=-1500;xmax=1000;ymin=-1500;ymax=1000;zmin=-500;zmax=1500;alpha=150;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=implicit;equation=-0.20x%20-0.28y%20+%200.94z%20-%20544.22%20~%200;cubes=16;visible=true;fixdomain=false;xmin=-1500;xmax=1000;ymin=-1500;ymax=1000;zmin=-500;zmax=1500;alpha=150;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=implicit;equation=(x%20+%20135.05)%5E2%20+%20(y%20+%20192.87)%5E2%20+%20(z%20-%20493.45)%5E2%20~%20965.74%5E2;cubes=16;visible=true;fixdomain=false;xmin=-1500;xmax=1000;ymin=-1500;ymax=1000;zmin=-500;zmax=1500;alpha=100;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=point;point=(-1197.36,24.71,336.55);visible=true;color=rgb(0,0,0);size=10&type=vector;vector=%3C946.52,%20-82.81,%20172.91%3E;visible=true;color=rgb(0,0,0);size=4;initialpt=(-1197.36,24.71,336.55)&type=point;point=(806.81,-150.64,702.67);visible=true;color=rgb(0,0,0);size=10&type=point;point=(-419.02,-1059.53,175.78);visible=true;color=rgb(0,0,0);size=10&type=point;point=(-135.05,-192.87,493.45);visible=true;color=rgb(0,0,0);size=10&type=window;hsrmode=0;nomidpts=true;anaglyph=-1;center=-0.317485775338329,-1.8782080166036121,9.816900601961878,1;focus=0,0,0,1;up=0.9756466580973304,0.20745563415558366,0.07124435697384073,1;transparent=false;alpha=140;twoviews=false;unlinkviews=false;axisextension=0.7;shownormals=false;shownormalsatpts=false;xaxislabel=x;yaxislabel=y;zaxislabel=z;edgeson=true;faceson=true;showbox=false;showaxes=true;showticks=true;perspective=true;centerxpercent=0.31543025039293726;centerypercent=0.4216527150945403;rotationsteps=30;autospin=true;xygrid=false;yzgrid=false;xzgrid=false;gridsonbox=true;gridplanes=true;gridcolor=rgb(128,128,128);xmin=-1500;xmax=1000;ymin=-1500;ymax=1000;zmin=-500;zmax=1500;xscale=100;yscale=100;zscale=100;zcmin=-4;zcmax=4;xscalefactor=20;yscalefactor=20;zscalefactor=20;tracemode=0;keep2d=false;zoom=0.00008
    #
    [
        Cell('Maximum Furl Angle',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('STEP 1:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Find maximum furl plane')
    ],
    [
        # Keep the tail a certain angle from the vertical parallel to the rotor & blades.
        Cell('AngleBetweenTailAndRotor')
    ],
    [
        Cell('=5deg',
             alias='AngleBetweenTailAndRotor'),
    ],
    [
        # Define a point P, on the plane formed by the tail when maximally furled.
        # In coordinates local to the Tail_Assembly document.
        # y is on the horizontal axis and x is on the vertical axis
        # when viewing from the top.
        #
        #        ^ x
        #        |
        #        |
        # <------+
        # y
        #
        Cell('Py'),
        Cell('Px')
    ],
    [

        Cell('=.OuterTailHingeParentPlacement.Base.x * cos(90deg - AngleBetweenTailAndRotor) + .OuterTailHingeParentPlacement.Base.y',
             alias='Py'),
        Cell('=-1 * .OuterTailHingeParentPlacement.Base.x * sin(90deg - AngleBetweenTailAndRotor) + .OuterTailHingeParentPlacement.Base.x',
             alias='Px'),
    ],
    [
        # Calculate slope and z-intercept of line formed by OuterTailHingeParentPlacement.Base and P on XY plane.
        # This defines the "maximum furl plane".
        Cell('slope'),
        Cell('xIntercept'),
        Cell('NormalVectorOfMaximumFurlPlane')
    ],
    [
        Cell('=(Px - .OuterTailHingeParentPlacement.Base.x) / (Py - .OuterTailHingeParentPlacement.Base.y)',
             alias='slope'),
        Cell('=Px - (slope * Py)',
             alias='xIntercept'),
        # Get the normal vector of the maximum furl plane,
        # from the coefficients of the general equation.
        Cell('=vector(-1; slope; 0)',
             alias='NormalVectorOfMaximumFurlPlane')
    ],
    [
        Cell('STEP 2:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Find plane of rotation for boom')
    ],
    [
        # Furl tail (end of boom) 0°, 90°, 180°, and 270° to form 4 outer-most points of a circle.
        Cell('EndOfBoom0Rotation'),
        Cell('EndOfBoom90Rotation'),
        Cell('EndOfBoom180Rotation'),
        Cell('EndOfBoom270Rotation')
    ],
    [
        Cell('=rotation(FurlAxis; 0deg)',
             alias='EndOfBoom0Rotation'),
        Cell('=rotation(FurlAxis; 90deg)',
             alias='EndOfBoom90Rotation'),
        Cell('=rotation(FurlAxis; 180deg)',
             alias='EndOfBoom180Rotation'),
        Cell('=rotation(FurlAxis; 270deg)',
             alias='EndOfBoom270Rotation')
    ],
    [
        Cell('EndOfBoom0Placement'),
        Cell('EndOfBoom90Placement'),
        Cell('EndOfBoom180Placement'),
        Cell('EndOfBoom270Placement')
    ],
    [
        Cell('=placement(.OuterTailHingeBase - EndOfBoom0Rotation * .OuterTailHingeBase; EndOfBoom0Rotation)',
             alias='EndOfBoom0Placement'),
        Cell('=placement(.OuterTailHingeBase - EndOfBoom90Rotation * .OuterTailHingeBase; EndOfBoom90Rotation)',
             alias='EndOfBoom90Placement'),
        Cell('=placement(.OuterTailHingeBase - EndOfBoom180Rotation * .OuterTailHingeBase; EndOfBoom180Rotation)',
             alias='EndOfBoom180Placement'),
        Cell('=placement(.OuterTailHingeBase - EndOfBoom270Rotation * .OuterTailHingeBase; EndOfBoom270Rotation)',
             alias='EndOfBoom270Placement')
    ],
    [
        Cell('FurledEndOfBoom0Placement'),
        Cell('FurledEndOfBoom90Placement'),
        Cell('FurledEndOfBoom180Placement'),
        Cell('FurledEndOfBoom270Placement')
    ],
    [
        Cell('=TailAssemblyPlacement * EndOfBoom0Placement * TailBoomVaneAssemblyParentPlacement * EndOfBoomPlacement',
             alias='FurledEndOfBoom0Placement'),
        Cell('=TailAssemblyPlacement * EndOfBoom90Placement * TailBoomVaneAssemblyParentPlacement * EndOfBoomPlacement',
             alias='FurledEndOfBoom90Placement'),
        Cell('=TailAssemblyPlacement * EndOfBoom180Placement * TailBoomVaneAssemblyParentPlacement * EndOfBoomPlacement',
             alias='FurledEndOfBoom180Placement'),
        Cell('=TailAssemblyPlacement * EndOfBoom270Placement * TailBoomVaneAssemblyParentPlacement * EndOfBoomPlacement',
             alias='FurledEndOfBoom270Placement')
    ],
    [
        # Create two axes of the circle.
        Cell('Axis1'),
        Cell('Axis2')
    ],
    [
        Cell('=FurledEndOfBoom180Placement.Base - FurledEndOfBoom0Placement.Base',
             alias='Axis1'),
        Cell('=FurledEndOfBoom270Placement.Base - FurledEndOfBoom90Placement.Base',
             alias='Axis2')
    ],
    [
        # Cross product Axis1 and Axis2 to find normal vector of the plane of rotation for the boom, Vg.
        # https://en.wikipedia.org/wiki/Cross_product
        Cell('Vg'),
        Cell('Axis1 × Axis2')
    ],
    [
        Cell('=vcross(Axis1; Axis2)',
             alias='Vg'),
        Cell('Cross Product', styles=[Style.ITALIC])
    ],
    [
        # Normalize Vg from step above.
        Cell('Vh'),
        Cell('Normalize Vg')
    ],
    [
        Cell('=Vg / .Vg.Length', alias='Vh')
    ],
    [
        #
        # Find d (distance from origin) in the general equation of a plane:
        #
        #   ax + by + cz + d = 0
        #
        # See:
        # https://en.wikipedia.org/wiki/Euclidean_planes_in_three-dimensional_space#Point%E2%80%93normal_form_and_general_form_of_the_equation_of_a_plane
        #
        # Normal vector times a point on the plane.
        #
        Cell('BoomRotationPlaneDistance (d)'),
    ],
    [
        Cell('=-Vh * .FurledEndOfBoom0Placement.Base',
             alias='BoomRotationPlaneDistance')
    ],
    [
        Cell('STEP 3:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Find sphere containing the plane of rotation for the boom')
    ],
    [
        Cell('CenterOfSphere'),
        Cell('Radius')
    ],
    [
        Cell('=.FurledEndOfBoom0Placement.Base + Axis1 / 2',
             alias='CenterOfSphere'),
        Cell('=.Axis1.Length / 2',
             alias='Radius')
    ],
    [
        Cell('STEP 4:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Find line formed by the intersection of maximum furl plane and plane of rotation for boom')
    ],
    [
        # Define the x, y, and z of the origin point for the line.
        Cell('xLineOrigin'),
        Cell('yLineOrigin'),
        Cell('zLineOrigin')
    ],
    [
        Cell('=.CenterOfSphere.x - Radius * 1.1',
             alias='xLineOrigin'),
        Cell('=(xLineOrigin - xIntercept) / slope',
             alias='yLineOrigin'),
        Cell('=-(BoomRotationPlaneDistance + .Vh.x * xLineOrigin + .Vh.y * yLineOrigin) / .Vh.z',
             alias='zLineOrigin')
    ],
    [
        Cell('LineOrigin')
    ],
    [
        Cell('=vector(xLineOrigin; yLineOrigin; zLineOrigin)',
             alias='LineOrigin')
    ],
    [
        # Cross product Vh and NormalVectorOfMaximumFurlPlane to find direction vector of line intersecting the two planes.
        # https://en.wikipedia.org/wiki/Cross_product
        # See "Intersection Line of 2 Planes - How to Find It - Step by Step Method & Explanation - Vector Equation" on YouTube:
        # https://youtu.be/O6O_64zIEYI?t=116
        Cell('DirectionVector'),
        Cell('Vh × NormalVectorOfMaximumFurlPlane')
    ],
    [
        Cell('=vcross(Vh; NormalVectorOfMaximumFurlPlane)',
             alias='DirectionVector'),
        Cell('Cross Product', styles=[Style.ITALIC])
    ],
    [
        # Normalize the direction vector.
        Cell('NormalizedDirectionVector')
    ],
    [
        Cell('=.DirectionVector / .DirectionVector.Length',
             alias='NormalizedDirectionVector')
    ],
    [
        Cell('STEP 5:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Find intersection point on the line and sphere closest to boom starting point')
    ],
    [
        Cell('ValueOfTForPointOnLineClosestToCenterOfSphere'),
        Cell('PointOnLineClosestToCenterOfSphere')
    ],
    [
        # See "Calculating Ray-Sphere Intersections" on YouTube:
        # https://www.youtube.com/watch?v=HFPlKQGChpE
        Cell('=(CenterOfSphere - LineOrigin) * NormalizedDirectionVector',
             alias='ValueOfTForPointOnLineClosestToCenterOfSphere'),
        Cell('=LineOrigin + ValueOfTForPointOnLineClosestToCenterOfSphere * NormalizedDirectionVector',
             alias='PointOnLineClosestToCenterOfSphere')
    ],
    [
        Cell('yVector'),
        Cell('yDistance'),
        Cell('xDistance')
    ],
    [
        Cell('=CenterOfSphere - PointOnLineClosestToCenterOfSphere',
             alias='yVector'),
        Cell('=yVector.Length',
             alias='yDistance'),
        Cell('=sqrt(Radius^2 - yDistance^2)',
             alias='xDistance')
    ],
    [
        Cell('ValueOfTForFarthestIntersectionPoint'),
        Cell('FarthestIntersectionPoint')
    ],
    [
        Cell('=ValueOfTForPointOnLineClosestToCenterOfSphere + xDistance',
             alias='ValueOfTForFarthestIntersectionPoint'),
        Cell('=LineOrigin + ValueOfTForFarthestIntersectionPoint * NormalizedDirectionVector',
             alias='FarthestIntersectionPoint')
    ],
    [
        Cell('STEP 6:',
             styles=[Style.UNDERLINE, Style.ITALIC]),
        Cell('Calculate angle between boom starting point, center of sphere, and intersection point')
    ],
    [
        # Use special case of law of cosines for isosceles triangle to calculate maximum furl angle.
        # https://en.wikipedia.org/wiki/Law_of_cosines#Isosceles_case
        Cell('dVector'),
        Cell('dDistance'),
        Cell('MaximumFurlAngle'),
        Cell('FurlRotation')
    ],
    [
        Cell('=.FarthestIntersectionPoint - .FurledEndOfBoom0Placement.Base',
             alias='dVector'),
        Cell('=dVector.Length',
             alias='dDistance'),
        Cell('=acos(1 - dDistance ^ 2 / (2 * Radius ^ 2))',
             alias='MaximumFurlAngle'),
        Cell('=rotation(FurlAxis; MaximumFurlAngle)',
             alias='FurlRotation')
    ],
    [
        Cell('----------'), Cell('----------'), Cell('----------')
    ],
    #
    # Furled High End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection
    # -------------------------------------------------------------------------
    # Find the high end stop width and length.
    #
    # The below calculations are relative to the Tail_Assembly document.
    #
    # The following is a 3D plot of the furled high end stop plane and yaw bearing cylinder:
    # https://c3d.libretexts.org/CalcPlot3D/index.html?type=implicit;equation=x%5E2%20+%20y%5E2%20~%2030.15%5E2;cubes=32;visible=true;fixdomain=false;xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=100;zmax=400;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=implicit;equation=-0.51x%20-%200.19y%20+%200.84z%20-%20193.74%20~%200;cubes=16;visible=true;fixdomain=false;xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=100;zmax=400;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=point;point=(-47.14,-74.44,185.88);visible=true;color=rgb(0,0,0);size=10&type=point;point=(-1.55,-30.11,223.87);visible=true;color=rgb(0,0,0);size=10&type=point;point=(-1.55,-77.17,213.31);visible=true;color=rgb(0,0,0);size=10&type=window;hsrmode=0;nomidpts=true;anaglyph=-1;center=-8.983761846851909,-0.20469189522930448,4.387496359776474,1;focus=0,0,0,1;up=0.4346730111543097,-0.1849020372518452,0.881402637841618,1;transparent=false;alpha=140;twoviews=false;unlinkviews=false;axisextension=0.7;shownormals=false;shownormalsatpts=false;xaxislabel=x;yaxislabel=y;zaxislabel=z;edgeson=true;faceson=true;showbox=false;showaxes=true;showticks=true;perspective=true;centerxpercent=0.45759597456831236;centerypercent=0.8607261684051503;rotationsteps=30;autospin=true;xygrid=false;yzgrid=false;xzgrid=false;gridsonbox=true;gridplanes=true;gridcolor=rgb(128,128,128);xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=100;zmax=400;xscale=20;yscale=20;zscale=20;zcmin=-4;zcmax=4;xscalefactor=20;yscalefactor=20;zscalefactor=20;tracemode=0;keep2d=false;zoom=0.000667
    #
    # Values correspond to default values for a T Shaped wind turbine.
    #
    # The three points in the plot are:
    #   1. FurledHighEndStopTailAssemblyPlacement.Base
    #   2. YawBearingHighEndStopTangentPoint
    #   3. HighEndStopPointWhereXEqualsTangent
    #
    [
        Cell('Furled High End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('TailFurlBase'),
        Cell('TailFurlPlacement'),
        Cell('FurledHighEndStopTailAssemblyPlacement'),
    ],
    [
        # center - rotation.multVec(center)
        Cell('=.OuterTailHingeBase - FurlRotation * .OuterTailHingeBase',
             alias='TailFurlBase'),
        Cell('=placement(TailFurlBase; FurlRotation)',
             alias='TailFurlPlacement'),
        # Transform vectors in the Tail_Stop_HighEnd document to furled position in Tail_Assembly document.
        Cell('=.TailAssemblyPlacement * .TailFurlPlacement * .TailBoomVaneAssemblyParentPlacement * .HighEndStopPlacement',
             alias='FurledHighEndStopTailAssemblyPlacement'),
    ],
    [
        # Define two vectors, HighEndStopBoomDirectionVector and HighEndStopYawBearingDirectionVector, on the Furled High End Stop plane.
        Cell('HighEndStopBoomDirectionVector'),
        Cell('HighEndStopYawBearingDirectionVector'),
        # Normal vector to Furled High End Stop plane.
        Cell('Vn'),
    ],
    [
        # The following unit vectors are local to the Tail_Stop_HighEnd document.
        Cell('=.FurledHighEndStopTailAssemblyPlacement.Rotation * vector(1; 0; 0)',
             alias='HighEndStopBoomDirectionVector'),
        Cell('=.FurledHighEndStopTailAssemblyPlacement.Rotation * vector(0; 1; 0)',
             alias='HighEndStopYawBearingDirectionVector'),
        Cell('=.FurledHighEndStopTailAssemblyPlacement.Rotation * vector(0; 0; 1)',
             alias='Vn')
    ],
    [
        #
        # Find d (distance from origin) in the general equation of a plane:
        #
        #   ax + by + cz + d = 0
        #
        # See:
        # https://en.wikipedia.org/wiki/Euclidean_planes_in_three-dimensional_space#Point%E2%80%93normal_form_and_general_form_of_the_equation_of_a_plane
        #
        # Normal vector times a point on the plane.
        #
        Cell('FurledHighEndStopPlaneDistance (d)')
    ],
    [
        # (This should be negated following the above formula strictly.)
        Cell('=.Vn * .FurledHighEndStopTailAssemblyPlacement.Base',
             alias='FurledHighEndStopPlaneDistance')
    ],
    [
        Cell('AngleBetweenYAxisAndHighEndStop'),
        Cell('TangentAngle')
    ],
    [
        # From the dot product between vector HighEndStopBoomDirectionVector and y-axis vector (0, 1, 0).
        # https://en.wikipedia.org/wiki/Dot_product#Geometric_definition
        Cell('=acos(.HighEndStopBoomDirectionVector.y)',
             alias='AngleBetweenYAxisAndHighEndStop'),
        Cell('=360deg - AngleBetweenYAxisAndHighEndStop',
             alias='TangentAngle')
    ],
    #
    # Find point on yaw bearing pipe which is tangent to the furled high end end stop plane.
    #
    # Equation of yaw bearing pipe cylinder:
    # x^2 + y^2 = r^2
    #
    # Parametric equations for yaw bearing pipe cylinder:
    # x = r * cos(θ)
    # y = r * sin(θ)
    #
    # Plug in (r *cos(θ)) for x and (r * sin(θ)) for y into equation of plane:
    # a * x + b * y + c * z = d and solve in terms of z
    #
    # https://www.wolframalpha.com/input?i=a+*+%28r+*+cos%28%CE%B8%29%29+%2B+b+*+%28r+*+sin%28%CE%B8%29%29+%2B+c+*+z+%3D+d+solve+for+z
    #
    # z = (d - a r cos(θ) - b r sin(θ)) / c
    #
    [
        Cell('TangentAngleZ'),
        Cell('TangentAngleX'),
        Cell('TangentAngleY'),
    ],
    [
        Cell('=(FurledHighEndStopPlaneDistance - Vn.x * YawPipeRadius * cos(TangentAngle) - Vn.y * YawPipeRadius * sin(TangentAngle)) / Vn.z',
             alias='TangentAngleZ'),
        #
        # Solve for x, given z.
        #
        # x = (d - c z - b r sin(θ)) / a
        #
        # https://www.wolframalpha.com/input?i=a+*+x+%2B+b+*+%28r+*+sin%28%CE%B8%29%29+%2B+c+*+z+%3D+d+solve+for+x
        #
        Cell('=(FurledHighEndStopPlaneDistance - Vn.z * TangentAngleZ - Vn.y * YawPipeRadius * sin(TangentAngle)) / Vn.x',
             alias='TangentAngleX'),
        #
        # Solve for y, given z and x.
        #
        # y = (d - a x - c z) / b
        #
        # https://www.wolframalpha.com/input?i=a+*+x+%2B+b+*+y+%2B+c+*+z+%3D+d+solve+for+y
        #
        Cell('=(FurledHighEndStopPlaneDistance - Vn.x * TangentAngleX - Vn.z * TangentAngleZ) / Vn.y',
             alias='TangentAngleY')
    ],
    [
        Cell('YawBearingHighEndStopTangentPoint')
    ],
    [
        Cell('=vector(TangentAngleX; TangentAngleY; TangentAngleZ)',
             alias='YawBearingHighEndStopTangentPoint')
    ],
    [
        Cell('References', styles=[Style.ITALIC, Style.UNDERLINE])
    ],
    [
        Cell('Finding a point on a 3d line',
             styles=[Style.ITALIC]),
        Cell('What is the equation for a 3D line?',
             styles=[Style.ITALIC])
    ],
    [
        Cell('https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154'),
        Cell('https://math.stackexchange.com/questions/404440/what-is-the-equation-for-a-3d-line/404446#404446')
    ],
    [
        # T is a reserved alias since FreeCAD 20.
        Cell('T_tangent'),
        Cell('HighEndStopPointWhereXEqualsTangent'),
        Cell('HighEndStopWidthVector')
    ],
    [
        Cell('=(TangentAngleX - .FurledHighEndStopTailAssemblyPlacement.Base.x) / .HighEndStopBoomDirectionVector.x',
             alias='T_tangent'),
        Cell('=.FurledHighEndStopTailAssemblyPlacement.Base + T_tangent * .HighEndStopBoomDirectionVector',
             alias='HighEndStopPointWhereXEqualsTangent'),
        Cell('=.YawBearingHighEndStopTangentPoint - .HighEndStopPointWhereXEqualsTangent',
             alias='HighEndStopWidthVector')
    ],
    [
        Cell('HighEndStop', styles=[Style.BOLD, Style.UNDERLINE])
    ],
    [
        Cell('Width', styles=[Style.UNDERLINE]),
    ],
    [
        Cell('=HighEndStopWidthVector.Length',
             alias='HighEndStopWidth')
    ],
    #
    # ASCII drawings of high end stop planes for understanding below aliases (e.g. UpperBottomLeftCorner).
    #
    # Upper plane farthest from ground, seen from top view of turbine.
    # Lower plane closest to the ground, seen from bottom view of turbine.
    #
    # ::
    #
    #         Upper
    #     - - - - - - -
    #     | \         | \\
    #     |   \       |   \\
    #     - - - - - - -     \\
    #       \     \     \     \\
    #         \     - - - - - - -
    #           \   |       \   |
    #             \ |         \ |
    #               - - - - - - -
    #                   Lower
    #
    # 3D ASCII Drawing Source: https://1j01.github.io/ascii-hypercube/
    #
    # Both Lower and Upper planes have Top, Left, Right, and Bottom sides.
    # Top is farthest from the hinge, and closest to the vane.
    # Bottom is closest to the hinge, and farthest from the vane.
    # Left is closest to the yaw bearing, and farthest from boom (in furled position).
    # Right is farthest from the yaw bearing, and closest to the boom (in furled position).
    #
    # ::
    #
    #              Top
    #          ┌─────────┐          ^
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #     Left │         │ Right    |  HighEndStopLength
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          │         │          |
    #          └─────────┘          v
    #            Bottom
    #
    # 2D ASCII Drawing Source: https://asciiflow.com/legacy/
    #
    [
        # of High End Stop
        Cell('UpperBottomLeftCorner'),
        Cell('=.FurledHighEndStopTailAssemblyPlacement * vector(0; 0; FlatMetalThickness) + .HighEndStopYawBearingDirectionVector * HighEndStopWidth',
             alias='UpperBottomLeftCorner')
    ],
    # SafetyCatch
    # -----------
    # Depedent upon high end stop.
    # Relative to Tail_Assembly document.
    #
    [
        Cell('SafetyCatch', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('SafetyCatchAngle'),
        Cell('SafetyCatchWidth'),
        Cell('SafetyCatchLength')
    ],
    [
        Cell('=AngleBetweenYAxisAndHighEndStop - 90deg',
             alias='SafetyCatchAngle'),
        Cell('=YawPipeRadius * 1.67',
             alias='SafetyCatchWidth'),
        Cell('=HighEndStopWidth * 0.6',
             alias='SafetyCatchLength')
    ],
    [
        # Xgiven
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Xupper'),
        Cell('=SafetyCatchWidth / 2',
             alias='Xupper')
    ],
    [
        # T
        # see https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154
        Cell('Tupper'),
        Cell('=(Xupper - .UpperBottomLeftCorner.x) / .HighEndStopBoomDirectionVector.x',
             alias='Tupper')
    ],
    [
        Cell('SafetyCatchPosition'),
        Cell('=.UpperBottomLeftCorner + Tupper * .HighEndStopBoomDirectionVector',
             alias='SafetyCatchPosition')
    ],
    [
        Cell('SafetyCatchZPadding'),
        Cell('12', alias='SafetyCatchZPadding')
    ],
    [
        # Z position of the safety catch
        # Plus padding for a little extra clearance.
        Cell('SafetyCatchZ'),
        Cell('=.SafetyCatchPosition.z + SafetyCatchZPadding',
             alias='SafetyCatchZ')
    ],
    [
        Cell('HighEndStop', styles=[Style.BOLD, Style.UNDERLINE])
    ],
    [
        Cell('Length', styles=[Style.UNDERLINE])
    ],
    [
        # Extend high end stop about 1cm past safety catch in the X-direction.
        Cell('=(SafetyCatchPosition.x + 10 - .FurledHighEndStopTailAssemblyPlacement.Base.x) / .HighEndStopBoomDirectionVector.x',
             alias='HighEndStopLength'),
    ],
    # YawPipeLength
    # -------------
    # Depedent upon safety catch position.
    #
    [
        Cell('YawPipeLength', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # Ensure yaw pipe is long enough to fit safety catch.
        # The below condition evaluates to false when VerticalPlaneAngle in increased
        # from 15° to 20° for H & Star Shape default values.
        Cell('YawPipeLength'),
        Cell('=SafetyCatchZ <= YawPipeProjectedLength - FlatMetalThickness ? YawPipeProjectedLength : SafetyCatchZ + FlatMetalThickness',
             alias='YawPipeLength'),
    ],
    #
    # Extend High End Stop to Low End Stop
    # ------------------------------------
    # Find how much to extend the high end stop to touch the low end stop.
    #
    # MOTIVATION:
    # This eases manufacturing since you can place the high end stop,
    # and then the low end stop without measuring angles.
    #
    # The below calculations are relative to the Tail_Assembly document.
    #
    # The following is a 3D plot of three planes of intersection:
    # https://c3d.libretexts.org/CalcPlot3D/index.html?type=implicit;equation=z%20~%20168.66;cubes=16;visible=true;fixdomain=false;xmin=-200;xmax=100;ymin=-200;ymax=100;zmin=0;zmax=350;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=implicit;equation=0.93x%20-%200.35y%20+%200.09z%20~%20-3.58;cubes=16;visible=true;fixdomain=false;xmin=-200;xmax=100;ymin=-200;ymax=100;zmin=0;zmax=350;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=vector;vector=%3C-35.48,%20-93.07,%200%3E;visible=true;color=rgb(0,0,0);size=2;initialpt=(0,53.6,168.66)&type=implicit;equation=0.34x%20+%200.94y%20~%20-77.9;cubes=16;visible=true;fixdomain=false;xmin=-200;xmax=100;ymin=-200;ymax=100;zmin=0;zmax=350;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=point;point=(-45.21,-66.52,168.66);visible=true;color=rgb(0,0,0);size=4&type=point;point=(0,53.6,168.66);visible=true;color=rgb(0,0,0);size=4&type=window;hsrmode=0;nomidpts=true;anaglyph=-1;center=-5.501893548992319,3.338611221803924,7.65394293715053,1;focus=0,0,0,1;up=0.6847789029021875,-0.3441629255767391,0.64236261939697,1;transparent=false;alpha=140;twoviews=false;unlinkviews=false;axisextension=0.7;shownormals=false;shownormalsatpts=false;xaxislabel=x;yaxislabel=y;zaxislabel=z;edgeson=true;faceson=true;showbox=true;showaxes=true;showticks=true;perspective=true;centerxpercent=0.31190724389040614;centerypercent=0.6890812498140327;rotationsteps=30;autospin=true;xygrid=false;yzgrid=false;xzgrid=false;gridsonbox=true;gridplanes=false;gridcolor=rgb(128,128,128);xmin=-200;xmax=100;ymin=-200;ymax=100;zmin=0;zmax=350;xscale=20;yscale=20;zscale=20;zcmin=-4;zcmax=4;xscalefactor=20;yscalefactor=20;zscalefactor=20;tracemode=0;keep2d=false;zoom=0.000571
    #
    # The two high end stop planes are dynamic based on the position of the lower low end stop plane.
    #
    # Values correspond to default values for a T Shaped wind turbine.
    #
    [
        Cell('Extend High End Stop to Low End Stop', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('HighEndStopTailAssemblyPlacement')
    ],
    [
        Cell('=.TailAssemblyPlacement * .TailBoomVaneAssemblyParentPlacement * .HighEndStopPlacement',
             alias='HighEndStopTailAssemblyPlacement'),
    ],
    [
        # Relative to TailAssembly document.
        Cell('HighEndStopBottomFrontRightPoint'),
        Cell('HighEndStopTopFrontRightPoint'),
        Cell('HighEndStopFrontRightVector')
    ],
    [
        Cell('=.HighEndStopTailAssemblyPlacement * vector(-HingeOuterPipeDiameter; 0; 0)',
             alias='HighEndStopBottomFrontRightPoint'),
        Cell('=.HighEndStopTailAssemblyPlacement * vector(-HingeOuterPipeDiameter; 0; FlatMetalThickness)',
             alias='HighEndStopTopFrontRightPoint'),
        Cell('=HighEndStopTopFrontRightPoint - HighEndStopBottomFrontRightPoint',
             alias='HighEndStopFrontRightVector')
    ],
    [
        # STEP 1
        # Find front right point on corner of high end stop parallel to bottom of low end stop.
        Cell('TwhereHighEndStopFrontRightVectorAndLowerLowEndStopPlaneIntersect'),
        Cell('ZScaleFactor'),
        Cell('HighEndStopFrontRightPoint')
    ],
    [
        #
        # The following value is expected to be negative or between 0 and 1.
        # It's between 0 and 1 for H Shape with a VerticalPlaneAngle of 20°.
        # If it's ever greater than 1, than there may be an issue with the model.
        #
        # https://www.wolframalpha.com/input?i=a+x+%2B+b+y+%2B+c+%28z+%2B+f+*+t%29+%3D+-d+solve+for+t
        # -(a x + b y + c z + d)/(c f)
        #
        Cell('=-(LowerLowEndStopPlaneNormalVector * HighEndStopBottomFrontRightPoint + LowerLowEndStopPlaneDistance) / (LowerLowEndStopPlaneNormalVector.z * FlatMetalThickness)',
             alias='TwhereHighEndStopFrontRightVectorAndLowerLowEndStopPlaneIntersect'),
        Cell('=max(TwhereHighEndStopFrontRightVectorAndLowerLowEndStopPlaneIntersect; 0)',
             alias='ZScaleFactor'),
        Cell('=HighEndStopBottomFrontRightPoint + ZScaleFactor * vector(0; 0; FlatMetalThickness)',
             alias='HighEndStopFrontRightPoint')
    ],
    [
        Cell('HighEndStopPlane', styles=[Style.UNDERLINE])
    ],
    [
        Cell('NormalVector'),
        Cell('Distance')
    ],
    [
        # Similar to Vn calculation above.
        # We could define the z-vector statically for this.
        # vector(0; 0; 1) local to Tail_Stop_HighEnd document.
        Cell('=.HighEndStopTailAssemblyPlacement.Rotation * vector(0; 0; 1)',
             alias='HighEndStopPlaneNormalVector'),
        # Similar to FurledHighEndStopPlaneDistance calculation above.
        Cell('=.HighEndStopPlaneNormalVector * .HighEndStopFrontRightPoint * -1',
             alias='HighEndStopPlaneDistance')
    ],
    [
        Cell('FrontPerpendicularHighEndStopPlane', styles=[Style.UNDERLINE])
    ],
    [
        Cell('NormalVector'),
        Cell('Distance')
    ],
    [
        # Similar to Vn calculation above.
        # vector(-1; 0; 0) local to Tail_Stop_HighEnd document.
        Cell('=.HighEndStopTailAssemblyPlacement.Rotation * vector(-1; 0; 0)',
             alias='FrontPerpendicularHighEndStopPlaneNormalVector'),
        # Similar to FurledHighEndStopPlaneDistance calculation above.
        Cell('=.FrontPerpendicularHighEndStopPlaneNormalVector * .HighEndStopFrontRightPoint * -1',
             alias='FrontPerpendicularHighEndStopPlaneDistance')
    ],
    [
        # STEP 2
        # Find intersection line of left perpendicular low end stop plane & high end stop plane.
        # Cross product LeftPerpendicularLowEndStopPlaneNormalVector and HighEndStopPlaneNormalVector.
        # https://en.wikipedia.org/wiki/Cross_product
        # See "Intersection Line of 2 Planes - How to Find It - Step by Step Method & Explanation - Vector Equation" on YouTube:
        # https://youtu.be/O6O_64zIEYI?t=116
        Cell('IntersectionVector'),
        Cell('LeftPerpendicularLowEndStopPlaneNormalVector × HighEndStopPlaneNormalVector')
    ],
    [
        Cell('=vcross(LeftPerpendicularLowEndStopPlaneNormalVector; HighEndStopPlaneNormalVector)',
             alias='IntersectionVector'),
        Cell('Cross Product', styles=[Style.ITALIC]),
    ],
    [
        # STEP 3
        # Find arbitrary point on line of intersection.
        Cell('PointOnLineOfIntersectionY'),
        Cell('PointOnLineOfIntersection')
    ],
    [
        # y position of point on line of intersection where x = 0:
        # https://www.wolframalpha.com/input?i=b+*+y+%2B+c+*+z+%2B+d+%3D+0++solve+for+y
        # -(d + c * z) / b
        Cell('=-(LeftPerpendicularLowEndStopPlaneDistance + .LeftPerpendicularLowEndStopPlaneNormalVector.z * -HighEndStopPlaneDistance) / .LeftPerpendicularLowEndStopPlaneNormalVector.y',
             alias='PointOnLineOfIntersectionY'),
        Cell('=vector(0; PointOnLineOfIntersectionY; -HighEndStopPlaneDistance)',
             alias='PointOnLineOfIntersection')
    ],
    [
        # STEP 4
        # Find point where front perpendicular high end stop plane intersects the line
        # formed by the intersection of left perpendicular low end stop plane and
        # high end stop plane
        Cell('TwherePlanesIntersect'),
        Cell('IntersectionPoint')
    ],
    [
        #
        # Define parametric equation for line of intersection (z is constant and x = 0 for point on line):
        # x = a * t
        # y = c + b * t
        #
        # Define equation of third plane where z is constant:
        # a * x + b * y = -d
        #
        # Plug in values for x & y into equation of third plane for t:
        # https://www.wolframalpha.com/input?i=a+*+%28x+*+t%29+%2B+b+*+%28c+-+y+*+t%29+%3D+-d+solve+for+t
        # t = (b * c + d) / (-a * x + b * y)
        #
        Cell('=(FrontPerpendicularHighEndStopPlaneNormalVector.y * PointOnLineOfIntersectionY + FrontPerpendicularHighEndStopPlaneDistance) / (-FrontPerpendicularHighEndStopPlaneNormalVector.x * IntersectionVector.x - FrontPerpendicularHighEndStopPlaneNormalVector.y * IntersectionVector.y)',
             alias='TwherePlanesIntersect'),
        Cell('=PointOnLineOfIntersection + TwherePlanesIntersect * IntersectionVector',
             alias='IntersectionPoint')
    ],
    [
        # STEP 5
        # Find distance between high end stop and low end stop.
        Cell('HighEndToLowEndStopExtensionVector'),
        Cell('HighEndStopWidthExtensionToLowEndStop')
    ],
    [
        Cell('=IntersectionPoint - .HighEndStopFrontRightPoint',
             alias='HighEndToLowEndStopExtensionVector'),
        Cell('=HighEndToLowEndStopExtensionVector.Length',
             alias='HighEndStopWidthExtensionToLowEndStop')
    ]
]
