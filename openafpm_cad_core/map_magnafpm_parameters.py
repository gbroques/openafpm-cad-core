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
        'MagnetMaterial': 'Ferrite' if isclose(magnafpm['mag_density'], 5) else 'Neodymium',
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
