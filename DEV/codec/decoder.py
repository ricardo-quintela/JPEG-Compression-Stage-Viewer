from typing import Tuple
from numpy import zeros, uint8, ndarray

from imgtools import converter_to_rgb
from imgtools import restore_padding
from imgtools import join_channels


def decode(data: Tuple[ndarray], width: int, height: int) -> ndarray:
    """Decodifica a matriz de bytes dada em formato jpeg
    para uma imagem

    Args:
        data (Tuple[ndarray]): A matriz de bytes em formato JPEG
        width (int): a largura da imagem original
        height (int): a altura da imagem original

    Returns:
        ndarray: a imagem descodificada
    """

    image_r, image_g, image_b = converter_to_rgb(data[0], data[1], data[2])

    image_rgb_padded = join_channels(image_r, image_g, image_b)

    image_rgb = restore_padding(image_rgb_padded, width, height)

    return image_rgb
