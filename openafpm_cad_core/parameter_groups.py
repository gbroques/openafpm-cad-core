
"""Module containing parameter group definitions.

The wind turbine has many parameters which are organized into 3 broad categories.
"""

from typing import TypedDict

__all__ = [
    'MagnafpmParameters',
    'FurlingParameters',
    'UserParameters',
]


class MagnafpmParameters(TypedDict):
    """Parameters from the MagnAFPM tool.

    These mainly relate to:

    * the alternator (a.k.a. generator)
    * how electricity is generated
    * and (**magn**)etism.
    """
    RotorDiameter: float
    """The width of the circle swept by the rotating blades.

    Also referred to as the "turbine diameter".
    """

    RotorTopology: str
    """One of 'Double', 'Single and metal disk', and 'Single'.


    Two magnet rotors sandwiching the stator is most common.

    The single rotor is featured in the 1.2m diameter turbine,
    and the single rotor with magnet disk is featured in the 1.8m
    diameter design in "A Wind Turbine Recipe Book (2014)".

    The single rotor topologies for smaller designs is due to
    using the same 46x30x10mm magnets used in larger designs.

    A double rotor topology can be used in smaller designs by
    using smaller magnets.

    See "Rotor mounting options" section on the right-hand side of page 46 in "A Wind Turbine Recipe Book (2014)".
    """

    RotorDiskRadius: float
    """Outer radius of rotor disk(s) for the generator."""

    RotorDiskInnerRadius: float  # TODO: Rename to GeneratorInnerRadius?
    """Inner radius of the effective length of the generator."""

    RotorDiskThickness: float
    """Thickness of rotor disk.

    See "Rotor Disk Thickness" section at:
        https://openafpm.net/design-tips
    """

    MagnetLength: float  # TODO: Rename to MagnetRadialDimension?
    """Length of magnet.

    Not always the longest dimension of the magnet,
    but the radial dimension of the magnet
    (in terms of the rotor circle).
    """

    MagnetWidth: float  # TODO: Rename to MagnetTangentialDimension?
    """Width of magnet.

    Not always shorter than MagnetLength,
    but the tangential dimension of the magnet
    (in terms of the rotor circle).
    """

    MagnetThickness: float
    """Thickness of magnet.

    See "Magnet Thickness" section at:
        https://openafpm.net/design-tips
    """

    MagnetMaterial: str
    """Material of magnet: 'Neodymium' or 'Ferrite'.

    Neodymium magnets are more powerful than Ferrite magnets.

    However, Ferrite magnets are immune to corrosion and cheaper than Neodymium magnets.

    See "Number of Poles" and "Winding Type" sections at:
        https://openafpm.net/design-tips
    """

    NumberMagnet: int  # NumberOfMagnets, MagnetCount, NumberOfPoles?
    """Number of magnets per rotor disk."""

    StatorThickness: float
    """Thickness of stator."""

    CoilType: int
    """Type of coil: (1) rectangular, (2) keyhole, or (3) triangular.

    See Winding Type section at:
        https://openafpm.net/design-tips
    """

    CoilLegWidth: float
    """Distance from the inner-most edge, surrounding the hole, to the outer-most edge of the coil.

    See "Wire sizes and power losses" section on page 55 of "A Wind Turbine Recipe Book (2014)".
    """

    CoilHoleWidthAtOuterRadius: float
    """Width of coil hole at the outer radius of the effective length of the generator.

    Also corresponds to the width of the coil hole at the outer radius of the rotor disk(s).

    In conjuction with CoilHoleWidthAtInnerRadius, controls the type of coil:

    * rectangular
    * keyhole
    * or triangular

    See Winding Type section at:
        https://openafpm.net/design-tips

    "Coil hole at R out" in Winding Type diagram.
    """

    CoilHoleWidthAtInnerRadius: float
    """Width of coil hole at the inner radius of the effective length of the generator.

    Also corresponds to the width of the coil hole at the outer radius of the rotor disk(s)
    minus the magnet length and a small offset to align the corners of the magnets to the rotor disk.

    In conjuction with CoilHoleWidthAtOuterRadius, controls the type of coil:

    * rectangular
    * keyhole
    * or triangular

    See Winding Type section at:
        https://openafpm.net/design-tips

    "Coil hole at R in" in Winding Type diagram.
    """

    MechanicalClearance: float
    """Air gap distance between stator and one rotor disk."""

    InnerDistanceBetweenMagnets: float
    """The distance between two consecutive magnets at the inner radius.

    For determining which kind of Magnet Jig to use: inner or outer.
    """

    NumberOfCoilsPerPhase: int
    """Number of coils in a phase.

    **Phase** is defined as:

        The timing of the cyclical aternation of voltage in a circuit.
        Different phases will peak at different times.

        A group of coils with the same timing is known as a 'phase'.

    — page 61, Glossary section of "A Wind Turbine Recipe Book (2014)".

    See "Three-phase stators" section on page 35 and
    "Connecting the coils" section on page 38 of "A Wind Turbine Recipe Book (2014)".
    """

    WireWeight: float
    """Total copper mass for coils in kilograms including two extra coils for contingency.
    """

    WireDiameter: float
    """Diameter of copper wire in coils.
    """

    NumberOfWiresInHand: int
    """Number of wires in hand when winding a coil.
    """

    TurnsPerCoil: int
    """Number of turns per coil.
    """


