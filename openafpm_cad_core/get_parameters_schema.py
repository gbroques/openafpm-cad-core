"""
Module to generate JSON schema document describing parameters
for validation purposes.

See JSON Schema:
https://json-schema.org/understanding-json-schema/
"""
from typing import List, get_type_hints

from .get_docstring_by_key import get_docstring_by_key
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .pipe_size import PipeSize

MIN_NUMBER_MAGNET = 8
MAX_NUMBER_MAGNET = 32


def get_parameters_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "description": "Parameters describing the wind turbine model categorized into three broad groups.",
        "properties": {
            "magnafpm": {
                "type": "object",
                "description": "Parameters from the MagnAFPM tool.",
                "properties": {
                    "RotorDiskRadius": {
                        "title": "Rotor Disk Radius",
                        "description": get_description("magnafpm", "RotorDiskRadius"),
                        "type": get_type("magnafpm", "RotorDiskRadius"),
                        "minimum": 0
                    },
                    "RotorDiskInnerRadius": {
                        "title": "Rotor Disk Inner Radius",
                        "description": get_description("magnafpm", "RotorDiskInnerRadius"),
                        "type": get_type("magnafpm", "RotorDiskInnerRadius"),
                        "minimum": 0
                    },
                    "DiskThickness": {
                        "title": "Disk Thickness",
                        "description": get_description("magnafpm", "DiskThickness"),
                        "type": get_type("magnafpm", "DiskThickness"),
                        "minimum": 0
                    },
                    "MagnetLength": {
                        "title": "Magnet Length",
                        "description": get_description("magnafpm", "MagnetLength"),
                        "type": get_type("magnafpm", "MagnetLength"),
                        "minimum": 0
                    },
                    "MagnetWidth": {
                        "title": "Magnet Width",
                        "description": get_description("magnafpm", "MagnetWidth"),
                        "type": get_type("magnafpm", "MagnetWidth"),
                        "minimum": 0
                    },
                    "MagnetThickness": {
                        "title": "Magnet Thickness",
                        "description": get_description("magnafpm", "MagnetThickness"),
                        "type": get_type("magnafpm", "MagnetThickness"),
                        "minimum": 0
                    },
                    "MagnetMaterial": {
                        "title": "Magnet Material",
                        "description": get_description("magnafpm", "MagnetMaterial"),
                        "type": get_type("magnafpm", "MagnetMaterial"),
                        "enum": ["Neodymium", "Ferrite"]
                    },
                    "NumberMagnet": {
                        "title": "Number Magnet",
                        "description": get_description("magnafpm", "NumberMagnet"),
                        "type": get_type("magnafpm", "NumberMagnet"),
                        "enum": multiples_of(4, MIN_NUMBER_MAGNET, MAX_NUMBER_MAGNET)
                    },
                    "StatorThickness": {
                        "title": "Stator Thickness",
                        "description": get_description("magnafpm", "StatorThickness"),
                        "type": get_type("magnafpm", "StatorThickness"),
                        "minimum": 0
                    },
                    "CoilType": {
                        "title": "Coil Type",
                        "description": get_description("magnafpm", "CoilType"),
                        "type": get_type("magnafpm", "CoilType"),
                        "enum": [1, 2, 3]
                    },
                    "CoilLegWidth": {
                        "title": "Coil Leg Width",
                        "description": get_description("magnafpm", "CoilLegWidth"),
                        "type": get_type("magnafpm", "CoilLegWidth"),
                        "minimum": 0
                    },
                    "CoilInnerWidth1": {
                        "title": "Coil Inner Width 1",
                        "description": get_description("magnafpm", "CoilInnerWidth1"),
                        "type": get_type("magnafpm", "CoilInnerWidth1"),
                        "minimum": 0
                    },
                    "CoilInnerWidth2": {
                        "title": "Coil Inner Width 2",
                        "description": get_description("magnafpm", "CoilInnerWidth2"),
                        "type": get_type("magnafpm", "CoilInnerWidth2"),
                        "minimum": 0
                    },
                    "MechanicalClearance": {
                        "title": "Mechanical Clearance",
                        "description": get_description("magnafpm", "MechanicalClearance"),
                        "type": get_type("magnafpm", "MechanicalClearance"),
                        "minimum": 0
                    },
                    "InnerDistanceBetweenMagnets": {
                        "title": "Inner Distance Between Magnets",
                        "description": get_description("magnafpm", "InnerDistanceBetweenMagnets"),
                        "type": get_type("magnafpm", "InnerDistanceBetweenMagnets"),
                        "minimum": 0
                    },
                    "NumberOfCoilsPerPhase": {
                        "title": "Number of Coils per Phase",
                        "description": get_description("magnafpm", "NumberOfCoilsPerPhase"),
                        "type": get_type("magnafpm", "NumberOfCoilsPerPhase"),
                        "minimum": MIN_NUMBER_MAGNET // 4,
                        # Number of coils (=NumberMagnet * 3/4) divided by 3, for a three-phase stator.
                        "maximum": MAX_NUMBER_MAGNET // 4
                    },
                    "WireWeight": {
                        "title": "Wire Weight",
                        "description": get_description("magnafpm", "WireWeight"),
                        "type": get_type("magnafpm", "WireWeight")
                    },
                    "WireDiameter": {
                        "title": "Wire Diameter",
                        "description": get_description("magnafpm", "WireDiameter"),
                        "type": get_type("magnafpm", "WireDiameter")
                    },
                    "NumberOfWiresInHand": {
                        "title": "Number of Wires in Hand",
                        "description": get_description("magnafpm", "NumberOfWiresInHand"),
                        "type": get_type("magnafpm", "NumberOfWiresInHand")
                    },
                    "TurnsPerCoil": {
                        "title": "Turns per Coil",
                        "description": get_description("magnafpm", "TurnsPerCoil"),
                        "type": get_type("magnafpm", "TurnsPerCoil")
                    }
                }
            },
            "furling": {
                "type": "object",
                "description": "Parameters relating to the tail and 'furling' action.",
                "properties": {
                    "VerticalPlaneAngle": {
                        "title": "Vertical Plane Angle",
                        "description": get_description("furling", "VerticalPlaneAngle"),
                        "type": get_type("furling", "VerticalPlaneAngle"),
                        "minimum": 0,
                        "maximum": 360
                    },
                    "HorizontalPlaneAngle": {
                        "title": "Horizontal Plane Angle",
                        "description": get_description("furling", "HorizontalPlaneAngle"),
                        "type": get_type("furling", "HorizontalPlaneAngle"),
                        "minimum": 0,
                        "maximum": 360
                    },
                    "BracketLength": {
                        "title": "Bracket Length",
                        "description": get_description("furling", "BracketLength"),
                        "type": get_type("furling", "BracketLength"),
                        "minimum": 0
                    },
                    "BracketWidth": {
                        "title": "Bracket Width",
                        "description": get_description("furling", "BracketWidth"),
                        "type": get_type("furling", "BracketWidth"),
                        "minimum": 0
                    },
                    "BracketThickness": {
                        "title": "Bracket Thickness",
                        "description": get_description("furling", "BracketThickness"),
                        "type": get_type("furling", "BracketThickness"),
                        "minimum": 0
                    },
                    "BoomLength": {
                        "title": "Boom Length",
                        "description": get_description("furling", "BoomLength"),
                        "type": get_type("furling", "BoomLength"),
                        "minimum": 0
                    },
                    "BoomPipeDiameter": {
                        "title": "Boom Pipe Diameter",
                        "description": get_description("furling", "BoomPipeDiameter"),
                        "type": get_type("furling", "BoomPipeDiameter"),
                        "enum": [pipe_size.value for pipe_size in list(PipeSize)]
                    },
                    "BoomPipeThickness": {
                        "title": "Boom Pipe Thickness",
                        "description": get_description("furling", "BoomPipeThickness"),
                        "type": get_type("furling", "BoomPipeThickness"),
                        "minimum": 0,
                        "maximum": 6
                    },
                    "VaneThickness": {
                        "title": "Vane Thickness",
                        "description": get_description("furling", "VaneThickness"),
                        "type": get_type("furling", "VaneThickness"),
                        "minimum": 0
                    },
                    "VaneLength": {
                        "title": "Vane Length",
                        "description": get_description("furling", "VaneLength"),
                        "type": get_type("furling", "VaneLength"),
                        "minimum": 0
                    },
                    "VaneWidth": {
                        "title": "Vane Width",
                        "description": get_description("furling", "VaneWidth"),
                        "type": get_type("furling", "VaneWidth"),
                        "minimum": 0
                    },
                    "Offset": {
                        "title": "Offset",
                        "description": get_description("furling", "Offset"),
                        "type": get_type("furling", "Offset"),
                        "minimum": 0
                    }
                }
            },
            "user": {
                "type": "object",
                "description": "Parameters with default values that may be overridden by individual users to satisfy unique needs.",
                "properties": {
                    "HubHolesPlacement": {
                        "title": "Hub Holes Placement",
                        "description": get_description("user", "HubHolesPlacement"),
                        "type": get_type("user", "HubHolesPlacement"),
                        "minimum": 0
                    },
                    "RotorDiskCentralHoleDiameter": {
                        "title": "Rotor Disk Central Hole Diameter",
                        "description": get_description("user", "RotorDiskCentralHoleDiameter"),
                        "type": get_type("user", "RotorDiskCentralHoleDiameter"),
                        "minimum": 0
                    },
                    "Holes": {
                        "title": "Holes",
                        "description": get_description("user", "Holes"),
                        "type": get_type("user", "Holes"),
                        "minimum": 0
                    },
                    "MetalLengthL": {
                        "title": "Metal Length L",
                        "description": get_description("user", "MetalLengthL"),
                        "type": get_type("user", "MetalLengthL"),
                        "minimum": 0
                    },
                    "MetalThicknessL": {
                        "title": "Metal Thickness L",
                        "description": get_description("user", "MetalThicknessL"),
                        "type": get_type("user", "MetalThicknessL"),
                        "minimum": 0
                    },
                    "FlatMetalThickness": {
                        "title": "Flat Metal Thickness",
                        "description": get_description("user", "FlatMetalThickness"),
                        "type": get_type("user", "FlatMetalThickness"),
                        "minimum": 0
                    },
                    "YawPipeDiameter": {
                        "title": "Yaw Pipe Diameter",
                        "description": get_description("user", "YawPipeDiameter"),
                        "type": get_type("user", "YawPipeDiameter"),
                        "enum": [pipe_size.value for pipe_size in list(PipeSize)]
                    },
                    "PipeThickness": {
                        "title": "Pipe Thickness",
                        "description": get_description("user", "PipeThickness"),
                        "type": get_type("user", "PipeThickness"),
                        "minimum": 0,
                        "maximum": 6
                    },
                    "ResineRotorMargin": {
                        "title": "Resine Rotor Margin",
                        "description": get_description("user", "ResineRotorMargin"),
                        "type": get_type("user", "ResineRotorMargin"),
                        "minimum": 0
                    },
                    "HubHoles": {
                        "title": "Hub Holes",
                        "description": get_description("user", "HubHoles"),
                        "type": get_type("user", "HubHoles"),
                        "minimum": 0
                    }
                }
            }
        }
    }


