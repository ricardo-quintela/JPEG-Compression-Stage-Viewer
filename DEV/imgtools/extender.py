"""Contém funções para estender e cortar imagens
"""
from numpy import ndarray, newaxis, vstack, hstack

def add_padding(img: ndarray, min_size: int):
    """Adiciona preenchimento à imagem para complementar a falta de linhas/colunas
    para ajudar o codec JPEG na compressão


    Args:
        img (ndarray): a matriz da imagem
        min_size (int): o tamanho mínimo de linhas/colunas necessários para concluir

    Returns:
        Tuple[ndarray, int, int]: a imagem estendida e a linha antiga e o número da coluna
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
