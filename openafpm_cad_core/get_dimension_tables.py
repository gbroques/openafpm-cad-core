"""Module for retrieving dimensions to display in a tabular format."""
from typing import Any, Dict, List, Optional, Tuple, TypedDict

from FreeCAD import Document
from typing_extensions import NotRequired

from .get_documents_path import get_documents_path
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .upsert_spreadsheet_document import upsert_spreadsheet_document

__all__ = ['get_dimension_tables']


class Element(TypedDict):
    """
    Loosely-based on:
    https://developer.mozilla.org/en-US/docs/Web/API/Element
    """
    tagName: str
    children: NotRequired[List['Element']]
    properties: NotRequired[Dict[str, Any]]


book_reference_template = 'A Wind Turbine Recipe Book (2014 metric edition), %s'


def get_dimension_tables(magnafpm_parameters: MagnafpmParameters,
                         furling_parameters: FurlingParameters,
                         user_parameters: UserParameters) -> List[Element]:
    name = 'Master_of_Puppets'
    documents_path = get_documents_path()
    spreadsheet_document_path = documents_path.joinpath(f'{name}.FCStd')
    spreadsheet_document = upsert_spreadsheet_document(spreadsheet_document_path,
                                                       magnafpm_parameters,
                                                       furling_parameters,
                                                       user_parameters)
    rotor_disk_radius = magnafpm_parameters['RotorDiskRadius']
    tables = []
    tables.append(
        create_dimension_of_hub_plywood_pieces_table(spreadsheet_document)
    )
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
    tables.append(
        create_offset_table(spreadsheet_document)
    )
    if rotor_disk_radius < 187.5:
        tables.append(
            create_alternator_frame_to_yaw_pipe_sizes_table(
                spreadsheet_document)
        )
    else:
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
        create_magnet_positioning_jig_dimensions_table(
            spreadsheet_document)
    )
    tables.append(
        create_various_parts_dimensions_table(spreadsheet_document)
    )
    tables.append(create_total_pipe_length_by_outer_diameter_table(spreadsheet_document))
    tables.append(create_studs_nuts_and_washers_table(spreadsheet_document))
    return tables


def create_table(header: str,
                 rows: List[Tuple[str, Any]],
                 footer_rows: Optional[List[str]] = None) -> Element:
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
    if footer_rows:
        children.append(
            tfoot([
                tr([td(row, col_span=2)])
                for row in footer_rows
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
        [book_reference_template % 'page 24 left-hand side']
    )


def create_dimension_of_hub_plywood_pieces_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Dimensions of hub plywood pieces',
        [
            ('Thickness',
             round_and_format_length(spreadsheet_document.Blade.BladeAssemblyPlateThickness)),
            ('Disk diameter',
             round_and_format_length(spreadsheet_document.Blade.BladeAssemblyBackDiskDiameter)),
            ('Triangle side',
             round_and_format_length(spreadsheet_document.Blade.BladeAssemblyFrontTriangleSideLength)),
            ('Stainless steel screws', format_fastener(
                sum_hub_plywood_screws(spreadsheet_document),
                spreadsheet_document.Fastener.WoodScrewDiameter,
                spreadsheet_document.Blade.BladeAssemblyScrewLength)),
        ],
        [book_reference_template % 'page 20 right-hand side']
    )


def sum_hub_plywood_screws(spreadsheet_document: Document) -> int:
    return (
        spreadsheet_document.Blade.NumberOfBackDiskScrews +
        spreadsheet_document.Blade.MinimumNumberOfFrontTriangleScrews +
        spreadsheet_document.Blade.NumberOfAdditionalInnerScrews +
        spreadsheet_document.Blade.NumberOfAdditionalOuterScrews
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
        [book_reference_template % 'page 25 left-hand side']
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
        [book_reference_template % 'page 25 right-hand side']
    )


def create_frame_dimensions_table(spreadsheet_document: Document) -> Element:
    header = 'Frame Dimensions'
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    steel_angle_section_rows = [
        ('Steel angle section length total',
         format_length(sum_angle_bar_length(spreadsheet_document))),
        ('Steel angle section width',
         round_and_format_length(spreadsheet_document.Spreadsheet.MetalLengthL)),
        ('Steel angle section thickness',
         round_and_format_length(spreadsheet_document.Spreadsheet.MetalThicknessL))
    ]
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
                *steel_angle_section_rows
            ],
            [book_reference_template % 'page 26 right-hand side']
        )
    elif rotor_disk_radius < 275:
        return create_table(
            header,
            [
                ('G', round_and_format_length(spreadsheet_document.Alternator.GG)),
                ('H', round_and_format_length(spreadsheet_document.Alternator.HH)),
                *steel_angle_section_rows
            ],
            [book_reference_template % 'page 27 right-hand side']
        )
    else:
        return create_table(
            header,
            [
                ('A', round_and_format_length(
                    spreadsheet_document.Alternator.StarShapeTwoHoleEndBracketLength)),
                ('B', round_and_format_length(spreadsheet_document.Alternator.B)),
                ('C', round_and_format_length(spreadsheet_document.Alternator.CC)),
                *steel_angle_section_rows
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
        [book_reference_template % 'page 28 right-hand side']
    )


def create_offset_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Offset distance laterally from alternator center to yaw center',
        [
            ('Offset', round_and_format_length(spreadsheet_document.Spreadsheet.Offset))
        ],
        [book_reference_template % 'page 27 right-hand side']
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
            ),
            ('Side piece flat bar length', round_and_format_length(
                spreadsheet_document.YawBearing.SideLength)),
            ('Side piece flat bar width', round_and_format_length(
                spreadsheet_document.YawBearing.SideWidth)),
            ('Side piece flat bar thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.FlatMetalThickness)),
        ],
        [book_reference_template % 'page 29 left-hand side']
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
            ('Diameter D', round_and_format_length(
                spreadsheet_document.Tail.HingeOuterPipeDiameter, ndigits=1)),
            ('Hinge inner E', round_and_format_length(
                spreadsheet_document.Tail.HingeInnerPipeLength)),
            ('Diameter F', round_and_format_length(
                spreadsheet_document.Tail.HingeInnerPipeDiameter, ndigits=1))
        ],
        [book_reference_template % 'page 31 right-hand side']
    )


