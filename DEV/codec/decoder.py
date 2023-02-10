import numpy as np
import matplotlib.pyplot as plt

def decode(data: bytearray, num_lines: int, num_col: int):
    """Decodes the given byte array in JPEG format
    to an image

    Args:
        data (bytearray): the byte array in JPEG format
        num_lines (int): number of lines of the image
        num_col (int): number of columns of the image
    """

    data = data[:num_lines, :num_col]

    plt.figure(2)
    plt.imshow(data)
    plt.show()

    pass