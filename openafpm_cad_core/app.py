from typing import TypedDict

from .create_spreadsheet_document import create_spreadsheet_document
from .get_default_parameters import get_default_parameters
from .load_turbine import load_turbine
from .wind_turbine import WindTurbine


class MagnafpmParameters(TypedDict):
    RotorDiskRadius: float
    DiskThickness: float
    MagnetLength: float
    MagnetWidth: float
    MagnetThickness: float
    NumberMagnet: int
    StatorThickness: float
    CoilLegWidth: float
    CoilInnerWidth1: float
    CoilInnerWidth2: float
    MechanicalClearance: float


class UserParameters(TypedDict):
    HubHolesPlacement: float
    RotorInnerCircle: float
    Holes: float
    MetalLengthL: float
    MetalThicknessL: float
    FlatMetalThickness: float
    YawPipeRadius: float
    PipeThickness: float
    ResineRotorMargin: float
    HubHoles: float
    HorizontalPlaneAngle: float


class FurlingParameters(TypedDict):
    VerticalPlaneAngle: float
    BracketLength: float
    BracketWidth: float
    BracketThickness: float
    BoomLength: float
    BoomPipeRadius: float
    BoomPipeThickness: float
    VaneThickness: float
    VaneLength: float
    VaneWidth: float
    Offset: float


__all__ = [
    'create_spreadsheet_document',
    'get_default_parameters',
    'visualize'
]


def visualize(magnafpm_parameters: MagnafpmParameters,
              user_parameters: UserParameters,
              furling_parameters: FurlingParameters) -> WindTurbine:
    return load_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