def create_tail_vane_dimensions_table(spreadsheet_document: Document) -> Element:
    number_of_vane_bracket_fasteners = 4
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
            ),
            (
                'Vane bracket bolts',
                format_fastener(
                    number_of_vane_bracket_fasteners,
                    spreadsheet_document.Spreadsheet.HolesDiameter,
                    spreadsheet_document.Fastener.TailVaneBracketBoltLength)
            ),
            (
                'Vane bracket nuts',
                format_fastener(
                    number_of_vane_bracket_fasteners,
                    spreadsheet_document.Spreadsheet.HolesDiameter)
            ),
            (
                'Vane bracket washers (large)',
                format_fastener(
                    number_of_vane_bracket_fasteners,
                    spreadsheet_document.Spreadsheet.HolesDiameter)
            ),
        ],
        [book_reference_template % 'page 32 bottom']
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
            ('Cheek piece diameter', round_and_format_length(
                spreadsheet_document.Alternator.CoilWinderDiskRadius * 2)),
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
    number_of_locating_bolts = 3
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
                if rotor_disk_radius < 275 else 6
            ),
            ('Surround and island thickness',
             round_and_format_length(spreadsheet_document.Spreadsheet.StatorThickness)),
            ('Bolts (fully threaded)',
             format_fastener(
                 calculate_number_of_stator_mold_bolts(spreadsheet_document),
                 spreadsheet_document.Alternator.StatorMoldBoltDiameter,
                 spreadsheet_document.Alternator.StatorMoldBoltLength)),
            ('Locating Bolts (fully threaded)',
             format_fastener(
                 number_of_locating_bolts,
                 spreadsheet_document.Alternator.LocatingBoltDiameter,
                 spreadsheet_document.Alternator.LocatingBoltLength)),
            ('Nuts',
             format_fastener(
                 calculate_number_of_stator_mold_bolts(spreadsheet_document) + number_of_locating_bolts,
                 spreadsheet_document.Alternator.StatorMoldBoltDiameter)),
            ('Washers (large)',
             format_fastener(
                 calculate_number_of_stator_mold_bolts(spreadsheet_document) + number_of_locating_bolts,
                 spreadsheet_document.Alternator.StatorMoldBoltDiameter)),
            ('Screws',
             format_fastener(
                 # Surround screws
                 (4 * 2) * spreadsheet_document.Alternator.NumberOfStatorHoles +
                 # Island screws
                 2 * spreadsheet_document.Alternator.StatorMoldIslandNumberOfScrews,
                 spreadsheet_document.Fastener.WoodScrewDiameter,
                 spreadsheet_document.Alternator.StatorMoldScrewLength))
        ],
        [book_reference_template % 'page 40 left-hand side']
    )


def calculate_number_of_stator_mold_bolts(spreadsheet_document: Document) -> int:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    return (
        spreadsheet_document.Alternator.StatorMoldIslandNumberOfBolts +
        spreadsheet_document.Alternator.NumberOfStatorHoles * 4
        if rotor_disk_radius < 275 else
        spreadsheet_document.Alternator.StatorMoldIslandNumberOfBolts + 24
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
            ('Bolts (fully threaded)', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
                spreadsheet_document.Spreadsheet.HubHolesDiameter,
                spreadsheet_document.Fastener.HubHolesBoltLength)),
            ('Nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Screws', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldScrews,
                spreadsheet_document.Fastener.WoodScrewDiameter,
                spreadsheet_document.Alternator.RotorMoldScrewLength)),
        ],
        [book_reference_template % 'page 42 left-hand side']
    )


