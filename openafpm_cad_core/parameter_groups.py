
"""Module containing parameter group definitions.
"""

from typing import TypedDict

__all__ = [
    'MagnafpmParameters',
    'UserParameters',
    'FurlingParameters'
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

    CoilInnerWidth1: float  # CoilOuterHoleWidth
    """Outer width of coil hole with respect to center of rotor disk."""

    CoilInnerWidth2: float  # CoilInnerHoleWidth
    """Inner width of coil hole with respect to center of rotor disk."""

    MechanicalClearance: float
    """Air gap distance between stator and one rotor disk."""


class UserParameters(TypedDict):
    """User Parameters."""

    RotorInnerCircle: float # RotorDiskInnerHoleRadius
    """Inner hole radius of the rotor disk."""

    Holes: float # StatorMountHoleRadius
    """Radius of various holes like stator mounting holes and vane bracket holes."""

    MetalLengthL: float
    """Width of angle bars used in frame."""

    MetalThicknessL: float
    """Thickness of angle bars used in frame."""

    FlatMetalThickness: float
    """Thickness of various metal pieces."""

    YawPipeRadius: float
    """Radius of yaw bearing pipe including thickness."""

    PipeThickness: float
    """Thickness of yaw bearing and tail hinge pipes."""

    ResineRotorMargin: float
    """Margin of resin to surround and protect the outer edge of the magnets."""

    HubHolesPlacement: float
    """Distance between center of hub hole and center of hub."""

    HubHoles: float # HubHolesCircumradius
    """Radius of hub holes."""

    HorizontalPlaneAngle: float
    """Angle of the alernator from a horizontal plane when welding the tail hinge."""


class FurlingParameters(TypedDict):
    """Furling Parameters."""

    VerticalPlaneAngle: float  # TailHingeAngle
    """Angle between outer pipe of yaw-bearing and inner pipe of tail hinge."""

    BracketLength: float  # VaneBracketLength
    """Length of vane brackets."""

    BracketWidth: float  # VaneBracketWidth
    """Width of vane brackets."""

    BracketThickness: float  # VaneBracketThickness
    """Thickness of vane brackets."""

    BoomLength: float  # TailBoomPipeLength
    """Length of tail boom pipe."""

    BoomPipeRadius: float  # TailBoomPipeRadius
    """Inner radius of tail boom pipe."""

    BoomPipeThickness: float  # TailBoomPipeThickness
    """Thickness of tail boom pipe."""

    VaneLength: float
    """Length of vane."""

    VaneWidth: float
    """Width of vane."""

    VaneThickness: float
    """Thickness of vane."""

    Offset: float # AlternatorOffset?
    """Distance from stub axle shaft to yaw-bearing for furling action."""
