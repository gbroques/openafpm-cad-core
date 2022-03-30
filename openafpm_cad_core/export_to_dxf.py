import shutil
import zipfile
from pathlib import Path
from tempfile import gettempdir
from typing import Set
from uuid import uuid1

import importDXF

from .get_2d_projection import get_2d_projection
from .get_dxf_export_set import get_dxf_export_set
from .load import load_all
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .preview_dxf_as_svg import preview_dxf_as_svg


def export_to_dxf(magnafpm_parameters: MagnafpmParameters,
                  furling_parameters: FurlingParameters,
                  user_parameters: UserParameters) -> bytes:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters)
    export_set = get_dxf_export_set(root_documents)
    # 0.48 comes from 150 (the default RotorDiskRadius for T shape)
    # divided by a desired 72 px which happens to look good.
    font_size = round(magnafpm_parameters['RotorDiskRadius'] * 0.48)
    padding = round(font_size * 0.222)  # 16 / 72 = 0.222 repeating
    row_gap = round(font_size * 0.889)  # 64 / 72 = 0.889 repeating
    column_gap = row_gap / 2  # 32 is half of 64
    text_margin_bottom = round(font_size * 0.667)  # 48 / 72 = 0.667 repeating
    svg = preview_dxf_as_svg(export_set, font_size=font_size, padding=padding,
                             row_gap=row_gap, column_gap=column_gap,
                             text_margin_bottom=text_margin_bottom)
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
