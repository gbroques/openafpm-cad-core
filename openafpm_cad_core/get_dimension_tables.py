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
    # TODO: Create only for T Shape?
    #       This information is repeated for H & Star in
    #       create_frame_dimensions_flat_bar_table
    tables.append(
        create_offset_table(spreadsheet_document)
    )
    if rotor_disk_radius < 187.5:
        tables.append(
            create_alternator_frame_to_yaw_pipe_sizes_table(
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
        create_magnets_and_coils_table(spreadsheet_document)
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
    tables.append(
        create_magnet_positioning_and_jig_dimensions_table(
            spreadsheet_document)
    )
    tables.append(
        create_various_parts_dimensions_table(spreadsheet_document)
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
                td(row[1])
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


def create_yaw_bearing_pipe_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Yaw Bearing Pipe Sizes',
        [
            ('Tower top stub outer diameter',
             round_and_format_length(spreadsheet_document.Tail.HingeInnerPipeDiameter, ndigits=1)),
            ('Yaw pipe outer diameter',
             round_and_format_length(spreadsheet_document.Spreadsheet.YawPipeDiameter, ndigits=1)),
        ],
        book_reference_template % 'page 24 left-hand side'
    )


def create_wheel_bearing_hub_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Wheel Bearing Hub',
        [
            ('Pitch Circle Diameter (PCD)',
             round_and_format_length(spreadsheet_document.Spreadsheet.HubPitchCircleDiameter)),
            ('Number of bolts', spreadsheet_document.Hub.NumberOfHoles),
            ('Bolt diameter', round_and_format_length(
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
        ],
        book_reference_template % 'page 25 left-hand side'
    )


def create_steel_disk_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Steel Disk Sizes',
        [
            ('Diameter', round_and_format_length(
                spreadsheet_document.Spreadsheet.RotorDiskRadius * 2)),
            ('Thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.RotorDiskThickness)),
            ('Central hole diameter',
             round_and_format_length(spreadsheet_document.Spreadsheet.RotorDiskCentralHoleDiameter)),
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
                    round_and_format_length(
                        spreadsheet_document.Alternator.TShapeTwoHoleEndBracketLength)
                ),
                ('Channel pieces B,C', round_and_format_length(
                    spreadsheet_document.Alternator.BC)),
                ('End bracket D', round_and_format_length(spreadsheet_document.Alternator.D)),
                ('Position of shaft X', round_and_format_length(
                    spreadsheet_document.Alternator.X)),
                ('Steel angle section width',
                 round_and_format_length(spreadsheet_document.Spreadsheet.MetalLengthL)),
                ('Steel angle section thickness',
                 round_and_format_length(spreadsheet_document.Spreadsheet.MetalThicknessL))
            ],
            book_reference_template % 'page 26 right-hand side'
        )
    elif rotor_disk_radius < 275:
        return create_table(
            header,
            [
                ('G', round_and_format_length(spreadsheet_document.Alternator.GG)),
                ('H', round_and_format_length(spreadsheet_document.Alternator.HH))
            ],
            book_reference_template % 'page 27 right-hand side'
        )
    else:
        return create_table(
            header,
            [
                ('A', round_and_format_length(
                    spreadsheet_document.Alternator.StarShapeTwoHoleEndBracketLength)),
                ('B', round_and_format_length(spreadsheet_document.Alternator.B)),
                ('C', round_and_format_length(spreadsheet_document.Alternator.CC))
            ]
        )


def create_alternator_frame_to_yaw_pipe_sizes_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Alternator Frame to Yaw Pipe Sizes',
        [
            ('Length of yaw bearing pipe',
             round_and_format_length(spreadsheet_document.HighEndStop.YawPipeLength)),
            ('I', round_and_format_length(spreadsheet_document.Alternator.I)),
            ('J', round_and_format_length(spreadsheet_document.Alternator.j)),
            ('K', round_and_format_length(spreadsheet_document.Alternator.k))
        ],
        book_reference_template % 'page 28 right-hand side'
    )


def create_offset_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Offset distance laterally from alternator center to yaw center',
        [
            ('Offset', round_and_format_length(spreadsheet_document.Spreadsheet.Offset))
        ],
        book_reference_template % 'page 27 right-hand side'
    )


