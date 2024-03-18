from enum import Enum, unique


@unique
class PlywoodThickness(int, Enum):
    """Enumeration of plywood thicknesses for a couple of standard materials in millimeters.
    """
    MM_4 = 4
    MM_6 = 6
    MM_8 = 8
    MM_9 = 9
    MM_10 = 10
    MM_12 = 12
    MM_15 = 15
    MM_18 = 18
    MM_20 = 20
    MM_21 = 21
    MM_24 = 24
    MM_25 = 25
    MM_27 = 27
    MM_30 = 30
    MM_35 = 35
    MM_40 = 40
