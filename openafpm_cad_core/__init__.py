from .master_of_puppets import create_master_of_puppets
from .wind_turbine import create_wind_turbine, WindTurbine

# TODO: Yaw bearing
# T SHAPE
# =======
# 1. Top plate body (on Yaw pipe body)
# 2. Yaw pipe body
# 3. Low plate body (Outer bottom edge of Yaw pipe body)
# 4. Hinge inner body (Pipe)
# 5. Junction under yaw pipe hinge inner (under both Yaw pipe body and Hinge Inner Body)
# 6. Junction to tail body (in betwwen Yaw pipe body and Hinge inner body)

# H SHAPE
# =======
# 1. Top plate body (on Yaw pipe body) (TopForAssembly)
# 2. Side (next to top plate body 90 deg)
# 3. Yaw pipe body
# 4. Hinge inner body (Pipe)
# 5. Junction under yaw pipe hinge inner (under both Yaw pipe body and Hinge Inner Body)

# STAR SHAPE
# ==========
# 1. Top plate body (on Yaw pipe body) (TopForAssembly)
# 2. Side (next to top plate body 90 deg)
# 3. Yaw pipe body


def visualize(magnafpm_parameters: dict,
              user_parameters: dict,
              furling_parameters: dict) -> WindTurbine:
    master_of_puppets_doc_name = 'Master of Puppets'
    imported_spreadsheet_name = 'Spreadsheet001'
    master_spreadsheet_name = 'Spreadsheet'
    master_of_puppets_doc = create_master_of_puppets(
        master_of_puppets_doc_name,
        imported_spreadsheet_name,
        master_spreadsheet_name,
        magnafpm_parameters,
        user_parameters,
        furling_parameters)
    master_of_puppets_doc.recompute()

    return create_wind_turbine(
        magnafpm_parameters, user_parameters, furling_parameters)
