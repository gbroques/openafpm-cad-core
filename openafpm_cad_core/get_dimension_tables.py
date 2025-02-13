"""Module for retrieving dimensions to display in a tabular format."""
from typing import Any, Dict, List, Optional, Tuple, TypedDict

from FreeCAD import Document

try:
    # TODO: Remove this once freecad conda forge package includes python 3.11.
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

from .find_descendent_by_label import find_descendent_by_label
from .find_object_by_label import find_object_by_label
from .load import load_alernator
from .load_spreadsheet_document import load_spreadsheet_document
from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine_shape import (WindTurbineShape,
                                 map_rotor_disk_radius_to_wind_turbine_shape)

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
jacking_rods_length = 250  # in mm
estimated_coil_winder_handle_length = 350 # 35cm


def get_dimension_tables(magnafpm_parameters: MagnafpmParameters,
                         furling_parameters: FurlingParameters,
                         user_parameters: UserParameters,
                         img_path_prefix: str = '') -> List[Element]:
    spreadsheet_document = load_spreadsheet_document(magnafpm_parameters,
                                                     furling_parameters,
                                                     user_parameters)
    rotor_disk_radius = magnafpm_parameters['RotorDiskRadius']
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
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
        create_frame_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_offset_table(spreadsheet_document)
    )
    if wind_turbine_shape == WindTurbineShape.T:
        tables.append(
            create_alternator_frame_to_yaw_pipe_sizes_table(
                spreadsheet_document, img_path_prefix)
        )
    else:
        tables.append(
            create_frame_dimensions_flat_bar_table_top_view(spreadsheet_document, img_path_prefix)
        )
        tables.append(
            create_frame_dimensions_flat_bar_table_side_view(spreadsheet_document, img_path_prefix)
        )
    tables.append(
        create_steel_pipe_dimensions_for_tail_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_tail_junction_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_tail_vane_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_magnets_and_coils_table(spreadsheet_document)
    )
    tables.append(
        create_coil_winder_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_stator_mold_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_rotor_mold_dimensions_table(spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_magnet_positioning_jig_dimensions_table(
            spreadsheet_document, img_path_prefix)
    )
    tables.append(
        create_various_parts_dimensions_table(spreadsheet_document)
    )
    tables.append(create_total_pipe_length_by_outer_diameter_table(spreadsheet_document))
    tables.append(create_studs_nuts_and_washers_table(spreadsheet_document))
    tables.append(create_resin_table(spreadsheet_document))
    return tables


def create_table(header: str,
                 rows: List[Tuple[str, Any]],
                 footer_rows: Optional[List[str]] = None,
                 img_src_and_alt: Optional[Tuple[str, str]] = None,
                 img_style: Optional[str] = None) -> Element:
    col_span = 3 if img_src_and_alt else 2
    children = [
        thead([
            tr([
                th(header, col_span=col_span)
            ])
        ]),
        tbody([
            tr([
                td(row[0]),
                td(row[1])
            ]) for row in rows
        ])
    ]
    if img_src_and_alt:
        src, alt = img_src_and_alt
        table_body = children[1]
        first_row = table_body['children'][0]
        first_row['children'].append(td(img(src, alt, img_style), row_span=len(rows)))
    if footer_rows:
        children.append(
            tfoot([
                tr([td(row, col_span=col_span)])
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
            (
                'Yaw pipe wall thickness',
                round_and_format_length(spreadsheet_document.Spreadsheet.PipeThickness)
            ),
            ('Yaw pipe length',
             round_and_format_length(spreadsheet_document.HighEndStop.YawPipeLength)),
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
            ('Stainless steel screws', format_screw(
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


def create_frame_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    header = 'Frame Dimensions'
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    steel_angle_section_rows = [
        ('Steel angle section width',
         round_and_format_length(spreadsheet_document.Spreadsheet.MetalLengthL)),
        ('Steel angle section thickness',
         round_and_format_length(spreadsheet_document.Spreadsheet.MetalThicknessL)),
        ('Steel angle section length total',
         format_length(sum_angle_bar_length(spreadsheet_document))),
    ]
    if wind_turbine_shape == WindTurbineShape.T:
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
            [book_reference_template % 'page 26 right-hand side'],
            (img_path_prefix + 't-shape-frame.png', 'T shape frame')
        )
    elif wind_turbine_shape == WindTurbineShape.H:
        return create_table(
            header,
            [
                ('G', round_and_format_length(spreadsheet_document.Alternator.GG)),
                ('H', round_and_format_length(spreadsheet_document.Alternator.HH)),
                *steel_angle_section_rows
            ],
            [book_reference_template % 'page 27 right-hand side'],
            (img_path_prefix + 'h-shape-frame.png', 'H shape frame')
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
            ],
            img_src_and_alt=(img_path_prefix + 'star-shape-frame.png', 'Star shape frame')
        )


def create_alternator_frame_to_yaw_pipe_sizes_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    return create_table(
        'Alternator Frame to Yaw Pipe Sizes',
        [
            ('Length of yaw bearing pipe',
             round_and_format_length(spreadsheet_document.HighEndStop.YawPipeLength)),
            ('I', round_and_format_length(spreadsheet_document.Alternator.I)),
            ('J', round_and_format_length(spreadsheet_document.Alternator.j)),
            ('K', round_and_format_length(spreadsheet_document.Alternator.k))
        ],
        [book_reference_template % 'page 28 right-hand side'],
        img_src_and_alt=(img_path_prefix + 't-shape-yaw-bearing-frame-junction.png', 'T shape yaw bearing frame junction')
    )


def create_offset_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Offset distance laterally from alternator center to yaw center',
        [
            ('Offset', round_and_format_length(spreadsheet_document.Spreadsheet.Offset))
        ],
        [book_reference_template % 'page 27 right-hand side']
    )


def create_frame_dimensions_flat_bar_table_top_view(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    return create_table(
        'Frame Dimensions, Flat Bar Top View',
        [
            ('Offset', round_and_format_length(spreadsheet_document.Spreadsheet.Offset)),
            ('L length of flat bar', round_and_format_length(
                spreadsheet_document.YawBearing.L)),
            ('M width of flat bar', round_and_format_length(
                spreadsheet_document.YawBearing.MM))
        ],
        [book_reference_template % 'page 29 left-hand side'],
        (img_path_prefix + 'top-of-extended-frame.png', 'Top of extended frame')
    )


def create_frame_dimensions_flat_bar_table_side_view(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    return create_table(
        'Frame Dimensions, Flat Bar Side View',
        [
            ('N flat bar thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.FlatMetalThickness)),
            (
                'O length of yaw bearing pipe',
                round_and_format_length(spreadsheet_document.HighEndStop.YawPipeLength)
            ),
            ('P side piece flat bar length', round_and_format_length(
                spreadsheet_document.YawBearing.SideLength)),
            ('Q side piece flat bar width', round_and_format_length(
                spreadsheet_document.YawBearing.SideWidth)),
            ('R side piece flat bar thickness', round_and_format_length(
                spreadsheet_document.Spreadsheet.FlatMetalThickness)),
            ('S length from top of channel section to weld flat bar', round_and_format_length(
                spreadsheet_document.WindTurbine.LengthFromTopOfChannelSectionToWeldTopBar)),
        ],
        img_src_and_alt=(img_path_prefix + 'side-of-extended-frame.svg', 'Side of extended frame')
    )


def create_steel_pipe_dimensions_for_tail_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
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
                spreadsheet_document.Tail.HingeInnerPipeDiameter, ndigits=1)),
            (
                'Wall thickness of tail hinge pipes',
                round_and_format_length(spreadsheet_document.Spreadsheet.PipeThickness)
            )
        ],
        [book_reference_template % 'page 31 right-hand side'],
        (img_path_prefix + 'tail-boom-dimensions.png', 'Tail boom dimensions')
    )


def create_tail_vane_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
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
        [book_reference_template % 'page 32 bottom', 'Vane bracket bolts, nuts, and washers are stainless steel'],
        (img_path_prefix + 'tail-vane-dimensions.png', 'Tail vane dimensions')
    )


def create_magnets_and_coils_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Magnets and Coils',
        [
            ('Number of rotor disks', get_number_of_rotors(spreadsheet_document.Spreadsheet.RotorTopology)),
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


def create_tail_junction_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
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
        ],
        img_src_and_alt=(img_path_prefix + 'tail-hinge-junction-cover-top-dimensions.svg', 'Width of cross piece D')
    )


