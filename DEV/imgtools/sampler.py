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
        channel1 (ndarray): o primeiro canal
        channel2 (ndarray): o segundo canal
        channel3 (ndarray): o terceiro canal
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = channel1.shape

    width_divide_cr = int(scale[0]/scale[1])
    width_divide_cb = width_divide_cr
    height_divide_cr = 1
    height_divide_cb = 1

    if scale[2] != 0:
        width_divide_cb = int(scale[0]/scale[2])
    else:
        height_divide_cr = width_divide_cr
        height_divide_cb = height_divide_cr

    channel2_resized = resize(channel2, (int(height / height_divide_cb), int(width / width_divide_cb)))
    channel3_resized = resize(channel3, (int(height / height_divide_cr), int(width / width_divide_cr)))

    return channel1, channel2_resized, channel3_resized


def up_sample(
    y_channel: ndarray,
    channel2: ndarray,
    channel3: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        y_channel (ndarray): o canal Y
        channel2 (ndarray): o canal cb
        channel3 (ndarray): o canal cr
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """

    width, height = y_channel.shape

    channel2_resized = resize(channel2, (int(height), int(width)))
    channel3_resized = resize(channel3, (int(height), int(width)))

    return y_channel, channel2_resized, channel3_resized
