import FreeCAD as App

__all__ = ['close_all_documents']


def close_all_documents() -> None:
    [App.closeDocument(d.Name) for d in App.listDocuments().values()]
