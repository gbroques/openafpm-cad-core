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
        Cell('DiskThickness'),
        Cell('MagnetThickness'),
        Cell('MagnetLength')
    ],
    [
        Cell('=Spreadsheet.DiskThickness',
             alias='DiskThickness'),
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
        Cell('ResineRotorMargin')
    ],
    [
        Cell('=Spreadsheet.ResineRotorMargin',
             alias='ResineRotorMargin')
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
        Cell('HubPitchCircleRadius')
    ],
    [
        Cell('=Hub.HubPitchCircleRadius',
             alias='HubPitchCircleRadius')
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
        Cell('StatorInnerHoleRadius')
    ],
    [
        Cell('=(RotorDiskRadius + CoilLegWidth + 20) / cos(30)',
             alias='HexagonalStatorOuterCircumradius'),
        Cell('=RotorDiskRadius - MagnetLength - CoilLegWidth - OffsetToAlignCornersOfMagnetToDisk',
             alias='StatorInnerHoleRadius')
    ],
    [
        # "Holes circumradius" is the radius of the circle that
        # goes through the mounting holes of the stator.
        # This is used in the Frame later to ensure
        # the Frame holes and Stator holes align.
        Cell('CircularStatorHolesCircumradius'),
        Cell('HexagonalStatorHolesCircumradius'),
        Cell('StatorHolesCircumradius')
    ],
    [
        Cell('=RotorDiskRadius + CoilLegWidth + 20',
             alias='CircularStatorHolesCircumradius'),
        Cell('=RotorDiskRadius + CoilLegWidth + 0.5 * (HexagonalStatorOuterCircumradius - RotorDiskRadius - CoilLegWidth)',
             alias='HexagonalStatorHolesCircumradius'),
        Cell('=RotorDiskRadius < 275 ? CircularStatorHolesCircumradius : HexagonalStatorHolesCircumradius',
             alias='StatorHolesCircumradius')
    ],
    [
        Cell('TShapeNumberOfStatorHoles'),
        Cell('HShapeNumberOfStatorHoles'),
        Cell('NumberOfStatorHoles')
    ],
    [
        Cell('3',
             alias='TShapeNumberOfStatorHoles'),
        Cell('4',
             alias='HShapeNumberOfStatorHoles'),
        Cell('=RotorDiskRadius < 187.5 ? TShapeNumberOfStatorHoles : HShapeNumberOfStatorHoles',
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
        Cell('Mold', styles=[Style.UNDERLINE])
    ],
    # For metric hex bolt dimensions, see:
    # https://www.atlrod.com/metric-hex-bolt-dimensions/
    [
        Cell('StatorMoldBoltDiameter'),
        Cell('StatorMoldBoltWidthAcrossCorners')
    ],
    [
        # M12 Bolt
        Cell('12',
             alias='StatorMoldBoltDiameter'),
        Cell('20.78',  # C (MAX)
             alias='StatorMoldBoltWidthAcrossCorners')
    ],
    [
        # Controls radius of screw holes for both Stator & Rotor molds.
        # These appear to be pilot holes for a 5mm diameter screw.
        Cell('ScrewHoleRadius'),
        Cell('DistanceBetweenOuterHolesAndStatorMold'),
        Cell('DistanceBetweenInnerHolesAndStatorMold')
    ],
    [
        Cell('2',
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
        Cell('DistanceOfLocatingHoleFromCenter'),
        Cell('StatorMoldScrewLength')
    ],
    [
        Cell('=(StatorMoldIslandNumberOfScrewSectors - StatorMoldIslandNumberOfBolts) / 2',
             alias='StatorMoldIslandNumberOfScrews'),
        Cell('=0.63559 * StatorMoldSideLength',
             alias='DistanceOfLocatingHoleFromCenter'),
        Cell('=StatorThickness * 2',
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
        Cell('10',
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
        Cell('VerticalOffset'),
        Cell('TriangularCoilHoleHeight')
    ],
    [
        Cell('=CoilWinderAssemblyThicknessTotal + DistanceThreadsExtendFromNuts * 2',
             alias='CoilWinderPinLength'),
        Cell('=CoilWinderDiskSmallHoleRadius * cos(60)',
             alias='VerticalOffset'),
        Cell('=MagnetLength - VerticalOffset',
             alias='TriangularCoilHoleHeight')
    ],
    [
        Cell('OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('InnerHorizontalDistanceBetweenCenterOfSmallHoles')
    ],
    [
        Cell('=CoilInnerWidth1 - CoilWinderDiskSmallHoleDiameter',
             alias='OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('=CoilType != 3 ? (CoilInnerWidth2 - CoilWinderDiskSmallHoleDiameter) : OuterHorizontalDistanceBetweenCenterOfSmallHoles',
             alias='InnerHorizontalDistanceBetweenCenterOfSmallHoles')
    ],
    [
        Cell('Rotor', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('RotorDiskThickness'),
        Cell('JackingHoleDiameter')
    ],
    [
        Cell('=MagnetThickness + DiskThickness',
             alias='RotorDiskThickness'),
        Cell('10',
             alias='JackingHoleDiameter')
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
        Cell('RotorMoldSurroundThickness')
    ],
    [
        Cell('15',
             alias='RotorMoldBaseThickness'),
        Cell('6',
             alias='RotorMoldLidThickness'),
        Cell('=DiskThickness + ceil(MagnetThickness * PercentageOfMagnetThicknessCoveredByResin)',
             alias='RotorMoldSurroundThickness')
    ],
    [
        Cell('RotorMoldIslandThickness'),
        Cell('RotorMoldScrewLength'),
        Cell('RotorMoldSurroundRadius')
    ],
    [
        Cell('=RotorMoldSurroundThickness - DiskThickness',
             alias='RotorMoldIslandThickness'),
        Cell('=RotorMoldSurroundThickness + RotorMoldBaseThickness',
             alias='RotorMoldScrewLength'),
        Cell('=RotorDiskRadius + ResineRotorMargin',
             alias='RotorMoldSurroundRadius')
    ],
    [
        Cell('DistanceBetweenRotorMoldScrewsAndResin'),
        Cell('RotorMoldScrewHolesCircumradius'),
        Cell('NumberOfRotorMoldBolts')
    ],
    [
        Cell('22',
             alias='DistanceBetweenRotorMoldScrewsAndResin'),
        Cell('=RotorDiskRadius + ResineRotorMargin + DistanceBetweenRotorMoldScrewsAndResin',
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
        Cell('StatorMountingStudsLength')
    ],
    [
        Cell('=DistanceThreadsExtendFromNuts * 2 + MetalThicknessL + HexNutThickness * 2 + DistanceBetweenFrameAndBackRotor + RotorDiskThickness + MechanicalClearance + StatorThickness + WasherThickness',
             alias='StatorMountingStudsLength')
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
    # Yaw Bearing to Frame Junction (T Shape)
    # ---------------------------------------
    [
        Cell('Yaw Bearing to Frame Junction (T Shape)',
             styles=[Style.UNDERLINE, Style.BOLD])
    ],
    # The formula for I comes from solving a system of equations for I as a function of RotorDiskRadius.
    # The function should produce the following outputs, where f(RotorDiskRadius) = I:
    # * RotorDiskRadius = 125, I = 9
    # * RotorDiskRadius = 150, I = 24
    # * RotorDiskRadius = 175, I = 32
    # See A Wind Turbine Recipe Book (2014 edition), page 28.
    # Alternator Frame to Yaw Tube Sizes mm table for recommended values of I.
    # WolframAlpha was used to solve this system of equations automatically.
    #   See: https://www.wolframalpha.com/input/?i=systems+of+equations+calculator&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation1%22%7D+-%3E%22125+%3D+a*%289%5E2%29+%2B+b*9+%2B+c%22&assumption=%22FSelect%22+-%3E+%7B%7B%22SolveSystemOf3EquationsCalculator%22%7D%7D&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation2%22%7D+-%3E%22150+%3D+a*%2824%5E2%29+%2B+b*24+%2B+c%22&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation3%22%7D+-%3E%22175+%3D+a*%2832%5E2%29+%2B+b*32+%2B+c%22
    # We contrain the system of equations to produce a horizontal parabola opening right,
    # in order to avoid negative numbers that break the model when RotorDiskRadius is large.
    # The general form of a horizontal parabola opening right, where x is RotorDiskRadius and y is I:
    #   x = a*(y^2) + b*y + c
    #
    #   125 = a*(9^2) + b*9 + c
    #   150 = a*(24^2) + b*24 + c
    #   175 = a*(32^2) + b*32 +
    #
    # Solving for a, b, and c:
    #   a = 32/552
    #   b = -(235/552)
    #   c = 2845/23
    # Then we use WolframAlpha to solve "x = (35/552)*y^2 + (-235/552)*y + 2845/23 in terms of y"
    #   See: https://www.wolframalpha.com/input/?i=x+%3D+%2835%2F552%29*y%5E2+%2B+%28-235%2F552%29*y+%2B+2845%2F23+in+terms+of+y
    # This results in two equations, and we choose the positive half of the parabola as negative values break the model:
    #   y = 1 / 70 * (sqrt(77280 * x - 9503975) + 235)
    [
        Cell('ParabolicEquationForI'), Cell('=1 / 70 * (sqrt(77280 * RotorDiskRadius - 9503975) + 235)',
                                            alias='ParabolicEquationForI'),
    ],
    # Find the vertex of the above parabola:
    #   See: https://www.wolframalpha.com/input/?i=x+%3D+%2835%2F552%29*y%5E2+%2B+%28-235%2F552%29*y+%2B+2845%2F23+find+vertex
    # (x, y) = (1900795/15456, 47/14)
    # Then solve for y = m * x + b, where b is 0 (since we want this to cross the y-axis at 0).
    # (47/14) = m * (1900795/15456) + 0
    # m = (51888/1900795)
    #   See: https://www.wolframalpha.com/input/?i=%2847%2F14%29+%3D+m+*+%281900795%2F15456%29,
    [
        Cell('LinearEquationForI'), Cell('=RotorDiskRadius * (51888/1900795)',
                                         alias='LinearEquationForI'),
    ],
    # If x is less than the vertex of the parabola,
    # then we choose a linear equation that crosses through
    # the vertex of the parabola and the origin (0, 0).
    # This ensures I is always a positive value, for any positive value of RotorDiskRadius.
    [
        Cell('I'), Cell('=RotorDiskRadius < (1900795/15456) ? LinearEquationForI : ParabolicEquationForI',
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
        Cell('Frame', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        # Distance from hole to outside edge of frame.
        Cell('HoleMargin'),
        Cell('HolesRadius')
    ],
    [
        Cell('20',
             alias='HoleMargin'),
        Cell('=HolesDiameter / 2',
             alias='HolesRadius')
    ],
    [
        Cell('YawPipeRadius')
    ],
    [
        Cell('=YawPipeDiameter / 2',
             alias='YawPipeRadius')
    ],
    [
        Cell('T Shape', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X'), Cell('TShapeTwoHoleEndBracketLength (A)')
    ],
    [
        Cell('=Offset - (I + YawPipeRadius + MetalThicknessL)',
             alias='X'),
        # 30 degrees because 360 / 3 = 120 - 90 = 30.
        # Divide by 3 for because the T Shape has 3 holes.
        # cos(30) * StatorHolesCircumradius = bottom of right triangle
        # * 2 to get both sides.
        # Add the distance from hole to edge of the metal on each side, + (HoleMargin * 2).
        # Add the radius for holes on each side, + HolesDiameter.
        Cell('=cos(30) * StatorHolesCircumradius * 2 + (HoleMargin * 2) + HolesDiameter',
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
        Cell('=TShapeVerticalDistance - MetalLengthL - MetalThicknessL',
             alias='BC'),
        Cell('=MetalLengthL * 2',
             alias='D')
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
        Cell('HorizontalDistanceBetweenHoles')
    ],
    [
        Cell('=1 / cos(Theta)',
             alias='IsoscelesRightTriangleHypotenuseRatio'),
        Cell('=StatorHolesCircumradius * IsoscelesRightTriangleHypotenuseRatio',
             alias='HorizontalDistanceBetweenHoles')
    ],
    [
        # G and H are reserved aliases since FreeCAD 20.
        Cell('GG'), Cell('HH')
    ],
    [
        Cell('=HorizontalDistanceBetweenHoles + HoleMargin * 2',
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
        # 25 is the margin from the holes to the edge of the metal.
        Cell('=2 * sin(30) * StatorHolesCircumradius + 2 * (25 + HolesRadius)',
             alias='StarShapeTwoHoleEndBracketLength'),
        Cell('=2 * StatorHolesCircumradius * ((1 - sin(30) * sin(30))^0.5) - MetalLengthL',
             alias='B'),
        Cell('=StatorHolesCircumradius - MetalLengthL + HolesRadius + 25',
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
        Cell('=StatorThickness / 2 + MechanicalClearance + RotorDiskThickness + DistanceBetweenFrameAndBackRotor + MetalLengthL',
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
        Cell('=create(<<rotation>>; AlternatorZ; AlternatorY; AlternatorX)',
             alias='AlternatorRotation'),
        Cell('=create(<<vector>>; 0; 0; 0)',
             alias='AlternatorBase'),
        Cell('=create(<<placement>>; AlternatorBase; AlternatorRotation)',
             alias='AlternatorPlacement')
    ]
]
