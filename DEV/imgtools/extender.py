"""Contém funções para estender e cortar imagens
"""
from typing import Tuple

from numpy import ndarray, newaxis, vstack, hstack
from cv2 import resize, INTER_LINEAR


def add_padding(img: ndarray, min_size: int) -> Tuple[ndarray, int, int]:
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


def restore_padding(img: ndarray, width: int, height: int) -> ndarray:
    """Restora a imagem original removendo o preenchimento adicionado
    na altura da compressão

    Args:
        img (ndarray): a matriz da imagem
        width (int): a largura da imagem original
        height (int): a altura da imagem original

    Returns:
        ndarray: a matriz da imagem restaurada
    """
    return img[:width, :height]



def down_sample(
    channel1: ndarray, channel2: ndarray, channel3: ndarray, scale: Tuple[int, int, int]
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        channel1 (ndarray): o primeiro canal
        channel2 (ndarray): o segundo canal
        channel3 (ndarray): o terceiro canal
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = channel1.shape

    height_divide_cr = int(scale[0] / scale[1])
    height_divide_cb = height_divide_cr
    width_divide_cr = 1
    width_divide_cb = 1

    if scale[2] != 0:
        height_divide_cb = int(scale[0] / scale[2])
    else:
        width_divide_cr = height_divide_cr
        width_divide_cb = width_divide_cr

    channel2_resized = resize(
        channel2, (int(height / height_divide_cb), int(width / width_divide_cb)), interpolation=INTER_LINEAR
    )
    channel3_resized = resize(
        channel3, (int(height / height_divide_cr), int(width / width_divide_cr)), interpolation=INTER_LINEAR
    )

    return channel1, channel2_resized, channel3_resized


def up_sample(
    channel1: ndarray, channel2: ndarray, channel3: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        channel1 (ndarray): o primeiro canal
        channel2 (ndarray): o segundo canal
        channel3 (ndarray): o terceiro canal
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    # caso tenham a mesma shape não é necessário processar
    if channel1.shape == channel2.shape == channel3.shape:
        return channel1, channel2, channel3

    # extrair a shape do primeiro canal que terá o tamanho original
    width, height = channel1.shape

    channel2_resized = resize(channel2, (int(height), int(width)))
    channel3_resized = resize(channel3, (int(height), int(width)))

    return channel1, channel2_resized, channel3_resized

