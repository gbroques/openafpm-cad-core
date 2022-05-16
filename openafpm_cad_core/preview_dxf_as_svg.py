from .export_set_to_svg import export_set_to_svg, get_svg_style_options
from .get_dxf_export_set import get_dxf_export_set
from .load import load_all
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['preview_dxf_as_svg']


def preview_dxf_as_svg(magnafpm_parameters: MagnafpmParameters,
                       furling_parameters: FurlingParameters,
                       user_parameters: UserParameters,
                       font_family: str = 'sans-serif',
                       foreground: str = '#FFFFFF',
                       background: str = '#000000') -> str:
    root_documents, spreadsheet_document = load_all(
        magnafpm_parameters, furling_parameters, user_parameters)
    export_set = get_dxf_export_set(root_documents)
    options = get_svg_style_options(magnafpm_parameters['RotorDiskRadius'])
    return export_set_to_svg(
        export_set,
        font_family=font_family,
        foreground=foreground,
        background=background
        ** options)
