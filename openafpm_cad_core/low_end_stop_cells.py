from typing import List

from .spreadsheet import Cell, Style

__all__ = ['low_end_stop_cells']


low_end_stop_cells: List[List[Cell]] = [
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
        Cell('RotorDiskRadius'),
        Cell('FlatMetalThickness'),
        Cell('YawPipeDiameter'),
        Cell('CalculatedWindTurbineShape')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.FlatMetalThickness',
             alias='FlatMetalThickness'),
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter'),
        Cell('=Spreadsheet.CalculatedWindTurbineShape',
             alias='CalculatedWindTurbineShape')
    ],
    [
        Cell('VerticalPlaneAngle'),
    ],
    [
        Cell('=Spreadsheet.VerticalPlaneAngle',
             alias='VerticalPlaneAngle'),
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
        Cell('TailBoomTriangularBraceWidth'),
        Cell('OuterTailHingeParentPlacement'),
        Cell('TailAssemblyAngle')
    ],
    [
        Cell('=Tail.TailBoomTriangularBraceWidth',
             alias='TailBoomTriangularBraceWidth'),
        Cell('=Tail.OuterTailHingeParentPlacement',
             alias='OuterTailHingeParentPlacement'),
        Cell('=Tail.TailAssemblyAngle',
             alias='TailAssemblyAngle')
    ],
    [
        Cell('HingeOuterPipeRadius')
    ],
    [
        Cell('=Tail.HingeOuterPipeRadius',
             alias='HingeOuterPipeRadius'),
    ],
    # Calculated
    # ----------
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('YawPipeRadius'),
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius')
    ],
    # Low End Stop
    # ------------
    # Document: Tail_Hinge_Outer, Part: Stop_LowEnd
    # Document: Tail_Stop_LowEnd, Part: Tail_Stop_LowEnd
    [
        Cell('Low End Stop',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # Relative to Tail_Hinge_Outer
        Cell('LowEndStopZ'), Cell('=TailBoomTriangularBraceWidth - FlatMetalThickness',
                                  alias='LowEndStopZ')
    ],
    [
        Cell('LowEndStopBase'),
        Cell('=vector(0; 0; LowEndStopZ)',
             alias='LowEndStopBase')
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
        Cell('=HingeOuterPipeRadius * 0.5',
             alias='OuterLowEndStopWidth'),
        Cell('=floor(YawPipeDiameter / 6)',
             alias='LowEndStopYawBearingOverlap'),
        Cell('=HingeOuterPipeRadius + OuterLowEndStopWidth',
             alias='LowEndStopWidth')
    ],
    [
        Cell('LowEndStopTailAssemblyPlacementAxisAligned'),
        Cell('LowEndStopTailAssemblyBase')
    ],
    [
        # Create LowEndStopTailAssemblyPlacementAxisAligned WITHOUT rotation, and only translation
        # since the angle of rotation is calculated after determining the low end stop plane.
        Cell('=OuterTailHingeParentPlacement * placement(LowEndStopBase; rotation(vector(0; 0; 0); 0))',
             alias='LowEndStopTailAssemblyPlacementAxisAligned'),
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
        Cell('LowEndStopTailAssemblyBaseAxisAligned')
    ],
    [
        Cell('=placement(vector(0; 0; 0); vector(0; 0; 1); TailAssemblyAngle)',
             alias='AlignLowEndStopWithXAxis'),
        Cell('=AlignLowEndStopWithXAxis * LowEndStopTailAssemblyBase',
             alias='LowEndStopTailAssemblyBaseAxisAligned')
    ],
    [
        # Normal vector to (lower) Low End Stop plane aligned with x-axis.
        Cell('Vn'),
    ],
    [
        Cell('=.AlignLowEndStopWithXAxis.Rotation * .LowEndStopTailAssemblyPlacementAxisAligned.Rotation * vector(0; 0; 1)',
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
        Cell('LowEndStopPlaneDistance (d)')
    ],
    [
        Cell('=.Vn * LowEndStopTailAssemblyBaseAxisAligned',
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
        Cell('=(LowEndStopPlaneDistance - Vn.x * YawPipeRadius * cos(0)) / Vn.z',
             alias='ZeroAngleZ'),
        Cell('=(LowEndStopPlaneDistance - Vn.x * YawPipeRadius * cos(180)) / Vn.z',
             alias='PiAngleZ')
    ],
    [
        Cell('ZeroAnglePoint'),
        Cell('PiAnglePoint')
    ],
    [
        Cell('=vector(YawPipeRadius; 0; ZeroAngleZ)',
             alias='ZeroAnglePoint'),
        Cell('=vector(-YawPipeRadius; 0; PiAngleZ)',
             alias='PiAnglePoint')
    ],
    #
    # Subtract above two vectors to find semi-major axis length for the ellipse
    # formed by the intersection of the yaw bearing pipe and low end stop plane.
    #
    [
        Cell('MajorAxis'),
        Cell('SemiMajorAxisLength'),
        Cell('XDownScaleFactor')
    ],
    [
        Cell('=ZeroAnglePoint - PiAnglePoint',
             alias='MajorAxis'),
        Cell('=MajorAxis.Length / 2',
             alias='SemiMajorAxisLength'),
        Cell('=YawPipeRadius / SemiMajorAxisLength',
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
        Cell('=(LowEndStopPlaneDistance - Vn.x * TangentPointX) / Vn.z',
             alias='TangentPointZ')
    ],
    [
        Cell('AxisAlignedTangentPoint')
    ],
    [
        Cell('=vector(TangentPointX; TangentPointY2d; TangentPointZ)',
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
        # Relative to Tail_Stop_LowEnd document.
        # The "long end" is the part of the stop that extends towards the yaw pipe.
        Cell('VectorTowardsLongEnd'),
        Cell('TangentPointLowEndStopLocal'),
        Cell('LowEndStopAngle')
    ],
    [
        Cell('=vector(0; -1; 0)',
             alias='VectorTowardsLongEnd'),
        Cell('=minvert(.LowEndStopTailAssemblyPlacementAxisAligned) * TangentPoint',
             alias='TangentPointLowEndStopLocal'),
        Cell('=acos(.TangentPointLowEndStopLocal * .VectorTowardsLongEnd / (.TangentPointLowEndStopLocal.Length * .VectorTowardsLongEnd.Length))',
             alias='LowEndStopAngle')
    ],
    [
        Cell('LowEndStopPlacement'),
        Cell('LowEndStopLengthScaleFactor'),
        Cell('LowEndStopLength')
    ],
    [
        Cell('=placement(LowEndStopBase; rotation(vector(0; 0; -1); LowEndStopAngle))',
             alias='LowEndStopPlacement'),
        #
        # For T Shape, scale low end stop length by 1.15 for ALWAYS.
        # For H & Star Shape, scale low end stop length by 1.1 ONLY if side piece doesn't extend to middle of yaw bearing pipe.
        # This factor can't be too big otherwise the low end stop may hit the side piece that stiffens
        # the top piece instead of making contact with the yaw bearing pipe.
        # Increasing MetalLengthL to 90 and VerticalPlaneAngle to 20 for Star Shape from default values
        # results in CanSideExtendToMiddleOfYawBearingPipe evaluating to True.
        #
        Cell('=CalculatedWindTurbineShape == <<T>> ? 1.15 : (CanSideExtendToMiddleOfYawBearingPipe == True ? 1 : 1.1)',
             alias='LowEndStopLengthScaleFactor'),
        Cell('=.TangentPointLowEndStopLocal.Length * LowEndStopLengthScaleFactor',
             alias='LowEndStopLength')
    ],
    # Extend High End Stop to Low End Stop
    # ------------------------------------
    [
        Cell('Extend High End Stop to Low End Stop', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    # The below calculations are relative to the TailAssembly document.
    [
        Cell('VectorTowardsHighEndStop'),
        Cell('LowEndStopTailAssemblyPlacement'),
        Cell('LowEndStopBottomLeftPoint')
    ],
    [
        Cell('=vector(-1; 0; 0)',
             alias='VectorTowardsHighEndStop'),
        Cell('=OuterTailHingeParentPlacement * LowEndStopPlacement',
             alias='LowEndStopTailAssemblyPlacement'),
        Cell('=LowEndStopTailAssemblyPlacement * vector(-LowEndStopYawBearingOverlap; 0; 0)',
             alias='LowEndStopBottomLeftPoint')
    ],
    [
        Cell('LeftPerpendicularLowEndStopPlane', styles=[Style.UNDERLINE])
    ],
    [
        Cell('NormalVector'), Cell('Distance')
    ],
    [
        Cell('=LowEndStopTailAssemblyPlacement.Rotation * VectorTowardsHighEndStop',
             alias='LeftPerpendicularLowEndStopPlaneNormalVector'),
        Cell('=.LeftPerpendicularLowEndStopPlaneNormalVector * .LowEndStopBottomLeftPoint * -1',
             alias='LeftPerpendicularLowEndStopPlaneDistance')
    ],
    [
        Cell('LowerLowEndStopPlane', styles=[Style.UNDERLINE])
    ],
    [
        Cell('NormalVector'), Cell('Distance')
    ],
    [
        Cell('=LowEndStopTailAssemblyPlacement.Rotation * vector(0; 0; 1)',
             alias='LowerLowEndStopPlaneNormalVector'),
        Cell('=.LowerLowEndStopPlaneNormalVector * LowEndStopBottomLeftPoint * -1',
             alias='LowerLowEndStopPlaneDistance')
    ],
]
