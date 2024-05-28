import json

from openafpm_cad_core.app import (WindTurbineShape, get_default_parameters,
                                   hash_parameters, unhash_parameters)

parameters = get_default_parameters(WindTurbineShape.T)
print(json.dumps(parameters, indent=2) + '\n')

hash = hash_parameters(
    parameters['magnafpm'],
    parameters['user'],
    parameters['furling'])
print(f'Hash: {hash}\n')

unhashed_parameters = unhash_parameters(hash)
print(f'Does hashing preserve equality? {parameters == unhashed_parameters}')
