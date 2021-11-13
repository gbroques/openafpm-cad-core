import shutil
from pathlib import Path
from typing import List

import freecad_to_obj
from FreeCAD import Document

from .find_object_by_label import find_object_by_label
from .get_furl_transforms import get_furl_transforms
from .make_archive import make_archive
from .save_documents import save_documents

__all__ = ['WindTurbineModel']


class WindTurbineModel:
    def __init__(self,
                 root_document: Document,
                 spreadsheet_document: Document):
        self.root_document = root_document
        self.spreadsheet_document = spreadsheet_document

        # get_furl_transforms and to_obj needs to be called before save_to method.
        self.obj_file_contents = to_obj(root_document)
        self.furl_transforms = get_furl_transforms(root_document)

    def to_obj(self):
        return self.obj_file_contents

    def get_furl_transforms(self):
        return self.furl_transforms

    def save_to(self, path) -> bytes:
        document_source = Path(self.root_document.FileName).parent
        archive_source = Path(path).joinpath('documents')

        # Save documents to where the archive will be created from first.
        save_documents(
            self.root_document.Name,
            self.spreadsheet_document.Name,
            source=document_source,
            destination=archive_source)

        archive_destination = Path(path).joinpath('WindTurbine.zip')
        bytes_content = make_archive(
            str(archive_source), str(archive_destination))
        # Delete the directory the archive was created from.
        shutil.rmtree(archive_source)
        return bytes_content


def to_obj(root_document: Document) -> str:
    wind_turbine = find_object_by_label(
        root_document, root_document.Name)
    obj_file_contents = freecad_to_obj.export(
        [wind_turbine], object_name_getter, keep_unresolved)
    return obj_file_contents


def object_name_getter(obj: object, path: List[object]) -> str:
    rotor_disk_labels = {
        'Rotor_Disk',
        'Rotor_ResinCast',
        'Rotor_Magnets'
    }
    if obj.Label in rotor_disk_labels:
        is_front = any([o.Label.endswith('Front') for o in path])
        label_suffix = 'Front' if is_front else 'Back'
        return obj.Label + '_' + label_suffix
    return obj.Label


def keep_unresolved(obj: object, path: List[object]) -> bool:
    return obj.Label in {
        'Frame',
        'YawBearing',
        'Tail_Hinge_Outer',
        'Tail_Hinge_Inner',
        'Vane_Bracket_Top'
    }