def create_frame_dimensions_flat_bar_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Frame Dimensions, Flat Bar',
        [
            ('Offset', round_and_format_length(spreadsheet_document.Spreadsheet.Offset)),
            ('L length of flat bar', round_and_format_length(
                spreadsheet_document.YawBearing.L)),
            ('M width of flat bar', round_and_format_length(
                spreadsheet_document.YawBearing.MM)),
            ('Flat bar thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.FlatMetalThickness)),
            (
                'Length of yaw bearing pipe',
                round_and_format_length(spreadsheet_document.HighEndStop.YawPipeLength)
            )
        ],
        book_reference_template % 'page 29 left-hand side'
    )


def create_steel_pipe_dimensions_for_tail_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Steel Pipe Dimensions for Tail',
        [
            ('Boom length A', round_and_format_length(
                spreadsheet_document.Spreadsheet.BoomLength)),
            ('Diameter B', round_and_format_length(
                spreadsheet_document.Spreadsheet.BoomPipeDiameter, ndigits=1)),
            ('Hinge outer C', round_and_format_length(
                spreadsheet_document.Tail.HingeOuterPipeLength)),
            # See Also: Tail.HingeOuterPipeRadius in tail_cells.py
            ('Diameter D', round_and_format_length(
                spreadsheet_document.Spreadsheet.YawPipeDiameter, ndigits=1)),
            ('Hinge inner E', round_and_format_length(
                spreadsheet_document.Tail.HingeInnerPipeLength)),
            ('Diameter F', round_and_format_length(
                spreadsheet_document.Tail.HingeInnerPipeDiameter, ndigits=1))
        ],
        book_reference_template % 'page 31 right-hand side'
    )


def create_tail_vane_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Tail Vane Dimensions',
        [
            (
                'Tail hinge angle',
                round_and_format_angle(
                    spreadsheet_document.Spreadsheet.VerticalPlaneAngle)
            ),
            ('Vane plywood dimension G', round_and_format_length(
                spreadsheet_document.Spreadsheet.VaneWidth)),
            ('Vane plywood dimension H', round_and_format_length(
                spreadsheet_document.Spreadsheet.VaneLength)),
            ('Vane plywood thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.VaneThickness)),
            (
                'Vane bracket flat bar width',
                round_and_format_length(spreadsheet_document.Spreadsheet.BracketWidth)
            ),
            (
                'Vane bracket flat bar thickness',
                round_and_format_length(
                    spreadsheet_document.Spreadsheet.BracketThickness)
            ),
            (
                'Vane bracket flat bar length J',
                round_and_format_length(spreadsheet_document.Spreadsheet.BracketLength)
            )
        ],
        book_reference_template % 'page 32 bottom'
    )


def create_magnets_and_coils_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Magnets and Coils',
        [
            ('Number of rotor disks', 2),
            ('Magnets per rotor disk', spreadsheet_document.Spreadsheet.NumberMagnet),
            ('Magnet material', spreadsheet_document.Spreadsheet.MagnetMaterial),
            ('Magnet length', round_and_format_length(
                spreadsheet_document.Spreadsheet.MagnetLength)),
            ('Magnet width', round_and_format_length(
                spreadsheet_document.Spreadsheet.MagnetWidth)),
            ('Magnet thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.MagnetThickness)),
            ('Number of coils', spreadsheet_document.Spreadsheet.NumberOfCoilsPerPhase * 3),
            ('Weight of wire', round_and_format_weight(
                spreadsheet_document.Spreadsheet.WireWeight)),
            ('Wire diameter', format_length(
                spreadsheet_document.Spreadsheet.WireDiameter)),
            ('Number of wires in hand',
             spreadsheet_document.Spreadsheet.NumberOfWiresInHand),
            ('Turns per coil', spreadsheet_document.Spreadsheet.TurnsPerCoil)
        ]
    )


def create_tail_junction_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Tail Junction Cross Piece Dimensions',
        [
            (
                'Width of cross piece D', round_and_format_length(
                    spreadsheet_document.Tail.TailHingeJunctionFullWidth -
                    (spreadsheet_document.Spreadsheet.YawPipeDiameter / 2) -
                    spreadsheet_document.Tail.HingeInnerPipeRadius
                )
            ),
            ('Position from end of yaw bearing pipe',
             round_and_format_length(spreadsheet_document.Tail.TailHingeJunctionHeight))
        ]
    )


