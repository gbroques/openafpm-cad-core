import Draft
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Console, Document
from PySide import QtGui

main_document_name = 'Master_of_Puppets'


def get_document(name: str) -> Document:
    documents_by_name = App.listDocuments()
    return documents_by_name[name]


def get_main_document() -> Document:
    return get_document(main_document_name)


def furl_tail(furl_angle: float):
    tail_document = get_document('Tail')
    tail_document.openTransaction('furl')

    main_document = get_main_document()

    # tail
    tail = tail_document.getObjectsByLabel('Tail')[0]

    # center
    center = main_document.HighEndStop.OuterTailHingeBase

    # axis
    axis = main_document.HighEndStop.FurlAxis

    Draft.rotate(
        [tail],
        furl_angle,
        center,
        axis=axis,
        copy=False)

    # Recompute to prevent switching to Tail document automatically.
    App.activeDocument().recompute()

    tail_document.commitTransaction()


class TaskPanel:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle('Furl Tail')

        self.furl_angle = 0.0

        layout = QtGui.QVBoxLayout(self.form)

        # Row 1
        row1 = QtGui.QHBoxLayout()

        label = QtGui.QLabel(
            '<strong>Furl Angle:</strong> (in degrees)', self.form)
        self.double_spin_box = self.create_double_spin_box()

        row1.addWidget(label)
        row1.addWidget(self.double_spin_box)

        layout.addLayout(row1)

    def create_double_spin_box(self):
        double_spin_box = QtGui.QDoubleSpinBox(self.form)
        double_spin_box.setRange(-360, 360)
        double_spin_box.valueChanged.connect(
            self.handle_double_spin_box_value_changed)
        main_document = get_main_document()
        double_spin_box.setValue(
            main_document.HighEndStop.MaximumFurlAngle.Value)
        return double_spin_box

    def handle_double_spin_box_value_changed(self, value: float):
        self.furl_angle = value

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        furl_tail(self.furl_angle)
        Gui.Control.closeDialog()


documents_by_name = App.listDocuments()

if 'Tail' in documents_by_name and main_document_name in documents_by_name:
    Gui.Control.showDialog(TaskPanel())
else:
    Console.PrintWarning(
        f'{main_document_name} & Tail documents must be open.\n')
