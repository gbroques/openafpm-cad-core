from argparse import ArgumentParser
from pprint import pformat

from openafpm_cad_core.app import loadmat, map_magnafpm_parameters

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Loads a Matlab .mat file and prints it.')
    parser.add_argument('path',
                        metavar='<path>',
                        type=str,
                        help='Output path.')
    args = parser.parse_args()
    magnafpm_parameters = map_magnafpm_parameters(loadmat(args.path))
    string = pformat(magnafpm_parameters, indent=12, sort_dicts=False)
    replacements = [('{', ' '), ('}', ''), ("'", '"')]
    for old, new in replacements:
        string = string.replace(old, new)
    print(string)
