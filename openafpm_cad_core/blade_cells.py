from typing import List

from .plywood_thickness import PlywoodThickness
from .spreadsheet import Cell, Style

__all__ = ['blade_cells']


blade_cells: List[List[Cell]] = [
    [
        Cell('Inputs', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('Spreadsheet', styles=[Style.UNDERLINE])
        # -------------------------------------------
    ],
    [
        Cell('RotorDiameter'),
        Cell('BladeWidth'),
        Cell('HubPitchCircleDiameter')
    ],
    [
        Cell('=Spreadsheet.RotorDiameter',
             alias='RotorDiameter'),
        Cell('=Spreadsheet.BladeWidth',
             alias='BladeWidth'),
        Cell('=Spreadsheet.HubPitchCircleDiameter',
             alias='HubPitchCircleDiameter')
    ],
    [
        Cell('HubHolesDiameter'),
        Cell('ScrewHoleDiameter')
    ],
    [
        Cell('=Spreadsheet.HubHolesDiameter',
             alias='HubHolesDiameter'),
        Cell('=Fastener.ScrewHoleDiameter',
             alias='ScrewHoleDiameter'),
    ],
    [
        Cell('Static', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('BladeTemplateThickness')
    ],
    [
        Cell('6',
             alias='BladeTemplateThickness')
    ],
    [
        Cell('Calculated', styles=[Style.UNDERLINE, Style.BOLD])
    ],
    [
        Cell('HubPitchCircleRadius'),
        Cell('HubHolesRadius'),
        Cell('ScrewHoleRadius')
    ],
    [
        Cell('=HubPitchCircleDiameter / 2',
             alias='HubPitchCircleRadius'),
        Cell('=HubHolesDiameter / 2',
             alias='HubHolesRadius'),
        Cell('=ScrewHoleDiameter / 2',
             alias='ScrewHoleRadius')
    ],
    [
        Cell('=RotorDiameter / 2',
             alias='BladeRadius'),
        # TODO: Should we round this?
        Cell('=0.055 * RotorDiameter - 8',
             alias='MinimumBladeWidth')
    ],
    [
        Cell('BladeAssemblyBackDiskDiameter'),
        Cell('BladeAssemblyFrontTriangleSideLength')
    ],
    [
        Cell('=0.106 * RotorDiameter - 3.121',
             alias='BladeAssemblyBackDiskDiameter'),
        Cell('=0.147 * RotorDiameter + 6.213',
             alias='BladeAssemblyFrontTriangleSideLength')
    ],
    [
        Cell('BladeTemplateDim_V'),
        Cell('BladeTemplateDim_W')
    ],
    [
        Cell('=round(0.086 * RotorDiameter - 10.669)',
             alias='BladeTemplateDim_V'),
        Cell('=round(0.018 * RotorDiameter + 12.986)',
             alias='BladeTemplateDim_W')
    ],
    [
        Cell('UnroundedBladeAssemblyPlateThickness'),
        Cell('UnroundedBladeAssemblyScrewLength'),
        Cell('BladeAssemblyScrewLength')
    ],
    [
        Cell('=0.004 * RotorDiameter + 2.426',
             alias='UnroundedBladeAssemblyPlateThickness'),
        Cell('=0.010 * RotorDiameter + 8.755',
             alias='UnroundedBladeAssemblyScrewLength'),
        # Round down to nearest multiple of 5
        Cell('=round(UnroundedBladeAssemblyScrewLength - mod(UnroundedBladeAssemblyScrewLength; 5))',
             alias='BladeAssemblyScrewLength')
    ],
    [
        Cell('BladeAssemblyPlateThickness', styles=[Style.UNDERLINE]),
        Cell('Round to nearest plywood thickness')
    ],
    [
        Cell('Range7'),
        Cell('=UnroundedBladeAssemblyPlateThickness < 28.5' +
             f' ? {PlywoodThickness.MM_27.value} : {PlywoodThickness.MM_30}',
             alias='Range7')
    ],
    [
        Cell('Range6'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 25.5 ? {PlywoodThickness.MM_24.value} : Range7',
             alias='Range6')
    ],
    [
        Cell('Range5'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 22.5 ? {PlywoodThickness.MM_21.value} : Range6',
             alias='Range5')
    ],
    [
        Cell('Range4'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 19.5 ? {PlywoodThickness.MM_18.value} : Range5',
             alias='Range4')
    ],
    [
        Cell('Range3'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 16.5 ? {PlywoodThickness.MM_15.value} : Range4',
             alias='Range3')
    ],
    [
        Cell('Range2'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 13.5 ? {PlywoodThickness.MM_12.value} : Range3',
             alias='Range2')
    ],
    [
        Cell('Range1'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 10.5 ? {PlywoodThickness.MM_9.value} : Range2',
             alias='Range1')
    ],
    [
        Cell('BladeAssemblyPlateThickness'),
        Cell(f'=UnroundedBladeAssemblyPlateThickness < 7.5 ? {PlywoodThickness.MM_6.value} : Range1',
             alias='BladeAssemblyPlateThickness')
    ],
    [
        Cell('TotalNumberOfBladeScrews'),
        Cell('UnroundedMinimumNumberOfFrontTriangleScrews'),
        Cell('UnroundedNumberOfBackDiskScrews'),
    ],
    [
        Cell('=0.013 * RotorDiameter + 16.929',
             alias='TotalNumberOfBladeScrews'),
        Cell('=TotalNumberOfBladeScrews * 0.48',
             alias='UnroundedMinimumNumberOfFrontTriangleScrews'),
        Cell('=TotalNumberOfBladeScrews - UnroundedMinimumNumberOfFrontTriangleScrews',
             alias='UnroundedNumberOfBackDiskScrews'),
    ],
    [
        Cell('MinimumNumberOfFrontTriangleScrews'),
        Cell('NumberOfBackDiskScrews')
    ],
    [
        # Round up to nearest multiple of 3.
        Cell('=UnroundedMinimumNumberOfFrontTriangleScrews + 3 - mod(UnroundedMinimumNumberOfFrontTriangleScrews; 3)',
             alias='MinimumNumberOfFrontTriangleScrews'),
        # Round up to nearest multiple of 3.
        Cell('=UnroundedNumberOfBackDiskScrews + 3 - mod(UnroundedNumberOfBackDiskScrews; 3)',
             alias='NumberOfBackDiskScrews')
    ],
    [
        Cell('MinimumNumberOfFrontTriangleScrewsPerBlade'),
        Cell('NumberOfBackDiskScrewsPerBlade')
    ],
    [
        Cell('=MinimumNumberOfFrontTriangleScrews / 3',
             alias='MinimumNumberOfFrontTriangleScrewsPerBlade'),
        Cell('=NumberOfBackDiskScrews / 3',
             alias='NumberOfBackDiskScrewsPerBlade')
    ],
    [
        Cell('LessThan3000'),
        Cell('GreaterThanOrEqualTo3000'),
        Cell('BladeThickness')
    ],
    [
        Cell('=RotorDiameter * 0.0083333333333 + 20 ',
             alias='LessThan3000'),
        Cell('=RotorDiameter * 0.025 - 30',
             alias='GreaterThanOrEqualTo3000'),
        Cell('=RotorDiameter < 3000 ? LessThan3000 : GreaterThanOrEqualTo3000',
             alias='BladeThickness')
    ],
    [
        Cell('Front Triangle Screw Calculations', styles=[Style.UNDERLINE, Style.BOLD])
        # Increase number of screws by 1 or 2 when BladeWidth exceeds the minimum value.
    ],
    [
        Cell('DistanceFromCenter'),
        Cell('=BladeWidth - BladeTemplateDim_W',
             alias='DistanceFromCenter')
    ],
    [
        Cell('MinimumDistanceFromCenter'),
        Cell('=MinimumBladeWidth - BladeTemplateDim_W',
             alias='MinimumDistanceFromCenter')
    ],
    [
        Cell('HalfScrewsPerBlade'),
        Cell('=round(MinimumNumberOfFrontTriangleScrewsPerBlade * 0.5)',
             alias='HalfScrewsPerBlade')
    ],
    [
        Cell('MinimumNumberOfInnerScrews'),
        Cell('=min(HalfScrewsPerBlade; MinimumNumberOfFrontTriangleScrewsPerBlade - HalfScrewsPerBlade)',
             alias='MinimumNumberOfInnerScrews')
    ],
    [
        Cell('MinimumNumberOfOuterScrews'),
        Cell('=MinimumNumberOfFrontTriangleScrewsPerBlade - MinimumNumberOfInnerScrews',
             alias='MinimumNumberOfOuterScrews')
    ],
    [
        Cell('TriangleHeight'),
        Cell('=BladeAssemblyFrontTriangleSideLength * sqrt(3) / 2',
             alias='TriangleHeight')
    ],
    [
        Cell('InscribedCircleRadius'),
        Cell('=TriangleHeight / 3',
             alias='InscribedCircleRadius')
    ],
    [
        Cell('DistanceBetweenScrewHolesCircumradii'),
        Cell('=(InscribedCircleRadius - ScrewHoleRadius - (HubPitchCircleRadius + HubHolesRadius)) / 3',
             alias='DistanceBetweenScrewHolesCircumradii')
    ],
    [
        Cell('TriangleCenterToVertexDistance'),
        Cell('=TriangleHeight * 2 / 3',
             alias='TriangleCenterToVertexDistance')
    ],
    [
        Cell('InnerScrewLineDistanceFromCenter'),
        Cell('=HubPitchCircleRadius + HubHolesRadius + DistanceBetweenScrewHolesCircumradii',
             alias='InnerScrewLineDistanceFromCenter')
    ],
    [
        Cell('OuterScrewLineDistanceFromCenter'),
        Cell('=InnerScrewLineDistanceFromCenter + DistanceBetweenScrewHolesCircumradii',
             alias='OuterScrewLineDistanceFromCenter')
    ],
    [
        Cell('Alpha'),
        Cell('=acos(BladeTemplateDim_W / TriangleCenterToVertexDistance)',
             alias='Alpha')
    ],
    [
        Cell('Beta'),
        Cell('=180 deg - 60 deg - Alpha',
             alias='Beta')
    ],
    [
        Cell('Gamma'),
        Cell('=180 deg - 90 deg - Beta',
             alias='Gamma')
    ],
    [
        Cell('InnerScrewBetaHypotenuse'),
        Cell('=InnerScrewLineDistanceFromCenter / cos(Beta)',
             alias='InnerScrewBetaHypotenuse'),
        Cell('OuterScrewBetaHypotenuse'),
        Cell('=OuterScrewLineDistanceFromCenter / cos(Beta)',
             alias='OuterScrewBetaHypotenuse')
    ],
    [
        Cell('InnerScrewLineTriangle_Adjacent'),
        Cell('=InnerScrewBetaHypotenuse + BladeTemplateDim_W',
             alias='InnerScrewLineTriangle_Adjacent'),
        Cell('OuterScrewLineTriangle_Adjacent'),
        Cell('=OuterScrewBetaHypotenuse + BladeTemplateDim_W',
             alias='OuterScrewLineTriangle_Adjacent')
    ],
    [
        Cell('InnerScrewLineTriangle_Hypotenuse'),
        Cell('=InnerScrewLineTriangle_Adjacent / cos(Gamma)',
             alias='InnerScrewLineTriangle_Hypotenuse'),
        Cell('OuterScrewLineTriangle_Hypotenuse'),
        Cell('=OuterScrewLineTriangle_Adjacent / cos(Gamma)',
             alias='OuterScrewLineTriangle_Hypotenuse')
    ],
    [
        Cell('InnerScrewGammaAdjacent'),
        Cell('=max(InnerScrewBetaHypotenuse - DistanceFromCenter; 0)',
             alias='InnerScrewGammaAdjacent'),
        Cell('OuterScrewGammaAdjacent'),
        Cell('=max(OuterScrewBetaHypotenuse - DistanceFromCenter; 0)',
             alias='OuterScrewGammaAdjacent')
    ],
    [
        Cell('InnerScrewGammaHypotenuse'),
        Cell('=InnerScrewGammaAdjacent / cos(Gamma)',
             alias='InnerScrewGammaHypotenuse'),
        Cell('OuterScrewGammaHypotenuse'),
        Cell('=OuterScrewGammaAdjacent / cos(Gamma)',
             alias='OuterScrewGammaHypotenuse')
    ],
    [
        Cell('InnerScrewGammaOpposite'),
        Cell('=sqrt(InnerScrewGammaHypotenuse ^ 2 - InnerScrewGammaAdjacent ^ 2)',
             alias='InnerScrewGammaOpposite'),
        Cell('OuterScrewGammaOpposite'),
        Cell('=sqrt(OuterScrewGammaHypotenuse ^ 2 - OuterScrewGammaAdjacent ^ 2)',
             alias='OuterScrewGammaOpposite')
    ],
    [
        Cell('MinimumInnerScrewGammaAdjacent'),
        Cell('=max(InnerScrewBetaHypotenuse - MinimumDistanceFromCenter; 0)',
             alias='MinimumInnerScrewGammaAdjacent'),
        Cell('MinimumOuterScrewGammaAdjacent'),
        Cell('=max(OuterScrewBetaHypotenuse - MinimumDistanceFromCenter; 0)',
             alias='MinimumOuterScrewGammaAdjacent')
    ],
    [
        Cell('MinimumInnerScrewGammaHypotenuse'),
        Cell('=MinimumInnerScrewGammaAdjacent / cos(Gamma)',
             alias='MinimumInnerScrewGammaHypotenuse'),
        Cell('MinimumOuterScrewGammaHypotenuse'),
        Cell('=MinimumOuterScrewGammaAdjacent / cos(Gamma)',
             alias='MinimumOuterScrewGammaHypotenuse')
    ],
    [
        Cell('MinimumInnerScrewGammaOpposite'),
        Cell('=sqrt(MinimumInnerScrewGammaHypotenuse ^ 2 - MinimumInnerScrewGammaAdjacent ^ 2)',
             alias='MinimumInnerScrewGammaOpposite'),
        Cell('MinimumOuterScrewGammaOpposite'),
        Cell('=sqrt(MinimumOuterScrewGammaHypotenuse ^ 2 - MinimumOuterScrewGammaAdjacent ^ 2)',
             alias='MinimumOuterScrewGammaOpposite')
    ],
    [
        Cell('BladeTemplateTrailingEdgeAngle'),
        Cell('=atan(BladeRadius / (BladeWidth - BladeTemplateDim_W))',
             alias='BladeTemplateTrailingEdgeAngle')
    ],
    [
        Cell('MinimumBladeTemplateTrailingEdgeAngle'),
        Cell('=atan(BladeRadius / (MinimumBladeWidth - BladeTemplateDim_W))',
             alias='MinimumBladeTemplateTrailingEdgeAngle')
    ],
    [
        Cell('Epsilon'),
        Cell('=90 deg - BladeTemplateTrailingEdgeAngle',
             alias='Epsilon')
    ],
    [
        Cell('MinimumEpsilon'),
        Cell('=90 deg - MinimumBladeTemplateTrailingEdgeAngle',
             alias='MinimumEpsilon')
    ],
    [
        Cell('Delta'),
        Cell('=InnerScrewGammaHypotenuse == 0 ? 0 deg : asin(InnerScrewGammaAdjacent / InnerScrewGammaHypotenuse)',
             alias='Delta')
    ],
    [
        Cell('DeltaSupplementaryAngle'),
        Cell('=180 deg - Delta',
             alias='DeltaSupplementaryAngle')
    ],
    [
        Cell('Zeta'),
        Cell('=180 deg - DeltaSupplementaryAngle - Epsilon',
             alias='Zeta')
    ],
    [
        Cell('MinimumDelta'),
        Cell('=asin(MinimumInnerScrewGammaAdjacent / MinimumInnerScrewGammaHypotenuse)',
             alias='MinimumDelta')
    ],
    [
        Cell('MinimumDeltaSupplementaryAngle'),
        Cell('=180 deg - MinimumDelta',
             alias='MinimumDeltaSupplementaryAngle')
    ],
    [
        Cell('MinimumZeta'),
        Cell('=180 deg - MinimumDeltaSupplementaryAngle - MinimumEpsilon',
             alias='MinimumZeta')
    ],
    [
        Cell('InnerScrewHypotenuseAddition'),
        Cell('=InnerScrewGammaOpposite / sin(Zeta) * sin(Epsilon)',
             alias='InnerScrewHypotenuseAddition'),
        Cell('OuterScrewHypotenuseAddition'),
        Cell('=OuterScrewGammaOpposite / sin(Zeta) * sin(Epsilon)',
             alias='OuterScrewHypotenuseAddition')
    ],
    [
        Cell('MinimumInnerScrewHypotenuseAddition'),
        Cell('=MinimumInnerScrewGammaOpposite / sin(MinimumZeta) * sin(MinimumEpsilon)',
             alias='MinimumInnerScrewHypotenuseAddition'),
        Cell('MinimumOuterScrewHypotenuseAddition'),
        Cell('=MinimumOuterScrewGammaOpposite / sin(MinimumZeta) * sin(MinimumEpsilon)',
             alias='MinimumOuterScrewHypotenuseAddition')
    ],
    [
        Cell('InnerScrewHypotenuseOffset'),
        Cell('=InnerScrewGammaHypotenuse + InnerScrewHypotenuseAddition',
             alias='InnerScrewHypotenuseOffset'),
        Cell('OuterScrewHypotenuseOffset'),
        Cell('=OuterScrewGammaHypotenuse + OuterScrewHypotenuseAddition',
             alias='OuterScrewHypotenuseOffset')
    ],
    [
        Cell('MinimumInnerScrewHypotenuseOffset'),
        Cell('=MinimumInnerScrewGammaHypotenuse + MinimumInnerScrewHypotenuseAddition',
             alias='MinimumInnerScrewHypotenuseOffset'),
        Cell('MinimumOuterScrewHypotenuseOffset'),
        Cell('=MinimumOuterScrewGammaHypotenuse + MinimumOuterScrewHypotenuseAddition',
             alias='MinimumOuterScrewHypotenuseOffset')
    ],
    [
        Cell('InnerScrewHypotenuseOffsetDifference'),
        Cell('=MinimumInnerScrewHypotenuseOffset - InnerScrewHypotenuseOffset',
             alias='InnerScrewHypotenuseOffsetDifference'),
        Cell('OuterScrewHypotenuseOffsetDifference'),
        Cell('=MinimumOuterScrewHypotenuseOffset - OuterScrewHypotenuseOffset',
             alias='OuterScrewHypotenuseOffsetDifference')
    ],
    [
        Cell('InnerScrewLineHypotenuse'),
        Cell('=InnerScrewLineTriangle_Hypotenuse - InnerScrewHypotenuseOffset',
             alias='InnerScrewLineHypotenuse'),
        Cell('OuterScrewLineHypotenuse'),
        Cell('=OuterScrewLineTriangle_Hypotenuse - OuterScrewHypotenuseOffset',
             alias='OuterScrewLineHypotenuse')
    ],
    [
        Cell('MaximumDistanceBetweenInnerScrews'),
        Cell('=InnerScrewLineHypotenuse / (MinimumNumberOfInnerScrews + 1)',
             alias='MaximumDistanceBetweenInnerScrews'),
        Cell('MaximumDistanceBetweenOuterScrews'),
        Cell('=OuterScrewLineHypotenuse / (MinimumNumberOfOuterScrews + 1)',
             alias='MaximumDistanceBetweenOuterScrews')
    ],
    [
        Cell('NumberOfAdditionalInnerScrews'),
        Cell('=round(InnerScrewHypotenuseOffsetDifference / MaximumDistanceBetweenInnerScrews)',
             alias='NumberOfAdditionalInnerScrews'),
        Cell('NumberOfAdditionalOuterScrews'),
        Cell('=round(OuterScrewHypotenuseOffsetDifference / MaximumDistanceBetweenOuterScrews)',
             alias='NumberOfAdditionalOuterScrews')
    ],
    [
        Cell('NumberOfInnerScrews'),
        Cell('=MinimumNumberOfInnerScrews + NumberOfAdditionalInnerScrews',
             alias='NumberOfInnerScrews'),
        Cell('NumberOfOuterScrews'),
        Cell('=MinimumNumberOfOuterScrews + NumberOfAdditionalOuterScrews',
             alias='NumberOfOuterScrews')
    ],
    [
        Cell('DistanceBetweenInnerScrews'),
        Cell('=InnerScrewLineHypotenuse / (NumberOfInnerScrews + 1)',
             alias='DistanceBetweenInnerScrews'),
        Cell('DistanceBetweenOuterScrews'),
        Cell('=OuterScrewLineHypotenuse / (NumberOfOuterScrews + 1)',
             alias='DistanceBetweenOuterScrews')
    ],
    [
        Cell('InnerScrewLineLength'),
        Cell('=InnerScrewLineHypotenuse - DistanceBetweenInnerScrews * 2',
             alias='InnerScrewLineLength'),
        Cell('OuterScrewLineLength'),
        Cell('=OuterScrewLineHypotenuse - DistanceBetweenOuterScrews * 2',
             alias='OuterScrewLineLength')
    ],
    [
        Cell('FirstInnerScrewOffset'),
        Cell('=InnerScrewHypotenuseOffset + DistanceBetweenInnerScrews',
             alias='FirstInnerScrewOffset'),
        Cell('FirstOuterScrewOffset'),
        Cell('=OuterScrewHypotenuseOffset + DistanceBetweenOuterScrews',
             alias='FirstOuterScrewOffset')
    ],
]