def get_type(group_name: str, parameter_name: str) -> str:
    parameter_group_by_name = get_parameter_group_by_name()
    parameter_group = parameter_group_by_name[group_name]
    type_hints = get_type_hints(parameter_group)
    type_hint = type_hints[parameter_name]
    return map_type_to_json_schema_type(type_hint)


def map_type_to_json_schema_type(type_hint) -> str:
    """https://json-schema.org/understanding-json-schema/reference/type.html"""
    if type_hint == str:
        return 'string'
    elif type_hint == int:
        return 'integer'
    elif type_hint == float:
        return 'number'
    elif type_hint == dict:
        return 'object'
    elif type_hint == list:
        return 'array'
    elif type_hint == bool:
        return 'boolean'
    else:
        return 'null'


def get_docstring(group_name: str, parameter_name: str) -> str:
    parameter_group_by_name = get_parameter_group_by_name()
    parameter_group = parameter_group_by_name[group_name]
    docstring = get_docstring_by_key(parameter_group)
    return docstring[parameter_name]


def get_description(group_name: str, parameter_name: str) -> str:
    doctstring = get_docstring(group_name, parameter_name)
    return doctstring.splitlines()[0]


def get_parameter_group_by_name() -> dict:
    return {
        'magnafpm': MagnafpmParameters,
        'furling': FurlingParameters,
        'user': UserParameters
    }


def multiples_of(integer: int, start: int, end: int) -> List[int]:
    return list(range(start, end + 1, integer))
