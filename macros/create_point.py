"""
FreeCAD macro that creates point(s) from placement(s) or vector(s) in a spreadsheet.

To aid in visualizing how certain vectors are calculated.

Usage:
Select Placement or Vector in a spreadsheet, then activate macro.
"""
import random
import string
from typing import Optional, Tuple, List

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console, Document, Placement, Vector
from PySide import QtGui


def get_random_color() -> Tuple[float, float, float, float]:
    return (
        random.randint(0, 255) * 1.0,
        random.randint(0, 255) * 1.0,
        random.randint(0, 255) * 1.0,
        1.0
    )


def map_number_to_column(number: int) -> str:
    """
    >>> map_number_to_column(1)
    'A'

    >>> map_number_to_column(2)
    'B'

    >>> map_number_to_column(26)
    'Z'

    >>> map_number_to_column(27)
    'AA'

    >>> map_number_to_column(28)
    'AB'

    >>> map_number_to_column(52)
    'AZ'

    >>> map_number_to_column(702)
    'ZZ'
    """
    if number < 1:
        raise ValueError('Number {} must be greater than 0.'.format(number))
    num_letters = len(string.ascii_uppercase)
    if number > num_letters:
        first = map_number_to_column((number - 1) // num_letters)
        second = map_number_to_column(number % num_letters)
        return first + second
    return string.ascii_uppercase[number - 1]


def create_points(document: Document,
                  selected_points: List[Tuple[Vector, str]]) -> None:
    color = get_random_color()
    document.openTransaction('create_points')
    for selected_point in selected_points:
        vector, label = selected_point
        point = document.addObject("Part::Sphere", label)
        point.Placement.Base = vector
        point.Label = label
        point.ViewObject.ShapeColor = color
    document.recompute()
    document.commitTransaction()


def round_vector(vector: Vector, precision=2) -> Vector:
    return Vector([round(e, ndigits=precision) for e in vector])


class TaskPanel:
    def __init__(self,
                 default_document: Document,
                 selected_points: List[Tuple[Vector, str]]):
        self.document = default_document
        self.selected_points = selected_points

        self.form = QtGui.QWidget()
        self.form.setWindowTitle('Create Point(s)')

        layout = QtGui.QVBoxLayout(self.form)

        # Row
        row1 = QtGui.QHBoxLayout()

        label = QtGui.QLabel('<strong>Document:</strong>', self.form)
        self.combo_box = self.create_combo_box()

        row1.addWidget(label)
        row1.addWidget(self.combo_box)

        layout.addLayout(row1)

        # Row for each point
        for selected_point in selected_points:
            row = QtGui.QHBoxLayout()
            vector, name = selected_point
            label = QtGui.QLabel(f'<strong>{name}:</strong>', self.form)
            vector = QtGui.QLabel(str(round_vector(vector)), self.form)

            row.addWidget(label)
            row.addWidget(vector)

            layout.addLayout(row)

    def create_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        documents = list(App.listDocuments().keys())
        combo_box.addItems(documents)
        combo_box.activated[str].connect(self.handle_combo_box_activated)
        index = documents.index(self.document.Name)
        combo_box.setCurrentIndex(index)
        return combo_box

    def handle_combo_box_activated(self, selected_document: str):
        self.document = App.listDocuments()[selected_document]

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        create_points(self.document, self.selected_points)
        Gui.Control.closeDialog()


def find_selected_points() -> Optional[List[Tuple[Vector, str]]]:
    main_window = Gui.getMainWindow()
    # MDI (Multiple Document Interface)
    mdi_area = main_window.findChild(QtGui.QMdiArea)

    active_sub_window = mdi_area.activeSubWindow()
    if active_sub_window is None:
        Console.PrintWarning(f'No active sub-window.\n')
        return
    if active_sub_window.widget().metaObject().className() == 'SpreadsheetGui::SheetView':
        sheet = active_sub_window.widget()
        table = sheet.findChild(QtGui.QTableView)
        indexes = table.selectedIndexes()
        if len(indexes) == 0:
            Console.PrintWarning('No selected cell in spreasheet.\n')
        selected_points = []
        for index in indexes:
            row = str(index.row() + 1)
            column = map_number_to_column(index.column() + 1)
            cell_address = column + row
            selection = Gui.Selection.getSelection()
            if len(selection) > 0:
                if len(selection) > 1:
                    Console.PrintWarning(
                        f'{len(selection)} objects selected, picking 1st.\n')
                selected_sheet = selection[0]
                if selected_sheet.TypeId == 'Spreadsheet::Sheet':
                    obj = selected_sheet.get(cell_address)
                    label = selected_sheet.getAlias(cell_address)
                    if isinstance(obj, Placement):
                        selected_points.append((obj.Base, label))
                    elif isinstance(obj, Vector):
                        selected_points.append((obj, label))
                    else:
                        Console.PrintWarning(
                            f'Selected cell {cell_address} does not contain vector.\n')
                else:
                    Console.PrintWarning(
                        f'Selected object must be sheet.\n')
            else:
                Console.PrintWarning('No selected objects.\n')
        return selected_points
    else:
        Console.PrintWarning('No active spreadsheet.\n')


selected_points = find_selected_points()
if selected_points and len(selected_points) > 0:
    default_document = App.ActiveDocument
    panel = TaskPanel(default_document, selected_points)
    Gui.Control.showDialog(panel)
