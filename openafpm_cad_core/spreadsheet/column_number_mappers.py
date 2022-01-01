"""Module containing functions to map a number to a column and vise-versa."""
import string

__all__ = ['map_number_to_column', 'map_column_to_number']


def map_number_to_column(number: int) -> str:
    """Maps a number representing a column to a number.

    The first column corresponds to 1, instead of 0.

    >>> map_number_to_column(1)
    'A'

    >>> map_number_to_column(2)
    'B'

    >>> map_number_to_column(26)
    'Z'

    >>> map_number_to_column(27)
    'AA'

    >>> map_number_to_column(28)
    'AB'

    >>> map_number_to_column(52)
    'AZ'

    >>> map_number_to_column(702)
    'ZZ'
    """
    if number < 1:
        raise ValueError('Number {} must be greater than 0.'.format(number))
    num_letters = len(string.ascii_uppercase)
    if number > num_letters:
        first = map_number_to_column((number - 1) // num_letters)
        second = map_number_to_column(number % num_letters)
        return first + second
    return string.ascii_uppercase[number - 1]


def map_column_to_number(column: str) -> int:
    """Maps a letter representing a column to a number.

    >>> map_column_to_number('A')
    1

    >>> map_column_to_number('B')
    2

    >>> map_column_to_number('Z')
    26

    >>> map_column_to_number('AA')
    27

    >>> map_column_to_number('AB')
    28

    >>> map_column_to_number('AZ')
    52

    >>> map_column_to_number('ZZ')
    702
    """
    sum = 0
    for char in column:
        if char not in string.ascii_uppercase:
            raise ValueError(
                'Column "{}" must only contain uppercase ASCII characters.'.format(column))
        value = string.ascii_uppercase.find(char) + 1
        num_letters = len(string.ascii_uppercase)
        sum = sum * num_letters + value
    return sum