def create_coil_winder_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    coil_type = spreadsheet_document.Spreadsheet.CoilType
    if coil_type == 1:
        img_src_and_alt = (img_path_prefix + 'rectangular-coil-winder-dimensions.svg', 'Rectangular coil winder dimensions')
    elif coil_type == 2:
        img_src_and_alt = (img_path_prefix + 'keyhole-coil-winder-dimensions.svg', 'Keyhole coil winder dimensions')
    else:
        img_src_and_alt = (img_path_prefix + 'triangular-coil-winder-dimensions.svg', 'Triangular coil winder dimensions')
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
            )),
            ('Threaded rod diameter', f'M{round(spreadsheet_document.Alternator.CoilWinderCenterRodDiameter)}'),
            ('Pin diameter', f'M{round(spreadsheet_document.Alternator.CoilWinderPinDiameter)}')
        ],
        img_src_and_alt = img_src_and_alt,
        # Decrease size of coil winder dimensions, other images have a max-width of 480px by default
        img_style='max-width: 330px'
    )


def create_stator_mold_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    number_of_locating_bolts = 3
    if wind_turbine_shape == WindTurbineShape.T:
        img_src = img_path_prefix + 't-shape-stator-mould-dimensions.png'
    elif wind_turbine_shape == WindTurbineShape.H:
        img_src = img_path_prefix + 'h-shape-stator-mould-dimensions.png'
    else:
        img_src = img_path_prefix + 'star-shape-stator-mould-dimensions.png'
    return create_table(
        'Stator Mould Dimensions',
        [
            ('Mould side A', round_and_format_length(
                spreadsheet_document.Alternator.StatorMoldSideLength)),
            ('Outer radius B', round_and_format_length(
                spreadsheet_document.Alternator.StatorHolesCircumradius
                if wind_turbine_shape != wind_turbine_shape.STAR else
                spreadsheet_document.Alternator.HexagonalStatorOuterCircumradius)),
            ('Inner radius C', round_and_format_length(
                spreadsheet_document.Alternator.StatorInnerHoleRadius)),
            (
                'Number of mounts',
                spreadsheet_document.Alternator.NumberOfStatorHoles
                if wind_turbine_shape != wind_turbine_shape.STAR else 6
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
             format_screw(
                 spreadsheet_document.Alternator.StatorMoldSurroundNumberOfScrews +
                 spreadsheet_document.Alternator.StatorMoldIslandNumberOfScrews,
                 spreadsheet_document.Fastener.WoodScrewDiameter,
                 spreadsheet_document.Alternator.StatorMoldScrewLength))
        ],
        [book_reference_template % 'page 40 left-hand side'],
        (img_src, 'Stator mould dimensions')
    )


