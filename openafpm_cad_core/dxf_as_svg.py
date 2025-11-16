from FreeCAD import Document
from typing import List
from .export_set_to_svg import export_set_to_svg, get_svg_style_options
from .get_dxf_export_set import get_dxf_export_set
from .load import load_all
from .make_get_part_count import make_get_part_count
from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters

__all__ = ["load_dxf_as_svg", "get_dxf_as_svg"]


def load_dxf_as_svg(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
    font_family: str = "sans-serif",
    foreground: str = "#FFFFFF",
    background: str = "#000000",
) -> str:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters
    )
    return get_dxf_as_svg(
        root_documents,
        magnafpm_parameters,
        font_family,
        foreground,
        background,
    )


def get_dxf_as_svg(
    root_documents: List[Document],
    magnafpm_parameters: MagnafpmParameters,
    font_family: str = "sans-serif",
    foreground: str = "#FFFFFF",
    background: str = "#000000",
) -> str:
    export_set = get_dxf_export_set(root_documents)
    get_part_count = make_get_part_count(root_documents, magnafpm_parameters)
    options = get_svg_style_options(magnafpm_parameters["RotorDiskRadius"])
    return export_set_to_svg(
        export_set,
        get_part_count,
        font_family=font_family,
        foreground=foreground,
        background=background,
        **options,
    )
