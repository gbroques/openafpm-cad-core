from .wind_turbine import create_wind_turbine, WindTurbine
from .create_spreadsheet_task_panel import CreateSpreadsheetTaskPanel

__all__ = [
    'visualize',
    'CreateSpreadsheetTaskPanel'
]

# TODO: Yaw bearing
# T SHAPE
# =======
# 1. Top plate body (on Yaw pipe body)
# 2. Yaw pipe body
# 3. Low plate body (Outer bottom edge of Yaw pipe body)
# TODO: C-shaped steel arc as a support for wires that pass down the hole at the center of the yaw pipe.
#       Wires will be secured to this support with cable ties that prevent them moving and chafing.

# Tail Hinge
# ----------
# 1. Hinge inner body (Pipe)
# 2. Junction under yaw pipe hinge inner (under both Yaw pipe body and Hinge Inner Body) TODO: Is this needed?
# 3. Junction to tail body (in betwwen Yaw pipe body and Hinge inner body)
# TODO: Two side cover pieces over junction

# H SHAPE
# =======
# 1. Top plate body (on Yaw pipe body) (TopForAssembly)
# 2. Side (next to top plate body 90 deg)
# 3. Yaw pipe body

# Tail Hinge
# ----------
# 1. Hinge inner body (Pipe)
# 2. Junction under yaw pipe hinge inner (under both Yaw pipe body and Hinge Inner Body) TODO: Is this needed?

# STAR SHAPE
# ==========
# 1. Top plate body (on Yaw pipe body) (TopForAssembly)
# 2. Side (next to top plate body 90 deg)
# 3. Yaw pipe body


def visualize(magnafpm_parameters: dict,
              user_parameters: dict,
              furling_parameters: dict) -> WindTurbine:
    return create_wind_turbine(
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
