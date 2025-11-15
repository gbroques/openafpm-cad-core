import json

from openafpm_cad_core.app import (WindTurbineShape, get_default_parameters,
                                   hash_parameters, unhash_parameters)

parameters = get_default_parameters(WindTurbineShape.T)
print(json.dumps(parameters, indent=2) + '\n')
del parameters['description']

hash = hash_parameters(
    parameters['magnafpm'],
    parameters['furling'],
    parameters['user'])

print(f'Hash: {hash}')
print(f'Length: {len(hash)}')
unhashed_parameters = unhash_parameters(hash)
print(f'Does hashing preserve equality? {parameters == unhashed_parameters}')
