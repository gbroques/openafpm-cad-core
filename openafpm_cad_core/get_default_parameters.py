"""Module for retrieving default values for wind turbine variants."""
from typing import Dict, List, TypedDict, Union

from typing_extensions import NotRequired

from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_shape import WindTurbineShape

__all__ = ['get_default_parameters', 'get_presets', 'Parameters']


class Parameters(TypedDict):
    """Dictionary containing magnafpm, furling, and user parameters."""
    description: NotRequired[str]
    magnafpm: MagnafpmParameters
    furling: FurlingParameters
    user: UserParameters


def get_default_parameters(preset: Union[WindTurbineShape, str]) -> Parameters:
    """Get default parameters for "T Shape", "H Shape", "Star Shape", or another preset turbine.
    """
    key = preset if isinstance(preset, str) else preset.value
    return default_parameters[key]


def get_presets() -> List[str]:
    return list(default_parameters.keys())


default_parameters: Dict[str, Parameters] = {
    "T Shape": {
        "magnafpm": {
            "RotorDiameter": 2400,
            "RotorDiskRadius": 150,
            "RotorDiskInnerRadius": 100,
            "RotorDiskThickness": 10,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "Neodymium",
            "NumberMagnet": 12,
            "StatorThickness": 13,
            "CoilType": 1,
            "CoilLegWidth": 21.5,
            "CoilInnerWidth1": 30,
            "CoilInnerWidth2": 30,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 20,
            "NumberOfCoilsPerPhase": 3,
            "WireWeight": 2.6,
            "WireDiameter": 1.4,
            "NumberOfWiresInHand": 2,
            "TurnsPerCoil": 43
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 300,
            "BracketWidth": 30,
            "BracketThickness": 5,
            "BoomLength": 1000,
            "BoomPipeDiameter": 48.3,
            "BoomPipeThickness": 5,
            "VaneThickness": 6,
            "VaneLength": 1200,
            "VaneWidth": 500,
            "Offset": 125
        },
        "user": {
            "BladeWidth": 124,
            "HubPitchCircleDiameter": 100,
            "RotorDiskCentralHoleDiameter": 65,
            "HolesDiameter": 12,
            "MetalLengthL": 50,
            "MetalThicknessL": 6,
            "FlatMetalThickness": 10,
            "YawPipeDiameter": 60.3,
            "PipeThickness": 5,
            "RotorResinMargin": 5,
            "HubHolesDiameter": 12
        }
    },
    "H Shape": {
        "magnafpm": {
            "RotorDiameter": 4200,
            "RotorDiskRadius": 225,
            "RotorDiskInnerRadius": 100,
            "RotorDiskThickness": 10,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "Neodymium",
            "NumberMagnet": 16,
            "StatorThickness": 13,
            "CoilType": 1,
            "CoilLegWidth": 32,
            "CoilInnerWidth1": 30,
            "CoilInnerWidth2": 30,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 36,
            "NumberOfCoilsPerPhase": 4,
            "WireWeight": 2.6,
            "WireDiameter": 1.4,
            "NumberOfWiresInHand": 2,
            "TurnsPerCoil": 43
        },
        "furling": {
            "VerticalPlaneAngle": 15,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 600,
            "BracketWidth": 50,
            "BracketThickness": 6,
            "BoomLength": 1800,
            "BoomPipeDiameter": 48.3,
            "BoomPipeThickness": 5,
            "VaneThickness": 9,
            "VaneLength": 2000,
            "VaneWidth": 900,
            "Offset": 250
        },
        "user": {
            "BladeWidth": 223,
            "HubPitchCircleDiameter": 130,
            "RotorDiskCentralHoleDiameter": 95,
            "HolesDiameter": 14,
            "MetalLengthL": 60,
            "MetalThicknessL": 6,
            "FlatMetalThickness": 10,
            "YawPipeDiameter": 88.9,
            "PipeThickness": 5,
            "RotorResinMargin": 5,
            "HubHolesDiameter": 14
        }
    },
    "Star Shape": {
        "magnafpm": {
            "RotorDiameter": 6000,
            "RotorDiskRadius": 350,
            "RotorDiskInnerRadius": 100,
            "RotorDiskThickness": 10,
            "MagnetLength": 58,
            "MagnetWidth": 27,
            "MagnetThickness": 10,
            "MagnetMaterial": "Neodymium",
            "NumberMagnet": 32,
            "StatorThickness": 15,
            "CoilType": 2,
            "CoilLegWidth": 22.4,
            "CoilInnerWidth1": 40,
            "CoilInnerWidth2": 27,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 44,
            "NumberOfCoilsPerPhase": 8,
            "WireWeight": 2.6,
            "WireDiameter": 1.4,
            "NumberOfWiresInHand": 2,
            "TurnsPerCoil": 43
        },
        "furling": {
            "VerticalPlaneAngle": 15,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 900,
            "BracketWidth": 50,
            "BracketThickness": 6,
            "BoomLength": 2600,
            "BoomPipeDiameter": 73,
            "BoomPipeThickness": 5,
            "VaneThickness": 12,
            "VaneLength": 3000,
            "VaneWidth": 1260,
            "Offset": 348
        },
        "user": {
            "BladeWidth": 322,
            "HubPitchCircleDiameter": 205,
            "RotorDiskCentralHoleDiameter": 163,
            "HolesDiameter": 14,
            "MetalLengthL": 80,
            "MetalThicknessL": 8,
            "FlatMetalThickness": 12,
            "YawPipeDiameter": 114.3,
            "PipeThickness": 6,
            "RotorResinMargin": 5,
            "HubHolesDiameter": 20
        }
    },
    "T Shape 2F": {
        "description": (
            "2m meter diameter wind turbine with T-shape frame and (F)errite magnets. " +
            "Useful for testing triangular coils and the outer magnet jig."
        ),
        "magnafpm": {
            "RotorDiameter": 2400,
            "RotorDiskRadius": 151.39,
            "RotorDiskInnerRadius": 99.32,
            "RotorDiskThickness": 8,
            "MagnetLength": 50,
            "MagnetWidth": 50,
            "MagnetThickness": 20,
            "MagnetMaterial": "Ferrite",
            "NumberMagnet": 12,
            "StatorThickness": 13,
            "CoilType": 3,
            "CoilLegWidth": 20.63,
            "CoilInnerWidth1": 50,
            "CoilInnerWidth2": 8,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 2,
            "NumberOfCoilsPerPhase": 3,
            "WireWeight": 2.6,
            "WireDiameter": 1.4,
            "NumberOfWiresInHand": 2,
            "TurnsPerCoil": 43
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 300,
            "BracketWidth": 30,
            "BracketThickness": 5,
            "BoomLength": 1000,
            "BoomPipeDiameter": 48.3,
            "BoomPipeThickness": 5,
            "VaneThickness": 6,
            "VaneLength": 1200,
            "VaneWidth": 500,
            "Offset": 125
        },
        "user": {
            "BladeWidth": 124,
            "HubPitchCircleDiameter": 100,
            "RotorDiskCentralHoleDiameter": 65,
            "HolesDiameter": 12,
            "MetalLengthL": 50,
            "MetalThicknessL": 6,
            "FlatMetalThickness": 10,
            "YawPipeDiameter": 60.3,
            "PipeThickness": 5,
            "RotorResinMargin": 10,
            "HubHolesDiameter": 12
        }
    },
    "H Shape 4F": {
        "description": (
            "4 meter diameter wind turbine with H-shape frame and (F)errite magnets. " +
            "Useful for testing triangular coils with a reduced coil leg width."
        ),
        "magnafpm": {
            "RotorDiameter": 4200,
            "RotorDiskRadius": 274.77,
            "RotorDiskInnerRadius": 198.63,
            "RotorDiskThickness": 10,
            "MagnetLength": 75,
            "MagnetWidth": 50,
            "MagnetThickness": 20,
            "MagnetMaterial": "Ferrite",
            "NumberMagnet": 24,
            "StatorThickness": 14,
            "CoilType": 3,
            "CoilLegWidth": 25.92,
            "CoilInnerWidth1": 50,
            "CoilInnerWidth2": 8,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 2,
            "NumberOfCoilsPerPhase": 6,
            "WireWeight": 19.68,
            "WireDiameter": 0.95,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 322
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 600,
            "BracketWidth": 50,
            "BracketThickness": 6,
            "BoomLength": 1800,
            "BoomPipeDiameter": 48.3,
            "BoomPipeThickness": 3,
            "VaneThickness": 12,
            "VaneLength": 2000,
            "VaneWidth": 900,
            "Offset": 250
        },
        "user": {
            "BladeWidth": 223,
            "HubPitchCircleDiameter": 130,
            "RotorDiskCentralHoleDiameter": 95,
            "HolesDiameter": 14,
            "MetalLengthL": 60,
            "MetalThicknessL": 6,
            "FlatMetalThickness": 10,
            "YawPipeDiameter": 101.6,
            "PipeThickness": 5,
            "RotorResinMargin": 10,
            "HubHolesDiameter": 14
        }
    }
}
