
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
    """Thickness of rotor disk.
    
    See "Rotor Disk Thickness" section at:
        https://openafpm.net/design-tips
    """

    MagnetLength: float
    """Length of magnet."""

    MagnetWidth: float
    """Width of magnet."""

    MagnetThickness: float
    """Thickness of magnet.
    
    See "Magnet Thickness" section at:
        https://openafpm.net/design-tips
    """

    NumberMagnet: int  # NumberOfMagnets
    """Number of magnets."""

    StatorThickness: float
    """Thickness of stator."""

    CoilLegWidth: float
    """Distance from the inner-most edge, surrounding the hole, to the outer-most edge of the coil.
    
    See "Wire sizes and power losses" section on page 55 of "A Wind Turbine Recipe Book (2014)".
    """

    CoilInnerWidth1: float  # CoilHoleOuterWidth
    """Outer width of coil hole with respect to center of rotor disk.
    
    In conjuction with CoilInnerWidth2, controls the shape of the inner hole and type of coil:

    * rectangular
    * keyhole
    * or triangular

    See Winding Type section at:
        https://openafpm.net/design-tips

    This is "Coil hole at R in" in Winding Type diagram.
    """

    CoilInnerWidth2: float  # CoilHoleInnerWidth
    """Inner width of coil hole with respect to center of rotor disk.
    
    In conjuction with CoilInnerWidth1, controls the shape of the inner hole and type of coil:

    * rectangular
    * keyhole
    * or triangular

    See Winding Type section at:
        https://openafpm.net/design-tips

    This is "Coil hole at R out" in Winding Type diagram.
    """

    MechanicalClearance: float
    """Air gap distance between stator and one rotor disk."""


class FurlingParameters(TypedDict):
    """Furling Parameters."""

    VerticalPlaneAngle: float  # TailHingeAngle?
    """Angle between outer pipe of yaw-bearing and inner pipe of tail hinge.
    
    See "The inclined hinge" section on pages 30 - 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomLength: float  # BoomPipeLength
    """Length of tail boom pipe.
    
    See "Tail boom" section on page 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomPipeRadius: float
    """Inner radius of tail boom pipe.
    
    See "Tail boom" section on page 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomPipeThickness: float
    """Thickness of tail boom pipe."""

    VaneLength: float
    """Length of vane."""

    VaneWidth: float
    """Width of vane."""

    VaneThickness: float
    """Thickness of vane."""

    BracketLength: float  # VaneBracketLength
    """Length of vane brackets."""

    BracketWidth: float  # VaneBracketWidth
    """Width of vane brackets."""

    BracketThickness: float  # VaneBracketThickness
    """Thickness of vane brackets."""

    Offset: float  # AlternatorOffset?
    """Distance from center of alternator to yaw-bearing for furling action.

    For T shape, Offset is used in calculation of X.
    
    Where X is described on the right-hand side of page 26 of "A Wind Turbine Recipe Book (2014)".
    
    For H Shape, see "Mounting the alternator to the yaw bearing" section on page 27 of "A Wind Turbine Recipe Book (2014)".

    Notably, the diagram on the left-hand side of page 29.
    """


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
    """Margin of resin to surround and protect the outer edge of the magnets.
    
    See left-hand side of page 42 of "A Wind Turbine Recipe Book (2014)".
    """

    HubHolesPlacement: float  # HubHolesCircumradius
    """Distance between center of hub hole and center of hub."""

    HubHoles: float  # HubHoleRadius
    """Radius of hub holes."""

    HorizontalPlaneAngle: float
    """Angle of the alernator frame from a horizontal plane when welding the tail hinge.
    
    See "The inclined hinge" section on pages 30 - 31 of "A Wind Turbine Recipe Book (2014)".
    """