def create_coil_winder_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Coil Winder Dimensions',
        [
            ('A', round_and_format_length(
                spreadsheet_document.Alternator.RectangularVerticalDistanceOfHolesFromCenter * 2)),
            ('B', round_and_format_length(
                spreadsheet_document.Alternator.OuterHorizontalDistanceBetweenCenterOfSmallHoles)),
            ('C', round_and_format_length(
                spreadsheet_document.Alternator.InnerHorizontalDistanceBetweenCenterOfSmallHoles
                if spreadsheet_document.Spreadsheet.CoilType != 3 else
                spreadsheet_document.Alternator.CoilWinderDiskBottomHoleRadius * 2
            ))
        ]
    )


def create_stator_mold_dimensions_table(spreadsheet_document: Document) -> Element:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    return create_table(
        'Stator Mould Dimensions',
        [
            ('Mould side A', round_and_format_length(
                spreadsheet_document.Alternator.StatorMoldSideLength)),
            ('Outer radius B', round_and_format_length(
                spreadsheet_document.Alternator.StatorHolesCircumradius)),
            ('Inner radius C', round_and_format_length(
                spreadsheet_document.Alternator.StatorInnerHoleRadius)),
            (
                'Number of mounts',
                spreadsheet_document.Alternator.NumberOfStatorHoles
                if rotor_disk_radius <= 275 else 6
            ),
            ('Surround and island thickness',
             round_and_format_length(spreadsheet_document.Spreadsheet.StatorThickness))
        ],
        book_reference_template % 'page 40 left-hand side'
    )


def create_rotor_mold_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Rotor Mould Dimensions',
        [
            ('Mould side A', round_and_format_length(
                spreadsheet_document.Alternator.RotorMoldSideLength)),
            ('Rotor radius B', round_and_format_length(
                spreadsheet_document.Alternator.RotorMoldSurroundRadius)),
            ('Island radius C', round_and_format_length(
                spreadsheet_document.Alternator.IslandRadius)),
            ('Surround thickness',
             round_and_format_length(spreadsheet_document.Alternator.RotorMoldSurroundThickness)),
            ('Island thickness', round_and_format_length(
                spreadsheet_document.Alternator.RotorMoldIslandThickness)),
        ],
        book_reference_template % 'page 42 left-hand side'
    )


def create_magnet_positioning_and_jig_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Magnet Positioning Jig Dimensions',
        [
            ('Number of magnets', spreadsheet_document.Spreadsheet.NumberMagnet),
            ('Smaller radius D', round_and_format_length(
                spreadsheet_document.Spreadsheet.RotorDiskRadius -
                spreadsheet_document.Spreadsheet.MagnetLength
            )),
            ('Larger radius E', round_and_format_length(
                spreadsheet_document.Spreadsheet.RotorDiskRadius)),
            ('Circle radius', round_and_format_length(
                spreadsheet_document.Spreadsheet.MagnetWidth / 2))
        ],
        book_reference_template % 'page 42 & 43'
    )


def create_various_parts_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Various Parts Dimensions',
        [
            (
                'Hub studs length',
                'TODO: Adjust when blades are added.'
            ),
            ('Hub studs diameter', round_and_format_length(
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            (
                'Stator studs length',
                round_and_format_length(
                    spreadsheet_document.Alternator.StatorMountingStudsLength)
            ),
            (
                'Stator studs diameter',
                round_and_format_length(spreadsheet_document.Spreadsheet.HolesDiameter)),
            (
                'Vane bracket bolts diameter',
                round_and_format_length(spreadsheet_document.Spreadsheet.HolesDiameter)
            ),
            (
                'Thickness of all flat steel pieces',
                round_and_format_length(
                    spreadsheet_document.Spreadsheet.FlatMetalThickness)
            ),
            (
                'Wall thickness of yaw and tail hinge pipes',
                round_and_format_length(spreadsheet_document.Spreadsheet.PipeThickness)
            )
        ],
        book_reference_template % 'page 46 left-hand side'
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


def round_and_format_length(length: float, ndigits=None) -> str:
    return format_length(round(length, ndigits))


def format_length(length: float) -> str:
    return f'{length} mm'


def round_and_format_angle(angle: float, ndigits=None) -> str:
    return f'{round(angle, ndigits)}°'


def round_and_format_weight(length: float, ndigits=2) -> str:
    return f'{round(length, ndigits)} kg'
