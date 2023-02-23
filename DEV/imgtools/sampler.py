"""Contem funções de subamostragem das imagens
"""

from typing import Tuple

from numpy import ndarray
from cv2 import resize


def down_sample(
    channel1: ndarray,
    channel2: ndarray,
    channel3: ndarray,
    scale: Tuple[int, int, int]
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        y_channel (ndarray): o primeiro canal
        cb_channel (ndarray): o segundo canal
        cr_channel (ndarray): o terceiro canal
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = channel1.shape

    # 4 2 2
    # 4 2 0

    # 4 4 4
    # 4 4 2
    # 4 2 1
    # 4 1 1

    if scale[1] == 2:
        height /= 2
    if scale[2] == 0:
        width /= 2

    channel2_resized = resize(channel2, (int(height), int(width)))
    channel3_resized = resize(channel3, (int(height), int(width)))

    return channel1, channel2_resized, channel3_resized


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
