'''Custom Sphinx directive for viewing FreeCAD spreadsheets defined in Python code as HTML tables.

To use, add the ``.. freecad-spreadsheet::`` directive to the docstring of any zero-argument function producing a 2-dimensional list of ``Cell`` objects (i.e. ``List[List[Cell]]``).

For example:

.. code-block:: python

   def get_cells() -> List[List[Cell]]:
       """Get example cells for a FreeCAD Spreadhseet.
       
       .. freecad-spreadsheet::
       """
       return [
           [
               Cell('Inputs', styles=[Style.UNDERLINE])
           ],
           [
               Cell('BracketThickness'),
               Cell('=Spreadsheet.BracketThickness',
                   alias='BracketThickness')
           ]
       ]

The FreeCAD Spreadsheet directive will produce HTML tables with various class names to emulate how FreeCAD styles spreadsheets.

These class names include ``underline`` and ```freecad-spreadsheet-alias``.

It's recommended to include a custom CSS stylesheet to target these class names:

.. code-block:: css

   /**
    * FreeCAD Spreadsheet directive styles.
    */
   .underline {
       text-decoration: underline
   }

   .freecad-spreadsheet-alias {
       background-color: #feffaa !important;
   }
   .freecad-spreadsheet-alias > span {
       border-bottom: 1px dotted;
   }

    /**
     * Make tables span 100% width of parent,
     * and cell content wrap instead of horizontal scrolling.
     * .wy-table-responsive class is specific to sphinx_rtd_theme.
     */
   .wy-table-responsive > table.docutils {
       table-layout: fixed;
       width: 100%;
   }
   .wy-table-responsive > .docutils td {
       word-wrap: break-word;
       white-space: normal;
   }

See `Adding Custom CSS to Sphinx Documentation <https://docs.readthedocs.io/en/stable/guides/adding-custom-css.html>`_ for details on how to do this.
'''
import importlib
import re
from itertools import repeat
from typing import List

import FreeCAD as App
from docutils import nodes
from docutils.nodes import Element, Inline, TextElement
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .spreadsheet import Cell, Style

logger = logging.getLogger(__name__)


class underline(Inline, TextElement):
    """Underline text for emphasis.

    :meta private:
    """
    pass


def visit_underline(self, node: Element):
    """Visitor function for underline node.

    :meta private:
    """
    self.body.append(self.starttag(node, 'span', CLASS='underline'))


def depart_underline(self, node: Element):
    """Depart function for underline node.

    :meta private:
    """
    pass


class spreadsheet_alias(Inline, TextElement):
    """Represents an aliased cell in a FreeCAD spreadsheet.

    :meta private:
    """

    def __init__(self, alias, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.alias = alias


def visit_spreadsheet_alias(self, node: Element) -> None:
    """Visitor function for spreadsheet_alias node.

    :meta private:
    """
    self.body.append(f'<span title={node.alias}>')


def depart_spreadsheet_alias(self, node: Element) -> None:
    """Depart function for spreadsheet_alias node.

    :meta private:
    """
    self.body.append('</span>')


class FreeCADSpreadsheet(SphinxDirective):

    has_content = False
    optional_arguments = 0

    def run(self):
        source_info = self.get_source_info()
        source = source_info[0]
        pattern = re.compile('.* of (.*)')
        # (e.g. openafpm_cad_core.create_spreadsheet_document.fastener_cells.get_fastener_cells)
        class_path = pattern.match(source).group(1)
        class_path_parts = class_path.split('.')
        # (e.g. get_fastener_cells)
        function_name = class_path_parts[-1]
        # (e.g. enafpm_cad_core.create_spreadsheet_document.fastener_cells)
        module_path = '.'.join(class_path_parts[:-1])
        function_module = importlib.import_module(module_path)
        function = getattr(function_module, function_name)
        try:
            cells = function()
            data, number_of_columns = _build_rows(cells)
        except TypeError:
            logger.warning(
                'Unable to call {}.\n'.format(function_name) +
                'Expecting zero-agrument function that returns List[List[Cell]]:\n' +
                '    {}()\n'.format(function_name), location=source_info)
            data = []
            number_of_columns = 0
        return _build_table(data, number_of_columns)


def _build_table(data, number_of_columns):
    colwidths = tuple(repeat(1, times=number_of_columns))
    table = nodes.table()
    tgroup = nodes.tgroup(cols=number_of_columns)
    table += tgroup
    for colwidth in colwidths:
        tgroup += nodes.colspec(colwidth=colwidth)
    tbody = nodes.tbody()
    tgroup += tbody
    for data_row in data:
        tbody += _create_table_row(data_row)
    return [table]


def _build_rows(cells: List[List[Cell]]):
    rows = []
    number_of_columns = 0
    for column in cells:
        number_of_columns = max(number_of_columns, len(column))
        row = []
        for cell in column:
            num_styles = len(cell.styles)
            if num_styles:
                prev_node = None
                for i, style in enumerate(cell.styles):
                    node = _get_node(style)
                    is_last_style = i == num_styles - 1
                    node_instance = None
                    if not is_last_style:
                        node_instance = node()
                    else:
                        node_instance = node(text=str(cell))
                    if i == 0:
                        row.append(node_instance)
                    else:
                        prev_node += node_instance
                    prev_node = node_instance
            else:
                if cell.alias:
                    node = spreadsheet_alias(cell.alias, text=str(cell))
                    row.append(
                        node
                    )
                else:
                    row.append(
                        nodes.inline(text=str(cell))
                    )
        rows.append(row)
    return rows, number_of_columns


def _get_node(style: Style):
    if style == Style.BOLD:
        return nodes.strong
    elif style == Style.ITALIC:
        return nodes.emphasis
    elif style == Style.UNDERLINE:
        return underline
    else:
        raise ValueError('Unrecognized Style ' + str(style))


def _create_table_row(row_cells):
    row = nodes.row()
    for cell in row_cells:
        entry = None
        if isinstance(cell, spreadsheet_alias):
            entry = nodes.entry(classes=['freecad-spreadsheet-alias'])
            entry['title'] = cell.alias
        else:
            entry = nodes.entry()
        row += entry
        entry += cell
    return row


def setup(app: App) -> None:
    """Setup extension.

    :param app: application object controlling high-level functionality,
                such as the setup of extensions, event dispatching, and logging.

    See Also:
    https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx
    """
    app.add_node(underline, html=(visit_underline, depart_underline))
    app.add_node(spreadsheet_alias, html=(
        visit_spreadsheet_alias, depart_spreadsheet_alias))
    app.add_directive('freecad-spreadsheet', FreeCADSpreadsheet)
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
