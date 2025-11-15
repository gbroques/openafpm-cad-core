"""Module to hash and unhash parameters into a unique string.

The algorithm is as follows:
1. Order parameters based on parameter group definitions.
2. Disregard keys, and only consider values.
3. Convert enum values into integer values.
4. Base 62 encode numeric values while preserving decimal point '.' for float values.
5. Concatenate all values together with a '-'.
"""

import copy
import string
from typing import List, TypedDict

from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters
from .get_parameters_schema import get_parameters_schema

# https://en.wikipedia.org/wiki/Base62
CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase
VALUE_DELIMITER = "-"
DECIMAL_DELIMITER = "."

__all__ = ["hash_parameters", "unhash_parameters"]


def hash_parameters(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> str:
    schema = get_parameters_schema(magnafpm_parameters["RotorDiskRadius"])
    parameters_by_group = convert_enum_values_to_integers(
        {
            "magnafpm": magnafpm_parameters,
            "furling": furling_parameters,
            "user": user_parameters,
        },
        schema,
    )
    group_keys = get_group_keys()
    order = flatten(group_keys)
    items = []
    for parameters in parameters_by_group.values():
        items.extend(parameters.items())
    sorted_items = sorted(items, key=lambda p: order.index(p[0]))
    encoded_values = map(lambda item: encode(item[1]), sorted_items)
    return VALUE_DELIMITER.join(encoded_values)


def unhash_parameters(parameter_hash: str) -> dict:
    parameters_by_group = {"magnafpm": {}, "furling": {}, "user": {}}
    groups = parameters_by_group.keys()
    group_keys = get_group_keys()
    values = list(map(decode, parameter_hash.split(VALUE_DELIMITER)))
    rotor_disk_radius = values[2]
    schema = get_parameters_schema(rotor_disk_radius)
    i = 0
    for group, group_keys in zip(groups, group_keys):
        group_properties = schema["properties"][group]["properties"]
        for key in group_keys:
            parameter_properties = group_properties[key]
            has_enum = "enum" in parameter_properties
            value = values[i]
            parameters_by_group[group][key] = (
                parameter_properties["enum"][value] if has_enum else value
            )
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
        left, right = (int(n) for n in str(num).split("."))
        return encode(left) + DECIMAL_DELIMITER + encode(right)
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return "".join(arr)


def decode(string, alphabet=CHARSET):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    if DECIMAL_DELIMITER in string:
        left, right = string.split(DECIMAL_DELIMITER)
        return int(decode(left)) + float("." + str(decode(right)))
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = strlen - (idx + 1)
        num += alphabet.index(char) * (base**power)
        idx += 1

    return num


def convert_enum_values_to_integers(parameters_by_group: dict, schema: dict) -> dict:
    parameters_by_group_copy = copy.deepcopy(parameters_by_group)
    for group, parameters in parameters_by_group_copy.items():
        group_properties = schema["properties"][group]["properties"]
        for key, value in parameters.items():
            parameter_properties = group_properties[key]
            if "enum" in parameter_properties:
                enum = parameter_properties["enum"]
                parameters[key] = enum.index(value)
    return parameters_by_group_copy
