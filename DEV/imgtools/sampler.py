"""Contem funções de subamostragem das imagens
"""

from typing import Tuple

from numpy import ndarray
from cv2 import resize


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
        channel2, (int(height / height_divide_cb), int(width / width_divide_cb))
    )
    channel3_resized = resize(
        channel3, (int(height / height_divide_cr), int(width / width_divide_cr))
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
