"""Contains functions for image reading purposes
"""

from os.path import isfile

from matplotlib.pyplot import imread
from numpy import ndarray


def read_bmp(path: str) -> ndarray:
    """Reads a bmp file

    Args:
        path (str): the path to the bmp file

    Returns:
        ndarray: an array with the image pixel values in RGB format
            or None if the file is invalid or an error occurs
    """

    if not path.endswith(".bmp"):
        print("File format is not of type 'bmp'")
        return

    if not isfile(path):
        print("Given path is not a file")
        return

    return imread(path)
