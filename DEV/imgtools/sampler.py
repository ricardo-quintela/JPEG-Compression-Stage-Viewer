"""Contem funções de subamostragem das imagens
"""

from typing import Tuple

from numpy import ndarray
from cv2 import resize


def down_sample(
    y_channel: ndarray,
    cb_channel: ndarray,
    cr_channel: ndarray,
    scale: Tuple[int, int, int]
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        y_channel (ndarray): o canal Y
        cb_channel (ndarray): o canal cb
        cr_channel (ndarray): o canal cr
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = y_channel.shape

    width_divide_cr = int(scale[0]/scale[1])
    width_divide_cb = width_divide_cr
    height_divide_cr = 1
    height_divide_cb = 1

    if scale[2] != 0:
        width_divide_cb = int(scale[0]/scale[2])
    else:
        height_divide_cr = width_divide_cr
        height_divide_cb = height_divide_cr

    cb_channel_resized = resize(cb_channel, (int(height / height_divide_cb), int(width / width_divide_cb)))
    cr_channel_resized = resize(cr_channel, (int(height / height_divide_cr), int(width / width_divide_cr)))

    return y_channel, cb_channel_resized, cr_channel_resized


def up_sample(
    y_channel: ndarray,
    cb_channel: ndarray,
    cr_channel: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        y_channel (ndarray): o canal Y
        cb_channel (ndarray): o canal cb
        cr_channel (ndarray): o canal cr
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = y_channel.shape

    cb_channel_resized = resize(cb_channel, (int(height), int(width)))
    cr_channel_resized = resize(cr_channel, (int(height), int(width)))

    return y_channel, cb_channel_resized, cr_channel_resized
