from typing import List, Tuple

from .create_placement_cells import create_placement_cells
from .spreadsheet import Alignment, Cell, Style

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
        Cell('RotorDiskRadius')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius')
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
        # ------------------------------------------
    ],
    [
        Cell('CanSideExtendToMiddleOfYawBearingPipe')
    ],
    [
        Cell('=YawBearing.CanSideExtendToMiddleOfYawBearingPipe',
             alias='CanSideExtendToMiddleOfYawBearingPipe'),
    ],
    [
        Cell('Tail', styles=[Style.UNDERLINE])
        # ------------------------------------
    ],
    [
        Cell('TailHingeJunctionChamfer'),
        Cell('LowEndStopBase')
    ],
    [
        Cell('=Tail.TailHingeJunctionChamfer',
             alias='TailHingeJunctionChamfer'),
        Cell('=Tail.LowEndStopBase',
             alias='LowEndStopBase')
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
        Cell('=create(<<vector>>; sin(VerticalPlaneAngle); 0; cos(VerticalPlaneAngle))',
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
    *create_placement_cells(name='TailAssembly',
                            base=(
                                '=TailHingeJunctionChamfer * cos(180 - HorizontalPlaneAngle)',
                                '=TailHingeJunctionChamfer * sin(-(180 - HorizontalPlaneAngle))',
                                '0'),
                            axis=('0', '0', '-1'),
                            angle='=180 - HorizontalPlaneAngle'),
    *create_placement_cells(name='OuterTailHinge',
                            base=(
                                '=Tail.OuterTailHingeX',
                                '0',
                                '=Tail.OuterTailHingeZ'),
                            axis=('0', '1', '0'),
                            angle='=VerticalPlaneAngle'),
    # TailBoomVaneAssemblyLink
    *create_placement_cells(name='Tail',
                            base=(
                                '=Tail.TailX',
                                '=Tail.TailY',
                                '=Tail.TailZ'),
                            axis=('0', '0', '1'),
                            angle='=Tail.TailAngle'),
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
        Cell('TailBoomVaneAssemblyParentPlacement'),
    ],
    [
        Cell('=TailPlacement * TailBoomVaneAssemblyPlacement',
             alias='TailBoomVaneAssemblyParentPlacement')
    ],
    #
    # Low End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection
    # ------------------------------------------------------------------
    # Find point of tangency for low end stop plane and yaw bearing cylinder
    # to calculate the length and angle of rotation for low end stop.
    #
    # The below calculations are relative to the Tail_Assembly document.
    #
    # The following is a 3D plot of the intersection between the axis-aligned yaw bearing cylinder and low end stop plane
    # relative to the Tail_Assembly document:
    # https://c3d.libretexts.org/CalcPlot3D/index.html?type=implicit;equation=x%5E2%20+%20y%5E2%20~%20(30.15)%5E2;cubes=32;visible=true;fixdomain=false;xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=0;zmax=300;alpha=180;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=implicit;equation=0.34x%20+%200.94z%20-%20178.91%20~%200;cubes=16;visible=true;fixdomain=false;xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=0;zmax=300;alpha=-1;hidemyedges=false;view=0;format=normal;constcol=rgb(255,0,0)&type=point;point=(110.51,0,150.17);visible=true;color=rgb(0,0,0);size=10&type=point;point=(30.15,0,179.42);visible=true;color=rgb(0,0,0);size=10&type=point;point=(-30.15,0,201.37);visible=true;color=rgb(0,0,0);size=10&type=window;hsrmode=0;nomidpts=true;anaglyph=-1;center=63.872070381998746,-900.2378721263345,430.68797546933126,1;focus=0,0,0,1;up=-0.13950133092094227,0.5117757898589425,0.8477174762770563,1;transparent=false;alpha=140;twoviews=false;unlinkviews=false;axisextension=0.7;shownormals=false;shownormalsatpts=false;xaxislabel=x;yaxislabel=y;zaxislabel=z;edgeson=true;faceson=true;showbox=false;showaxes=true;showticks=true;perspective=true;centerxpercent=0.5379715726590277;centerypercent=0.6732795173163939;rotationsteps=30;autospin=true;xygrid=false;yzgrid=false;xzgrid=false;gridsonbox=true;gridplanes=true;gridcolor=rgb(128,128,128);xmin=-150;xmax=150;ymin=-150;ymax=150;zmin=0;zmax=300;xscale=20;yscale=20;zscale=20;zcmin=-4;zcmax=4;xscalefactor=20;yscalefactor=20;zscalefactor=20;tracemode=0;tracepoint=0,0,0,1;keep2d=false;zoom=0.000667
    #
    # Values correspond to default values for a T Shaped wind turbine.
    #
    # The three points in the plot are (1) LowEndStopTailAssemblyBaseAxisAligned, (2) ZeroAnglePoint, and (3) PiAnglePoint.
    #
    [
        Cell('Low End Stop Plane, Yaw Bearing Cylinder, Ellipse of Intersection',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('OuterLowEndStopWidth'),
        # Distance low end stop overlaps with yaw bearing pipe.
        # A cut is performed between these two.
        Cell('LowEndStopYawBearingOverlap'),
        Cell('LowEndStopWidth')
    ],
    [
        Cell('=YawPipeRadius * 0.5',
             alias='OuterLowEndStopWidth'),
        Cell('=floor(YawPipeDiameter / 6)',
             alias='LowEndStopYawBearingOverlap'),
        Cell('=YawPipeRadius + OuterLowEndStopWidth',
             alias='LowEndStopWidth')
    ],
    [
        Cell('OuterTailHingeParentPlacement'),
        Cell('LowEndStopTailAssemblyPlacement'),
        Cell('LowEndStopTailAssemblyBase')
    ],
    [
        Cell('=TailAssemblyPlacement * OuterTailHingePlacement',
             alias='OuterTailHingeParentPlacement'),
        # Create LowEndStopTailAssemblyPlacement WITHOUT rotation, and only translation
        # since the angle of rotation is calculated after determining the low end stop plane.
        Cell('=OuterTailHingeParentPlacement * create(<<placement>>; LowEndStopBase; create(<<rotation>>))',
             alias='LowEndStopTailAssemblyPlacement'),
        Cell('=OuterTailHingeParentPlacement * LowEndStopBase',
             alias='LowEndStopTailAssemblyBase'),
    ],
    [
        #
        # General approach:
        # Define a series of transformations to convert the problem from 3D into 2D
        # where an external point forms tangent lines to a circle.
        #
        Cell('AlignLowEndStopWithXAxis'),
    ],
    [
        Cell('=create(<<placement>>; create(<<vector>>); create(<<vector>>; 0; 0; 1); TailAssemblyAngle)',
             alias='AlignLowEndStopWithXAxis')
    ],
    #
    # Define two points on low end stop plane to get two vectors on the plane.
    #
    [
        # Relative to Tail_Stop_LowEnd document.
        Cell('LowEndStopPlanePoint1'),
        Cell('LowEndStopPlanePoint1TailAssembly'),
        Cell('LowEndStopPlanePoint1TailAssemblyAxisAligned')
    ],
    [
        Cell('=create(<<vector>>; 0; -YawPipeRadius; 0)',
             alias='LowEndStopPlanePoint1'),
        Cell('=LowEndStopTailAssemblyPlacement * LowEndStopPlanePoint1',
             alias='LowEndStopPlanePoint1TailAssembly'),
        Cell('=AlignLowEndStopWithXAxis * LowEndStopPlanePoint1TailAssembly',
             alias='LowEndStopPlanePoint1TailAssemblyAxisAligned')
    ],
    [
        # Relative to Tail_Stop_LowEnd document.
        Cell('LowEndStopPlanePoint2'),
        Cell('LowEndStopPlanePoint2TailAssembly'),
        Cell('LowEndStopPlanePoint2TailAssemblyAxisAligned')
    ],
    [
        Cell('=create(<<vector>>; LowEndStopWidth; 0; 0)',
             alias='LowEndStopPlanePoint2'),
        Cell('=LowEndStopTailAssemblyPlacement * LowEndStopPlanePoint2',
             alias='LowEndStopPlanePoint2TailAssembly'),
        Cell('=AlignLowEndStopWithXAxis * LowEndStopPlanePoint2TailAssembly',
             alias='LowEndStopPlanePoint2TailAssemblyAxisAligned')
    ],
    [
        Cell('LowEndStopTailAssemblyBaseAxisAligned')
    ],
    [
        Cell('=AlignLowEndStopWithXAxis * LowEndStopTailAssemblyBase',
             alias='LowEndStopTailAssemblyBaseAxisAligned')
    ],
    [
        # Calculate two vectors, Vd and Ve, on the Low End Stop plane.
        Cell('Vd'), Cell('Ve')
    ],
    [
        Cell('=LowEndStopPlanePoint1TailAssemblyAxisAligned - LowEndStopTailAssemblyBaseAxisAligned',
             alias='Vd'),
        Cell('=LowEndStopPlanePoint2TailAssemblyAxisAligned - LowEndStopTailAssemblyBaseAxisAligned',
             alias='Ve')
    ],
    [
        # Cross product Vd and Ve to find vector perpendicular to the Low End Stop plane, Vf.
        # https://en.wikipedia.org/wiki/Cross_product
        Cell('Vf'),
        Cell('Vd × Ve')
    ],
    [
        Cell('=create(<<vector>>; .Vd.y * .Ve.z - .Vd.z * .Ve.y; .Vd.z * .Ve.x - .Vd.x * .Ve.z; .Vd.x * .Ve.y - .Vd.y * .Ve.x)',
             alias='Vf'),
        Cell('Cross Product', styles=[Style.ITALIC])
    ],
    [
        # Normalize Vf from step above.
        Cell('Vo'),
        Cell('Normalize Vf')
    ],
    [
        Cell('=.Vf / .Vf.Length', alias='Vo')
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
        Cell('LowEndStopPlaneDistance (d)')
    ],
    [
        Cell('=Vo * LowEndStopPlanePoint1TailAssemblyAxisAligned',
             alias='LowEndStopPlaneDistance')
    ],
    #
    # Find two points on yaw bearing pipe that intersect with the low end stop plane along the x-axis.
    #
    # Equation of yaw bearing pipe cylinder:
    # x^2 + y^2 = r^2
    #
    # Parametric equations for yaw bearing pipe cylinder:
    # x = r * cos(θ)
    # y = r * sin(θ)
    #
    # Plug in (r *cos(θ)) for x into equation of plane with no y-component:
    # a * x + c * z = d and solve in terms of z
    #
    # https://www.wolframalpha.com/input?i=a+*+%28r+*+cos%28%CE%B8%29%29+%2B+c+*+z+%3D+d+solve+for+z
    # z = (d - a * r * cos(θ)) / c
    #
    [
        Cell('ZeroAngleZ'),
        Cell('PiAngleZ')
    ],
    [
        Cell('=(LowEndStopPlaneDistance - Vo.x * YawPipeRadius * cos(0)) / Vo.z',
             alias='ZeroAngleZ'),
        Cell('=(LowEndStopPlaneDistance - Vo.x * YawPipeRadius * cos(180)) / Vo.z',
             alias='PiAngleZ')
    ],
    [
        Cell('ZeroAnglePoint'),
        Cell('PiAnglePoint')
    ],
    [
        Cell('=create(<<vector>>; YawPipeRadius; 0; ZeroAngleZ)',
             alias='ZeroAnglePoint'),
        Cell('=create(<<vector>>; -YawPipeRadius; 0; PiAngleZ)',
             alias='PiAnglePoint')
    ],
    #
    # Subtract above two vectors to find length of major axis length for the ellipse
    # formed by the intersection of the yaw bearing pipe and low end stop plane.
    #
    [
        Cell('MajorAxisLength'),
        Cell('XDownScaleFactor')
    ],
    [
        Cell('=(ZeroAnglePoint - PiAnglePoint).Length / 2',
             alias='MajorAxisLength'),
        Cell('=YawPipeRadius / MajorAxisLength',
             alias='XDownScaleFactor')
    ],
    #
    # Scale down x from transformed low end stop point.
    # This forms the external point tangent to a circle in 2d.
    #
    [
        Cell('ScaledDownLowEndStopX')
    ],
    [
        Cell('=.LowEndStopTailAssemblyBaseAxisAligned.x * XDownScaleFactor',
             alias='ScaledDownLowEndStopX')
    ],
    #
    # Use equation of tangent line to circle and solve in terms of m (slope):
    # https://www.wolframalpha.com/input?i=0+%3D+mx+%2B+r+*+sqrt%281+%2B+m%5E2%29+solve+for+m
    # Pick whichever of the two possible equations yield a positive slope.
    #
    #     y = mx + r * sqrt(1 + m^2)
    #
    #     Let y = 0 since external point is on the y-axis.
    #
    #     m = r / sqrt(-r^2 + x^2)
    #
    [
        Cell('SlopeOfTangentLine')
    ],
    [
        Cell('=YawPipeRadius / sqrt(-(YawPipeRadius^2) + ScaledDownLowEndStopX^2)',
             alias='SlopeOfTangentLine')
    ],
    #
    # Substitute equation of tangent line into equation of circle to solve for x.
    # Use equation of tangent line with negative y-intercept:
    # https://www.wolframalpha.com/input?i=x%5E2+%2B+%28mx+-+r+*+sqrt%281+%2B+m%5E2%29%29%5E2+%3D+r%5E2+solve+for+x
    #
    # Then plug in x value into equation of tangent equation to solve for y.
    #
    [
        Cell('TangentPointX2d'),
        Cell('TangentPointY2d')
    ],
    [
        Cell('=(SlopeOfTangentLine * YawPipeRadius) / sqrt(1 + SlopeOfTangentLine^2)',
             alias='TangentPointX2d'),
        Cell('=SlopeOfTangentLine * TangentPointX2d - YawPipeRadius * sqrt(1 + SlopeOfTangentLine^2)',
             alias='TangentPointY2d')
    ],
    #
    # Scale x back up before getting 3d tangency point.
    # Find z-coordinate of 3d tangency point by plugging in x value into equation of plane
    # with zero y-component:
    #
    # https://www.wolframalpha.com/input?i=a+x+%2B+c+z+-+d+%3D+0+in+terms+of+z
    #
    # z = (d - a x) / c
    #
    [
        Cell('XUpScaleFactor'),
        Cell('TangentPointX'),
        Cell('TangentPointY')
    ],
    [
        Cell('=1 / XDownScaleFactor',
             alias='XUpScaleFactor'),
        Cell('=XUpScaleFactor * TangentPointX2d',
             alias='TangentPointX'),
        Cell('=(LowEndStopPlaneDistance - Vo.x * TangentPointX) / Vo.z',
             alias='TangentPointZ')
    ],
    [
        Cell('AxisAlignedTangentPoint')
    ],
    [
        Cell('=create(<<vector>>; TangentPointX; TangentPointY2d; TangentPointZ)',
             alias='AxisAlignedTangentPoint')
    ],
    [
        Cell('Point on Yaw Bearing cylinder where Low End Stop touches it')
    ],
    [
        Cell('TangentPoint')
    ],
    [
        Cell('=minvert(AlignLowEndStopWithXAxis) * AxisAlignedTangentPoint',
             alias='TangentPoint')
    ],
    [
        Cell('TangentVector'),
        Cell('FrontBottomRightVector'),
        Cell('LowEndStopAngle')
    ],
    [
        Cell('=TangentPoint - LowEndStopTailAssemblyBase',
             alias='TangentVector'),
        Cell('=LowEndStopPlanePoint1TailAssembly - LowEndStopTailAssemblyBase',
             alias='FrontBottomRightVector'),
        Cell('=acos(TangentVector * FrontBottomRightVector / (.TangentVector.Length * .FrontBottomRightVector.Length))',
             alias='LowEndStopAngle')
    ],
    [
        Cell('LowEndStopPlacement'),
        Cell('LowEndStopLengthScaleFactor'),
        Cell('LowEndStopLength')
    ],
    [
        Cell('=create(<<placement>>; LowEndStopBase; create(<<rotation>>; create(<<vector>>; 0; 0; -1); LowEndStopAngle))',
             alias='LowEndStopPlacement'),
        #
        # For T Shape, scale low end stop length by 1.15 for ALWAYS.
        # For H & Star Shape, scale low end stop length by 1.1 ONLY if side piece doesn't extend to middle of yaw bearing pipe.
        # This factor can't be too big otherwise the low end stop may hit the side piece that stiffens
        # the top piece instead of making contact with the yaw bearing pipe.
        # Increasing MetalLengthL to 90 and VerticalPlaneAngle to 20 for Star Shape from default values
        # results in CanSideExtendToMiddleOfYawBearingPipe evaluating to True.
        #
        Cell('=RotorDiskRadius < 187.5 ? 1.15 : CanSideExtendToMiddleOfYawBearingPipe == True ? 1 : 1.1',
             alias='LowEndStopLengthScaleFactor'),
        Cell('=TangentVector.Length * LowEndStopLengthScaleFactor',
             alias='LowEndStopLength')
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
        Cell('=create(<<vector>>; -1; slope; 0)',
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
        Cell('=create(<<rotation>>; FurlAxis; 0deg)',
             alias='EndOfBoom0Rotation'),
        Cell('=create(<<rotation>>; FurlAxis; 90deg)',
             alias='EndOfBoom90Rotation'),
        Cell('=create(<<rotation>>; FurlAxis; 180deg)',
             alias='EndOfBoom180Rotation'),
        Cell('=create(<<rotation>>; FurlAxis; 270deg)',
             alias='EndOfBoom270Rotation')
    ],
    [
        Cell('EndOfBoom0Placement'),
        Cell('EndOfBoom90Placement'),
        Cell('EndOfBoom180Placement'),
        Cell('EndOfBoom270Placement')
    ],
    [
        Cell('=create(<<placement>>; .OuterTailHingeBase - EndOfBoom0Rotation * .OuterTailHingeBase; EndOfBoom0Rotation)',
             alias='EndOfBoom0Placement'),
        Cell('=create(<<placement>>; .OuterTailHingeBase - EndOfBoom90Rotation * .OuterTailHingeBase; EndOfBoom90Rotation)',
             alias='EndOfBoom90Placement'),
        Cell('=create(<<placement>>; .OuterTailHingeBase - EndOfBoom180Rotation * .OuterTailHingeBase; EndOfBoom180Rotation)',
             alias='EndOfBoom180Placement'),
        Cell('=create(<<placement>>; .OuterTailHingeBase - EndOfBoom270Rotation * .OuterTailHingeBase; EndOfBoom270Rotation)',
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
        Cell('=create(<<vector>>; .Axis1.y * .Axis2.z - .Axis1.z * .Axis2.y; .Axis1.z * .Axis2.x - .Axis1.x * .Axis2.z; .Axis1.x * .Axis2.y - .Axis1.y * .Axis2.x)',
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
        Cell('=create(<<vector>>; xLineOrigin; yLineOrigin; zLineOrigin)',
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
        Cell('=create(<<vector>>; .Vh.y * .NormalVectorOfMaximumFurlPlane.z - .Vh.z * .NormalVectorOfMaximumFurlPlane.y; .Vh.z * .NormalVectorOfMaximumFurlPlane.x - .Vh.x * .NormalVectorOfMaximumFurlPlane.z; .Vh.x * .NormalVectorOfMaximumFurlPlane.y - .Vh.y * .NormalVectorOfMaximumFurlPlane.x)',
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
        Cell('yDistance'),
        Cell('xDistance')
    ],
    [
        Cell('=(CenterOfSphere - PointOnLineClosestToCenterOfSphere).Length',
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
        Cell('dDistance'),
        Cell('MaximumFurlAngle'),
        Cell('FurlRotation')
    ],
    [
        Cell('=(.FarthestIntersectionPoint - .FurledEndOfBoom0Placement.Base).Length',
             alias='dDistance'),
        Cell('=acos(1 - dDistance ^ 2 / (2 * Radius ^ 2))',
             alias='MaximumFurlAngle'),
        Cell('=create(<<rotation>>; FurlAxis; MaximumFurlAngle)',
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
    #   1. HighEndStopFurledTailAssemblyBase
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
        Cell('FurledHighEndStopTailAssemblyPlacement')
    ],
    [
        # center - rotation.multVec(center)
        Cell('=.OuterTailHingeBase - FurlRotation * .OuterTailHingeBase',
             alias='TailFurlBase'),
        Cell('=create(<<placement>>; TailFurlBase; FurlRotation)',
             alias='TailFurlPlacement'),
        Cell('=TailAssemblyPlacement * TailFurlPlacement * TailBoomVaneAssemblyParentPlacement',
             alias='FurledHighEndStopTailAssemblyPlacement')
    ],
    [
        Cell('HighEndStopBoomDirectionVectorBase'),
        Cell('HighEndStopYawBearingDirectionVector'),
    ],
    [
        # + 1 in z to create a normalized vector in the direction of the boom.
        Cell('=HighEndStopBase + create(<<vector>>; 0; 0; 1)',
             alias='HighEndStopBoomDirectionVectorBase'),
        # + 1 in y to create a normalized vector in the direction of the yaw bearing.
        Cell('=HighEndStopBase + create(<<vector>>; 0; 1; 0)',
             alias='HighEndStopYawBearingDirectionVector')
    ],
    [
        Cell('HighEndStopFurledTailAssemblyBase'),
        Cell('HighEndStopBoomDirectionVectorFurledTailAssemblyBase'),
        Cell('HighEndStopYawBearingDirectionVectorTailAssembly')
    ],
    [
        Cell('=FurledHighEndStopTailAssemblyPlacement * HighEndStopBase',
             alias='HighEndStopFurledTailAssemblyBase'),
        Cell('=FurledHighEndStopTailAssemblyPlacement * HighEndStopBoomDirectionVectorBase',
             alias='HighEndStopBoomDirectionVectorFurledTailAssemblyBase'),
        Cell('=FurledHighEndStopTailAssemblyPlacement * HighEndStopYawBearingDirectionVector',
             alias='HighEndStopYawBearingDirectionVectorTailAssembly')
    ],
    [
        # Calculate two vectors, Va and Vb, on the Furled High End Stop plane.
        Cell('Va'), Cell('Vb')
    ],
    [
        Cell('=.HighEndStopBoomDirectionVectorFurledTailAssemblyBase - .HighEndStopFurledTailAssemblyBase',
             alias='Va'),
        Cell('=.HighEndStopYawBearingDirectionVectorTailAssembly - .HighEndStopFurledTailAssemblyBase',
             alias='Vb')
    ],
    [
        # Cross product Va and Vb to find vector perpendicular to the High End Stop plane, Vn.
        # Since Va and Vb have length 1, then Vn will be normalized already.
        # https://en.wikipedia.org/wiki/Cross_product
        Cell('Vn'),
        Cell('Va × Vb')
    ],
    [
        Cell('=create(<<vector>>; .Va.y * .Vb.z - .Va.z * .Vb.y; .Va.z * .Vb.x - .Va.x * .Vb.z; .Va.x * .Vb.y - .Va.y * .Vb.x)',
             alias='Vn'),
        Cell('Cross Product', styles=[Style.ITALIC])
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
        Cell('=.Vn * .HighEndStopFurledTailAssemblyBase',
             alias='FurledHighEndStopPlaneDistance')
    ],
    [
        Cell('AngleBetweenYAxisAndHighEndStop'),
        Cell('TangentAngle')
    ],
    [
        # From the dot product between vector Va and y-axis vector (0, 1, 0).
        # https://en.wikipedia.org/wiki/Dot_product#Geometric_definition
        Cell('=acos(.Va.y)',
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
        Cell('=create(<<vector>>; TangentAngleX; TangentAngleY; TangentAngleZ)',
             alias='YawBearingHighEndStopTangentPoint')
    ],
    [
        Cell('References', styles=[Style.ITALIC, Style.UNDERLINE])
    ],
    [
        Cell('Finding a point on a 3d line',
             styles=[Style.ITALIC]),
        Cell('What is the equation for a 3D line?',
             styles=[Style.ITALIC]),
    ],
    [
        Cell('https://math.stackexchange.com/questions/576137/finding-a-point-on-a-3d-line/576154#576154'),
        Cell('https://math.stackexchange.com/questions/404440/what-is-the-equation-for-a-3d-line/404446#404446')
    ],
    [
        # T is a reserved alias since FreeCAD 20.
        Cell('T_tangent'),
        Cell('HighEndStopPointWhereXEqualsTangent'),
    ],
    [
        Cell('=(TangentAngleX - .HighEndStopFurledTailAssemblyBase.x) / .Va.x',
             alias='T_tangent'),
        Cell('=.HighEndStopFurledTailAssemblyBase + T_tangent * .Va',
             alias='HighEndStopPointWhereXEqualsTangent')
    ],
    [
        Cell('HighEndStop', styles=[Style.BOLD, Style.UNDERLINE])
    ],
    [
        Cell('Width', styles=[Style.UNDERLINE]), Cell('Length', styles=[Style.UNDERLINE])
    ],
    [
        Cell('=(.YawBearingHighEndStopTangentPoint - .HighEndStopPointWhereXEqualsTangent).Length',
             alias='HighEndStopWidth'),
        # Make high end stop extend YawPipeRadius * 2 in the X-direction.
        Cell('=(YawPipeRadius * 2 - .HighEndStopFurledTailAssemblyBase.x) / .Va.x',
             alias='HighEndStopLength'),
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
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; 0)',
             alias='UpperBottomLeftCorner')
    ],
    [
        Cell('UpperBottomLeftCornerTailAssembly'),
        Cell('=FurledHighEndStopTailAssemblyPlacement * UpperBottomLeftCorner',
             alias='UpperBottomLeftCornerTailAssembly')
    ],
    [
        # of High End Stop
        Cell('UpperTopLeftCorner'),
        Cell('=create(<<vector>>; -FlatMetalThickness / 2; BoomPipeRadius + HighEndStopWidth; HighEndStopLength)',
             alias='UpperTopLeftCorner')
    ],
    [
        Cell('UpperTopLeftCornerTailAssembly'),
        Cell('=FurledHighEndStopTailAssemblyPlacement * UpperTopLeftCorner',
             alias='UpperTopLeftCornerTailAssembly')
    ],
    # SafetyCatch
    # -----------
    # Depedent upon high end stop.
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
        Cell('=(Xupper - .UpperBottomLeftCornerTailAssembly.x) / (.UpperTopLeftCornerTailAssembly.x - .UpperBottomLeftCornerTailAssembly.x)',
             alias='Tupper')
    ],
    [
        Cell('SafetyCatchPosition'),
        Cell('=.UpperBottomLeftCornerTailAssembly + Tupper * (.UpperTopLeftCornerTailAssembly - .UpperBottomLeftCornerTailAssembly)',
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
    ]
]
