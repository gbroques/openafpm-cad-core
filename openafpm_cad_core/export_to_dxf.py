import shutil
import zipfile
from pathlib import Path
from tempfile import gettempdir
from typing import List
from uuid import uuid1

import Draft
import FreeCAD as App
import importDXF
from FreeCAD import Document, Placement, Vector

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
        object_to_export = get_object_to_export(object)
        # Reset Placement of object,
        # as objects not aligned with the XY plane are exported to DXF incorrectly.
        # See Also: https://forum.freecadweb.org/viewtopic.php?p=539543
        object_to_export.Placement = Placement()
        importDXF.export([object_to_export], export_to)

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


def get_object_to_export(object):
    if object.Label == 'Tail_Stop_HighEnd':
        return get_high_end_stop_shape(object)
    else:
        return object


def get_high_end_stop_shape(object):
    """The High End Stop requires special care when exporting to DXF.
    Create a 2D projection of the second to largest face via the Draft workbench.

    See Also:
        https://wiki.freecadweb.org/Draft_Shape2DView
    """
    document = object.Document
    faces = object.Shape.Faces
    App.setActiveDocument(document.Name)
    second_to_largest_face = sorted(
        faces, key=lambda f: f.Area, reverse=True)[1]
    index = None
    for i, face in enumerate(faces, start=1):
        if face.isEqual(second_to_largest_face):
            index = i
            break
    shape = Draft.makeShape2DView(
        object, Vector(1, 0, 0), facenumbers=[index - 1])
    shape.ProjectionMode = 'Individual Faces'
    document.recompute()
    return shape