def calculate_number_of_stator_mold_bolts(spreadsheet_document: Document) -> int:
    return (
        spreadsheet_document.Alternator.StatorMoldIslandNumberOfBolts +
        spreadsheet_document.Alternator.StatorMoldSurroundNumberOfBolts
    )


def create_rotor_mold_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    number_of_rotors = get_number_of_rotors(spreadsheet_document.Spreadsheet.RotorTopology)
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
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts * number_of_rotors,
                spreadsheet_document.Spreadsheet.HubHolesDiameter,
                spreadsheet_document.Fastener.HubHolesBoltLength)),
            ('Nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfRotorMoldBolts * number_of_rotors,
                spreadsheet_document.Spreadsheet.HubHolesDiameter)),
            ('Screws', format_screw(
                spreadsheet_document.Alternator.NumberOfRotorMoldScrews * number_of_rotors,
                spreadsheet_document.Fastener.WoodScrewDiameter,
                spreadsheet_document.Alternator.RotorMoldScrewLength)),
        ],
        [book_reference_template % 'page 42 left-hand side'],
        (img_path_prefix + 'rotor-mould-dimensions.png', 'Rotor mould dimensions')
    )


def create_magnet_positioning_jig_dimensions_table(spreadsheet_document: Document, img_path_prefix: str = '') -> Element:
    rows = [
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
    ]
    if spreadsheet_document.Spreadsheet.MagnetMaterial == 'Neodymium':
        rows.append(('Washers (standard)', format_fastener(
            spreadsheet_document.Alternator.NumberOfRotorMoldBolts,
            spreadsheet_document.Spreadsheet.HubHolesDiameter)))
    return create_table(
        'Magnet Positioning Jig Dimensions',
        rows,
        [book_reference_template % 'page 42 & 43'],
        (img_path_prefix + 'magnet-positioning-jig-dimensions.png', 'Magnet positioning jig dimensions')
    )


