from math import isclose

from .parameter_groups import MagnafpmParameters

__all__ = ['map_magnafpm_parameters']


def map_magnafpm_parameters(magnafpm: dict) -> MagnafpmParameters:
    return {
        'RotorDiameter': round(magnafpm['Rturb'] * 2000),
        'RotorDiskRadius': round(magnafpm['Rout'], ndigits=2),
        'RotorDiskInnerRadius': round(magnafpm['Rin'], ndigits=2),
        'RotorDiskThickness': magnafpm['hr'],
        'MagnetLength': magnafpm['la'],
        'MagnetWidth': magnafpm['wm'],
        'MagnetThickness': magnafpm['hm'],
        'MagnetMaterial': 'Ferrite' if isclose(magnafpm['mag_density'], 5) else 'Neodymium',
        'NumberMagnet': magnafpm['magnet_num'],
        'StatorThickness': magnafpm['tw'],
        'CoilType': magnafpm['coil_type'],
        'CoilLegWidth': round(magnafpm['wc'], ndigits=2),
        'CoilInnerWidth1': magnafpm['coil_hole_Rout_constr'],
        'CoilInnerWidth2': magnafpm['coil_hole_Rin_constr'],
        'MechanicalClearance': magnafpm['g'],
        'InnerDistanceBetweenMagnets': magnafpm['dist_magnet_Rin'],
        'NumberOfCoilsPerPhase': magnafpm['q'],
        'WireWeight': round(magnafpm['mcu_constr'], ndigits=2),
        'WireDiameter': magnafpm['dc'],
        'NumberOfWiresInHand': magnafpm['No_wires_at_hand'],
        'TurnsPerCoil': magnafpm['Nc']
    }
