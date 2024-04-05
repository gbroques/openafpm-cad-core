from pathlib import Path

__all__ = ['get_documents_path']


def get_documents_path() -> Path:
    package_path = Path(__file__).parent.absolute()
    return package_path.joinpath('documents')
