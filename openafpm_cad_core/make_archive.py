"""Module for "zipping up" the contents of a directory recursively into an archive.
"""
import os
import shutil

__all__ = ['make_archive']


def make_archive(source: str) -> bytes:
    """Recursively "zip up" the contents of source into an archive.

    Adapted from:
        http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-a-directory-recursively-including-the-root-folder/

    .. code-block:: python

       make_archive('/path/to/folder')

    :param source: Directory from where to create the archive from.
    :returns: Binary content of ZIP archive file.
    """
    format = 'zip'
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(source, format, archive_from, archive_to)
    destination = source + '.' + format
    with open(destination, 'rb') as zip:
        bytes_content = zip.read()
    return bytes_content
