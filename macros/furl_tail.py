import Draft
import FreeCAD as App

documents_by_name = App.listDocuments()

tail_document = documents_by_name['Tail']
tail_document.openTransaction('furl')

main_document = documents_by_name['Master_of_Puppets']

# tail
tail = tail_document.getObjectsByLabel('Tail')[0]

# furl_angle
furl_angle = main_document.HighEndStop.FurlAngle.Value

vertical_plane_angle = main_document.Spreadsheet.VerticalPlaneAngle

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

tail_document.commitTransaction()
