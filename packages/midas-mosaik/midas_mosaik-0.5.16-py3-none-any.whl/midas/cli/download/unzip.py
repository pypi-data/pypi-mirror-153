import os
from zipfile import ZipFile


def unzip(path, fname, target):
    """Unzip a file.

    Parameters
    ----------
    path: str
        The path where the file to unzip is located. This is also the
        path where the unzipped files will be located.
    fname: str
        The name of the file to unzip.
    target: str
        The name of the folder to which the files of the archive will
        be extracted to.

    """
    with ZipFile(os.path.join(path, fname), "r") as zip_ref:
        zip_ref.extractall(os.path.join(path, target))
