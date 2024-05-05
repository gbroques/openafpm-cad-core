from typing import List

from .spreadsheet import Alignment, Cell, Style

__all__ = ['alternator_cells']


alternator_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('RotorDiskRadius'),
        Cell('StatorThickness'),
        Cell('MechanicalClearance')
    ],
    [
        Cell('=Spreadsheet.RotorDiskRadius',
             alias='RotorDiskRadius'),
        Cell('=Spreadsheet.StatorThickness',
             alias='StatorThickness'),
        Cell('=Spreadsheet.MechanicalClearance',
             alias='MechanicalClearance')
    ],
    [
        Cell('RotorDiskThickness'),
        Cell('MagnetThickness'),
        Cell('MagnetLength')
    ],
    [
        Cell('=Spreadsheet.RotorDiskThickness',
             alias='RotorDiskThickness'),
        Cell('=Spreadsheet.MagnetThickness',
             alias='MagnetThickness'),
        Cell('=Spreadsheet.MagnetLength',
             alias='MagnetLength')
    ],
    [
        Cell('MetalLengthL'),
        Cell('MetalThicknessL'),
        Cell('CoilLegWidth')
    ],
    [
        Cell('=Spreadsheet.MetalLengthL',
             alias='MetalLengthL'),
        Cell('=Spreadsheet.MetalThicknessL',
             alias='MetalThicknessL'),
        Cell('=Spreadsheet.CoilLegWidth',
             alias='CoilLegWidth')
    ],
    [
        Cell('Offset'),
        Cell('HolesDiameter'),
        Cell('YawPipeDiameter')
    ],
    [
        Cell('=Spreadsheet.Offset',
             alias='Offset'),
        Cell('=Spreadsheet.HolesDiameter',
             alias='HolesDiameter'),
        Cell('=Spreadsheet.YawPipeDiameter',
             alias='YawPipeDiameter'),
    ],
    [
        Cell('RotorResinMargin'),
        Cell('NumberMagnet')
    ],
    [
        Cell('=Spreadsheet.RotorResinMargin',
             alias='RotorResinMargin'),
        Cell('=Spreadsheet.NumberMagnet',
             alias='NumberMagnet')
    ],
    [
        Cell('CoilInnerWidth1'),
        Cell('CoilInnerWidth2'),
        Cell('CoilType'),
    ],
    [
        Cell('=Spreadsheet.CoilInnerWidth1',
             alias='CoilInnerWidth1'),
        Cell('=Spreadsheet.CoilInnerWidth2',
             alias='CoilInnerWidth2'),
        Cell('=Spreadsheet.CoilType',
             alias='CoilType'),
    ],
    [
        Cell('MagnetMaterial'),
        Cell('NumberOfCoilsPerPhase'),
        Cell('MagnetWidth')
    ],
    [
        Cell('=Spreadsheet.MagnetMaterial',
             alias='MagnetMaterial'),
        Cell('=Spreadsheet.NumberOfCoilsPerPhase',
             alias='NumberOfCoilsPerPhase'),
        Cell('=Spreadsheet.MagnetWidth',
             alias='MagnetWidth')
    ],
    [
        Cell('Hub', styles=[Style.UNDERLINE])
        # -----------------------------------
    ],
    [
        Cell('DistanceBetweenFrameAndBackRotor'),
        Cell('NumberOfHoles'),
        Cell('HubHolesRadius')
    ],
    [
        Cell('=Hub.DistanceBetweenFrameAndBackRotor',
             alias='DistanceBetweenFrameAndBackRotor'),
        Cell('=Hub.NumberOfHoles',
             alias='NumberOfHoles'),
        Cell('=Hub.HubHolesRadius',
             alias='HubHolesRadius')
    ],
    [
        Cell('HubPitchCircleRadius'),
        Cell('MiddlePadThickness')
    ],
    [
        Cell('=Hub.HubPitchCircleRadius',
             alias='HubPitchCircleRadius'),
        Cell('=Hub.MiddlePadThickness',
             alias='MiddlePadThickness')
    ],
    [
        Cell('Fastener', styles=[Style.UNDERLINE])
        # ----------------------------------------
    ],
    [
        Cell('HexNutThickness'),
        Cell('HubHexNutThickness'),
        Cell('DistanceThreadsExtendFromNuts'),
        Cell('WasherThickness')
    ],
    [
        Cell('=Fastener.HexNutThickness',
             alias='HexNutThickness'),
        Cell('=Fastener.HubHexNutThickness',
             alias='HubHexNutThickness'),
        Cell('=Fastener.DistanceThreadsExtendFromNuts',
             alias='DistanceThreadsExtendFromNuts'),
        Cell('=Fastener.WasherThickness',
             alias='WasherThickness')
    ],
    [
        Cell('ScrewHoleDiameter')
    ],
    [
        Cell('=Fastener.ScrewHoleDiameter',
             alias='ScrewHoleDiameter')
    ],
    [
        Cell('Blade', styles=[Style.UNDERLINE])
        # -------------------------------------
    ],
    [
        Cell('BladeAssemblyPlateThickness'),
        Cell('BladeThickness')
    ],
    [
        Cell('=Blade.BladeAssemblyPlateThickness',
             alias='BladeAssemblyPlateThickness'),
        Cell('=Blade.BladeThickness',
             alias='BladeThickness')
    ],
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('AlternatorTiltAngle'),
        Cell('=4deg', alias='AlternatorTiltAngle'),
        Cell('See right-hand side of page 29 of "A Wind Turbine Recipe Book (2014)".')
    ],
    [
        Cell('Stator', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # The radius of the circle that circumscribes the hexagon
        # of the stator resin cast for Star Shape.
        Cell('HexagonalStatorOuterCircumradius'),
        # Radius of the inner-most hole of stator.
        Cell('StatorInnerHoleRadius'),
        Cell('NumberOfCoils')
    ],
    [
        Cell('=(RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
             alias='HexagonalStatorOuterCircumradius'),
        Cell('=RotorDiskRadius - MagnetLength - CoilLegWidth - OffsetToAlignCornersOfMagnetToDisk',
             alias='StatorInnerHoleRadius'),
        # TODO: Number of coils = RotorRadius <= 125 ? 6 : 9
        # If we ever want to support the smallest wind turbines.
        Cell('=NumberMagnet * 0.75', alias='NumberOfCoils')
    ],
    [
        # "Holes circumradius" is the radius of the circle that
        # goes through the mounting holes of the stator.
        # This is used in the Frame later to ensure
        # the Frame holes and Stator holes align.
        Cell('TShapeStatorHolesCircumradius'),
        Cell('HShapeStatorHolesCircumradius'),
        Cell('StarShapeStatorHolesCircumradius'),
        Cell('StatorHolesCircumradius')
    ],
    [
        Cell('=RotorDiskRadius + CoilLegWidth + 20',
             alias='TShapeStatorHolesCircumradius'),
        # Ensure 20 mm between hole and coil for H Shape.
        Cell('=TShapeStatorHolesCircumradius + HolesRadius',
             alias='HShapeStatorHolesCircumradius'),
        Cell('=RotorDiskRadius + CoilLegWidth + 0.5 * (HexagonalStatorOuterCircumradius - RotorDiskRadius - CoilLegWidth)',
             alias='StarShapeStatorHolesCircumradius'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeStatorHolesCircumradius : (RotorDiskRadius < 275 ? HShapeStatorHolesCircumradius : StarShapeStatorHolesCircumradius)',
             alias='StatorHolesCircumradius')
    ],
    [
        Cell('TShapeNumberOfStatorHoles'),
        Cell('HShapeNumberOfStatorHoles'),
        Cell('StarShapeNumberOfStatorHoles'),
        Cell('NumberOfStatorHoles')
    ],
    [
        Cell('3',
             alias='TShapeNumberOfStatorHoles'),
        Cell('4',
             alias='HShapeNumberOfStatorHoles'),
        Cell('6',
             alias='StarShapeNumberOfStatorHoles'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfStatorHoles : ' +
             '(RotorDiskRadius < 275 ? HShapeNumberOfStatorHoles : StarShapeNumberOfStatorHoles)',
             alias='NumberOfStatorHoles')
    ],
    [
        Cell('TShapeEarSize'),
        Cell('HShapeEarSize'),
        Cell('EarSize')
    ],
    [
        Cell('25',
             alias='TShapeEarSize'),
        Cell('35',
             alias='HShapeEarSize'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeEarSize : HShapeEarSize',
             alias='EarSize')
    ],
    [
        # CoilsAngle needed to align the stator mounting points (the holes in the resin cast)
        # with the middle of the space between two coils, and not with the center of one coil.
        # This provides more space when making the hole in the resin,
        # without having to worry about hitting a coil.
        # This isn't strictly needed for Star Shape, but we rotate the coils anyways for consistency.
        Cell('TAndStarShapeCoilsAngle'),
        Cell('HShapeCoilsAngle'),
        Cell('CoilsAngle')
    ],
    [
        Cell('=360 / NumberOfCoils / 2',
             alias='TAndStarShapeCoilsAngle'),
        Cell('0',
             alias='HShapeCoilsAngle'),
        Cell('=RotorDiskRadius < 187.5 ? TAndStarShapeCoilsAngle : (RotorDiskRadius < 275 ? HShapeCoilsAngle : TAndStarShapeCoilsAngle)',
             alias='CoilsAngle')
    ],
    [
        # Make coil slightly thinner than stator resin cast to fix z-fighting rendering issue.
        Cell('CoilThicknessOffset'),
        Cell('CoilThickness')
    ],
    [
        Cell('0.2', alias='CoilThicknessOffset'),
        Cell('=StatorThickness - CoilThicknessOffset', alias='CoilThickness')
    ],
    [
        Cell('Mold', styles=[Style.UNDERLINE])
    ],
    # For metric hex bolt dimensions, see:
    # https://www.atlrod.com/metric-hex-bolt-dimensions/
    [
        Cell('StatorMoldBoltDiameter'),
        Cell('StatorMoldBoltWidthAcrossCorners'),
        Cell('StatorMoldBoltLength'),
    ],
    [
        # M12 Bolt
        Cell('12',
             alias='StatorMoldBoltDiameter'),
        Cell('20.78',  # C (MAX)
             alias='StatorMoldBoltWidthAcrossCorners'),
        Cell('65',
             alias='StatorMoldBoltLength')
    ],
    [
        Cell('LocatingBoltDiameter'),
        Cell('LocatingBoltLength'),
    ],
    [
        # M12 Bolt
        Cell('12',
             alias='LocatingBoltDiameter'),
        Cell('85',
             alias='LocatingBoltLength')
    ],
    [
        # Controls radius of screw holes for stator mold, rotor mold,
        # and blade hub rotor plates.
        # These appear to be pilot holes for a 5mm diameter screw.
        Cell('ScrewHoleRadius'),
        Cell('DistanceBetweenOuterHolesAndStatorMold'),
        Cell('DistanceBetweenInnerHolesAndStatorMold')
    ],
    [
        Cell('=ScrewHoleDiameter / 2',
             alias='ScrewHoleRadius'),
        # Ensure holes are close enough to create
        # pressure for the resin not to flow out.
        Cell('=StatorMoldBoltDiameter * 2',
             alias='DistanceBetweenOuterHolesAndStatorMold'),
        Cell('=StatorMoldBoltDiameter * 1.5',
             alias='DistanceBetweenInnerHolesAndStatorMold')
    ],
    [
        Cell('TShapeSketchY'),
        Cell('HShapeSketchY'),
        Cell('SketchY')
    ],
    [
        Cell('=-EarSize / 2',
             alias='TShapeSketchY'),
        Cell('0',
             alias='HShapeSketchY'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeSketchY : HShapeSketchY',
             alias='SketchY')
    ],
    [
        # TODO: Rename to IslandHolesCircumradius?
        Cell('IslandInnerRadius'),
        Cell('EarAngle'),
        Cell('StatorMoldSideLength')
    ],
    [
        Cell('=StatorInnerHoleRadius - DistanceBetweenInnerHolesAndStatorMold',
             alias='IslandInnerRadius'),
        Cell('=360 / NumberOfStatorHoles',
             alias='EarAngle'),
        Cell('=1.55 * 2 * StatorHolesCircumradius',
             alias='StatorMoldSideLength')
    ],
    [
        Cell('LargeHoleAngle'),
        Cell('LengthMiddleHoles'),
        Cell('StatorMoldHolesSketchAngle')
    ],
    [
        # Divide by 4 because there are 3 bolts and 4 spaces between each "ear"
        # for the T and H Shape Stator Mold.
        Cell('=EarAngle / 4',
             alias='LargeHoleAngle'),
        Cell('=(RotorDiskRadius < 275 ? StatorHolesCircumradius : HexagonalStatorOuterCircumradius) + DistanceBetweenOuterHolesAndStatorMold',
             alias='LengthMiddleHoles'),
        Cell('=RotorDiskRadius < 187.5 ? 0 : (RotorDiskRadius < 275 ? 45 : 0)',
             alias='StatorMoldHolesSketchAngle')
    ],
    [
        Cell('StatorMoldIslandNumberOfBolts'),
        Cell('StatorMoldIslandNumberOfScrewSectors'),
        Cell('StatorMoldIslandScrewAngle')
    ],
    [
        Cell('=RotorDiskRadius < 187.5 ? 4 : (RotorDiskRadius < 275 ? 6 : 12)',
             alias='StatorMoldIslandNumberOfBolts'),
        Cell('=RotorDiskRadius < 187.5 ? 12 : (RotorDiskRadius < 275 ? 18 : 36)',
             alias='StatorMoldIslandNumberOfScrewSectors'),
        Cell('=360deg / StatorMoldIslandNumberOfScrewSectors',
             alias='StatorMoldIslandScrewAngle'),
    ],
    [
        Cell('StatorMoldIslandNumberOfScrews'),
        Cell('DistanceOfLocatingHoleFromCenter')
    ],
    [
        Cell('=(StatorMoldIslandNumberOfScrewSectors - StatorMoldIslandNumberOfBolts) / 2',
             alias='StatorMoldIslandNumberOfScrews'),
        Cell('=0.63559 * StatorMoldSideLength',
             alias='DistanceOfLocatingHoleFromCenter')
    ],
    [
        Cell('UnroundedStatorMoldScrewLength'),
        Cell('StatorMoldScrewLength')
    ],
    [
        Cell('=StatorThickness * 2',
             alias='UnroundedStatorMoldScrewLength'),
        # Round down to nearest multiple of 5
        Cell('=UnroundedStatorMoldScrewLength - mod(UnroundedStatorMoldScrewLength; 5)',
             alias='StatorMoldScrewLength')
    ],
    [
        Cell('LocatingBolt1X'),
        Cell('LocatingBolt1Y')
    ],
    [
        Cell('=-DistanceOfLocatingHoleFromCenter * cos(45)',
             alias='LocatingBolt1X'),
        Cell('=-LocatingBolt1X + SketchY',
             alias='LocatingBolt1Y')
    ],
    [
        Cell('LocatingBolt2X'),
        Cell('LocatingBolt2Y')
    ],
    [
        Cell('=-LocatingBolt1X',
             alias='LocatingBolt2X'),
        Cell('=LocatingBolt1Y',
             alias='LocatingBolt2Y')
    ],
    [
        Cell('LocatingBolt3X'),
        Cell('LocatingBolt3Y')
    ],
    [
        Cell('=LocatingBolt2X',
             alias='LocatingBolt3X'),
        Cell('=LocatingBolt1X + SketchY',
             alias='LocatingBolt3Y')
    ],
    [
        Cell('Hexagonal Mold', styles=[Style.UNDERLINE])
    ],
    #
    #    ____ TopRightCorner
    #   /    \
    #  /      \ MiddleRightCorner
    #  \      /
    #   \____/
    #
    [
        Cell('TopRightCornerX'),
        Cell('TopRightCornerY')
    ],
    [
        Cell('=LengthMiddleHoles * cos(60)',
             alias='TopRightCornerX'),
        Cell('=LengthMiddleHoles * sin(60)',
             alias='TopRightCornerY')
    ],
    [
        Cell('LineFromMiddleRightToTopRightCornerSlope'),
        Cell('LineFromMiddleRightToTopRightCornerYIntercept')
    ],
    [
        Cell('=TopRightCornerY / (TopRightCornerX - LengthMiddleHoles)',
             alias='LineFromMiddleRightToTopRightCornerSlope'),
        Cell('=TopRightCornerY - LineFromMiddleRightToTopRightCornerSlope * TopRightCornerX',
             alias='LineFromMiddleRightToTopRightCornerYIntercept')
    ],
    [
        Cell('CoilWinder', styles=[Style.UNDERLINE])
    ],
    [
        # All 3 of these are for below CoilWinderDiskRadius calculation
        Cell('MagnetDiagonal'),
        Cell('CoilWinderDiskRadiusPadding'),
        Cell('MinimumCoilWinderDiskRadius')
    ],
    [
        Cell('=sqrt(MagnetWidth^2 + MagnetLength^2)',
             alias='MagnetDiagonal'),
        Cell('12',
             alias='CoilWinderDiskRadiusPadding'),
        Cell('60',
             alias='MinimumCoilWinderDiskRadius')
    ],
    [
        Cell('ProjectedCoilWinderDiskRadius'),
        Cell('CoilWinderDiskRadius')
    ],
    [
        Cell('=(MagnetDiagonal / 2) + CoilLegWidth + CoilWinderDiskRadiusPadding',
             alias='ProjectedCoilWinderDiskRadius'),
        Cell('=ProjectedCoilWinderDiskRadius <= MinimumCoilWinderDiskRadius ? MinimumCoilWinderDiskRadius : ProjectedCoilWinderDiskRadius',
             alias='CoilWinderDiskRadius')
    ],
    [
        Cell('CoilWinderDiskCenterHoleRadius'),
        Cell('CoilWinderDiskSmallHoleRadius'),
        Cell('CoilWinderDiskSmallHoleDiameter')
    ],
    [
        Cell('5',
             alias='CoilWinderDiskCenterHoleRadius'),
        Cell('2.5',
             alias='CoilWinderDiskSmallHoleRadius'),
        Cell('=CoilWinderDiskSmallHoleRadius * 2',
             alias='CoilWinderDiskSmallHoleDiameter')
    ],
    [
        Cell('CoilWinderDiskTapeNotchWidth'),
        Cell('CoilWinderDiskFillet'),
        Cell('CoilWinderCheekThickness')
    ],
    [
        Cell('23',
             alias='CoilWinderDiskTapeNotchWidth'),
        Cell('8',
             alias='CoilWinderDiskFillet'),
        Cell('12',
             alias='CoilWinderCheekThickness')
    ],
    [
        Cell('CoilWinderDiskBottomHoleRadius'),
        Cell('RectangularVerticalDistanceOfHolesFromCenter'),
        Cell('CoilWinderNumberOfSpacingNuts')
    ],
    [
        Cell('=CoilType != 3 ? 4 : CoilInnerWidth2 / 2',
             alias='CoilWinderDiskBottomHoleRadius'),
        # TODO: Rename to RectangularRadialDistanceOfHolesFromCenter?
        # Vertical may not make sense since coil winder parts are rotated by CoilWinderAngle.
        Cell('=MagnetLength / 2 - CoilWinderDiskSmallHoleRadius',
             alias='RectangularVerticalDistanceOfHolesFromCenter'),
        Cell('4',
             alias='CoilWinderNumberOfSpacingNuts')
    ],
    [
        Cell('CoilWinderNutStackThickness'),
        Cell('CoilWinderAssemblyThickness'),
        Cell('CoilWinderSpaceBetweenLayer')
    ],
    [
        Cell('=HexNutThickness * CoilWinderNumberOfSpacingNuts',
             alias='CoilWinderNutStackThickness'),
        Cell('=CoilWinderCheekThickness * 2 + StatorThickness',
             alias='CoilWinderAssemblyThickness'),
        Cell('=CoilWinderNutStackThickness + CoilWinderAssemblyThickness',
             alias='CoilWinderSpaceBetweenLayer')
    ],
    [
        Cell('CoilWinderNumberOfNutStacks'),
        Cell('CoilWinderAssemblyThicknessTotal'),
        Cell('CoilWinderCenterRodLength')
    ],
    [
        Cell('=NumberOfCoilsPerPhase - 1',
             alias='CoilWinderNumberOfNutStacks'),
        Cell('=CoilWinderAssemblyThickness * NumberOfCoilsPerPhase + CoilWinderNutStackThickness * CoilWinderNumberOfNutStacks',
             alias='CoilWinderAssemblyThicknessTotal'),
        Cell('=CoilWinderAssemblyThicknessTotal + HexNutThickness * 2 + DistanceThreadsExtendFromNuts * 2',
             alias='CoilWinderCenterRodLength')
    ],
    [
        Cell('CoilWinderPinLength'),
    ],
    [
        Cell('=CoilWinderAssemblyThicknessTotal + DistanceThreadsExtendFromNuts * 2',
             alias='CoilWinderPinLength')
    ],
    [
        Cell('ShouldRotateCoilWinderParts'),
        Cell('CoilWinderAngle'),
        Cell('CoilWinderPinsMirrorNormalVector')
    ],
    [
        # Equivalent to AND boolean logic.
        # https://forum.freecad.org/viewtopic.php?p=690156#p690156
        Cell('=MagnetWidth > MagnetLength ? (CoilType != 3 ? 1 : 0) : 0',
             alias='ShouldRotateCoilWinderParts'),
        # Rotate coil, pins, and spacer 90 deg if magnet width is greater than length.
        Cell('=ShouldRotateCoilWinderParts == 1 ? 90 : 0',
             alias='CoilWinderAngle'),
        Cell('=ShouldRotateCoilWinderParts == 1 ? vector(0; 1; 0) : vector(1; 0; 0)',
             alias='CoilWinderPinsMirrorNormalVector')
    ],
    [
        Cell('LargestMagnetDimension')
    ],
    [
        Cell('=max(MagnetLength; MagnetWidth)',
             alias='LargestMagnetDimension')
    ],
    [
        Cell('OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('InnerHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('RectangularLargestDistanceOfHolesFromCenter')
    ],
    [
        Cell('=CoilInnerWidth1 - CoilWinderDiskSmallHoleDiameter',
             alias='OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('=CoilType != 3 ? (CoilInnerWidth2 - CoilWinderDiskSmallHoleDiameter) : OuterHorizontalDistanceBetweenCenterOfSmallHoles',
             alias='InnerHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('=LargestMagnetDimension / 2 - CoilWinderDiskSmallHoleRadius',
             alias='RectangularLargestDistanceOfHolesFromCenter'),
    ],
    [
        Cell('RotorDiskCircumference'),
        Cell('CoilSectorArcLength'),
        Cell('CoilOuterWidthArcLength')
    ],
    [
        Cell('=RotorDiskRadius * 2 * pi',
             alias='RotorDiskCircumference'),
        Cell('=RotorDiskCircumference / NumberOfCoils',
             alias='CoilSectorArcLength'),
        Cell('=asin(CoilInnerWidth1 / (2 * RotorDiskRadius)) * 2 * RotorDiskRadius * pi / 180',
             alias='CoilOuterWidthArcLength')
    ],
    [
        Cell('ApproximateCoilArcLength'),
        Cell('CoilLegWidthReduction'),
        Cell('CoilLegWidthReduced')
    ],
    [
        Cell('=CoilOuterWidthArcLength.Value + CoilLegWidth * 2',
             alias='ApproximateCoilArcLength'),
        Cell('=(ApproximateCoilArcLength - CoilSectorArcLength) / 2',
             alias='CoilLegWidthReduction'),
        # Ensure CoilLegWidthReduced is less than CoilLegWidth to prevent model from breaking when NOT H Shape 4F
        Cell('=CoilLegWidthReduction < 0 ? ' +
             'CoilLegWidth * 0.8 : ' +
             'CoilLegWidth - CoilLegWidthReduction',
             alias='CoilLegWidthReduced'),
    ],
    [
        Cell('DoCoilsOverlap')
    ],
    [
        Cell('=ApproximateCoilArcLength > CoilSectorArcLength ? 1 : 0',
             alias='DoCoilsOverlap')
    ],
    [
        # Setup short aliases for making complex equation more readable
        Cell('Mw'),  # Magnet width
        Cell('Ml'),  # Magnet length
        Cell('Pr')  # Pin radius
    ],
    [
        # Set to MagnetLength when rectanuglar or keyhole coil type to prevent
        # Stator_Coil_Triangular_Reduced & Stator_CoilWinder_Triangular_Spacer
        # from breaking.
        Cell('=CoilType != 3 ? MagnetLength : MagnetWidth',
             alias='Mw'),
        Cell('=MagnetLength',
             alias='Ml'),
        Cell('=CoilWinderDiskSmallHoleRadius',
             alias='Pr')
    ],
    [
        Cell('TriangularHorizontalDistanceBetweenPins'),
        Cell('TriangularCoilWinderCircumradius'),
        Cell('TriangularVerticalDistanceOfHolesFromCenter')
    ],
    [
        Cell('=Mw - CoilWinderDiskSmallHoleRadius * 2',
             alias='TriangularHorizontalDistanceBetweenPins'),
        # References:
        # https://math.stackexchange.com/a/4905815/1315686
        # https://www.wolframalpha.com/input?i=%28R+-+r%29%5E2+%3D+%28l+-+r+-+R%29%5E2+%2B+%28%28w-2r%29+%2F+2%29%5E2+solve+for+R
        Cell('=(4 * Ml ^ 2 - 8 * Ml * Pr + (Mw - 2 * Pr) ^ 2) / (8 * (Ml - 2 * Pr))',
             alias='TriangularCoilWinderCircumradius'),
        Cell('=Ml - Pr - TriangularCoilWinderCircumradius',
             alias='TriangularVerticalDistanceOfHolesFromCenter')
    ],
    [
        Cell('Rotor', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('RotorThickness'),
        Cell('JackingHoleDiameter'),
        # Switch to reduced weight rotor disks when RotorDiskRadius
        # exceeds this threshold.
        Cell('WeightReductionRotorDiskRadiusThreshold')
    ],
    [
        Cell('=MagnetThickness + RotorDiskThickness',
             alias='RotorThickness'),
        Cell('10',
             alias='JackingHoleDiameter'),
        Cell('230',
             alias='WeightReductionRotorDiskRadiusThreshold')
    ],
    [
        # Radius of the wooden island when casting the magnets of the rotor in resin
        # Effectively the radius of the inner hole of the rotor resin cast.
        # See "The magnet rotor mould" section on page 41 of "A Wind Turbine Recipe Book (2014)".
        Cell('SmallIslandRadius'),
        Cell('LargeIslandRadius'),
        Cell('IslandRadius')
    ],
    [
        Cell('=HubPitchCircleRadius + 0.5 * (RotorDiskRadius - MagnetLength - HubPitchCircleRadius)',
             alias='SmallIslandRadius'),
        # TODO: Duplicated with below InnerCircleResineRotor
        Cell('=RotorDiskRadius - MagnetLength - 25',
             alias='LargeIslandRadius'),
        Cell('=RotorDiskRadius < 187.5 ? SmallIslandRadius : LargeIslandRadius',
             alias='IslandRadius')
    ],
    [
        Cell('OffsetToAlignCornersOfMagnetToDisk'),
        Cell('DistanceOfMagnetFromCenter')
    ],
    [
        Cell('=RotorDiskRadius - sqrt(RotorDiskRadius ^ 2 - (MagnetWidth / 2) ^ 2)',
             alias='OffsetToAlignCornersOfMagnetToDisk'),
        Cell('=RotorDiskRadius - MagnetLength - OffsetToAlignCornersOfMagnetToDisk',
             alias='DistanceOfMagnetFromCenter')
    ],
    [
        Cell('Reduced Weight', styles=[Style.UNDERLINE])
    ],
    [
        Cell('InnerCircleResineRotor'),
        Cell('PaddingBetweenEdgeOfOuterPocketAndResin')
    ],
    [
        # TODO: Duplicated with above LargeIslandRadius
        Cell('=RotorDiskRadius - MagnetLength - 25',
             alias='InnerCircleResineRotor'),
        Cell('12',
             alias='PaddingBetweenEdgeOfOuterPocketAndResin'),
    ],
    [
        Cell('PocketInnerRadius'),
        Cell('PocketOuterRadius')
    ],
    [
        Cell('=HubPitchCircleRadius + 3 * HubHolesRadius',
             alias='PocketInnerRadius'),
        Cell('=InnerCircleResineRotor - PaddingBetweenEdgeOfOuterPocketAndResin',
             alias='PocketOuterRadius')
    ],
    [
        Cell('NumberOfPockets'),
        Cell('WidthInnerPocket'),
        Cell('WidthOuterPocket')
    ],
    [
        Cell('6',
             alias='NumberOfPockets'),
        Cell('=2 * pi * PocketInnerRadius / (NumberOfPockets * 2)',
             alias='WidthInnerPocket'),
        Cell('=2 * pi * PocketOuterRadius / (NumberOfPockets * 2)',
             alias='WidthOuterPocket')
    ],
    [
        Cell('Mold', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorMoldSideLength'),
        Cell('NumberOfRotorMoldScrews'),
        Cell('PercentageOfMagnetThicknessCoveredByResin')
    ],
    [
        Cell('=RotorDiskRadius * 2 * 1.3333',
             alias='RotorMoldSideLength'),
        Cell('16',
             alias='NumberOfRotorMoldScrews'),
        Cell('=MagnetMaterial == <<Ferrite>> ? 0.7 : 1.0',
             alias='PercentageOfMagnetThicknessCoveredByResin')
    ],
    [
        Cell('RotorMoldBaseThickness'),
        Cell('RotorMoldLidThickness'),
        Cell('RotorMoldIslandThickness'),

    ],
    [
        Cell('15',
             alias='RotorMoldBaseThickness'),
        Cell('6',
             alias='RotorMoldLidThickness'),
        Cell('=ceil(MagnetThickness * PercentageOfMagnetThicknessCoveredByResin)',
             alias='RotorMoldIslandThickness'),
    ],
    [
        Cell('RotorMoldSurroundThickness'),
        Cell('RotorMoldSurroundRadius')
    ],
    [
        Cell('=RotorDiskThickness + RotorMoldIslandThickness',
             alias='RotorMoldSurroundThickness'),
        Cell('=RotorDiskRadius + RotorResinMargin',
             alias='RotorMoldSurroundRadius')
    ],
    [
        Cell('UnroundedRotorMoldScrewLength'),
        Cell('RotorMoldScrewLength')
    ],
    [
        Cell('=RotorMoldSurroundThickness + RotorMoldBaseThickness',
             alias='UnroundedRotorMoldScrewLength'),
        Cell('=UnroundedRotorMoldScrewLength + - mod(UnroundedRotorMoldScrewLength; 5)',
             alias='RotorMoldScrewLength')
    ],
    [
        Cell('DistanceBetweenRotorMoldScrewsAndResin'),
        Cell('RotorMoldScrewHolesCircumradius'),
        Cell('NumberOfRotorMoldBolts')
    ],
    [
        Cell('22',
             alias='DistanceBetweenRotorMoldScrewsAndResin'),
        Cell('=RotorMoldSurroundRadius + DistanceBetweenRotorMoldScrewsAndResin',
             alias='RotorMoldScrewHolesCircumradius'),
        Cell('=RotorDiskRadius < 187.5 ? NumberOfHoles / 2 : NumberOfHoles',
             alias='NumberOfRotorMoldBolts')
    ],
    [
        Cell('MagnetJig', styles=[Style.UNDERLINE])
    ],
    [
        Cell('MagnetJigThickness')
    ],
    [
        Cell('6',
             alias='MagnetJigThickness')
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('StatorMountingStudsLength'),
        Cell('HubStudsLength')
    ],
    [
        Cell('=DistanceThreadsExtendFromNuts * 2 + MetalThicknessL + HexNutThickness * 2 + DistanceBetweenFrameAndBackRotor + RotorThickness + MechanicalClearance + StatorThickness + WasherThickness',
             alias='StatorMountingStudsLength'),
        Cell('=DistanceThreadsExtendFromNuts * 2 + HubHexNutThickness * 3 + MiddlePadThickness + RotorThickness * 2 + MechanicalClearance * 2 + StatorThickness + BladeAssemblyPlateThickness * 2 + WasherThickness * 2 + BladeThickness',
             alias='HubStudsLength')
    ],
    [
        Cell('Rotor Mounting Studs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('DistanceBetweenRotorDisks'),
        Cell('NumberOfNutsBetweenRotorDisks'),
        Cell('NumberOfWashersBetweenRotorDisks')
    ],
    [
        Cell('=MagnetThickness * 2 + MechanicalClearance * 2 + StatorThickness',
             alias='DistanceBetweenRotorDisks'),
        Cell('=floor(DistanceBetweenRotorDisks / HubHexNutThickness)',
             alias='NumberOfNutsBetweenRotorDisks'),
        Cell('=floor(DistanceBetweenRotorDisks % HubHexNutThickness / WasherThickness)',
             alias='NumberOfWashersBetweenRotorDisks')
    ],
    [
        Cell('Frame', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('DistanceBetweenCenterOfHoleAndFrameEdge'),
        Cell('HolesRadius'),
        Cell('YawPipeRadius')
    ],
    [
        Cell('=MetalLengthL / 2',
             alias='DistanceBetweenCenterOfHoleAndFrameEdge'),
        Cell('=HolesDiameter / 2',
             alias='HolesRadius'),
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius')
    ],
    [
        Cell('T Shape', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X'),
        Cell('TShapeTwoHoleEndBracketLength (A)')
    ],
    [
        # Based on right triangle forming with center of hub and hole of two hole end bracket.
        Cell('=cos(60) * StatorHolesCircumradius - DistanceBetweenCenterOfHoleAndFrameEdge',
             alias='X'),
        # 30 degrees because 360 / 3 = 120 - 90 = 30.
        # Divide by 3 for because the T Shape has 3 holes.
        # cos(30) * StatorHolesCircumradius = bottom of right triangle
        # * 2 to get both sides.
        # Add the distance between hole and edge of the metal on each side, + DistanceBetweenCenterOfHoleAndFrameEdge * 2.
        Cell('=cos(30) * StatorHolesCircumradius * 2 + DistanceBetweenCenterOfHoleAndFrameEdge * 2',
             alias='TShapeTwoHoleEndBracketLength')
    ],
    [
        # Total vertical distance of T Shape from bottom hole to two top holes.
        # This is the opposite, or vertical left side of the right triangle plus,
        # the stator resin cast radius.
        Cell('TShapeVerticalDistance'),
        Cell('BC'),
        Cell('D')
    ],
    [
        Cell('=(sin(30) * StatorHolesCircumradius) + StatorHolesCircumradius',
             alias='TShapeVerticalDistance'),
        # Subtract MetalLengthL as the top holes and bottom hole are centered in the brackets.
        # MetalLengthL is the length of the brackets.
        Cell('=TShapeVerticalDistance - MetalLengthL',
             alias='BC'),
        Cell('=MetalLengthL * 2',
             alias='D')
    ],
    [
        Cell('Yaw Bearing to Frame Junction (T Shape)',
             styles=[Style.UNDERLINE])
    ],
    [
        Cell('I'), Cell('=max(Offset - (YawPipeRadius + MetalThicknessL + X); 0)',
                        alias='I')
    ],
    [
        Cell('j'), Cell('=0.32 * RotorDiskRadius - 3',
                        alias='j')
    ],
    [
        Cell('k'), Cell('=0.2 * RotorDiskRadius - 5',
                        alias='k')
    ],
    [
        Cell('H Shape', styles=[Style.UNDERLINE])
    ],
    [
        Cell('CentralAngle'), Cell('Theta'), Cell('Inradius')
    ],
    [
        Cell('=360 / 4',
             alias='CentralAngle'),
        Cell('=CentralAngle / 2',
             alias='Theta'),
        Cell('=cos(Theta) * StatorHolesCircumradius',
             alias='Inradius')
    ],
    [
        Cell('IsoscelesRightTriangleHypotenuseRatio'),
        Cell('DistanceBetweenCenterOfHShapeFrameHoles')
    ],
    [
        Cell('=1 / cos(Theta)',
             alias='IsoscelesRightTriangleHypotenuseRatio'),
        # Since the H Shape frame is square, the distance between frame holes
        # is the same regardless of horizontal or vertical orientation.
        Cell('=StatorHolesCircumradius * IsoscelesRightTriangleHypotenuseRatio',
             alias='DistanceBetweenCenterOfHShapeFrameHoles')
    ],
    [
        # G and H are reserved aliases since FreeCAD 20.
        Cell('GG'), Cell('HH')
    ],
    [
        Cell('=DistanceBetweenCenterOfHShapeFrameHoles + DistanceBetweenCenterOfHoleAndFrameEdge * 2',
             alias='GG'),
        # To make the frame square.
        Cell('=Inradius * 2 - MetalLengthL',
             alias='HH')
    ],
    [
        Cell('Star Shape', styles=[Style.UNDERLINE])
    ],
    [
        Cell('StarShapeTwoHoleEndBracketLength (A)'),
        Cell('B'),
        # C is a reserved alias since FreeCAD 20.
        Cell('CC')
    ],
    [
        Cell('=2 * sin(30) * StatorHolesCircumradius + DistanceBetweenCenterOfHoleAndFrameEdge * 2',
             alias='StarShapeTwoHoleEndBracketLength'),
        Cell('=2 * StatorHolesCircumradius * ((1 - sin(30) * sin(30))^0.5) - MetalLengthL',
             alias='B'),
        Cell('=StatorHolesCircumradius - MetalLengthL + DistanceBetweenCenterOfHoleAndFrameEdge',
             alias='CC')
    ],
    [
        Cell('FrameLink', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Y',
             horizontal_alignment=Alignment.RIGHT),
        Cell('Z',
             horizontal_alignment=Alignment.RIGHT)
    ],
    [
        Cell('0',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameX'),
        Cell('0',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameY'),
        Cell('=StatorThickness / 2 + MechanicalClearance + RotorThickness + DistanceBetweenFrameAndBackRotor + MetalLengthL',
             horizontal_alignment=Alignment.RIGHT,
             alias='FrameZ')
    ],
    [
        Cell('Alternator', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    # Euler Angles
    [
        Cell('Euler Angles', styles=[Style.UNDERLINE]),
        Cell('Rotation order is Z, Y, X')
    ],
    [
        Cell('Z'), Cell('Y'), Cell('X')
    ],
    [
        Cell('=RotorDiskRadius < 187.5 ? -90 : -180', alias='AlternatorZ'),
        Cell('=RotorDiskRadius < 187.5 ? 0 : 90', alias='AlternatorY'),
        Cell('=RotorDiskRadius < 187.5 ? 90 : 0', alias='AlternatorX')
    ],
    [
        Cell('AlternatorRotation'),
        Cell('AlternatorBase'),
        Cell('AlternatorPlacement')
    ],
    [
        Cell('=rotation(AlternatorZ; AlternatorY; AlternatorX)',
             alias='AlternatorRotation'),
        Cell('=vector(0; 0; 0)',
             alias='AlternatorBase'),
        Cell('=placement(AlternatorBase; AlternatorRotation)',
             alias='AlternatorPlacement')
    ]
]
