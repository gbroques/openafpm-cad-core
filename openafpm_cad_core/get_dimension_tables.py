"""Module for retrieving dimensions to display in a tabular format."""

from typing import Any, List, Optional, Tuple, TypedDict

from FreeCAD import Document
from typing_extensions import NotRequired

from .create_spreadsheet_document import create_spreadsheet_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)

__all__ = ['get_dimension_tables']


class Element(TypedDict):
    """
    Loosely-based on:
    https://developer.mozilla.org/en-US/docs/Web/API/Element
    """
    tagName: str
    children: NotRequired[List['Element']]
    properties: NotRequired[dict]


book_reference_template = 'A Wind Turbine Recipe Book (2014 metric edition), %s'


def get_dimension_tables(magnafpm_parameters: MagnafpmParameters,
                         furling_parameters: FurlingParameters,
                         user_parameters: UserParameters) -> List[Element]:
    name = 'Master_of_Puppets'
    spreadsheet_document = create_spreadsheet_document(name,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    rotor_disk_radius = magnafpm_parameters['RotorDiskRadius']
    tables = []
    tables.append(
        create_yaw_bearing_pipe_sizes_table(spreadsheet_document)
    )
    tables.append(
        create_wheel_bearing_hub_table(spreadsheet_document)
    )
    tables.append(
        create_steel_disk_sizes_table(spreadsheet_document)
    )
    tables.append(
        create_frame_dimensions_table(spreadsheet_document)
    )
    if rotor_disk_radius < 187.5:
        tables.append(
            create_alternator_frame_to_yaw_tube_sizes_table(
                spreadsheet_document)
        )
    if rotor_disk_radius >= 187.5:
        tables.append(
            create_frame_dimensions_flat_bar_table(spreadsheet_document)
        )
    tables.append(
        create_steel_pipe_dimensions_for_tail_table(spreadsheet_document)
    )
    tables.append(
        create_tail_junction_dimensions_table(spreadsheet_document)
    )
    tables.append(
        create_tail_vane_dimensions_table(spreadsheet_document)
    )
    tables.append(
        create_coil_winder_dimensions_table(spreadsheet_document)
    )
    tables.append(
        create_stator_mold_dimensions_table(spreadsheet_document)
    )
    tables.append(
        create_rotor_mold_dimensions_table(spreadsheet_document)
    )
    return tables


def create_table(header: str,
                 rows: List[Tuple[str, Any]],
                 reference: Optional[str] = None) -> Element:
    children = [
        thead([
            tr([
                th(header, col_span=2)
            ])
        ]),
        tbody([
            tr([
                td(row[0]),
                td(round_if_float(row[1]))
            ]) for row in rows
        ])
    ]
    if reference:
        children.append(
            tfoot([
                tr([
                    td(reference, col_span=2)
                ])
            ])
        )
    return table(children)


def round_if_float(value: Any, ndigits: int = 2) -> Any:
    return round(value, ndigits=ndigits) if type(value) == float else value


def create_yaw_bearing_pipe_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Yaw Bearing Pipe Sizes',
        [
            ('Tower top stub outer diameter', spreadsheet_document.Tail.HingeInnerPipeDiameter),
            ('Yaw pipe outer diameter', spreadsheet_document.Spreadsheet.YawPipeDiameter),
        ],
        book_reference_template % 'page 24 left-hand side'
    )


def create_wheel_bearing_hub_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Wheel Bearing Hub',
        [
            ('Pitch Circle Diameter (PCD)', spreadsheet_document.Spreadsheet.HubHolesPlacement * 2),
            ('Number of bolts', spreadsheet_document.Hub.NumberOfHoles),
            ('Bolt diameter', spreadsheet_document.Spreadsheet.HubHoles * 2),
        ],
        book_reference_template % 'page 25 left-hand side'
    )


def create_steel_disk_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Steel Disk Sizes',
        [
            ('Diameter', spreadsheet_document.Spreadsheet.RotorDiskRadius * 2),
            ('Thickness', spreadsheet_document.Spreadsheet.DiskThickness),
            ('Central hole diameter', spreadsheet_document.Spreadsheet.RotorDiskCentralHoleDiameter),
        ],
        book_reference_template % 'page 25 right-hand side'
    )


def create_frame_dimensions_table(spreadsheet_document: Document) -> Element:
    header = 'Frame Dimensions'
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    if rotor_disk_radius < 187.5:
        return create_table(
            header,
            [
                (
                    'Length of upright A',
                    spreadsheet_document.Alternator.TShapeTwoHoleEndBracketLength
                ),
                ('Channel pieces B,C', spreadsheet_document.Alternator.BC),
                ('End bracket D', spreadsheet_document.Alternator.D),
                ('Position of shaft X', spreadsheet_document.Alternator.X),
                ('Steel angle section width', spreadsheet_document.Spreadsheet.MetalLengthL),
                ('Steel angle section thickness', spreadsheet_document.Spreadsheet.MetalThicknessL)
            ],
            book_reference_template % 'page 26 right-hand side'
        )
    elif rotor_disk_radius < 275:
        return create_table(
            header,
            [
                ('G', spreadsheet_document.Alternator.GG),
                ('H', spreadsheet_document.Alternator.HH)
            ],
            book_reference_template % 'page 27 right-hand side'
        )
    else:
        return create_table(
            header,
            [
                ('A', spreadsheet_document.Alternator.StarShapeTwoHoleEndBracketLength),
                ('B', spreadsheet_document.Alternator.B),
                ('C', spreadsheet_document.Alternator.CC)
            ]
        )


