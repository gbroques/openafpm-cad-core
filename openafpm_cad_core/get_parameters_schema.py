"""
Module to generate JSON schema document describing parameters
for validation purposes.

See JSON Schema:
https://json-schema.org/understanding-json-schema/
"""
from typing import List, get_type_hints

from .get_default_parameters import get_default_parameters
from .get_docstring_by_key import get_docstring_by_key
from .map_rotor_disk_radius_to_wind_turbine import \
    map_rotor_disk_radius_to_wind_turbine
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .pipe_size import PipeSize
from .wind_turbine import WindTurbine

MIN_NUMBER_MAGNET = 8
MAX_NUMBER_MAGNET = 32


def get_parameters_schema(rotor_disk_radius: float) -> dict:
    wind_turbine = map_rotor_disk_radius_to_wind_turbine(rotor_disk_radius)
    default_parameters = get_default_parameters(wind_turbine)
    default_yaw_pipe_diameter = default_parameters['user']['YawPipeDiameter']
    default_flat_metal_thickness = default_parameters['user']['FlatMetalThickness']
    default_rotor_disk_central_hole_diameter = default_parameters[
        'user']['RotorDiskCentralHoleDiameter']
    default_hub_holes_diameter = default_parameters['user']['HubHolesDiameter']
    default_hub_pitch_circle_diameter = default_parameters['user']['HubPitchCircleDiameter']
    default_holes_diameter = default_parameters['user']['HolesDiameter']
    default_rotor_resin_margin = default_parameters['user']['RotorResinMargin']

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
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "RotorDiskRadius")
                    },
                    "RotorDiskInnerRadius": {
                        "title": "Rotor Disk Inner Radius",
                        "description": get_description("magnafpm", "RotorDiskInnerRadius"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "RotorDiskInnerRadius")
                    },
                    "RotorDiskThickness": {
                        "title": "Rotor Disk Thickness",
                        "description": get_description("magnafpm", "RotorDiskThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "RotorDiskThickness")
                    },
                    "MagnetLength": {
                        "title": "Magnet Length",
                        "description": get_description("magnafpm", "MagnetLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "MagnetLength")
                    },
                    "MagnetWidth": {
                        "title": "Magnet Width",
                        "description": get_description("magnafpm", "MagnetWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "MagnetWidth")
                    },
                    "MagnetThickness": {
                        "title": "Magnet Thickness",
                        "description": get_description("magnafpm", "MagnetThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "MagnetThickness")
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
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "StatorThickness")
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
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "CoilLegWidth")
                    },
                    "CoilInnerWidth1": {
                        "title": "Coil Inner Width 1",
                        "description": get_description("magnafpm", "CoilInnerWidth1"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "CoilInnerWidth1")

                    },
                    "CoilInnerWidth2": {
                        "title": "Coil Inner Width 2",
                        "description": get_description("magnafpm", "CoilInnerWidth2"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "CoilInnerWidth2")
                    },
                    "MechanicalClearance": {
                        "title": "Mechanical Clearance",
                        "description": get_description("magnafpm", "MechanicalClearance"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "MechanicalClearance")
                    },
                    "InnerDistanceBetweenMagnets": {
                        "title": "Inner Distance Between Magnets",
                        "description": get_description("magnafpm", "InnerDistanceBetweenMagnets"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "InnerDistanceBetweenMagnets")
                    },
                    "NumberOfCoilsPerPhase": {
                        "title": "Number of Coils per Phase",
                        "description": get_description("magnafpm", "NumberOfCoilsPerPhase"),
                        "minimum": MIN_NUMBER_MAGNET // 4,
                        # Number of coils (=NumberMagnet * 3/4) divided by 3, for a three-phase stator.
                        "maximum": MAX_NUMBER_MAGNET // 4,
                        **get_numeric_type_and_multiple_of("magnafpm", "NumberOfCoilsPerPhase")
                    },
                    "WireWeight": {
                        "title": "Wire Weight",
                        "description": get_description("magnafpm", "WireWeight"),
                        **get_numeric_type_and_multiple_of("magnafpm", "WireWeight")
                    },
                    "WireDiameter": {
                        "title": "Wire Diameter",
                        "description": get_description("magnafpm", "WireDiameter"),
                        **get_numeric_type_and_multiple_of("magnafpm", "WireDiameter")
                    },
                    "NumberOfWiresInHand": {
                        "title": "Number of Wires in Hand",
                        "description": get_description("magnafpm", "NumberOfWiresInHand"),
                        **get_numeric_type_and_multiple_of("magnafpm", "NumberOfWiresInHand")
                    },
                    "TurnsPerCoil": {
                        "title": "Turns per Coil",
                        "description": get_description("magnafpm", "TurnsPerCoil"),
                        **get_numeric_type_and_multiple_of("magnafpm", "TurnsPerCoil")
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
                        "minimum": 0,
                        "maximum": 360,
                        **get_numeric_type_and_multiple_of("furling", "VerticalPlaneAngle")
                    },
                    "HorizontalPlaneAngle": {
                        "title": "Horizontal Plane Angle",
                        "description": get_description("furling", "HorizontalPlaneAngle"),
                        "minimum": 0,
                        "maximum": 360,
                        **get_numeric_type_and_multiple_of("furling", "HorizontalPlaneAngle")
                    },
                    "BracketLength": {
                        "title": "Bracket Length",
                        "description": get_description("furling", "BracketLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BracketLength")
                    },
                    "BracketWidth": {
                        "title": "Bracket Width",
                        "description": get_description("furling", "BracketWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BracketWidth")
                    },
                    "BracketThickness": {
                        "title": "Bracket Thickness",
                        "description": get_description("furling", "BracketThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BracketThickness")
                    },
                    "BoomLength": {
                        "title": "Boom Length",
                        "description": get_description("furling", "BoomLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BoomLength")
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
                        "minimum": 0,
                        "maximum": 6,
                        **get_numeric_type_and_multiple_of("furling", "BoomPipeThickness")
                    },
                    "VaneThickness": {
                        "title": "Vane Thickness",
                        "description": get_description("furling", "VaneThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneThickness")
                    },
                    "VaneLength": {
                        "title": "Vane Length",
                        "description": get_description("furling", "VaneLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneLength")
                    },
                    "VaneWidth": {
                        "title": "Vane Width",
                        "description": get_description("furling", "VaneWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneWidth")
                    },
                    "Offset": {
                        "title": "Offset",
                        "description": get_description("furling", "Offset"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "Offset")
                    }
                }
            },
            "user": {
                "type": "object",
                "description": "Parameters with default values that may be overridden by individual users to satisfy unique needs.",
                "properties": {
                    "HubPitchCircleDiameter": {
                        "title": "Hub Holes Placement",
                        "description": get_description("user", "HubPitchCircleDiameter"),
                        "minimum": default_hub_pitch_circle_diameter - 10,
                        "maximum": default_hub_pitch_circle_diameter + 40,
                        **get_numeric_type_and_multiple_of("user", "HubPitchCircleDiameter")
                    },
                    "RotorDiskCentralHoleDiameter": {
                        "title": "Rotor Disk Central Hole Diameter",
                        "description": get_description("user", "RotorDiskCentralHoleDiameter"),
                        "minimum": default_rotor_disk_central_hole_diameter - 10,
                        "maximum": default_rotor_disk_central_hole_diameter + 5,
                        **get_numeric_type_and_multiple_of("user", "RotorDiskCentralHoleDiameter")
                    },
                    "HolesDiameter": {
                        "title": "Holes Diameter",
                        "description": get_description("user", "HolesDiameter"),
                        "minimum": default_holes_diameter - 2,
                        "maximum": default_holes_diameter + 2,
                        **get_numeric_type_and_multiple_of("user", "HolesDiameter")
                    },
                    "MetalLengthL": {
                        "title": "Metal Length L",
                        "description": get_description("user", "MetalLengthL"),
                        "type": get_type("user", "MetalLengthL"),
                        "minimum": get_metal_length_l_minimum(wind_turbine),
                        "maximum": get_metal_length_l_maximum(wind_turbine),
                        "multipleOf": 10
                    },
                    "MetalThicknessL": {
                        "title": "Metal Thickness L",
                        "description": get_description("user", "MetalThicknessL"),
                        "minimum": get_metal_thickness_l_minimum(wind_turbine),
                        "maximum": get_metal_thickness_l_maximum(wind_turbine),
                        **get_numeric_type_and_multiple_of("user", "MetalThicknessL")
                    },
                    "FlatMetalThickness": {
                        "title": "Flat Metal Thickness",
                        "minimum": default_flat_metal_thickness - 2,
                        "maximum": default_flat_metal_thickness + 3,
                        **get_numeric_type_and_multiple_of("user", "FlatMetalThickness")
                    },
                    "YawPipeDiameter": {
                        "title": "Yaw Pipe Diameter",
                        "description": get_description("user", "YawPipeDiameter"),
                        "type": get_type("user", "YawPipeDiameter"),
                        "enum": get_yaw_pipe_diameter_enum(default_yaw_pipe_diameter)
                    },
                    "PipeThickness": {
                        "title": "Pipe Thickness",
                        "description": get_description("user", "PipeThickness"),
                        "minimum": get_pipe_thickness_minimum(wind_turbine),
                        "maximum": get_pipe_thickness_maximum(wind_turbine),
                        **get_numeric_type_and_multiple_of("user", "PipeThickness")
                    },
                    "RotorResinMargin": {
                        "title": "Rotor Resin Margin",
                        "description": get_description("user", "RotorResinMargin"),
                        "minimum": default_rotor_resin_margin,
                        "maximum": default_rotor_resin_margin + 5,
                        **get_numeric_type_and_multiple_of("user", "RotorResinMargin")
                    },
                    "HubHolesDiameter": {
                        "title": "Hub Holes Diameter",
                        "description": get_description("user", "HubHolesDiameter"),
                        "minimum": default_hub_holes_diameter - 2,
                        "maximum": default_hub_holes_diameter + 2,
                        **get_numeric_type_and_multiple_of("user", "HubHolesDiameter")
                    }
                }
            }
        }
    }