def create_magnet_positioning_jig_dimensions_table(spreadsheet_document: Document) -> Element:
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
                spreadsheet_document.Spreadsheet.MagnetWidth / 2)),
            ('Bolts (fully threaded)', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
                spreadsheet_document.Spreadsheet.HubHolesDiameter,
                spreadsheet_document.Fastener.HubHolesBoltLength)),
            ('Nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Washers (standard)', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
        ],
        [book_reference_template % 'page 42 & 43']
    )


def create_various_parts_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Various Parts Dimensions',
        [
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
        [book_reference_template % 'page 46 left-hand side']
    )


def create_studs_nuts_and_washers_table(spreadsheet_document: Document) -> Element:
    number_of_blade_assembly_fasteners = spreadsheet_document.Hub.NumberOfHoles * 2
    return create_table(
        'Studs, nuts, & washers',
        [
            (
                'Hub studs length',
                round_and_format_length(spreadsheet_document.Alternator.HubStudsLength)
            ),
            (
                'Hub studs diameter',
                round_and_format_length(spreadsheet_document.Spreadsheet.HubHolesDiameter)
            ),
            ('Blade assembly nuts', format_fastener(
                number_of_blade_assembly_fasteners,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Blade assembly washers (large)', format_fastener(
                number_of_blade_assembly_fasteners,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Rotor disk assembly nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfNutsBetweenRotorDisks +
                spreadsheet_document.Hub.NumberOfHoles,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Rotor disk assembly washers (standard)', format_fastener(
                spreadsheet_document.Alternator.NumberOfWashersBetweenRotorDisks,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            (
                'Stator studs length',
                round_and_format_length(spreadsheet_document.Alternator.StatorMountingStudsLength)
            ),
            (
                'Stator studs diameter',
                round_and_format_length(spreadsheet_document.Spreadsheet.HolesDiameter)
            ),
            ('Stator assembly nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfStatorHoles * 4,
                spreadsheet_document.Spreadsheet.HolesDiameter)),
            ('Stator assembly washers (standard)', format_fastener(
                spreadsheet_document.Alternator.NumberOfStatorHoles * 2,
                spreadsheet_document.Spreadsheet.HolesDiameter)),
        ]
    )


def create_total_pipe_length_by_outer_diameter_table(spreadsheet_document: Document) -> Element:
    pipe_outer_diameter_length_tuples = get_pipe_outer_diameter_length_tuples(spreadsheet_document)
    length_by_outer_diameter = {}
    for outer_diameter, length in pipe_outer_diameter_length_tuples:
        rounded_length = round(length)
        if outer_diameter not in length_by_outer_diameter:
            length_by_outer_diameter[outer_diameter] = rounded_length
        else:
            length_by_outer_diameter[outer_diameter] += rounded_length
    outer_diameter_length_items = sorted(length_by_outer_diameter.items())
    rows = [
        (f'{outer_diameter} mm outer diameter pipe length', format_length(length))
        for outer_diameter, length in outer_diameter_length_items
    ]
    return create_table('Total pipe length by outer diameter', rows)


def get_pipe_outer_diameter_length_tuples(spreadsheet_document: Document) -> List[Tuple[float, float]]:
    return [
        (
            spreadsheet_document.Spreadsheet.YawPipeDiameter,
            spreadsheet_document.HighEndStop.YawPipeLength
        ),
        (
            spreadsheet_document.Tail.HingeOuterPipeDiameter,
            spreadsheet_document.Tail.HingeOuterPipeLength
        ),
        (
            spreadsheet_document.Tail.HingeInnerPipeDiameter,
            spreadsheet_document.Tail.HingeInnerPipeLength
        ),
        (
            spreadsheet_document.Spreadsheet.BoomPipeDiameter,
            spreadsheet_document.Spreadsheet.BoomLength
        )
    ]


def sum_angle_bar_length(spreadsheet_document: Document) -> float:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    if rotor_disk_radius < 187.5:
        return sum([
            round(spreadsheet_document.Alternator.TShapeTwoHoleEndBracketLength),
            round(spreadsheet_document.Alternator.BC) * 2,
            round(spreadsheet_document.Alternator.D)
        ])
    elif rotor_disk_radius < 275:
        return sum([
            round(spreadsheet_document.Alternator.GG) * 2,
            round(spreadsheet_document.Alternator.HH) * 2
        ])
    else:
        return sum([
            round(spreadsheet_document.Alternator.StarShapeTwoHoleEndBracketLength) * 2,
            round(spreadsheet_document.Alternator.B) * 2,
            round(spreadsheet_document.Alternator.CC) * 2
        ])


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
    element: Element = {
        'tagName': tag_name,
        'properties': {
            'textContent': "" if content is None else str(content)
        }
    }
    if col_span is not None:
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


def format_fastener(quantity: int, diameter: int, length: Optional[float] = None) -> str:
    display = f'M{diameter}'
    if length is not None:
        display += f' × {round_and_format_length(length)}'
    display += f' — {quantity} pieces'
    return display
