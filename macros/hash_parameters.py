from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   hash_parameters, unhash_parameters)
import json
parameters = get_default_parameters(WindTurbine.H_SHAPE)
print(json.dumps(parameters, indent=2))
print()


hash = hash_parameters(
    parameters['magnafpm'],
    parameters['user'],
    parameters['furling'])

print('HASH')
print('----')
print(hash)
print()

print(json.dumps(unhash_parameters(hash), indent=2))
