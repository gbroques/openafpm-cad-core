"""
FreeCAD macro that creates point(s) from placement(s) or vector(s) in a spreadsheet.

To aid in visualizing how certain vectors are calculated.

Usage:
Select Placement or Vector in a spreadsheet, then activate macro.
"""
import random
from typing import List, Optional, Tuple

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


def create_points(document: Document,
                  selected_points: List[Tuple[Vector, str]]) -> None:
    # TODO: Provide more options around colors like:
    #       - Allow user to specify color.
    #       - Vary colors per points, or have them all be the same color.
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


def does_not_have_attrs(obj: object, *attrs) -> bool:
    return all([not hasattr(obj, attr) for attr in attrs])


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

        # TODO Improve workflow by:
        #      - Remember last selected document
        #      - Sort documents which ones are open as Gui windows
        #      - Potentially provide separate dropdown for documents with active Gui window
        #      - Provide text box filter for documents dropdown.
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
    log = Console.PrintWarning
    if main_window is None:
        log(f'Gui has no main window.\n')
        return
    active_window = main_window.getActiveWindow()
    if active_window is None:
        log(f'Main window has no active window.\n')
        return
    if does_not_have_attrs(active_window, 'getSheet', 'selectedCells'):
        log(f'Active window must be spreadsheet.\n')
        return
    sheet = active_window.getSheet()
    selected_cells = active_window.selectedCells()
    if len(selected_cells) == 0:
        log('Select cells that contain Vector or Placement objects.\n')
    selected_points = []
    for cell_address in selected_cells:
        obj = sheet.get(cell_address)
        label = sheet.getAlias(cell_address) or f'Point{cell_address}'
        if isinstance(obj, Placement):
            selected_points.append((obj.Base, label))
        elif isinstance(obj, Vector):
            selected_points.append((obj, label))
        else:
            log(
                f'Selected cell {cell_address} does not contain Vector or Placement object.\n')
    return selected_points


selected_points = find_selected_points()
if selected_points and len(selected_points) > 0:
    default_document = App.ActiveDocument
    panel = TaskPanel(default_document, selected_points)
    Gui.Control.showDialog(panel)
