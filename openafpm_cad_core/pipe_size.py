from enum import Enum, unique


@unique
class PipeSize(float, Enum):
    """Enumeration of pipe sizes.

    Outer diameter (OD) in mm including thickness.
    """
    OD_33_4 = 33.4
    OD_42_2 = 42.2
    OD_48_3 = 48.3
    OD_60_3 = 60.3
    OD_73_0 = 73.0
    OD_88_9 = 88.9
    OD_101_6 = 101.6
    OD_114_3 = 114.3
    OD_127_0 = 127.0
    OD_141_3 = 141.3
