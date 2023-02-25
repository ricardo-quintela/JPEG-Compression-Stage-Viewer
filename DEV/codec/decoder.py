"""Contém funções de decode para o codec JPEG
"""

from typing import Tuple
from numpy import ndarray

from imgtools import converter_to_rgb
from imgtools import restore_padding
from imgtools import join_channels
from imgtools import up_sample


def decode(data: Tuple[ndarray, ndarray, ndarray], width: int, height: int) -> ndarray:
    """Decodifica a matriz de bytes dada em formato jpeg
    para uma imagem

    Args:
        data (Tuple[ndarray, ndarray, ndarray]): Os canais da imagem
        width (int): a largura da imagem original
        height (int): a altura da imagem original

    Returns:
        ndarray: a imagem descodificada
    """

    up_sampled = up_sample(data[0], data[1], data[2])

    image_r, image_g, image_b = converter_to_rgb(up_sampled[0], up_sampled[1], up_sampled[2])

    image_rgb_padded = join_channels(image_r, image_g, image_b)

    image_rgb = restore_padding(image_rgb_padded, width, height)

    return image_rgb
