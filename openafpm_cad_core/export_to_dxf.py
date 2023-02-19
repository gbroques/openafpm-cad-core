import shutil
import zipfile
from pathlib import Path
from tempfile import gettempdir
from typing import Set
from uuid import uuid1

import importDXF

from .export_set_to_svg import export_set_to_svg, get_svg_style_options
from .get_2d_projection import get_2d_projection
from .get_dxf_export_set import get_dxf_export_set
from .load import load_all
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .make_get_part_count import make_get_part_count


def export_to_dxf(magnafpm_parameters: MagnafpmParameters,
                  furling_parameters: FurlingParameters,
                  user_parameters: UserParameters,
                  save_spreadsheet_document: bool = False) -> bytes:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters, save_spreadsheet_document)
    get_part_count = make_get_part_count(root_documents, magnafpm_parameters['NumberOfCoilsPerPhase'])
    export_set = get_dxf_export_set(root_documents)
    options = get_svg_style_options(magnafpm_parameters['RotorDiskRadius'])
    svg = export_set_to_svg(export_set, get_part_count, **options)
    return export_dxf_as_zip(export_set, svg)


def export_dxf_as_zip(export_set: Set[object], svg: str) -> bytes:
    dxf_directory = Path(gettempdir()).joinpath(str(uuid1()))
    dxf_directory.mkdir()
    for object in export_set:
        export_to = str(dxf_directory.joinpath(
            f'{object.Label}.dxf'))
        two_dimensional_projection = get_2d_projection(object)
        importDXF.export([two_dimensional_projection], export_to)

    dxf_files = []
    for dxf in dxf_directory.glob('*.dxf'):
        with open(dxf) as f:
            dxf_files.append((dxf, f.read()))
    archive_destination = dxf_directory.joinpath('DXF.zip')
    with zipfile.ZipFile(archive_destination, 'w') as zip:
        for (filepath, contents) in dxf_files:
            path = Path(filepath)
            zip.writestr(path.name, contents)
        zip.writestr('overview.svg', svg)
    with open(archive_destination, 'rb') as zip:
        bytes_content = zip.read()
    # Delete the directory the archive was created from.
    shutil.rmtree(dxf_directory)
    return bytes_content
