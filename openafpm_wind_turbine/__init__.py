from .master_of_puppets import create_master_of_puppets
from .wind_turbine import create_wind_turbine

# T Shape
# =======
rotor_radius = 150
rotor_inner_circle = 32.5
hub_holes_placement = 50
magnet_length = 46
stator_thickness = 13
hub_holes = 6
holes = 6
metal_length_l = 50
metal_thickness_l = 6
yaw_pipe_radius = 30.15
offset = 125

# H Shape
# =======
# rotor_radius = 230
# rotor_inner_circle = 47.5
# hub_holes_placement = 65
# magnet_length = 46
# stator_thickness = 13
# hub_holes = 7
# holes = 6
# metal_length_l = 50
# metal_thickness_l = 6
# yaw_pipe_radius = 44.5
# offset = 125

# Star Shape
# ==========
# rotor_radius = 349
# rotor_inner_circle = 81.5
# hub_holes_placement = 102.5
# magnet_length = 58
# stator_thickness = 15
# hub_holes = 8
# holes = 7
# metal_length_l = 65
# metal_thickness_l = 8
# yaw_pipe_radius = 57.15
# offset = 125

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


magn_afpm_parameters = {
    'RotorDiskRadius': rotor_radius,
    'DiskThickness': 10,
    'MagnetLength': magnet_length,
    'MagnetWidth': 30,
    'MagnetThickness': 10,
    'NumberMagnet': 12,
    'StatorThickness': stator_thickness,
    'CoilLegWidth': 22.5, # 22.5 reduced
    'CoilInnerWidth1': 30,
    'CoilInnerWidth2': 30,
    # Airgap length
    'MechanicalClearance': 3  # Distance between rotor and stator (~ 1 - 6 mm) 5 for others?
}

user_parameters = {
    # Distance between center of hub hole and center of alternator
    'HubHolesPlacement': hub_holes_placement,
    'RotorInnerCircle': rotor_inner_circle,
    'Holes': holes,  # Radius of outer holes on stator
    'MetalLengthL': metal_length_l,
    'MetalThicknessL': metal_thickness_l,
    'FlatMetalThickness': 10,
    'YawPipeRadius': yaw_pipe_radius,
    'PipeThickness': 5,
    'ResineRotorMargin': 5,
    'HubHoles': hub_holes  # Radius of hub holes
}

furling_tool_parameters = {
    'Angle': 20,
    'BracketLength': 300,
    'BracketWidth': 30,
    'BracketThickness': 5,
    'BoomLength': 1000,
    'BoomPipeRadius': 24.15,
    'BoomPipeThickness': 5,
    'VaneThickness': 6,
    'VaneLength': 1200,
    'VaneWidth': 500,
    'Offset': offset
}


def main():
    master_of_puppets_doc_name = 'Master of Puppets'
    imported_spreadsheet_name = 'Spreadsheet001'
    master_spreadsheet_name = 'Spreadsheet'
    master_of_puppets_doc = create_master_of_puppets(
        master_of_puppets_doc_name,
        imported_spreadsheet_name,
        master_spreadsheet_name,
        magn_afpm_parameters,
        user_parameters,
        furling_tool_parameters)
    master_of_puppets_doc.recompute()

    wind_turbine = create_wind_turbine(
        magn_afpm_parameters, user_parameters, furling_tool_parameters)
    wind_turbine.render()
