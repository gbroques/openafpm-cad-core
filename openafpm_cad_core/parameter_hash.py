"""Module to hash and unhash parameters into a unique string.

The algorithm is as follows:
1. Order parameters based on parameter group definitions.
2. Disregard keys, and only consider values.
3. Convert string values into numeric values.
4. Base 62 encode numeric values while preserving decimal point '.' for float values.
5. Concatenate all values together with a '-'.
"""

import string
from typing import List, TypedDict

from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

# https://en.wikipedia.org/wiki/Base62
CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase
VALUE_DELIMITER = '-'
DECIMAL_DELIMITER = '.'
MAGNET_MATERIALS = ['Neodymium', 'Ferrite']

__all__ = ['hash_parameters', 'unhash_parameters']


def hash_parameters(magnafpm_parameters: MagnafpmParameters,
                    furling_parameters: FurlingParameters,
                    user_parameters: UserParameters) -> str:
    parameters_by_group = string_to_numeric({
        'magnafpm': magnafpm_parameters,
        'user': user_parameters,
        'furling': furling_parameters
    })
    group_keys = get_group_keys()
    order = flatten(group_keys)
    items = []
    for parameters in parameters_by_group.values():
        items.extend(parameters.items())
    sorted_items = sorted(items, key=lambda p: order.index(p[0]))
    encoded_values = map(lambda item: encode(item[1]), sorted_items)
    return VALUE_DELIMITER.join(encoded_values)


def unhash_parameters(parameter_hash: str) -> dict:
    parameters_by_group = {
        'magnafpm': {},
        'furling': {},
        'user': {}
    }
    groups = parameters_by_group.keys()
    group_keys = get_group_keys()
    values = list(map(decode, parameter_hash.split(VALUE_DELIMITER)))
    i = 0
    for group, group_keys in zip(groups, group_keys):
        for key in group_keys:
            parameters_by_group[group][key] = values[i]
            i += 1
    return parameters_by_group


def get_group_keys():
    return map(get_keys, [MagnafpmParameters, FurlingParameters, UserParameters])


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_keys(typed_dict: TypedDict) -> List[str]:
    return list(typed_dict.__annotations__.keys())


def encode(num, alphabet=CHARSET):
    """Encode a positive number in Base X
    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    if isinstance(num, float):
        left, right = (int(n) for n in str(num).split('.'))
        return encode(left) + DECIMAL_DELIMITER + encode(right)
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def decode(string, alphabet=CHARSET):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    if DECIMAL_DELIMITER in string:
        left, right = string.split(DECIMAL_DELIMITER)
        return int(decode(left)) + float('.' + str(decode(right)))
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


def string_to_numeric(parameters_by_group: dict) -> dict:
    numeric_converters_by_group = {
        'magnafpm': {
            'MagnetMaterial': magnet_material_to_numeric
        },
        'furling': {},
        'user': {}
    }
    return convert_values(parameters_by_group, numeric_converters_by_group)


def numeric_to_string(parameters_by_group: dict) -> dict:
    string_converters_by_group = {
        'magnafpm': {
            'MagnetMaterial': magnet_material_from_numeric
        },
        'furling': {},
        'user': {}
    }
    return convert_values(parameters_by_group, string_converters_by_group)


def convert_values(parameters_by_group: dict, converters_by_group: dict) -> dict:
    parameters_by_group_copy = parameters_by_group.copy()
    for group, parameters in parameters_by_group_copy.items():
        converters_by_key = converters_by_group[group]
        for key, value in parameters.items():
            if key in converters_by_key:
                to_numeric = converters_by_key[key]
                parameters[key] = to_numeric(value)
    return parameters_by_group_copy


def magnet_material_to_numeric(magnet_material: str) -> int:
    return MAGNET_MATERIALS.index(magnet_material)


def magnet_material_from_numeric(magnet_material_int: int) -> str:
    return MAGNET_MATERIALS[magnet_material_int]