def create_various_parts_dimensions_table(spreadsheet_document: Document) -> Element:
    return create_table(
        'Various Parts Dimensions',
        [
            (
                'Thickness of all flat steel pieces',
                round_and_format_length(
                    spreadsheet_document.Spreadsheet.FlatMetalThickness)
            )
        ]
    )


def create_total_pipe_length_by_outer_diameter_table(spreadsheet_document: Document) -> Element:
    pipe_outer_diameter_length_tuples = get_pipe_outer_diameter_length_tuples(spreadsheet_document)
    pipe_outer_diameter_total_length_tuples = sum_length_by_diameter(pipe_outer_diameter_length_tuples)
    rows = [
        (f'{outer_diameter} mm outer diameter pipe length', format_length(length))
        for outer_diameter, length in pipe_outer_diameter_total_length_tuples
    ]
    return create_table('Total pipe length by outer diameter', rows)


def create_studs_nuts_and_washers_table(spreadsheet_document: Document) -> Element:
    number_of_blade_assembly_fasteners = spreadsheet_document.Hub.NumberOfHoles * 2
    studs_diameter_length_tuples = get_studs_diameter_length_tuples(spreadsheet_document)
    studs_diameter_total_length_tuples = sum_length_by_diameter(studs_diameter_length_tuples)
    rows = [
        (f'{diameter} mm diameter studs length total', format_length(length))
        for diameter, length in studs_diameter_total_length_tuples
    ]
    return create_table(
        'Studs, nuts, & washers',
        [
            (
                'Bearing hub studs',
                format_fastener(
                    spreadsheet_document.Hub.NumberOfHoles,
                    spreadsheet_document.Spreadsheet.HubHolesDiameter,
                    spreadsheet_document.Alternator.HubStudsLength)
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
                'Stator studs',
                format_fastener(
                    spreadsheet_document.Alternator.NumberOfStatorHoles,
                    spreadsheet_document.Spreadsheet.HolesDiameter,
                    spreadsheet_document.Alternator.StatorMountingStudsLength)
            ),
            ('Stator assembly nuts', format_fastener(
                spreadsheet_document.Alternator.NumberOfStatorHoles * 4,
                spreadsheet_document.Spreadsheet.HolesDiameter)),
            ('Stator assembly washers (standard)', format_fastener(
                spreadsheet_document.Alternator.NumberOfStatorHoles * 2,
                spreadsheet_document.Spreadsheet.HolesDiameter)),
            ('Jacking studs', format_fastener(
                spreadsheet_document.Alternator.NumberOfJackingHoles,
                spreadsheet_document.Alternator.JackingRodDiameter,
                jacking_rods_length)),
            ('Jacking hole diameter', format_length(spreadsheet_document.Alternator.JackingHoleDiameter)),
            ('Threaded rod for coil winder',
             format_fastener(
                1,
                 spreadsheet_document.Alternator.CoilWinderCenterRodDiameter,
                 spreadsheet_document.Alternator.CoilWinderCenterRodLength + estimated_coil_winder_handle_length)),
            * rows
        ],
        ['All except jacking studs are stainless steel']
    )


def create_resin_table(spreadsheet_document: Document) -> Element:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    # Multiply by scale factor to get same weight that recipe book suggests on page 63
    # Verify in the two upcoming workshops: India and Habibi.
    if wind_turbine_shape == WindTurbineShape.T:
        resin_weight_scale_factor = 1.49
    else:
        resin_weight_scale_factor = 1.7

    alternator_document = load_alernator()
    stator = find_object_by_label(alternator_document, 'Stator')
    stator_resin_cast = find_descendent_by_label(stator, 'ResinCast')
    coils = find_descendent_by_label(stator, 'Coils')
    rotor_back = find_object_by_label(alternator_document, 'Rotor_Back')
    rotor_resin_cast = find_descendent_by_label(rotor_back, 'Rotor_ResinCast')
    magnets = find_descendent_by_label(rotor_back, 'Rotor_Magnets')
    stator_resin_volume = stator_resin_cast.Shape.Volume - coils.Shape.Volume
    rotor_resin_volume = rotor_resin_cast.Shape.Volume - magnets.Shape.Volume
    number_of_rotors = get_number_of_rotors(spreadsheet_document.Spreadsheet.RotorTopology)
    total_rotor_resin_volume = rotor_resin_volume * number_of_rotors
    total_resin_volume = stator_resin_volume + total_rotor_resin_volume
    # Density is 1.15 g/cm3 according to:
    # https://www.strandek.co.uk/articles/what-is-vinyl-ester-resin/
    # Divide by 1,000 twice to convert g/cm3 to kg/mm3
    vinyl_ester_resin_density = 0.000001015  # kg/mm3
    weight_of_resin = total_resin_volume * vinyl_ester_resin_density * resin_weight_scale_factor
    return create_table(
        'Resin',
        [
            (
                'Estimated weight of vinyl ester resin',
                round_and_format_weight(weight_of_resin, ndigits=2)
            ),
            (
                'Estimated weight of talcum powder',
                round_and_format_weight(round(weight_of_resin, ndigits=2) / 2)
            )
        ]
    )


