import os
from pathlib import Path
from typing import List

from . import importObj as importOBJ
from .find_object_by_label import find_object_by_label
from .make_archive import make_archive

__all__ = ['WindTurbine']


class WindTurbine:
    def __init__(self, root_document):
        self.root_document = root_document

    def to_obj(self):
        wind_turbine = find_object_by_label(self.root_document, 'WindTurbine')
        obj_file_contents = importOBJ.export(
            [wind_turbine], object_name_getter, keep_unresolved)
        return obj_file_contents

    def save_to(self, path):
        package_path = Path(__file__).parent.absolute()
        source = package_path.joinpath('documents')
        destination = Path(path).joinpath('WindTurbine.zip')
        return make_archive(str(source), str(destination))


def object_name_getter(obj: object, path: List[object]) -> str:
    rotor_disk_labels = {
        'RotorDisk',
        'RotorResinCast',
        'Magnets'
    }
    if obj.Label in rotor_disk_labels:
        is_top = any([o.Label.startswith('Top') for o in path])
        label_prefix = 'Top' if is_top else 'Bottom'
        return label_prefix + obj.Label
    return obj.Label


def keep_unresolved(obj: object, path: List[object]) -> bool:
    return obj.Label in {
        'Frame',
        'YawBearing',
        'TailHinge'
    }
