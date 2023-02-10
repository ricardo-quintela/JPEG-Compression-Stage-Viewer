import numpy as np

from imgtools import read_bmp
# import matplotlib.pyplot as plt

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
    colunms = img[num_col-1, :][:, np.newaxis]
    rep_lines = lines.repeat(new_num_lines, axis=0)
    rep_col = lines.repeat(new_num_col, axis=1)

    img_padded = np.vstack([img, rep_lines])
    img_paddedd = np.vstack([img_padded, rep_col])

    plt.imshow(img_paddedd)
    plt.show()

    pass


