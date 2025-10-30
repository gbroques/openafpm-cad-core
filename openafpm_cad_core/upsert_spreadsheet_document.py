from pathlib import Path
from typing import Dict, List

import FreeCAD as App
from FreeCAD import Document

from .alternator_cells import alternator_cells
from .blade_cells import blade_cells
from .fastener_cells import get_fastener_cells
from .high_end_stop_cells import high_end_stop_cells
from .hub_cells import hub_cells
from .low_end_stop_cells import low_end_stop_cells
from .parameter_groups import FurlingParameters, MagnafpmParameters, UserParameters
from .parameters_by_key_to_cells import parameters_by_key_to_cells
from .spreadsheet import Cell, populate_spreadsheet
from .tail_cells import tail_cells
from .wind_turbine_cells import wind_turbine_cells
from .yaw_bearing_cells import yaw_bearing_cells
from .wind_turbine_shape import H_SHAPE_LOWER_BOUND, STAR_SHAPE_LOWER_BOUND

__all__ = ["upsert_spreadsheet_document"]


def upsert_spreadsheet_document(
    path: Path,
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Document:
    cells_by_spreadsheet_name = get_cells_by_spreadsheet_name(
        magnafpm_parameters, furling_parameters, user_parameters
    )
    return upsert_document(path, cells_by_spreadsheet_name)


def get_cells_by_spreadsheet_name(
    magnafpm_parameters: MagnafpmParameters,
    furling_parameters: FurlingParameters,
    user_parameters: UserParameters,
) -> Dict[str, List[List[Cell]]]:
    cells = parameters_by_key_to_cells(
        {
            "MagnAFPM": magnafpm_parameters,
            "Furling": furling_parameters,
            "User": user_parameters,
            "Shape": {
                "HShapeLowerBound": H_SHAPE_LOWER_BOUND,
                "StarShapeLowerBound": STAR_SHAPE_LOWER_BOUND,
                "WindTurbineShape": "=RotorDiskRadius < HShapeLowerBound ? <<T>> : (RotorDiskRadius < StarShapeLowerBound ? <<H>> : <<Star>>)",
            },
        }
    )
    return {
        "Spreadsheet": cells,
        "Fastener": get_fastener_cells(),
        "Hub": hub_cells,
        "Blade": blade_cells,
        "Alternator": alternator_cells,
        "YawBearing": yaw_bearing_cells,
        "Tail": tail_cells,
        "LowEndStop": low_end_stop_cells,
        "HighEndStop": high_end_stop_cells,
        "WindTurbine": wind_turbine_cells,
    }


def upsert_document(
    path: Path, cells_by_spreadsheet_name: Dict[str, List[List[Cell]]]
) -> Document:
    if path.exists():
        document = App.openDocument(str(path))
    else:
        document = App.newDocument(path.stem)
    populate_spreadsheets(document, cells_by_spreadsheet_name)
    document.recompute()
    if not path.exists():
        document.saveAs(str(path))
    return document


def populate_spreadsheets(
    document: Document, cells_by_spreadsheet_name: Dict[str, List[List[Cell]]]
) -> None:
    for spreadsheet_name, cells in cells_by_spreadsheet_name.items():
        sheet = document.getObject(spreadsheet_name)
        if sheet is None:
            sheet = document.addObject("Spreadsheet::Sheet", spreadsheet_name)
        else:
            sheet.clearAll()
        populate_spreadsheet(sheet, cells)
