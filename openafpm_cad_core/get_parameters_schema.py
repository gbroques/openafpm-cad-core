"""
Module to generate JSON schema document describing parameters
for validation purposes.

See JSON Schema:
https://json-schema.org/understanding-json-schema/
"""

from typing import List, get_type_hints

from .get_default_parameters import get_default_parameters
from .get_docstring_by_key import get_docstring_by_key
from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters
from .pipe_size import PipeSize
from .wind_turbine_shape import (
    WindTurbineShape,
)

MIN_NUMBER_MAGNET = 4
MAX_NUMBER_MAGNET = 32


def get_parameters_schema(wind_turbine_shape: WindTurbineShape) -> dict:
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_flat_metal_thickness = default_parameters["user"]["FlatMetalThickness"]
    default_rotor_disk_central_hole_diameter = default_parameters["user"][
        "RotorDiskCentralHoleDiameter"
    ]
    default_hub_holes_diameter = default_parameters["user"]["HubHolesDiameter"]
    default_hub_pitch_circle_diameter = default_parameters["user"][
        "HubPitchCircleDiameter"
    ]
    default_holes_diameter = default_parameters["user"]["HolesDiameter"]
    default_rotor_resin_margin = default_parameters["user"]["RotorResinMargin"]

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "description": "Parameters describing the wind turbine model categorized into three broad groups.",
        "properties": {
            "magnafpm": {
                "type": "object",
                "description": "Parameters from the MagnAFPM tool.",
                "properties": {
                    "RotorDiameter": {
                        "title": "Rotor Diameter",
                        "description": get_description("magnafpm", "RotorDiameter"),
                        "minimum": 1200,
                        "maximum": 7000,
                        **get_numeric_type_and_multiple_of("magnafpm", "RotorDiameter"),
                    },
                    "RotorTopology": {
                        "title": "Rotor Topology",
                        "description": get_description("magnafpm", "RotorTopology"),
                        "type": get_type("magnafpm", "RotorTopology"),
                        "enum": ["Double", "Single and metal disk", "Single"],
                    },
                    "RotorDiskRadius": {
                        "title": "Rotor Disk Radius",
                        "description": get_description("magnafpm", "RotorDiskRadius"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "RotorDiskRadius"
                        ),
                    },
                    "RotorDiskInnerRadius": {
                        "title": "Rotor Disk Inner Radius",
                        "description": get_description(
                            "magnafpm", "RotorDiskInnerRadius"
                        ),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "RotorDiskInnerRadius"
                        ),
                    },
                    "RotorDiskThickness": {
                        "title": "Rotor Disk Thickness",
                        "description": get_description(
                            "magnafpm", "RotorDiskThickness"
                        ),
                        "minimum": 3,
                        "maximum": 16,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "RotorDiskThickness"
                        ),
                    },
                    "MagnetLength": {
                        "title": "Magnet Length",
                        "description": get_description("magnafpm", "MagnetLength"),
                        "minimum": 5,
                        "maximum": 150,
                        **get_numeric_type_and_multiple_of("magnafpm", "MagnetLength"),
                    },
                    "MagnetWidth": {
                        "title": "Magnet Width",
                        "description": get_description("magnafpm", "MagnetWidth"),
                        "minimum": 5,
                        "maximum": 150,
                        **get_numeric_type_and_multiple_of("magnafpm", "MagnetWidth"),
                    },
                    "MagnetThickness": {
                        "title": "Magnet Thickness",
                        "description": get_description("magnafpm", "MagnetThickness"),
                        "minimum": 2,
                        "maximum": 50,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "MagnetThickness"
                        ),
                    },
                    "MagnetMaterial": {
                        "title": "Magnet Material",
                        "description": get_description("magnafpm", "MagnetMaterial"),
                        "type": get_type("magnafpm", "MagnetMaterial"),
                        "enum": [
                            "Ferrite C8",
                            "NdFeB N35",
                            "NdFeB N40",
                            "NdFeB N42",
                            "NdFeB N45",
                            "NdFeB N52",
                        ],
                    },
                    "NumberMagnet": {
                        "title": "Number Magnet",
                        "description": get_description("magnafpm", "NumberMagnet"),
                        "type": get_type("magnafpm", "NumberMagnet"),
                        "enum": multiples_of(4, MIN_NUMBER_MAGNET, MAX_NUMBER_MAGNET),
                    },
                    "StatorThickness": {
                        "title": "Stator Thickness",
                        "description": get_description("magnafpm", "StatorThickness"),
                        "minimum": 6,
                        "maximum": 21,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "StatorThickness"
                        ),
                    },
                    "CoilType": {
                        "title": "Coil Type",
                        "description": get_description("magnafpm", "CoilType"),
                        "type": get_type("magnafpm", "CoilType"),
                        "enum": [1, 2, 3],
                    },
                    "CoilLegWidth": {
                        "title": "Coil Leg Width",
                        "description": get_description("magnafpm", "CoilLegWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("magnafpm", "CoilLegWidth"),
                    },
                    "CoilHoleWidthAtOuterRadius": {
                        "title": "Coil Hole Width at Outer Radius",
                        "description": get_description(
                            "magnafpm", "CoilHoleWidthAtOuterRadius"
                        ),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "CoilHoleWidthAtOuterRadius"
                        ),
                    },
                    "CoilHoleWidthAtInnerRadius": {
                        "title": "Coil Hole Width at Inner Radius",
                        "description": get_description(
                            "magnafpm", "CoilHoleWidthAtInnerRadius"
                        ),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "CoilHoleWidthAtInnerRadius"
                        ),
                    },
                    "MechanicalClearance": {
                        "title": "Mechanical Clearance",
                        "description": get_description(
                            "magnafpm", "MechanicalClearance"
                        ),
                        "minimum": 0.5,
                        "maximum": 7,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "MechanicalClearance"
                        ),
                    },
                    "InnerDistanceBetweenMagnets": {
                        "title": "Inner Distance Between Magnets",
                        "description": get_description(
                            "magnafpm", "InnerDistanceBetweenMagnets"
                        ),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "InnerDistanceBetweenMagnets"
                        ),
                    },
                    "NumberOfCoilsPerPhase": {
                        "title": "Number of Coils per Phase",
                        "description": get_description(
                            "magnafpm", "NumberOfCoilsPerPhase"
                        ),
                        "minimum": MIN_NUMBER_MAGNET // 4,
                        # Number of coils (=NumberMagnet * 3/4) divided by 3, for a three-phase stator.
                        "maximum": MAX_NUMBER_MAGNET // 4,
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "NumberOfCoilsPerPhase"
                        ),
                    },
                    "WireWeight": {
                        "title": "Wire Weight",
                        "description": get_description("magnafpm", "WireWeight"),
                        **get_numeric_type_and_multiple_of("magnafpm", "WireWeight"),
                    },
                    "WireDiameter": {
                        "title": "Wire Diameter",
                        "description": get_description("magnafpm", "WireDiameter"),
                        **get_numeric_type_and_multiple_of("magnafpm", "WireDiameter"),
                    },
                    "NumberOfWiresInHand": {
                        "title": "Number of Wires in Hand",
                        "description": get_description(
                            "magnafpm", "NumberOfWiresInHand"
                        ),
                        **get_numeric_type_and_multiple_of(
                            "magnafpm", "NumberOfWiresInHand"
                        ),
                    },
                    "TurnsPerCoil": {
                        "title": "Turns per Coil",
                        "description": get_description("magnafpm", "TurnsPerCoil"),
                        **get_numeric_type_and_multiple_of("magnafpm", "TurnsPerCoil"),
                    },
                },
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
                        **get_numeric_type_and_multiple_of(
                            "furling", "VerticalPlaneAngle"
                        ),
                    },
                    "HorizontalPlaneAngle": {
                        "title": "Horizontal Plane Angle",
                        "description": get_description(
                            "furling", "HorizontalPlaneAngle"
                        ),
                        "minimum": 0,
                        "maximum": 360,
                        **get_numeric_type_and_multiple_of(
                            "furling", "HorizontalPlaneAngle"
                        ),
                    },
                    "BracketLength": {
                        "title": "Bracket Length",
                        "description": get_description("furling", "BracketLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BracketLength"),
                    },
                    "BracketWidth": {
                        "title": "Bracket Width",
                        "description": get_description("furling", "BracketWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BracketWidth"),
                    },
                    "BracketThickness": {
                        "title": "Bracket Thickness",
                        "description": get_description("furling", "BracketThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of(
                            "furling", "BracketThickness"
                        ),
                    },
                    "BoomLength": {
                        "title": "Boom Length",
                        "description": get_description("furling", "BoomLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "BoomLength"),
                    },
                    "BoomPipeDiameter": {
                        "title": "Boom Pipe Diameter",
                        "description": get_description("furling", "BoomPipeDiameter"),
                        "type": get_type("furling", "BoomPipeDiameter"),
                        "enum": [pipe_size.value for pipe_size in list(PipeSize)],
                    },
                    "BoomPipeThickness": {
                        "title": "Boom Pipe Thickness",
                        "description": get_description("furling", "BoomPipeThickness"),
                        "minimum": 0,
                        "maximum": 6,
                        **get_numeric_type_and_multiple_of(
                            "furling", "BoomPipeThickness"
                        ),
                    },
                    "VaneThickness": {
                        "title": "Vane Thickness",
                        "description": get_description("furling", "VaneThickness"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneThickness"),
                    },
                    "VaneLength": {
                        "title": "Vane Length",
                        "description": get_description("furling", "VaneLength"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneLength"),
                    },
                    "VaneWidth": {
                        "title": "Vane Width",
                        "description": get_description("furling", "VaneWidth"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "VaneWidth"),
                    },
                    "Offset": {
                        "title": "Offset",
                        "description": get_description("furling", "Offset"),
                        "minimum": 0,
                        **get_numeric_type_and_multiple_of("furling", "Offset"),
                    },
                },
            },
            "user": {
                "type": "object",
                "description": (
                    "Parameters with default values "
                    + "that may be overridden by users to meet individual needs."
                ),
                "properties": {
                    "WindTurbineShape": {
                        "title": "Wind Turbine Shape",
                        "description": get_description("user", "WindTurbineShape"),
                        "type": get_type("user", "WindTurbineShape"),
                        "enum": [
                            "Calculated",
                            WindTurbineShape.T.value.split()[0],
                            WindTurbineShape.H.value.split()[0],
                            WindTurbineShape.STAR.value.split()[0],
                        ],
                    },
                    "BladeWidth": {
                        "title": "Blade Width",
                        "description": get_description("user", "BladeWidth"),
                        # TODO: Set minimum and maximum based on RotorDiameter
                        # These are calculated in blade_cells.py
                        # MinimumBladeWidth
                        # =0.055 * RotorDiameter - 8
                        # BladeTemplateDim_V
                        # =round(0.086 * RotorDiameter - 10.669)
                        "minimum": 0,
                        "maximum": 380,
                        **get_numeric_type_and_multiple_of("user", "BladeWidth"),
                    },
                    "HubPitchCircleDiameter": {
                        "title": "Hub Pitch Circle Diameter",
                        "description": get_description(
                            "user", "HubPitchCircleDiameter"
                        ),
                        "minimum": get_hub_pitch_circle_diameter_minimum(
                            wind_turbine_shape
                        ),
                        "maximum": default_hub_pitch_circle_diameter + 40,
                        **get_numeric_type_and_multiple_of(
                            "user", "HubPitchCircleDiameter"
                        ),
                    },
                    "RotorDiskCentralHoleDiameter": {
                        "title": "Rotor Disk Central Hole Diameter",
                        "description": get_description(
                            "user", "RotorDiskCentralHoleDiameter"
                        ),
                        "minimum": default_rotor_disk_central_hole_diameter - 30,
                        "maximum": default_rotor_disk_central_hole_diameter + 5,
                        **get_numeric_type_and_multiple_of(
                            "user", "RotorDiskCentralHoleDiameter"
                        ),
                    },
                    "HolesDiameter": {
                        "title": "Holes Diameter",
                        "description": get_description("user", "HolesDiameter"),
                        "minimum": get_holes_diameter_minimum(wind_turbine_shape),
                        "maximum": default_holes_diameter + 2,
                        **get_numeric_type_and_multiple_of("user", "HolesDiameter", 2),
                    },
                    "MetalLengthL": {
                        "title": "Metal Length L",
                        "description": get_description("user", "MetalLengthL"),
                        "type": get_type("user", "MetalLengthL"),
                        "minimum": get_metal_length_l_minimum(wind_turbine_shape),
                        "maximum": get_metal_length_l_maximum(wind_turbine_shape),
                        "multipleOf": 10,
                    },
                    "MetalThicknessL": {
                        "title": "Metal Thickness L",
                        "description": get_description("user", "MetalThicknessL"),
                        "minimum": get_metal_thickness_l_minimum(wind_turbine_shape),
                        "maximum": get_metal_thickness_l_maximum(wind_turbine_shape),
                        **get_numeric_type_and_multiple_of("user", "MetalThicknessL"),
                    },
                    "FlatMetalThickness": {
                        "title": "Flat Metal Thickness",
                        "minimum": get_flat_metal_thickness_minimum(wind_turbine_shape),
                        "maximum": default_flat_metal_thickness + 3,
                        **get_numeric_type_and_multiple_of(
                            "user", "FlatMetalThickness"
                        ),
                    },
                    "YawPipeDiameter": {
                        "title": "Yaw Pipe Diameter",
                        "description": get_description("user", "YawPipeDiameter"),
                        "type": get_type("user", "YawPipeDiameter"),
                        "enum": get_yaw_pipe_diameter_enum(wind_turbine_shape),
                    },
                    "PipeThickness": {
                        "title": "Pipe Thickness",
                        "description": get_description("user", "PipeThickness"),
                        "minimum": get_pipe_thickness_minimum(wind_turbine_shape),
                        "maximum": get_pipe_thickness_maximum(wind_turbine_shape),
                        **get_numeric_type_and_multiple_of("user", "PipeThickness"),
                    },
                    "RotorResinMargin": {
                        "title": "Rotor Resin Margin",
                        "description": get_description("user", "RotorResinMargin"),
                        "minimum": default_rotor_resin_margin,
                        "maximum": default_rotor_resin_margin + 5,
                        **get_numeric_type_and_multiple_of("user", "RotorResinMargin"),
                    },
                    "HubHolesDiameter": {
                        "title": "Hub Holes Diameter",
                        "description": get_description("user", "HubHolesDiameter"),
                        "minimum": get_hub_holes_diameter_minimum(wind_turbine_shape),
                        "maximum": default_hub_holes_diameter + 2,
                        **get_numeric_type_and_multiple_of(
                            "user", "HubHolesDiameter", 2
                        ),
                    },
                },
            },
        },
    }


