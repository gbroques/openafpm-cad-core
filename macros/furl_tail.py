from math import cos, radians, sin

import Draft
import FreeCAD as App
from FreeCAD import Vector

documents_by_name = App.listDocuments()

tail_document = documents_by_name['Tail']

# tail
tail = tail_document.getObjectsByLabel('Tail')[0]

# furl_angle
main_document = documents_by_name['Master_of_Puppets']
furl_angle = main_document.HighEndStop.FurlAngle.Value

tail_angle = tail_document.Spreadsheet.TailAngle

# center
x = tail_document.Spreadsheet.OuterTailHingeX
y = 0
z = tail_document.Spreadsheet.OuterTailHingeZ
center = Vector(x, y, z)

# axis
axis = Vector(sin(radians(tail_angle)), 0, cos(radians(tail_angle)))

Draft.rotate(
    [tail],
    furl_angle,
    center,
    axis=axis,
    copy=False)
