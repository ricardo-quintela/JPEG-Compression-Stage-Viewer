"""Contains functions to extend and cut images
"""
from numpy import ndarray, newaxis, vstack, hstack

def add_padding(img: ndarray, min_size: int):
    """Adds padding to the image to complement the lack of rows/columns
    to aid the JPEG codec in compression


    Args:
        img (ndarray): the image array
        min_size (int): the minimum size of rows/cols required to complete

    Returns:
        Tuple[ndarray, int, int]: the extended image and the old row and column number
    """

    # unpack the image rows and cols
    num_rows, num_cols, *_ = img.shape

    # calculate how many rows need to be added
    new_num_rows = min_size - (num_rows % min_size)
    new_num_col = min_size - (num_cols % min_size)

    if new_num_col == 0 or new_num_rows == 0:
        return img, num_rows, num_cols

    # create a row array with the same constitution as the last row of the image
    last_row = img[num_rows-1, :][newaxis, :]

    # repeat the row N times to complete the min_size
    rep_rows = last_row.repeat(new_num_rows, axis=0)

    # add the rows to the image
    img_row_padded = vstack([img, rep_rows])

    # create a column array with the same constitution as the last column of the image
    last_column = img_row_padded[: ,num_cols-1][:, newaxis]

    # repeat the column M times to complete the min_size
    rep_column = last_column.repeat(new_num_col, axis=1)

    # add the columns to the image
    img_padded = hstack([img_row_padded, rep_column])

    return img_padded, num_rows, num_cols