def get_numeric_type_and_multiple_of(
    group_name: str, parameter_name: str, integer_mulitple_of: int = 1
) -> dict:
    json_schema_type = get_type(group_name, parameter_name)
    multiple_of = get_multiple_of(json_schema_type, integer_mulitple_of)
    return {"type": json_schema_type, "multipleOf": multiple_of}


def get_multiple_of(json_schema_type: str, integer_mulitple_of: int = 1) -> float:
    if json_schema_type == "integer":
        return integer_mulitple_of
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
        return "string"
    elif type_hint == int:
        return "integer"
    elif type_hint == float:
        return "number"
    elif type_hint == dict:
        return "object"
    elif type_hint == list:
        return "array"
    elif type_hint == bool:
        return "boolean"
    else:
        return "null"


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
        "magnafpm": MagnafpmParameters,
        "furling": FurlingParameters,
        "user": UserParameters,
    }


def multiples_of(integer: int, start: int, end: int) -> List[int]:
    return list(range(start, end + 1, integer))


def get_pipe_sizes() -> List[float]:
    return [pipe_size.value for pipe_size in list(PipeSize)]


def get_yaw_pipe_diameter_enum(wind_turbine_shape: WindTurbineShape) -> List[float]:
    """Get default diameter and one size up.

    For T Shape, also allow one size down from the default.
    """
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_yaw_pipe_diameter = default_parameters["user"]["YawPipeDiameter"]
    pipe_sizes = get_pipe_sizes()
    index = pipe_sizes.index(default_yaw_pipe_diameter)
    start = index - 1 if wind_turbine_shape == WindTurbineShape.T else index
    end = index + 2
    return pipe_sizes[start:end]


