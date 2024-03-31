from enum import Enum, unique


@unique
class PlywoodThickness(int, Enum):
    """Enumeration of birch plywood thicknesses in millimeters.
    """
    MM_6 = 6
    MM_9 = 9
    MM_12 = 12
    MM_15 = 15
    MM_18 = 18
    MM_21 = 21
    MM_24 = 24
    MM_27 = 27
    MM_30 = 30

