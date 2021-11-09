
"""Module containing parameter group definitions.
"""

from typing import TypedDict

__all__ = [
    'MagnafpmParameters',
    'FurlingParameters',
    'UserParameters',
]


class MagnafpmParameters(TypedDict):
    """Parameters from the MagnAFPM tool."""

    RotorDiskRadius: float
    """Radius of rotor disk."""

    DiskThickness: float  # RotorDiskThickness
    """Thickness of rotor disk."""

    MagnetLength: float
    """Length of magnet."""

    MagnetWidth: float
    """Width of magnet."""

    MagnetThickness: float
    """Thickness of magnet."""

    NumberMagnet: int  # NumberOfMagnets
    """Number of magnets."""

    StatorThickness: float
    """Thickness of stator."""

    CoilLegWidth: float
    """Distance from the inner-most edge, surrounding the hole, to the outer-most edge of the coil."""

    CoilInnerWidth1: float  # CoilHoleOuterWidth
    """Outer width of coil hole with respect to center of rotor disk."""

    CoilInnerWidth2: float  # CoilHoleInnerWidth
    """Inner width of coil hole with respect to center of rotor disk."""

    MechanicalClearance: float
    """Air gap distance between stator and one rotor disk."""


class FurlingParameters(TypedDict):
    """Furling Parameters."""

    VerticalPlaneAngle: float  # TailHingeAngle?
    """Angle between outer pipe of yaw-bearing and inner pipe of tail hinge."""

    BracketLength: float  # VaneBracketLength
    """Length of vane brackets."""

    BracketWidth: float  # VaneBracketWidth
    """Width of vane brackets."""

    BracketThickness: float  # VaneBracketThickness
    """Thickness of vane brackets."""

    BoomLength: float  # BoomPipeLength
    """Length of tail boom pipe."""

    BoomPipeRadius: float
    """Inner radius of tail boom pipe."""

    BoomPipeThickness: float
    """Thickness of tail boom pipe."""

    VaneLength: float
    """Length of vane."""

    VaneWidth: float
    """Width of vane."""

    VaneThickness: float
    """Thickness of vane."""

    Offset: float  # AlternatorOffset?
    """Distance from stub axle shaft to yaw-bearing for furling action."""


class UserParameters(TypedDict):
    """User Parameters."""

    RotorInnerCircle: float  # RotorDiskInnerHoleRadius
    """Inner hole radius of the rotor disk."""

    Holes: float  # HoleRadius
    """Radius of various holes like stator mounting holes and vane bracket holes."""

    MetalLengthL: float  # AngleBarLength
    """Width of angle bars used in frame."""

    MetalThicknessL: float  # AngleBarThickness
    """Thickness of angle bars used in frame."""

    FlatMetalThickness: float
    """Thickness of various metal pieces."""

    YawPipeRadius: float
    """Radius of yaw bearing pipe including thickness."""

    PipeThickness: float
    """Thickness of yaw bearing and tail hinge pipes."""

    ResineRotorMargin: float  # RotorResinCastMargin
    """Margin of resin to surround and protect the outer edge of the magnets."""

    HubHolesPlacement: float  # HubHolesCircumradius
    """Distance between center of hub hole and center of hub."""

    HubHoles: float  # HubHoleRadius
    """Radius of hub holes."""

    HorizontalPlaneAngle: float
    """Angle of the alernator from a horizontal plane when welding the tail hinge."""
