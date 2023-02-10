import numpy as np
import matplotlib.pyplot as plt

from imgtools import read_bmp

def encode(path: str):
    """Encodes the image file on the given path to a JPEG format

    Args:
        path (str): the path to the file
    """


    # Ex4

    img = read_bmp(path)

    [num_lines, num_col, channels] = img.shape

    new_num_lines = 32 - (num_lines % 32)
    new_num_col = 32 - (num_col % 32)

    lines = img[num_lines-1, :][np.newaxis, :]
    rep_lines = lines.repeat(new_num_lines, axis=0)

    img_line_padded = np.vstack([img, rep_lines])
    
    columns = img_line_padded[: ,num_col-1][:, np.newaxis]
    rep_col = columns.repeat(new_num_col, axis=1)
    
    img_padded = np.hstack([img_line_padded, rep_col])

    
    plt.imshow(img_padded)

    return img_padded, num_lines, num_col


