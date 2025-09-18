from typing import List

from .spreadsheet import Alignment, Cell, Style
from .create_placement_cells import create_placement_cells

__all__ = ['alternator_cells']


def generate_tape_notch_width_cells(n: int) -> List[List[Cell]]:
    cells: List[List[Cell]] = []
    i = n
    while i >= 0:
        true = f'MaximumCoilWinderDiskTapeNotchWidth - {i + 1}' if i == n else f'TnwRange{i + 1}'
        cells.append(
            [
                Cell(f'TnwRange{i}'),
                Cell('=(CoilWinderVerticalDimension - 2 * CoilWinderPinDiameter' +
                     f' - MaximumCoilWinderDiskTapeNotchWidth + {i}) / 2' +
                     f' < MinimumSpaceBetweenPinsAndTapeNotch ? {true} : MaximumCoilWinderDiskTapeNotchWidth - {i}',
                     alias=f'TnwRange{i}')
            ]
        )
        i = i - 1
    return cells


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
        Cell('NumberMagnet'),
        Cell('HubHolesDiameter')
    ],
    [
        Cell('=Spreadsheet.RotorResinMargin',
             alias='RotorResinMargin'),
        Cell('=Spreadsheet.NumberMagnet',
             alias='NumberMagnet'),
        Cell('=Spreadsheet.HubHolesDiameter',
             alias='HubHolesDiameter')
    ],
    [
        Cell('CoilHoleWidthAtOuterRadius'),
        Cell('CoilHoleWidthAtInnerRadius'),
        Cell('CoilType'),
    ],
    [
        Cell('=Spreadsheet.CoilHoleWidthAtOuterRadius',
             alias='CoilHoleWidthAtOuterRadius'),
        Cell('=Spreadsheet.CoilHoleWidthAtInnerRadius',
             alias='CoilHoleWidthAtInnerRadius'),
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
        Cell('RotorTopology'),
        Cell('WindTurbineShape')
    ],
    [
        Cell('=Spreadsheet.RotorTopology',
             alias='RotorTopology'),
        Cell('=Spreadsheet.WindTurbineShape',
             alias='WindTurbineShape')
    ],
    [
        Cell('Hub', styles=[Style.UNDERLINE])
        # -----------------------------------
    ],
    [
        Cell('DistanceBetweenFrameAndMiddlePad'),
        Cell('NumberOfHoles'),
        Cell('HubHolesRadius')
    ],
    [
        Cell('=Hub.DistanceBetweenFrameAndMiddlePad',
             alias='DistanceBetweenFrameAndMiddlePad'),
        Cell('=Hub.NumberOfHoles',
             alias='NumberOfHoles'),
        Cell('=Hub.HubHolesRadius',
             alias='HubHolesRadius')
    ],
    [
        Cell('HubPitchCircleRadius'),
        Cell('MiddlePadThickness'),
        Cell('RotorThickness')
    ],
    [
        Cell('=Hub.HubPitchCircleRadius',
             alias='HubPitchCircleRadius'),
        Cell('=Hub.MiddlePadThickness',
             alias='MiddlePadThickness'),
        Cell('=Hub.RotorThickness',
             alias='RotorThickness')
    ],
    [
        Cell('DistanceBetweenStatorAndFrame')
    ],
    [
        Cell('=Hub.DistanceBetweenStatorAndFrame',
             alias='DistanceBetweenStatorAndFrame')
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
        Cell('WoodScrewDiameter'),
        Cell('ScrewHoleDiameter')
    ],
    [
        Cell('=Fastener.WoodScrewDiameter',
             alias='WoodScrewDiameter'),
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
        # Radius of the inner-most hole of stator.
        Cell('StatorInnerHoleRadius'),
        Cell('NumberOfCoils'),
        Cell('CoilAngle')
    ],
    [
        # TODO: RotorDiskRadius - MagnetLength - OffsetToAlignCornersOfMagnetToDisk is equal to
        #       DistanceOfMagnetFromCenter which should be equal to RotorDiskInnerRadius
        Cell('=RotorDiskRadius - MagnetLength - OffsetToAlignCornersOfMagnetToDisk - CoilLegWidth',
             alias='StatorInnerHoleRadius'),
        Cell('=NumberMagnet * 0.75',
             alias='NumberOfCoils'),
        Cell('=360deg / NumberOfCoils',
             alias='CoilAngle')
    ],
    [
        Cell('TShapeApproximateDegreesBetweenTopLeftStatorMountingHoleAndLidNotch'),
        Cell('TShapeNumberOfCoilsBetweenTopLeftStatorMountingHoleAndLidNotch'),
        Cell('TShapeDegreesBetweenTopLeftStatorMountingHoleAndLidNotch')
    ],
    [
        Cell('=45deg',
             alias='TShapeApproximateDegreesBetweenTopLeftStatorMountingHoleAndLidNotch'),
        Cell('=round(TShapeApproximateDegreesBetweenTopLeftStatorMountingHoleAndLidNotch / CoilAngle)',
             alias='TShapeNumberOfCoilsBetweenTopLeftStatorMountingHoleAndLidNotch'),
        Cell('=CoilAngle * TShapeNumberOfCoilsBetweenTopLeftStatorMountingHoleAndLidNotch',
             alias='TShapeDegreesBetweenTopLeftStatorMountingHoleAndLidNotch')
    ],
    [
        Cell('StarShapeLidNotchApproximateDegrees'),
        Cell('StarShapeNumberOfCoilsBetween180'),
        Cell('StarShapeDegreesBetween180')
    ],
    [
        Cell('=30deg',
             alias='StarShapeLidNotchApproximateDegrees'),
        Cell('=round(StarShapeLidNotchApproximateDegrees / CoilAngle - 0.5) + 0.5',
             alias='StarShapeNumberOfCoilsBetween180'),
        Cell('=CoilAngle * StarShapeNumberOfCoilsBetween180',
             alias='StarShapeDegreesBetween180')
    ],
    [
        Cell('TShapeLidNotchDegrees'),
        Cell('HShapeLidNotchDegrees'),
        Cell('StarShapeLidNotchDegrees')
    ],
    [
        # 150° to stator mounting hole in quadrant II.
        Cell('=150deg + TShapeDegreesBetweenTopLeftStatorMountingHoleAndLidNotch',
             alias='TShapeLidNotchDegrees'),
        # Assume coil is aligned with 180° for H and Star shape.
        Cell('=180deg + CoilAngle / 2',
             alias='HShapeLidNotchDegrees'),
        # Assume coil is aligned with 180° for H and Star shape.
        Cell('=180deg + StarShapeDegreesBetween180',
             alias='StarShapeLidNotchDegrees')
    ],
    [
        Cell('LidNotchDegrees'),
        # Radius of electrical conduit, a tube used to protect and route the wires for the stator coils.
        Cell('WireTubeDiameter'),
        Cell('RadiusOfResinAroundWireTube')
    ],
    [
        Cell('=WindTurbineShape == <<T>> ? TShapeLidNotchDegrees : (WindTurbineShape == <<H>> ? HShapeLidNotchDegrees : StarShapeLidNotchDegrees)',
             alias='LidNotchDegrees'),
        Cell('16',
             alias='WireTubeDiameter'),
        Cell('5', alias='RadiusOfResinAroundWireTube')
    ],
    [
        Cell('NumberOfBoltsLidNotchIsFrom180')
    ],
    [
        Cell('=(LidNotchDegrees - 180 deg) / StatorMoldSurroundBoltAngle',
             alias='NumberOfBoltsLidNotchIsFrom180')

    ],
    [
        # For spacing between outside edge of coil and stator mold surround.
        # Needs to be large enough to fit wires and tube around coils.
        # Typically a 20mm diameter tube is used, but we assume a 16mm tube.
        Cell('MaximumSpaceBetweenCoilEdgeAndSurround'),
        Cell('OutsideCoilEdgeRadius')
    ],
    [
        Cell('=WireTubeDiameter + RadiusOfResinAroundWireTube',
             alias='SpaceBetweenCoilEdgeAndSurround'),
        Cell('=RotorDiskRadius + CoilLegWidth',
             alias='OutsideCoilEdgeRadius')
    ],
    [
        Cell('StatorMoldSurroundEdgeRadius'),
        # The radius of the circle that circumscribes the hexagon
        # of the stator resin cast for Star Shape.
        Cell('HexagonalStatorOuterCircumradius')
    ],
    [
        # Take whichever is largest, CoilLegWidth or RotorResinMargin, to avoid overlapping tube for wires with rotor.
        # 5 is the default value for RotorResinMargin.
        Cell('=RotorDiskRadius + max(CoilLegWidth; RotorResinMargin) + SpaceBetweenCoilEdgeAndSurround + (RotorResinMargin - 5)',
             alias='StatorMoldSurroundEdgeRadius'),
        Cell('=StatorMoldSurroundEdgeRadius / cos(30)',
             alias='HexagonalStatorOuterCircumradius')
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
        Cell('=StatorMoldSurroundEdgeRadius',
             alias='TShapeStatorHolesCircumradius'),
        # Ensure 20 mm between hole and coil for H Shape.
        Cell('=TShapeStatorHolesCircumradius + HolesRadius',
             alias='HShapeStatorHolesCircumradius'),
        Cell('=OutsideCoilEdgeRadius + 0.5 * (HexagonalStatorOuterCircumradius - RotorDiskRadius - CoilLegWidth)',
             alias='StarShapeStatorHolesCircumradius'),
        Cell('=WindTurbineShape == <<T>> ? TShapeStatorHolesCircumradius : (WindTurbineShape == <<H>> ? HShapeStatorHolesCircumradius : StarShapeStatorHolesCircumradius)',
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
        Cell('=WindTurbineShape == <<T>> ? TShapeNumberOfStatorHoles : ' +
             '(WindTurbineShape == <<H>> ? HShapeNumberOfStatorHoles : StarShapeNumberOfStatorHoles)',
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
        Cell('=WindTurbineShape == <<T>> ? TShapeEarSize : HShapeEarSize',
             alias='EarSize')
    ],
    [
        # CoilsAngle needed to align the stator mounting points (the holes in the resin cast)
        # with the middle of the space between two coils, and not with the center of one coil.
        # This provides more space when making the hole in the resin,
        # without having to worry about hitting a coil.
        Cell('TShapeCoilsAngle'),
        Cell('HAndStarShapeCoilsAngle'),
        Cell('CoilsAngle')
    ],
    [
        Cell('=360 / NumberOfCoils / 2',
             alias='TShapeCoilsAngle'),
        # Align H and Star Shape coils to 180° instead of 90°
        Cell('90',
             alias='HAndStarShapeCoilsAngle'),
        Cell('=WindTurbineShape == <<T>> ? TShapeCoilsAngle : HAndStarShapeCoilsAngle',
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
        Cell('MaximumStatorMoldBoltDiameter')
    ],
    [
        # M12 Bolt
        Cell('12',
             alias='MaximumStatorMoldBoltDiameter')
    ],
    [
        # Controls radius of screw holes for rotor mold and blade hub rotor plates.
        # These are pilot holes for a 5mm diameter screw.
        # TODO: Move this out of stator mold section and into a more appropriate place.
        Cell('ScrewHoleRadius'),
        Cell('MaximumDistanceBetweenOuterHolesAndStatorMold'),
        Cell('MaximumDistanceBetweenInnerHolesAndStatorMold')
    ],
    [
        Cell('=ScrewHoleDiameter / 2',
             alias='ScrewHoleRadius'),
        # Ensure holes are close enough to create
        # pressure for the resin not to flow out.
        Cell('=MaximumStatorMoldBoltDiameter * 2',
             alias='MaximumDistanceBetweenOuterHolesAndStatorMold'),
        Cell('=MaximumStatorMoldBoltDiameter * 1.5',
             alias='MaximumDistanceBetweenInnerHolesAndStatorMold')
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
        Cell('=WindTurbineShape == <<T>> ? TShapeSketchY : HShapeSketchY',
             alias='SketchY')
    ],
    [
        # TODO: Rename to StatorMoldIslandHolesCircumradius?
        Cell('IslandInnerRadius'),
        Cell('EarAngle')
    ],
    [
        Cell('=max(StatorInnerHoleRadius - MaximumDistanceBetweenInnerHolesAndStatorMold;' +
             ' StatorInnerHoleRadius * 0.78)',
             alias='IslandInnerRadius'),
        Cell('=360 / NumberOfStatorHoles',
             alias='EarAngle')
    ],
    [
        Cell('LargeHoleAngle'),
        Cell('StatorMoldHolesSketchAngle')
    ],
    [
        # Divide by 4 because there are 3 bolts and 4 spaces between each "ear"
        # for the T and H Shape Stator Mold.
        Cell('=EarAngle / 4',
             alias='LargeHoleAngle'),
        Cell('=WindTurbineShape == <<T>> ? 0 : (WindTurbineShape == <<H>> ? 45 : 0)',
             alias='StatorMoldHolesSketchAngle')
    ],
    [
        Cell('StatorMoldIslandNumberOfBolts'),
        Cell('StatorMoldIslandNumberOfScrewSectors'),
        Cell('StatorMoldIslandScrewAngle')
    ],
    [
        Cell('=StatorInnerHoleRadius < 110 ? 4 : (StatorInnerHoleRadius < 190 ? 6 : 12)',
             alias='StatorMoldIslandNumberOfBolts'),
        Cell('=StatorInnerHoleRadius < 110 ? 12 : (StatorInnerHoleRadius < 190 ? 18 : 36)',
             alias='StatorMoldIslandNumberOfScrewSectors'),
        Cell('=360deg / StatorMoldIslandNumberOfScrewSectors',
             alias='StatorMoldIslandScrewAngle'),
    ],
    [
        Cell('StatorMoldIslandNumberOfPolarPatternScrewOccurrences'),
        Cell('UnroundedStatorMoldScrewLength'),
        Cell('StatorMoldScrewLength')
    ],
    [
        Cell('=(StatorMoldIslandNumberOfScrewSectors - StatorMoldIslandNumberOfBolts) / 2',
             alias='StatorMoldIslandNumberOfPolarPatternScrewOccurrences'),
        Cell('=StatorThickness * 2',
             alias='UnroundedStatorMoldScrewLength'),
        # Round down to nearest multiple of 5
        Cell('=UnroundedStatorMoldScrewLength - mod(UnroundedStatorMoldScrewLength; 5)',
             alias='StatorMoldScrewLength')
    ],
    [
        Cell('StatorMoldSurroundNumberOfBolts'),
        Cell('StatorMoldSurroundNumberOfScrews'),
        Cell('StatorMoldIslandNumberOfScrews')
    ],
    [
        Cell('=WindTurbineShape == <<H>> ? NumberOfStatorHoles * 4 : 24',
             alias='StatorMoldSurroundNumberOfBolts'),
        Cell('=4 * 2 * NumberOfStatorHoles',
             alias='StatorMoldSurroundNumberOfScrews'),
        Cell('=2 * StatorMoldIslandNumberOfPolarPatternScrewOccurrences',
             alias='StatorMoldIslandNumberOfScrews')
    ],
    [
        Cell('StatorMoldIslandNumberOfFasteners'),
        Cell('StatorMoldIslandHolesCircumference'),
        Cell('StatorMoldIslandSpaceBetweenFasteners')
    ],
    [
        Cell('=StatorMoldIslandNumberOfBolts + StatorMoldIslandNumberOfScrews',
             alias='StatorMoldIslandNumberOfFasteners'),
        Cell('=2 * pi * IslandInnerRadius',
             alias='StatorMoldIslandHolesCircumference'),
        Cell('=StatorMoldIslandHolesCircumference / StatorMoldIslandNumberOfFasteners',
             alias='StatorMoldIslandSpaceBetweenFasteners')
    ],
    [
        Cell('ShouldDecreaseStatorMoldFastenerSizes'),
        Cell('StatorMoldBoltDiameter'),
        Cell('StatorMoldWoodScrewDiameter')
    ],
    [
        Cell('=StatorMoldIslandSpaceBetweenFasteners < 30 ? 1 : 0',
             alias='ShouldDecreaseStatorMoldFastenerSizes'),
        # Decrease from maximum M12 to M10 bolt if space between center of fasteners is less than 30
        Cell('=ShouldDecreaseStatorMoldFastenerSizes == 1 ? 10 : MaximumStatorMoldBoltDiameter',
             alias='StatorMoldBoltDiameter'),
        Cell('=ShouldDecreaseStatorMoldFastenerSizes == 1 ? 4 : WoodScrewDiameter',
             alias='StatorMoldWoodScrewDiameter')
    ],
    [
        Cell('StatorMoldScrewHoleDiameter'),
        Cell('StatorMoldScrewHoleRadius')
    ],
    [
        Cell('=StatorMoldWoodScrewDiameter == WoodScrewDiameter ? ScrewHoleDiameter : 3',
             alias='StatorMoldScrewHoleDiameter'),
        Cell('=StatorMoldScrewHoleDiameter / 2',
             alias='StatorMoldScrewHoleRadius')
    ],
    # For metric hex bolt dimensions, see:
    # https://www.atlrod.com/metric-hex-bolt-dimensions/
    [
        Cell('StatorMoldBoltWidthAcrossCorners'),
        Cell('StatorMoldHexNutThickness')
    ],
    [
        Cell('=StatorMoldBoltDiameter == 10 ? 18.48 : 20.78',  # C (MAX)
             alias='StatorMoldBoltWidthAcrossCorners'),
        # Hex nut thickness equations are derived from
        # plugging in BS 4190 Metric Hexagon Nut Black Thickness into
        # linear equation function finder.
        # http://www.worldfastener.com/bs-4190-metric-hexagon-nuts/
        # https://www.dcode.fr/function-equation-finder
        Cell('=1.64 * (StatorMoldBoltDiameter / 2) + 0.35',
             alias='StatorMoldHexNutThickness')
    ],
    [
        Cell('MinimumDistanceStatorMoldBoltsExtendFromNuts'),
        Cell('UnroundedStatorMoldBoltLength'),
        Cell('StatorMoldBoltLength')
    ],
    [
        Cell('2',
             alias='MinimumDistanceStatorMoldBoltsExtendFromNuts'),
        Cell('=4 * StatorThickness - HexNutThickness + WasherThickness +'
             ' StatorMoldHexNutThickness + MinimumDistanceStatorMoldBoltsExtendFromNuts',
             alias='UnroundedStatorMoldBoltLength'),
        # Round up to nearest multiple of 5
        Cell('=UnroundedStatorMoldBoltLength + 5 - mod(UnroundedStatorMoldBoltLength; 5)',
             alias='StatorMoldBoltLength')
    ],
    [
        Cell('LocatingBoltDiameter'),
        Cell('UnroundedLocatingBoltLength'),
        Cell('LocatingBoltLength')
    ],
    [
        Cell('=StatorMoldBoltDiameter',
             alias='LocatingBoltDiameter'),
        Cell('=WasherThickness * 2 + StatorThickness * 5 + StatorMoldHexNutThickness +' +
             ' MinimumDistanceStatorMoldBoltsExtendFromNuts',
             alias='UnroundedLocatingBoltLength'),
        Cell('=UnroundedLocatingBoltLength + 5 - mod(UnroundedLocatingBoltLength; 5)',
             alias='LocatingBoltLength')
    ],
    [
        Cell('StatorMoldSideLength'),
        Cell('DistanceOfLocatingHoleFromCenter')
    ],
    [
        Cell('=1.55 * 2 * StatorHolesCircumradius',
             alias='StatorMoldSideLength'),
        Cell('=0.63559 * StatorMoldSideLength',
             alias='DistanceOfLocatingHoleFromCenter'),
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
        Cell('StatorMoldSurroundHolesEdgeCircumradius'),
        # TODO: Similar to IslandInnerRadius -> StatorMoldIslandHolesCircumradius rename above
        # Should we rename LengthMiddleHoles to StatorMoldSurroundHolesCircumradius?
        Cell('LengthMiddleHoles'),
        Cell('DistanceBetweenOuterHolesAndStatorMold')
    ],
    [
        Cell('=WindTurbineShape == <<H>> ? StatorHolesCircumradius : HexagonalStatorOuterCircumradius',
             alias='StatorMoldSurroundHolesEdgeCircumradius'),
        Cell('=min(StatorMoldSurroundHolesEdgeCircumradius + MaximumDistanceBetweenOuterHolesAndStatorMold;' +
             ' StatorMoldSurroundHolesEdgeCircumradius * 1.13)',
             alias='LengthMiddleHoles'),
        # Used in Stator_Mold_Lid
        Cell('=LengthMiddleHoles - StatorMoldSurroundHolesEdgeCircumradius',
             alias='DistanceBetweenOuterHolesAndStatorMold')
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
        Cell('BottomLeftCornerX'),
        Cell('BottomLeftCornerY')
    ],
    [
        Cell('=LengthMiddleHoles * cos(240)',
             alias='BottomLeftCornerX'),
        Cell('=LengthMiddleHoles * sin(240)',
             alias='BottomLeftCornerY')
    ],
    [
        Cell('BottomRightCornerX'),
        Cell('BottomRightCornerY')
    ],
    [
        Cell('=LengthMiddleHoles * cos(300)',
             alias='BottomRightCornerX'),
        Cell('=LengthMiddleHoles * sin(300)',
             alias='BottomRightCornerY')
    ],
    [
        Cell('LineFromBottomRightToBottomLeftCornerSlope'),
        Cell('LineFromBottomRightToBottomLeftCornerYIntercept')
    ],
    [
        Cell('=(BottomRightCornerY - BottomLeftCornerY) / (BottomRightCornerX - BottomLeftCornerX)',
             alias='LineFromBottomRightToBottomLeftCornerSlope'),
        Cell('=BottomLeftCornerY - LineFromBottomRightToBottomLeftCornerSlope * BottomLeftCornerX',
             alias='LineFromBottomRightToBottomLeftCornerYIntercept')
    ],
    [
        Cell('StatorMoldSurroundBoltAngle'),
        Cell('DoesLidNotchAlignWithBolt')
    ],
    [
        Cell('=360deg / StatorMoldSurroundNumberOfBolts',
             alias='StatorMoldSurroundBoltAngle'),
        Cell('=mod(LidNotchDegrees; StatorMoldSurroundBoltAngle)' +
             ' == 0 ? 1 : 0',
             alias='DoesLidNotchAlignWithBolt')
    ],
    [
        # Applies Star Shape only
        Cell('DoesLidNotchAlignWithFirstBolt'),
        Cell('DoesLidNotchAlignWithSecondBolt')
    ],
    [
        Cell('=DoesLidNotchAlignWithBolt == 1 ? (NumberOfBoltsLidNotchIsFrom180 == 1 ? 1 : 0) : 0',
             alias='DoesLidNotchAlignWithFirstBolt'),
        Cell('=DoesLidNotchAlignWithBolt == 1 ? (NumberOfBoltsLidNotchIsFrom180 == 2 ? 1 : 0) : 0',
             alias='DoesLidNotchAlignWithSecondBolt')
    ],
    [
        # Applies Star Shape only
        Cell('FirstOuterBoltHolePolarPatternNumberOfOccurrences'),
        Cell('FirstOuterBoltHolePolarPatternAngle')
    ],
    [
        Cell('=DoesLidNotchAlignWithFirstBolt == 1 ? 5 : 6',
             alias='FirstOuterBoltHolePolarPatternNumberOfOccurrences'),
        Cell('=DoesLidNotchAlignWithFirstBolt == 1 ? 240 deg : 360 deg',
             alias='FirstOuterBoltHolePolarPatternAngle')
    ],
    [
        # Applies Star Shape only
        Cell('SecondOuterBoltHolePolarPatternNumberOfOccurrences'),
        Cell('SecondOuterBoltHolePolarPatternAngle')
    ],
    [
        Cell('=DoesLidNotchAlignWithSecondBolt == 1 ? 5 : 6',
             alias='SecondOuterBoltHolePolarPatternNumberOfOccurrences'),
        Cell('=DoesLidNotchAlignWithSecondBolt == 1 ? 240 deg : 360 deg',
             alias='SecondOuterBoltHolePolarPatternAngle')
    ],
    [
        # Hide bolt if lid notch aligns with it.
        Cell('LargeInnerPolarPatternOccurrences'),
        Cell('LargeInnerPolarPatternOverallAngle')
    ],
    [
        Cell('=DoesLidNotchAlignWithBolt == 1 ? NumberOfStatorHoles - 1 : NumberOfStatorHoles',
             alias='LargeInnerPolarPatternOccurrences'),
        Cell('=DoesLidNotchAlignWithBolt == 1 ? 240 deg : 360 deg',
             alias='LargeInnerPolarPatternOverallAngle')
    ],
    [
        Cell('CoilWinder', styles=[Style.UNDERLINE])
    ],
    [
        # All 3 of these are for below CoilWinderDiskRadius calculation
        Cell('MagnetDiagonal'),
        Cell('CoilWinderDiskRadiusPadding'),
        Cell('CoilWinderDiskRadius')
    ],
    [
        Cell('=sqrt(MagnetWidth^2 + MagnetLength^2)',
             alias='MagnetDiagonal'),
        Cell('12',
             alias='CoilWinderDiskRadiusPadding'),
        Cell('=MagnetDiagonal / 2 + CoilLegWidth + CoilWinderDiskRadiusPadding',
             alias='CoilWinderDiskRadius')
    ],
    [
        Cell('DistanceBetweenTriangularCoilAndTapeNotch'),
        Cell('LargestMagnetDimension'),
        Cell('SmallestMagnetDimension')
    ],
    [
        Cell('2',
             alias='DistanceBetweenTriangularCoilAndTapeNotch'),
        Cell('=max(MagnetLength; MagnetWidth)',
             alias='LargestMagnetDimension'),
        Cell('=min(MagnetLength; MagnetWidth)',
             alias='SmallestMagnetDimension')
    ],
    [
        Cell('CoilWinderVerticalDimension'),
        Cell('CoilWinderOuterHorizontalDimension'),
        Cell('CoilWinderInnerHorizontalDimension')
    ],
    [
        Cell('=MagnetWidth > MagnetLength ? (CoilType == 1 ? MagnetWidth : MagnetLength) : MagnetLength',
             alias='CoilWinderVerticalDimension'),
        Cell('=MagnetWidth > MagnetLength ? (CoilType == 1 ? MagnetLength : CoilHoleWidthAtOuterRadius) : CoilHoleWidthAtOuterRadius',
             alias='CoilWinderOuterHorizontalDimension'),
        Cell('=MagnetWidth > MagnetLength ? (CoilType == 1 ? MagnetLength : CoilHoleWidthAtInnerRadius) : CoilHoleWidthAtInnerRadius',
             alias='CoilWinderInnerHorizontalDimension'),
    ],
    [
        Cell('CoilWinderCenterRodDiameter', styles=[Style.UNDERLINE]),
        Cell('Ensure 2 mm of plywood between center hole and tape notch.')
    ],
    [
        Cell('CwbRange4'),
        Cell('=SmallestMagnetDimension < 19 ? 8 : 10',
             alias='CwbRange4')
    ],
    [
        Cell('CwbRange3'),
        Cell('=SmallestMagnetDimension < 17 ? 6 : CwbRange4',
             alias='CwbRange3')
    ],
    [
        Cell('CwbRange2'),
        Cell('=SmallestMagnetDimension < 15 ? 5 : CwbRange3',
             alias='CwbRange2')
    ],
    [
        Cell('CwbRange1'),
        Cell('=SmallestMagnetDimension < 13 ? 4 : CwbRange2',
             alias='CwbRange1')
    ],
    [
        Cell('CoilWinderCenterRodDiameter'),
        Cell('=SmallestMagnetDimension < 11 ? 3 : CwbRange1',
             alias='CoilWinderCenterRodDiameter')
    ],
    [
        Cell('_________________'), Cell('_________________')
    ],
    [
        Cell('CoilWinderPinDiameter', styles=[Style.UNDERLINE]),
        Cell('Ensure 2 mm of plywood between center hole and tape notch.')
    ],
    [
        Cell('CwpRange1'),
        Cell('=SmallestMagnetDimension < 14 ? 4 : 5',
             alias='CwpRange1')
    ],
    [
        Cell('CoilWinderPinDiameter'),
        Cell('=SmallestMagnetDimension < 12 ? 3 : CwpRange1',
             alias='CoilWinderPinDiameter')
    ],
    [
        Cell('_________________'), Cell('_________________')
    ],
    [
        Cell('CoilWinderCenterRodRadius'),
        Cell('CoilWinderHexNutThickness'),
        Cell('CoilWinderPinRadius')
    ],
    [
        Cell('=CoilWinderCenterRodDiameter / 2',
             alias='CoilWinderCenterRodRadius'),
        # Hex nut thickness equations are derived from
        # plugging in BS 4190 Metric Hexagon Nut Black Thickness into
        # linear equation function finder.
        # http://www.worldfastener.com/bs-4190-metric-hexagon-nuts/
        # https://www.dcode.fr/function-equation-finder
        # Duplicated in Fastener cells & Fastener_HexNut document.
        Cell('=1.64 * CoilWinderCenterRodRadius + 0.35',
             alias='CoilWinderHexNutThickness'),
        Cell('=CoilWinderPinDiameter / 2',
             alias='CoilWinderPinRadius')
    ],
    [
        Cell('MaximumCoilWinderDiskTapeNotchWidth'),
        Cell('MinimumSpaceBetweenPinsAndTapeNotch')
    ],
    [
        Cell('21',
             alias='MaximumCoilWinderDiskTapeNotchWidth'),
        Cell('2',
             alias='MinimumSpaceBetweenPinsAndTapeNotch')
    ],
    [
        Cell('CoilWinderDiskTapeNotchWidth', styles=[Style.UNDERLINE]),
        Cell('Ensure 2 mm of plywood between pins and tape notch.')
    ],
    *generate_tape_notch_width_cells(10),
    [
        Cell('CoilWinderDiskTapeNotchWidth'),
        Cell('=TnwRange0',
             alias='CoilWinderDiskTapeNotchWidth')
    ],
    [
        Cell('_________________'), Cell('_________________')
    ],
    [
        Cell('CoilWinderDiskFillet'),
        Cell('CoilWinderCheekThickness')
    ],
    [
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
        Cell('=CoilType != 3 ? 4 : CoilHoleWidthAtInnerRadius / 2',
             alias='CoilWinderDiskBottomHoleRadius'),
        # TODO: Rename to RectangularRadialDistanceOfHolesFromCenter?
        # Vertical may not make sense since coil winder parts are rotated by CoilWinderCoilsAngle.
        Cell('=CoilWinderVerticalDimension / 2 - CoilWinderPinRadius',
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
        Cell('=CoilWinderHexNutThickness * CoilWinderNumberOfSpacingNuts + WasherThickness * 2',
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
        Cell('=CoilWinderAssemblyThicknessTotal + CoilWinderHexNutThickness * 2 + DistanceThreadsExtendFromNuts * 2 + WasherThickness * 2',
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
        Cell('ShouldRotateCoil'),
        Cell('CoilWinderCoilsAngle')
    ],
    [
        # Equivalent to AND boolean logic.
        # https://forum.freecad.org/viewtopic.php?p=690156#p690156
        Cell('=MagnetWidth > MagnetLength ? (CoilType == 1 ? 1 : 0) : 0',
             alias='ShouldRotateCoil'),
        # Rotate coils 90 deg for rectangular coils when magnet width is greater than length .
        Cell('=ShouldRotateCoil == 1 ? 90 : 0',
             alias='CoilWinderCoilsAngle')
    ],
    [
        Cell('OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('InnerHorizontalDistanceBetweenCenterOfSmallHoles')
    ],
    [
        Cell('=CoilWinderOuterHorizontalDimension - CoilWinderPinDiameter',
             alias='OuterHorizontalDistanceBetweenCenterOfSmallHoles'),
        Cell('=CoilType != 3 ? (CoilWinderInnerHorizontalDimension - CoilWinderPinDiameter) : OuterHorizontalDistanceBetweenCenterOfSmallHoles',
             alias='InnerHorizontalDistanceBetweenCenterOfSmallHoles')
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
        Cell('=asin(CoilHoleWidthAtOuterRadius / (2 * RotorDiskRadius)) * 2 * RotorDiskRadius * pi / 180',
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
        # Set to LargestMagnetDimension when rectanuglar or keyhole coil type to prevent
        # Stator_Coil_Triangular_Reduced & Stator_CoilWinder_Triangular_Spacer
        # from breaking.
        Cell('=CoilType != 3 ? LargestMagnetDimension : MagnetWidth',
             alias='Mw'),
        Cell('=MagnetLength',
             alias='Ml'),
        Cell('=CoilWinderPinRadius',
             alias='Pr')
    ],
    [
        Cell('TriangularHorizontalDistanceBetweenPins'),
        Cell('TriangularCoilWinderCircumradius'),
        Cell('TriangularVerticalDistanceOfHolesFromCenter')
    ],
    [
        Cell('=Mw - CoilWinderPinRadius * 2',
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
        Cell('NumberOfJackingHoles'),
        Cell('JackingRodDiameter')
    ],
    [
        Cell('=WindTurbineShape == <<T>> ? 4 : 3',
             alias='NumberOfJackingHoles'),
        Cell('=min(HubHolesDiameter; 12)',
             alias='JackingRodDiameter')
    ],
    [
        Cell('JackingHoleDiameter', styles=[Style.UNDERLINE]),
        # See "Tapping a thread" section on the bottom right-hand
        # side of page 13 in "A Wind Turbine Recipe Book (2014)".
        Cell('Select size smaller than jacking rod diameter to tap threads.')
    ],
    [
        Cell('Range4'),
        Cell('=JackingRodDiameter >= 8 ? 7 : 5',
             alias='Range4_jhd')
    ],
    [
        Cell('Range3'),
        Cell('=JackingRodDiameter >= 10 ? 8.5 : Range4_jhd',
             alias='Range3_jhd')
    ],
    [
        Cell('Range2'),
        Cell('=JackingRodDiameter >= 12 ? 10.25 : Range3_jhd',
             alias='Range2_jhd')
    ],
    [
        Cell('Range1'),
        Cell('=JackingRodDiameter >= 14 ? 12 : Range2_jhd',
             alias='Range1_jhd')
    ],
    [
        Cell('Diameter'),
        Cell('=JackingRodDiameter >= 16 ? 14 : Range1_jhd',
             alias='JackingHoleDiameter')
    ],
    [
        Cell('____________'), Cell('____________')
    ],
    [
        # Switch to reduced weight rotor disks when RotorDiskRadius
        # exceeds this threshold.
        Cell('WeightReductionRotorDiskRadiusThreshold'),
        Cell('FrontRotorCount')
    ],
    [
        Cell('230',
             alias='WeightReductionRotorDiskRadiusThreshold'),
        Cell('=RotorTopology == <<Single>> ? 0 : 1',
             alias='FrontRotorCount')
    ],
    [
        Cell('FrontRotorThickness'),
    ],
    [
        Cell('=RotorTopology == <<Single>> ? 0 : (RotorTopology == <<Single and metal disk>> ? RotorDiskThickness : RotorThickness)',
             alias='FrontRotorThickness')
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
        Cell('=WindTurbineShape == <<T>> ? SmallIslandRadius : LargeIslandRadius',
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
        Cell('PercentageOfMagnetThicknessCoveredByResin')
    ],
    [
        Cell('=RotorDiskRadius * 2 * 1.3333',
             alias='RotorMoldSideLength'),
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
        Cell('RotorMoldScrewLength'),
        Cell('NumberOfRotorMoldBolts')
    ],
    [
        Cell('=RotorMoldSurroundThickness + RotorMoldBaseThickness',
             alias='UnroundedRotorMoldScrewLength'),
        Cell('=UnroundedRotorMoldScrewLength + - mod(UnroundedRotorMoldScrewLength; 5)',
             alias='RotorMoldScrewLength'),
        Cell('=WindTurbineShape == <<T>> ? NumberOfHoles / 2 : NumberOfHoles',
             alias='NumberOfRotorMoldBolts')
    ],
    [
        Cell('MaxDistanceBetweenRotorMoldScrewsAndResin'),
        Cell('MaxRotorMoldScrewHolesCircumradius'),
        Cell('RotorMoldScrewHolesCircumradius'),
    ],
    [
        Cell('22',
             alias='MaxDistanceBetweenRotorMoldScrewsAndResin'),
        Cell('=RotorMoldSurroundRadius + MaxDistanceBetweenRotorMoldScrewsAndResin',
             alias='MaxRotorMoldScrewHolesCircumradius'),
        Cell('=min(MaxRotorMoldScrewHolesCircumradius; RotorMoldSurroundRadius * 1.14)',
             alias='RotorMoldScrewHolesCircumradius'),
    ],
    [
        Cell('ApproximateSpaceBetweenRotorMoldScrews'),
        Cell('NumberOfRotorMoldScrews')
    ],
    [
        Cell('120',
             alias='ApproximateSpaceBetweenRotorMoldScrews'),
        Cell('=round(2 * pi * RotorMoldScrewHolesCircumradius / ApproximateSpaceBetweenRotorMoldScrews)',
             alias='NumberOfRotorMoldScrews')
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
        Cell('=DistanceThreadsExtendFromNuts * 2 + MetalThicknessL + HexNutThickness * 2 + DistanceBetweenStatorAndFrame + StatorThickness + WasherThickness',
             alias='StatorMountingStudsLength')
    ],
    [
        Cell('HubStudsRotorTopologyLength'),
        Cell('HubStudsLength')
    ],
    [
        Cell('=RotorTopology == <<Single>> ? RotorDiskThickness + DistanceThreadsExtendFromNuts * 1 : RotorThickness + DistanceThreadsExtendFromNuts * 2 + FrontRotorThickness + MechanicalClearance * (FrontRotorCount + 1) + StatorThickness + HubHexNutThickness + WasherThickness',
             alias='HubStudsRotorTopologyLength'),
        Cell('=HubHexNutThickness * 2 + MiddlePadThickness + HubStudsRotorTopologyLength + BladeAssemblyPlateThickness * 2 + WasherThickness + BladeThickness',
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
        Cell('=MagnetThickness + MechanicalClearance + StatorThickness + MechanicalClearance * FrontRotorCount + MagnetThickness * (RotorTopology == <<Double>> ? 1 : 0)',
             alias='DistanceBetweenRotorDisks'),
        Cell('=RotorTopology == <<Single>> ? 0 : floor(DistanceBetweenRotorDisks / HubHexNutThickness)',
             alias='NumberOfNutsBetweenRotorDisks'),
        Cell('=RotorTopology == <<Single>> ? 0 : floor(DistanceBetweenRotorDisks % HubHexNutThickness / WasherThickness)',
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
    *create_placement_cells(name='Frame',
                            base=(
                                '0',
                                '0',
                                '=StatorThickness / 2 + DistanceBetweenStatorAndFrame + MetalLengthL'),
                            axis=('0', '0', '1'),
                            angle='0'),
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
        Cell('=WindTurbineShape == <<T>> ? -90 : -180', alias='AlternatorZ'),
        Cell('=WindTurbineShape == <<T>> ? 0 : 90', alias='AlternatorY'),
        Cell('=WindTurbineShape == <<T>> ? 90 : 0', alias='AlternatorX')
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
