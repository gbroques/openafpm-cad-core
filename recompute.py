import FreeCAD as App


sort_in_dependency_order = True
document_by_name = App.listDocuments(sort_in_dependency_order)
documents = document_by_name.values()
for document in documents:
    for obj in doc.Objects:
        obj.recompute()
    document.recompute(None, True, True)