def create_alternator_frame_to_yaw_tube_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Alternator Frame to Yaw Tube Sizes',
        [
            ('Length of OD yaw tube', spreadsheet_document.YawBearing.YawPipeLength),
            ('I', spreadsheet_document.Alternator.I),
            ('J', spreadsheet_document.Alternator.j),
            ('K', spreadsheet_document.Alternator.k)
        ],
        book_reference_template % 'page 28 right-hand side'
    )


def create_frame_dimensions_flat_bar_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Frame Dimensions, Flat Bar',
        [
            ('L', spreadsheet_document.YawBearing.L),
            ('M', spreadsheet_document.YawBearing.MM),
            ('Offset', spreadsheet_document.Spreadsheet.Offset)
        ],
        book_reference_template % 'page 29 left-hand side'
    )


def create_steel_pipe_dimensions_for_tail_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Steel Pipe Dimensions for Tail',
        [
            ('Boom Length A', spreadsheet_document.Spreadsheet.BoomLength),
            ('Diameter B', spreadsheet_document.Spreadsheet.BoomPipeDiameter),
            ('Hinge Outer C', spreadsheet_document.Tail.HingeOuterPipeLength),
            ('Diameter D', spreadsheet_document.Tail.HingeOuterPipeRadius * 2),
            ('Hinge Inner E', spreadsheet_document.Tail.HingeInnerPipeLength),
            ('Diameter F', spreadsheet_document.Tail.HingeInnerPipeRadius)
        ],
        book_reference_template % 'page 31 right-hand side'
    )


def create_tail_vane_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Tail Vane Dimensions',
        [
            (
                'Tail hinge angle for battery charging',
                spreadsheet_document.Spreadsheet.VerticalPlaneAngle
            ),
            ('G', spreadsheet_document.Spreadsheet.VaneWidth),
            ('H', spreadsheet_document.Spreadsheet.VaneLength),
            ('Vane Thickness', spreadsheet_document.Spreadsheet.VaneThickness),
            (
                'Vane Bracket Thickness',
                spreadsheet_document.Spreadsheet.BracketThickness
            ),
            ('Vane Bracket Length J', spreadsheet_document.Spreadsheet.BracketLength),
            ('Vane Bracket Width', spreadsheet_document.Spreadsheet.BracketWidth)
        ],
        book_reference_template % 'page 32 bottom'
    )


def create_tail_junction_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Tail Junction Dimensions',
        [
            (
                'D', (
                    spreadsheet_document.Tail.TailHingeJunctionFullWidth -
                    (spreadsheet_document.Spreadsheet.YawPipeDiameter / 2) -
                    spreadsheet_document.Tail.HingeInnerPipeRadius
                )
            )
        ]
    )


def create_coil_winder_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Coil Winder Dimensions',
        [
            # Rectangular spacer dimensions
            ('A', spreadsheet_document.Alternator.RectangularVerticalDistanceOfHolesFromCenter * 2),
            ('B', spreadsheet_document.Spreadsheet.CoilInnerWidth1),
            ('C', spreadsheet_document.Spreadsheet.CoilInnerWidth2)
        ]
    )


def create_stator_mold_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Stator Mould Dimensions',
        [
            ('Mould side A', spreadsheet_document.Alternator.StatorMoldSideLength),
            ('Outer radius B', spreadsheet_document.Alternator.StatorHolesCircumradius),
            ('Inner radius C', spreadsheet_document.Alternator.StatorInnerHoleRadius),
            ('Mould thickness', spreadsheet_document.Spreadsheet.StatorThickness)
        ],
        book_reference_template % 'page 40'
    )


def create_rotor_mold_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Rotor Mould Dimensions',
        [
            ('Approx. mould side A', spreadsheet_document.Alternator.RotorMoldSideLength),
            ('Rotor radius B', spreadsheet_document.Alternator.RotorMoldSurroundRadius),
            ('Island radius C', spreadsheet_document.Alternator.IslandRadius),
            ('Island thickness', spreadsheet_document.Alternator.RotorMoldIslandThickness),
            ('Number of magnets', spreadsheet_document.Spreadsheet.NumberMagnet),
            ('Smaller radius D', (
                spreadsheet_document.Spreadsheet.RotorDiskRadius -
                spreadsheet_document.Spreadsheet.MagnetLength
            )),
            ('Larger radius E', spreadsheet_document.Spreadsheet.RotorDiskRadius),
            ('Circle radius', spreadsheet_document.Spreadsheet.MagnetWidth / 2)
        ],
        book_reference_template % 'page 42 & 43'
    )


def table(children: List[Element]) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table"""
    return {
        'tagName': 'table',
        'children': children
    }


def thead(children: List[Element]) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/thead"""
    return {
        'tagName': 'thead',
        'children': children
    }


def tbody(children: List[Element]) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tbody"""
    return {
        'tagName': 'tbody',
        'children': children
    }


def tfoot(children: List[Element]) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tfoot"""
    return {
        'tagName': 'tfoot',
        'children': children
    }


def tr(children: List[Element]) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr"""
    return {
        'tagName': 'tr',
        'children': children
    }


def td(content: Any = None, col_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td"""
    return tcell('td', content, col_span)


def th(content: Any = None, col_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/th"""
    return tcell('th', content, col_span)


def tcell(tag_name: str, content: Any = None, col_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/API/HTMLTableCellElement"""
    element = {
        'tagName': tag_name,
        'properties': {
            'textContent': "" if content is None else str(content)
        }
    }
    if col_span:
        element['properties']['colSpan'] = col_span
    return element
