import re

from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

CHARSET = "3456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

ORDER = [
    "MechanicalClearance",
    "DiskThickness",
    "MagnetThickness",
    "StatorThickness",
    "BracketThickness",
    "BoomPipeThickness",
    "VaneThickness",
    "Holes",
    "MetalThicknessL",
    "FlatMetalThickness",
    "PipeThickness",
    "ResineRotorMargin",
    "HubHoles",
    "NumberMagnet",
    "VerticalPlaneAngle",
    "BracketWidth",
    "MagnetWidth",
    "CoilInnerWidth1",
    "CoilInnerWidth2",
    "MetalLengthL",
    "MagnetLength",
    "HorizontalPlaneAngle",
    "Offset",
    # large numbers
    "RotorDiskRadius",
    "BracketLength",
    "VaneWidth",
    "BoomLength",
    "VaneLength",
    # likely to be floating point numbers
    "HubHolesPlacement",
    "BoomPipeRadius",
    "YawPipeDiameter",
    "RotorInnerCircle",
    "CoilLegWidth"
]

PART_SIG = '2' # Character to denote how many parts are next to each other without a delimeter
VALUE_DELIMITER = '0'
DECIMAL_POINT = '1'


def hash_parameters(magnafpm_parameters: MagnafpmParameters,
                    user_parameters: UserParameters,
                    furling_parameters: FurlingParameters) -> str:
    parameter_groups = [magnafpm_parameters,
                        user_parameters,
                        furling_parameters]
    items = []
    for parameters in parameter_groups:
        items.extend(parameters.items())
    sorted_items = sorted(items, key=lambda p: ORDER.index(p[0]))
    hash = ''
    for key, value in sorted_items:
        if isinstance(value, float):
            left, right = (int(n) for n in str(value).split('.'))
            hash += encode(left) + DECIMAL_POINT + encode(right)
        else:
            hash += encode(value)
        hash += VALUE_DELIMITER
    return compress_hash(hash[:-1])  # remove trailing value delimeter


def unhash_parameters(hash: str) -> str:
    hash = uncompress_hash(hash)
    numbers = []
    parts = hash.split(VALUE_DELIMITER)
    for part in parts:
        if DECIMAL_POINT in part:
            left, right = (str(decode(p))
                           for p in part.split(DECIMAL_POINT))
            value = float(left + '.' + right)
        else:
            value = decode(part)
        numbers.append(value)
    return dict(zip(ORDER, numbers))


def compress_hash(hash: str) -> str:
    # Match 3 or more times, to make compression worth it.
    for match in re.finditer(r'\b(?:[' + CHARSET + r']' + VALUE_DELIMITER + r'){3,}', hash):
        result = match.group(0)
        num_delim = result.count(VALUE_DELIMITER)
        compressed = PART_SIG + \
            str(encode(num_delim)) + result.replace(VALUE_DELIMITER, '')
        hash = hash.replace(result, compressed)
    return hash


def uncompress_hash(hash: str) -> str:
    for match in re.finditer(PART_SIG + r'[' + CHARSET + r']', hash):
        result = match.group(0)
        num_delim = decode(result[1])
        start = match.pos + 2
        end = num_delim + 2
        compressed = match.string[start:end]
        uncompressed = VALUE_DELIMITER.join(list(compressed)) + VALUE_DELIMITER
        to_replace = result + compressed
        hash = hash.replace(to_replace, uncompressed)
    return hash


def encode(num, alphabet=CHARSET):
    """Encode a positive number in Base X
    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
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
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
