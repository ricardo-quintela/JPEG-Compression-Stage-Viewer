from numpy import zeros, uint8, ndarray
from typing import Tuple

from imgtools import converter_to_rgb
from imgtools import restore_padding


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

    image_y = data[0]
    image_cb = data[1]
    image_cr = data[2]

    image_r, image_g, image_b = converter_to_rgb(image_y, image_cb, image_cr)

    shape = (data[0].shape[0], data[0].shape[1], 3)

    image_rgb_padded = zeros(shape, dtype=uint8)
    image_rgb_padded[:,:,0] = image_r
    image_rgb_padded[:,:,1] = image_g
    image_rgb_padded[:,:,2] = image_b

    image_rgb = restore_padding(image_rgb_padded, width, height)

    return image_rgb
