import os

from pathlib import Path

from . import importObj as importOBJ
from .make_archive import make_archive
from .common import find_object_by_label

__all__ = ['WindTurbine']


class WindTurbine:
    def __init__(self, root_document):
        self.root_document = root_document

    def to_obj(self):
        alternator = find_object_by_label(self.root_document, 'Alternator')
        obj_file_contents = importOBJ.export([alternator])
        return obj_file_contents

    def save_to(self, path):
        package_path = Path(__file__).parent.absolute()
        source = package_path.joinpath('documents')
        destination = Path(path).joinpath('WindTurbine.zip')
        return make_archive(source, destination)
