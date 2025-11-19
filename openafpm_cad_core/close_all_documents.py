import FreeCAD as App

__all__ = ['close_all_documents']


def close_all_documents() -> None:
    """Close all open FreeCAD documents safely, handling deleted objects."""
    documents = list(App.listDocuments().values())  # Create a copy to avoid iteration issues
    for doc in documents:
        # Check if document still exists and has a valid Name attribute
        if hasattr(doc, 'Name') and doc.Name:
            App.closeDocument(doc.Name)