def get_pipe_thickness_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 3
    elif wind_turbine_shape == WindTurbineShape.H:
        return 4
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 5
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_pipe_thickness_maximum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 5
    elif wind_turbine_shape == WindTurbineShape.H:
        return 6
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 8
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_hub_pitch_circle_diameter_minimum(
    wind_turbine_shape: WindTurbineShape,
) -> float:
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_hub_pitch_circle_diameter = default_parameters["user"][
        "HubPitchCircleDiameter"
    ]
    if wind_turbine_shape == WindTurbineShape.T:
        return default_hub_pitch_circle_diameter - 50
    else:
        return default_hub_pitch_circle_diameter - 10


def get_holes_diameter_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_holes_diameter = default_parameters["user"]["HolesDiameter"]
    if wind_turbine_shape == WindTurbineShape.T:
        return default_holes_diameter - 4
    else:
        return default_holes_diameter - 2


def get_hub_holes_diameter_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_hub_holes_diameter = default_parameters["user"]["HubHolesDiameter"]
    if wind_turbine_shape == WindTurbineShape.T:
        return default_hub_holes_diameter - 4
    else:
        return default_hub_holes_diameter - 2


def get_metal_length_l_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 40
    elif wind_turbine_shape == WindTurbineShape.H:
        return 50
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 60
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_metal_length_l_maximum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 60
    elif wind_turbine_shape == WindTurbineShape.H:
        return 70
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 100
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_metal_thickness_l_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 5
    elif wind_turbine_shape == WindTurbineShape.H:
        return 5
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 6
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_metal_thickness_l_maximum(wind_turbine_shape: WindTurbineShape) -> float:
    if wind_turbine_shape == WindTurbineShape.T:
        return 6
    elif wind_turbine_shape == WindTurbineShape.H:
        return 7
    elif wind_turbine_shape == WindTurbineShape.STAR:
        return 10
    else:
        raise ValueError(
            f'"{wind_turbine_shape}" not supported. '
            + f"Must be one of {WindTurbineShape.T}, {WindTurbineShape.H}, or {WindTurbineShape.STAR}."
        )


def get_flat_metal_thickness_minimum(wind_turbine_shape: WindTurbineShape) -> float:
    default_parameters = get_default_parameters(wind_turbine_shape)
    default_flat_metal_thickness = default_parameters["user"]["FlatMetalThickness"]
    if wind_turbine_shape == WindTurbineShape.T:
        return default_flat_metal_thickness - 5
    else:
        return default_flat_metal_thickness - 2
