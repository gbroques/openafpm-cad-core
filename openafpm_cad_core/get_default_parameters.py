"""Module for retrieving values for various wind turbine preset designs."""
from typing import Dict, List, Union

from .wind_turbine_shape import WindTurbineShape

__all__ = ['get_default_parameters', 'get_presets']


def get_default_parameters(preset: Union[WindTurbineShape, str]) -> dict:
    """Get default parameters for "T Shape", "H Shape", "Star Shape", or another preset turbine.
    """
    key = preset if isinstance(preset, str) else preset.value
    parameters = preset_by_name[key]
    if 'inheritsFrom' not in parameters:
        return parameters
    else:
        parent_parameters = preset_by_name[parameters['inheritsFrom']]
        merged_parameters = {'description': parameters['description']}
        for group in ['magnafpm', 'furling', 'user']:
            if group in parameters:
                merged_parameters[group] = parent_parameters[group] | parameters[group]
            else:
                merged_parameters[group] = parent_parameters[group]
        return merged_parameters


def get_presets() -> List[str]:
    return list(preset_by_name.keys())


preset_by_name: Dict[str, dict] = {
    "T Shape": {
        "description": (
            "2.4 meter diameter wind turbine with T-shape frame. " +
            "Based on 'A Wind Turbine Recipe Book (2014)' by Hugh Piggott."
        ),
        "magnafpm": {
            "RotorDiameter": 2400,
            "RotorTopology": "Double",
            "RotorDiskRadius": 150,
            "RotorDiskInnerRadius": 103.25,
            "RotorDiskThickness": 10,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 12,
            "StatorThickness": 13,
            "CoilType": 1,
            "CoilLegWidth": 21.5,
            "CoilHoleWidthAtOuterRadius": 30,
            "CoilHoleWidthAtInnerRadius": 30,
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
        "description": (
            "4.2 meter diameter wind turbine with H-shape frame. " +
            "Based on 'A Wind Turbine Recipe Book (2014)' by Hugh Piggott."
        ),
        "magnafpm": {
            "RotorDiameter": 4200,
            "RotorTopology": "Double",
            "RotorDiskRadius": 225,
            "RotorDiskInnerRadius": 178.50,
            "RotorDiskThickness": 10,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 16,
            "StatorThickness": 13,
            "CoilType": 1,
            "CoilLegWidth": 32,
            "CoilHoleWidthAtOuterRadius": 30,
            "CoilHoleWidthAtInnerRadius": 30,
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
        "description": (
            "6 meter diameter wind turbine with six-pointed star-shape frame. " +
            "Designs larger than 4.2 meters are not included in 'A Wind Turbine Recipe Book (2014)' by Hugh Piggott. " +
            "Several have been built by Wind Empowerment members, " +
            "and this design was developed by the Rural Electrification Research Group (RurERG)."
            # See:
            # https://rurerg.net/2016/01/16/july-2015-neodymium-magnet-generator-for-a-6m-rotor-swt-for-battery-charging/
        ),
        # https://www.openafpm.net/simulation/9102
        "magnafpm": {
            "RotorDiameter": 6000,
            "RotorTopology": "Double",
            "RotorDiskRadius": 372.24,
            "RotorDiskInnerRadius": 313.99,
            "RotorDiskThickness": 10,
            "MagnetLength": 58,
            "MagnetWidth": 27,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 32,
            "StatorThickness": 15,
            "CoilType": 2,
            "CoilLegWidth": 31.13,
            "CoilHoleWidthAtOuterRadius": 34.63,
            "CoilHoleWidthAtInnerRadius": 19.45,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 34.65,
            "NumberOfCoilsPerPhase": 8,
            "WireWeight": 15.99,
            "WireDiameter": 1.7,
            "NumberOfWiresInHand": 8,
            "TurnsPerCoil": 14
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
            "2 meter diameter wind turbine with T-shape frame and (F)errite magnets. " +
            "Based on the '2F wind turbine construction manual' 2014 edition by Hugh Piggott. " +
            "Useful for testing partially covered magnets, triangular coils, and the outer magnet jig."
        ),
        # TSR = 6, page 11
        # See https://www.openafpm.net/simulation/9098
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiameter": 2000,  # page 3
            "RotorDiskRadius": 148.57,
            "RotorDiskInnerRadius": 96.45,
            "RotorDiskThickness": 6,  # page 64
            "MagnetLength": 50,  # page 5
            "MagnetWidth": 50,  # page 5
            "MagnetThickness": 20,  # page 5
            "MagnetMaterial": "Ferrite",  # page 3
            "StatorThickness": 12,  # pages 69, 84, & 86
            "CoilType": 3,  # page 78
            "CoilLegWidth": 21.99,
            "CoilHoleWidthAtOuterRadius": 50,
            "CoilHoleWidthAtInnerRadius": 8,  # page 74
            "MechanicalClearance": 5,
            "InnerDistanceBetweenMagnets": 0.5,
            "WireWeight": 3.05,
            "WireDiameter": 1.5,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 82
        },
        "furling": {
            "VerticalPlaneAngle": 13,  # page 50 - 52
            "Offset": 100,  # page 9 & 46
            "VaneLength": 1000  # page 62 & 63
        },
        "user": {
            "YawPipeDiameter": 60.3,  # page 31
            "RotorResinMargin": 10
        }
    },
    "H Shape 4F": {
        # https://www.openafpm.net/simulation/8930
        "description": (
            "4 meter diameter wind turbine with H-shape frame and (F)errite magnets. " +
            "Useful for testing triangular coils with a reduced coil leg width."
        ),
        "inheritsFrom": "H Shape",
        "magnafpm": {
            "RotorDiameter": 4340,
            "RotorDiskRadius": 274.77,
            "RotorDiskInnerRadius": 198.63,
            "MagnetLength": 75,
            "MagnetWidth": 50,
            "MagnetThickness": 20,
            "MagnetMaterial": "Ferrite",
            "NumberMagnet": 24,
            "StatorThickness": 14,
            "CoilType": 3,
            "CoilLegWidth": 25.92,
            "CoilHoleWidthAtOuterRadius": 50,
            "CoilHoleWidthAtInnerRadius": 8,
            "InnerDistanceBetweenMagnets": 2,
            "NumberOfCoilsPerPhase": 6,
            "WireWeight": 19.68,
            "WireDiameter": 0.95,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 322
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "VaneThickness": 12
        },
        "user": {
            "YawPipeDiameter": 101.6,
            "RotorResinMargin": 10
        }
    },
    # https://www.openafpm.net/simulation/9011
    "1.2N MWT Hoverboard 16 pole 24V": {
        "description": (
            "1.2 meter diameter wind turbine with T-shape frame and Neodymium magnets. " +
            "Useful for testing small turbines and coil winder."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiameter": 1200,
            "RotorDiskRadius": 80.05,
            "RotorDiskInnerRadius": 54.89,
            "RotorDiskThickness": 5,
            "MagnetLength": 25,
            "MagnetWidth": 10,
            "MagnetThickness": 8,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 16,
            "StatorThickness": 8,
            "CoilType": 1,
            "CoilLegWidth": 9.36,
            "CoilHoleWidthAtOuterRadius": 10,
            "CoilHoleWidthAtInnerRadius": 10,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 11.56,
            "NumberOfCoilsPerPhase": 4,
            "WireWeight": 0.46,
            "WireDiameter": 0.71,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 103
          },
          "furling": {
            "VerticalPlaneAngle": 15,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 150,
            "BracketWidth": 20,
            "BracketThickness": 5,
            "BoomLength": 700,
            "BoomPipeDiameter": 33.4,
            "BoomPipeThickness": 3,
            "VaneThickness": 6,
            "VaneLength": 500,
            "VaneWidth": 200,
            "Offset": 69
          },
          "user": {
            "BladeWidth": 140,
            "HubPitchCircleDiameter": 50,
            "RotorDiskCentralHoleDiameter": 35,
            "HolesDiameter": 8,
            "MetalLengthL": 40,
            "MetalThicknessL": 5,
            "FlatMetalThickness": 5,
            "YawPipeDiameter": 48.3,
            "PipeThickness": 3,
            "RotorResinMargin": 5,
            "HubHolesDiameter": 8
          }
    },
    "1.8m 46x30x10mm magnets": {
        "description": (
            "1.8 meter diameter wind turbine based on 'A Wind Turbine Recipe Book (2014)' by Hugh Piggott. " +
            "Useful for testing single rotor and metal disk rotor topology."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiameter": 1800,
            "RotorTopology": "Single and metal disk",
            "RotorDiskRadius": 129.36,
            "RotorDiskInnerRadius": 82.48,
            "RotorDiskThickness": 6,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 8,
            "StatorThickness": 13,
            "CoilType": 1,
            "CoilLegWidth": 28.17,
            "CoilHoleWidthAtOuterRadius": 30,
            "CoilHoleWidthAtInnerRadius": 30,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 34.78,
            "NumberOfCoilsPerPhase": 2,
            "WireWeight": 3.07,
            "WireDiameter": 1.32,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 147.0
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 300,
            "BracketWidth": 30,
            "BracketThickness": 5,
            "BoomLength": 800,
            "BoomPipeDiameter": 48.3,
            "BoomPipeThickness": 5,
            "VaneThickness": 6,
            "VaneLength": 1000,
            "VaneWidth": 400,
            "Offset": 100
        },
        "user": {
            "BladeWidth": 95,
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
    "1.2m 46x30x10mm magnets": {
        "description": (
            "1.2 meter diameter wind turbine based on 'A Wind Turbine Recipe Book (2014)' by Hugh Piggott. " +
            "Useful for testing single rotor topology."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiameter": 1200,
            "RotorTopology": "Single",
            "RotorDiskRadius": 112.14,
            "RotorDiskInnerRadius": 65.13,
            "RotorDiskThickness": 6,
            "MagnetLength": 46,
            "MagnetWidth": 30,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "NumberMagnet": 8,
            "StatorThickness": 10,
            "CoilType": 1,
            "CoilLegWidth": 19.08,
            "CoilHoleWidthAtOuterRadius": 30,
            "CoilHoleWidthAtInnerRadius": 30,
            "MechanicalClearance": 3,
            "InnerDistanceBetweenMagnets": 21.15,
            "NumberOfCoilsPerPhase": 2,
            "WireWeight": 1.41,
            "WireDiameter": 0.9,
            "NumberOfWiresInHand": 1,
            "TurnsPerCoil": 164.0
        },
        "furling": {
            "VerticalPlaneAngle": 20,
            "HorizontalPlaneAngle": 55,
            "BracketLength": 200,
            "BracketWidth": 30,
            "BracketThickness": 5,
            "BoomLength": 700,
            "BoomPipeDiameter": 33.4,
            "BoomPipeThickness": 5,
            "VaneThickness": 6,
            "VaneLength": 500,
            "VaneWidth": 200,
            "Offset": 100
        },
        "user": {
            "BladeWidth": 95,
            "HubPitchCircleDiameter": 70,
            "RotorDiskCentralHoleDiameter": 35,
            "HolesDiameter": 8,
            "MetalLengthL": 40,
            "MetalThicknessL": 5,
            "FlatMetalThickness": 5,
            "YawPipeDiameter": 48.3,
            "PipeThickness": 3,
            "RotorResinMargin": 5,
            "HubHolesDiameter": 8
        }
    },
    "Magnet Width > Length, Rectangular Coil": {
        "description": (
            "Turbine with magnet width greater than magnet length and rectangular coils. " +
            "Useful for testing magnets overlapping coils & coil winder."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiskRadius": 150.78,
            "RotorDiskInnerRadius": 119.02,
            "MagnetLength": 30,
            "MagnetWidth": 46,
            "MagnetThickness": 10,
            "NumberMagnet": 12,
            "CoilType": 1,
            "CoilLegWidth": 18.52,
            "CoilHoleWidthAtOuterRadius": 46,
            "CoilHoleWidthAtInnerRadius": 46,
            "InnerDistanceBetweenMagnets": 16.3162,
            "WireWeight": 2.6,
            "WireDiameter": 1.4,
            "NumberOfWiresInHand": 2,
            "TurnsPerCoil": 43
        }
    },
    "Magnet Width > Length, Keyhole Coil": {
        "description": (
            "Turbine with magnet width greater than magnet length and keyhole coils. " +
            "Useful for testing magnets overlapping coils & coil winder."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiskRadius": 143.69,
            "RotorDiskInnerRadius": 111.84,
            "MagnetLength": 30,
            "MagnetWidth": 46,
            "MagnetThickness": 10,
            "NumberMagnet": 12,
            "CoilType": 2,
            "CoilLegWidth": 21,
            "CoilHoleWidthAtOuterRadius": 56.14,
            "CoilHoleWidthAtInnerRadius": 35.42,
            "InnerDistanceBetweenMagnets": 12.5582,
            "WireWeight": 2.65,
            "WireDiameter": 1.5,
            "TurnsPerCoil": 42
        }
    },
    "Magnet Width > Length, Triangular Coil": {
        "description": (
            "Turbine with magnet width greater than magnet length and triangular coils. " +
            "Useful for testing magnets overlapping coils & coil winder." +
            "Also uses outer magnet jig with neodymium magnets, " +
            "and triangular coils with a reduced coil leg width."
        ),
        "inheritsFrom": "T Shape",
        "magnafpm": {
            "RotorDiskRadius": 187.93,
            "RotorDiskInnerRadius": 134.65,
            "MagnetLength": 50,
            "MagnetWidth": 70,
            "MagnetThickness": 10,
            "MagnetMaterial": "NdFeB N40",
            "CoilType": 3,
            "CoilLegWidth": 12.38,
            "CoilHoleWidthAtOuterRadius": 70,
            "CoilHoleWidthAtInnerRadius": 8,
            "InnerDistanceBetweenMagnets": 0.5,
            "WireWeight": 2.28,
            "WireDiameter": 1.5,
            "TurnsPerCoil": 25
        }
    }
}