def sum_length_by_diameter(diameter_length_tuples: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    length_by_outer_diameter = {}
    for outer_diameter, length in diameter_length_tuples:
        rounded_length = round(length)
        if outer_diameter not in length_by_outer_diameter:
            length_by_outer_diameter[outer_diameter] = rounded_length
        else:
            length_by_outer_diameter[outer_diameter] += rounded_length
    return list(sorted(length_by_outer_diameter.items()))


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


def get_studs_diameter_length_tuples(spreadsheet_document: Document) -> List[Tuple[float, float]]:
    return [
        (
            spreadsheet_document.Spreadsheet.HubHolesDiameter,
            round(spreadsheet_document.Alternator.HubStudsLength) *
            spreadsheet_document.Hub.NumberOfHoles
        ),
        (
            spreadsheet_document.Spreadsheet.HolesDiameter,
            round(spreadsheet_document.Alternator.StatorMountingStudsLength) *
            spreadsheet_document.Alternator.NumberOfStatorHoles
        ),
        (
            spreadsheet_document.Alternator.JackingRodDiameter,
            jacking_rods_length *
            spreadsheet_document.Alternator.NumberOfJackingHoles
        ),
        (
             spreadsheet_document.Alternator.CoilWinderCenterRodDiameter,
             spreadsheet_document.Alternator.CoilWinderCenterRodLength + estimated_coil_winder_handle_length
        )
    ]


def sum_angle_bar_length(spreadsheet_document: Document) -> float:
    rotor_disk_radius = spreadsheet_document.Spreadsheet.RotorDiskRadius
    wind_turbine_shape = map_rotor_disk_radius_to_wind_turbine_shape(rotor_disk_radius)
    if wind_turbine_shape == WindTurbineShape.T:
        return sum([
            round(spreadsheet_document.Alternator.TShapeTwoHoleEndBracketLength),
            round(spreadsheet_document.Alternator.BC) * 2,
            round(spreadsheet_document.Alternator.D)
        ])
    elif wind_turbine_shape == WindTurbineShape.H:
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


def td(content: Any = None, col_span: Optional[int] = None, row_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td"""
    return tcell('td', content, col_span, row_span)


def th(content: Any = None, col_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/HTML/Element/th"""
    return tcell('th', content, col_span)


def tcell(tag_name: str, content: Any = None, col_span: Optional[int] = None, row_span: Optional[int] = None) -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/API/HTMLTableCellElement"""
    element: Element = {
        'tagName': tag_name,
        'properties': {}
    }
    if isinstance(content, dict):
        element['children'] = [content]
    else:
        element['properties'] = {
            'textContent': "" if content is None else str(content)
        }

    if col_span is not None:
        element['properties']['colSpan'] = col_span
    if row_span is not None:
        element['properties']['rowSpan'] = row_span
    return element


def img(src: str, alt: str, style: str = '') -> Element:
    """https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement"""
    element: Element = {
        'tagName': 'img',
        'properties': {
            'src': src,
            'alt': alt,
            'style': style
        }
    }
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
    return 'M' + format_screw(quantity, diameter, length)


def format_screw(quantity: int, diameter: int, length: Optional[float] = None) -> str:
    display = str(diameter)
    if length is not None:
        display += f' × {round_and_format_length(length)}'
    display += f' — {quantity} pieces'
    return display


def get_number_of_rotors(rotor_topology: str) -> int:
    return 2 if rotor_topology == 'Double' else 1