def get_numeric_type_and_multiple_of(group_name: str, parameter_name: str) -> dict:
    json_schema_type = get_type(group_name, parameter_name)
    multiple_of = get_multiple_of(json_schema_type)
    return {
        'type': json_schema_type,
        'multipleOf': multiple_of
    }


def get_multiple_of(json_schema_type: str) -> str:
    if json_schema_type == 'integer':
        return 1
    else:  # number
        return 0.01


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


def get_pipe_sizes() -> List[float]:
    return [pipe_size.value for pipe_size in list(PipeSize)]


def get_yaw_pipe_diameter_enum(default_yaw_pipe_diameter: float) -> List[float]:
    """Get default diameter and one size up."""
    pipe_sizes = get_pipe_sizes()
    index = pipe_sizes.index(default_yaw_pipe_diameter)
    return pipe_sizes[index-1:index+1]


def get_pipe_thickness_minimum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 3
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 4
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 5


def get_pipe_thickness_maximum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 5
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 6
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 8


def get_metal_length_l_minimum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 50
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 50
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 60


def get_metal_length_l_maximum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 60
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 70
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 100


def get_metal_thickness_l_minimum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 5
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 5
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 6


def get_metal_thickness_l_maximum(wind_turbine: WindTurbine) -> List[float]:
    if wind_turbine == WindTurbine.T_SHAPE or wind_turbine == WindTurbine.T_SHAPE_2F:
        return 6
    elif wind_turbine == WindTurbine.H_SHAPE:
        return 7
    elif wind_turbine == WindTurbine.STAR_SHAPE:
        return 10