class FurlingParameters(TypedDict):
    """Furling Parameters.

    These mainly relate to the tail, hinge, and "furling".

    "*Furling*" is defined as:

        an automatic self-protective operation that reduces exposure
        to violent winds by facing the blades away from the wind.

        That furling motion is produced by a lateral offset of
        the blade rotor from the center of yaw.

        The tail and its hinge control the yawing motion,
        so that it limits power production.

    — page 60, Glossary section of "A Wind Turbine Recipe Book (2014)".
    """

    VerticalPlaneAngle: float  # TailHingeAngle?
    """Angle between outer pipe of yaw-bearing and inner pipe of tail hinge (in degrees).

    See "The inclined hinge" section on pages 30 - 31 of "A Wind Turbine Recipe Book (2014)".
    """

    HorizontalPlaneAngle: float
    """Angle of the alternator frame from a horizontal plane when welding the tail hinge (in degrees).

    See "The inclined hinge" section on pages 30 - 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomLength: float  # BoomPipeLength
    """Length of tail boom pipe.

    See "Tail boom" section on page 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomPipeDiameter: float
    """Outer diameter of tail boom pipe including thickness.

    See "Tail boom" section on page 31 of "A Wind Turbine Recipe Book (2014)".
    """

    BoomPipeThickness: float
    """Thickness of tail boom pipe.
    """

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

    For T shape, ``Offset`` is used in calculation of ``X``.

    Where ``X`` is described on the right-hand side of page 26 of "A Wind Turbine Recipe Book (2014)".

    For H Shape, see "Mounting the alternator to the yaw bearing" section
    on page 27 of "A Wind Turbine Recipe Book (2014)".

    Notably, the diagram on the left-hand side of page 29.

    Further discussion can be found in "The tail" section on page 30.
    """


class UserParameters(TypedDict):
    """User parameters have default values, and may be overridden by individual users to satisfy unique needs."""

    BladeWidth: float
    """The width of the blade near the root.

    The width depends on available wood.

    If no value is specified, then it defaults to the minimum.

    See "Selecting the wood" section on the right-hand side
    of page 15 and "The blank shapes" section on page 16
    of "A Wind Turbine Recipe Book (2014)".
    """

    RotorDiskCentralHoleDiameter: int
    """Diameter of central hole for rotor disk."""

    HolesDiameter: int
    """Diameter of various holes like stator mounting holes and vane bracket holes."""

    MetalLengthL: int  # AngleBarLength
    """Width of angle bars used in frame."""

    MetalThicknessL: int  # AngleBarThickness
    """Thickness of angle bars used in frame."""

    FlatMetalThickness: int
    """Thickness of various flat metal pieces which can be cut by a 2D CNC laser cutter."""

    YawPipeDiameter: float
    """Outer diameter of yaw bearing pipe including thickness."""

    PipeThickness: int
    """Thickness of yaw bearing and tail hinge pipes."""

    RotorResinMargin: int
    """Margin of resin to surround and protect the outer edge of the magnets.

    See left-hand side of page 42 of "A Wind Turbine Recipe Book (2014)".
    """

    HubPitchCircleDiameter: int
    """Diameter of circle which passes through center of hub holes."""

    HubHolesDiameter: int
    """Diameter of hub holes."""
