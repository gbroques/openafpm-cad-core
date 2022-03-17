import shutil
import zipfile
from pathlib import Path
from tempfile import gettempdir
from typing import List
from uuid import uuid1

import importDXF
from FreeCAD import Document, Placement

from .find_object_by_label import find_object_by_label
from .load import load_all
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

FLAT_ATTRIBUTE = 'Openafpm_Flat'


def export_to_dxf(magnafpm_parameters: MagnafpmParameters,
                  furling_parameters: FurlingParameters,
                  user_parameters: UserParameters) -> bytes:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters)
    export_list = get_dxf_export_list(root_documents)
    return export_list_to_dxf(export_list)


def get_dxf_export_list(root_documents: List[Document]) -> List[object]:
    export_list = []
    for document in root_documents:
        root_object = find_object_by_label(document, document.Name)
        export_list.extend(get_flat_objects([root_object]))
    return export_list


def get_flat_objects(
        objects: List[object],
        flat_objects: List[object] = []) -> List[object]:
    for child in objects:
        if child.TypeId == 'App::Link':
            get_flat_objects([child.LinkedObject], flat_objects)
        elif child.TypeId == 'App::Part':
            get_flat_objects(child.Group, flat_objects)
        elif hasattr(child, FLAT_ATTRIBUTE) and getattr(child, FLAT_ATTRIBUTE):
            flat_objects.append(child)
    return flat_objects


def export_list_to_dxf(export_list: List[object]) -> bytes:
    dxf_directory = Path(gettempdir()).joinpath(str(uuid1()))
    dxf_directory.mkdir()
    for object in export_list:
        export_to = str(dxf_directory.joinpath(
            f'{object.Label}.dxf'))
        # Reset Placement of object,
        # as objects not aligned with the XY plane are exported to DXF incorrectly.
        # See Also: https://forum.freecadweb.org/viewtopic.php?p=539543
        object.Placement = Placement()
        importDXF.export([object], export_to)

    dxf_files = []
    for dxf in dxf_directory.glob('*.dxf'):
        with open(dxf) as f:
            dxf_files.append((dxf, f.read()))
    archive_destination = dxf_directory.joinpath('DXF.zip')
    with zipfile.ZipFile(archive_destination, 'w') as zip:
        for (filepath, contents) in dxf_files:
            path = Path(filepath)
            zip.writestr(path.name, contents)
    with open(archive_destination, 'rb') as zip:
        bytes_content = zip.read()
    # Delete the directory the archive was created from.
    shutil.rmtree(dxf_directory)
    return bytes_content
