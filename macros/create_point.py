"""
FreeCAD macro that creates a point from a vector in a spreadsheet.

To aid in visualizing how certain vectors are calculated.
"""
import random
import string
from typing import Optional, Tuple

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


def create_point(document: Document,
                 selected_point: Tuple[Vector, str]) -> None:
    vector, label = selected_point
    point = document.addObject("Part::Sphere", label)
    point.Placement.Base = vector
    point.Label = label
    point.ViewObject.ShapeColor = get_random_color()
    document.recompute()


def round_vector(vector: Vector, precision=2) -> Vector:
    return Vector([round(e, ndigits=precision) for e in vector])


class TaskPanel:
    def __init__(self,
                 default_document: Document,
                 selected_point: Tuple[Vector, str]):
        self.document = default_document
        self.selected_point = selected_point

        self.form = QtGui.QWidget()
        self.form.setWindowTitle('Create Point')

        layout = QtGui.QVBoxLayout(self.form)

        # Row 1
        row1 = QtGui.QHBoxLayout()

        vector, name = selected_point
        label = QtGui.QLabel(f'<strong>{name}:</strong>', self.form)
        vector = QtGui.QLabel(str(round_vector(vector)), self.form)

        row1.addWidget(label)
        row1.addWidget(vector)

        layout.addLayout(row1)

        # Row 2
        row2 = QtGui.QHBoxLayout()

        label = QtGui.QLabel('<strong>Document:</strong>', self.form)
        self.combo_box = self.create_combo_box()

        row2.addWidget(label)
        row2.addWidget(self.combo_box)

        layout.addLayout(row2)

    def create_combo_box(self):
        combo_box = QtGui.QComboBox(self.form)
        documents = list(App.listDocuments().keys())
        combo_box.addItems(documents)
        combo_box.activated[str].connect(self.handle_combo_box_activated)
        index = documents.index(self.document)
        combo_box.setCurrentIndex(index)
        return combo_box

    def handle_combo_box_activated(self, selected_document: str):
        self.document = App.listDocuments()[selected_document]

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        create_point(self.document, self.selected_point)
        Gui.Control.closeDialog()


def find_selected_point() -> Optional[Tuple[Vector, str]]:
    main_window = Gui.getMainWindow()
    # MDI (Multiple Document Interface)
    mdi_area = main_window.findChild(QtGui.QMdiArea)

    active_sub_window = mdi_area.activeSubWindow()
    if active_sub_window.widget().metaObject().className() == 'SpreadsheetGui::SheetView':
        sheet = active_sub_window.widget()
        table = sheet.findChild(QtGui.QTableView)
        indexes = table.selectedIndexes()
        if len(indexes) > 0:
            Console.PrintMessage(
                f'{len(indexes)} indexes selected, picking 1st.\n')
            first = indexes[0]
            row = str(first.row() + 1)
            column = map_number_to_column(first.column() + 1)
            cell_address = column + row
            selection = Gui.Selection.getSelection()
            if len(selection) > 0:
                Console.PrintMessage(
                    f'{len(selection)} objects selected, picking 1st.\n')
                selected_sheet = selection[0]
                if selected_sheet.TypeId == 'Spreadsheet::Sheet':
                    obj = selected_sheet.get(cell_address)
                    label = selected_sheet.getAlias(cell_address)
                    if isinstance(obj, Placement):
                        return obj.Base, label
                    elif isinstance(obj, Vector):
                        return obj, label
                    else:
                        Console.PrintWarning(
                            f'Selected cell {cell_address} does not contain vector.\n')
                else:
                    Console.PrintWarning(
                        f'Selected object must be sheet.\n')
            else:
                Console.PrintWarning('No selected objects.\n')
        else:
            Console.PrintWarning('No selected cell in spreasheet.\n')
    else:
        Console.PrintWarning('No active spreadsheet.\n')


selected_point = find_selected_point()
if selected_point:
    default_document = App.ActiveDocument.Name
    panel = TaskPanel(default_document, selected_point)
    Gui.Control.showDialog(panel)
