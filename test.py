"""
FreeCAD Macro to test openafpm_cad_core package.
"""
import sys
sys.path.append('/home/g/Desktop/squashfs-root/usr/lib/')
import FreeCAD
from openafpm_cad_core.app import visualize, get_default_parameters
from enum import Enum, unique


# T Shape
# =======
rotor_radius = 150
rotor_inner_circle = 32.5
hub_holes_placement = 50
magnet_length = 46
number_magnet = 12
stator_thickness = 13
coil_leg_width = 21
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
# number_magnet = 16
# stator_thickness = 13
# coil_leg_width = 22.5
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
# number_magnet = 32
# stator_thickness = 15
# coil_leg_width = 22.5
# hub_holes = 8
# holes = 7
# metal_length_l = 65
# metal_thickness_l = 8
# yaw_pipe_radius = 57.15
# offset = 125


magnafpm_parameters = {
    'RotorDiskRadius': rotor_radius,
    # RotorDiskThickness
    'DiskThickness': 10,
    'MagnetLength': magnet_length,
    'MagnetWidth': 30,
    'MagnetThickness': 10,
    # NumberOfMagnets
    'NumberMagnet': number_magnet,
    'StatorThickness': stator_thickness,
    'CoilLegWidth': coil_leg_width,
    # CoilOuterHoleWidth
    'CoilInnerWidth1': 30,
    # CoilInnerHoleWidth
    'CoilInnerWidth2': 30, # Inner and outer with respect to center of rotor disk.
    # Airgap length
    # Distance between rotor and stator (~ 1 - 6 mm) 5 for others?
    'MechanicalClearance': 3
}

user_parameters = {
    # Distance between center of hub hole and center of alternator
    # HubHolesCircumradius
    'HubHolesPlacement': hub_holes_placement,
    # RotorInnerHoleRadius
    'RotorInnerCircle': rotor_inner_circle,
    # StatorMountHoleRadius
    'Holes': holes,  # Radius of stator mount holes
    'MetalLengthL': metal_length_l, # Width of angle bar (frame)
    'MetalThicknessL': metal_thickness_l, # Thickness of angle bar (frame)
    'FlatMetalThickness': 10,
    'YawPipeRadius': yaw_pipe_radius,
    'PipeThickness': 5,
    # The hole in the surrond is about 5 mm larger in
    # radius than the magnet rotor so that the casting covers
    # and protects the edges of the magnets
    # RotorResinCastMargin
    'ResineRotorMargin': 5,
    # HubHoleRadius
    'HubHoles': hub_holes  # Radius of hub holes
}

furling_parameters = {
    'Angle': 20,
    'BracketLength': 300,
    'BracketWidth': 30,
    'BracketThickness': 5,
    'BoomLength': 1000,
    'BoomPipeRadius': 24.15,
    'BoomPipeThickness': 5,
    # TODO: Reorder: L x W x T
    'VaneThickness': 6,
    'VaneLength': 1200,
    'VaneWidth': 500,
    'Offset': offset
}

@unique
class WindTurbine(Enum):
    T_SHAPE = 'T Shape'
    H_SHAPE = 'H Shape'
    STAR_SHAPE = 'Star Shape'

parameters = get_default_parameters(WindTurbine.T_SHAPE.value)

wind_turbine = visualize(
    parameters['magnafpm'],
    parameters['user'], 
    parameters['furling'])

obj_file_contents = wind_turbine.to_obj()

with open('wind-turbine.obj', 'w') as f:
    f.write(obj_file_contents)
    print('wind-turbine.obj created.')
