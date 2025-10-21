from math import isclose

from .parameter_groups import MagnafpmParameters

__all__ = ['map_magnafpm_parameters']


def map_magnafpm_parameters(magnafpm: dict) -> MagnafpmParameters:
    return {
        'RotorDiameter': round(magnafpm['Rturb'] * 2000),
        'RotorTopology': map_rotor_topology(int(magnafpm['rotor'])),
        'RotorDiskRadius': round(magnafpm['Rout'], ndigits=2),
        'RotorDiskInnerRadius': round(magnafpm['Rin'], ndigits=2),
        'RotorDiskThickness': magnafpm['hr'],
        'MagnetLength': magnafpm['la'],
        'MagnetWidth': magnafpm['wm'],
        'MagnetThickness': magnafpm['hm'],
        'MagnetMaterial': map_bh_max_to_magnet_material(magnafpm['BHmax']),
        'NumberMagnet': int(magnafpm['magnet_num']),
        'StatorThickness': magnafpm['tw'],
        'CoilType': int(magnafpm['coil_type']),
        'CoilLegWidth': round(magnafpm['wc'], ndigits=2),
        'CoilHoleWidthAtOuterRadius': round(magnafpm['coil_hole_Rout_constr'], ndigits=2),
        'CoilHoleWidthAtInnerRadius': round(magnafpm['coil_hole_Rin_constr'], ndigits=2),
        'MechanicalClearance': magnafpm['g'],
        'InnerDistanceBetweenMagnets': round(magnafpm['dist_magnet_Rin'], ndigits=2),
        'NumberOfCoilsPerPhase': magnafpm['q'],
        'WireWeight': round(magnafpm['mcu_constr'], ndigits=2),
        'WireDiameter': magnafpm['dc'],
        'NumberOfWiresInHand': magnafpm['No_wires_at_hand'],
        'TurnsPerCoil': magnafpm['Nc']
    }


def map_rotor_topology(rotor: int) -> str:
    rotor_topology_by_rotor = {
        2: 'Double',
        1: 'Single and metal disk',
        0: 'Single'
    }
    if rotor not in rotor_topology_by_rotor:
        raise ValueError(f'Unrecognized "rotor" option with value "{rotor}"')
    else:
        return rotor_topology_by_rotor[rotor]

def map_bh_max_to_magnet_material(bh_max: int) -> str:
    if bh_max == 30:
        return 'Ferrite C8'
    elif bh_max == 287:
        return 'NdFeB N35'
    elif bh_max == 326:
        return 'NdFeB N40'
    elif bh_max == 342:
        return 'NdFeB N42'
    elif bh_max == 366:
        return 'NdFeB N45'
    elif bh_max == 422:
        return 'NdFeB N52'
    else:
        raise ValueError(f'Unable to map BHmax {bh_max} to MagnetMaterial')
