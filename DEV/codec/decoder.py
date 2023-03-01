"""Contém funções de decode para o codec JPEG
"""

from typing import Tuple
from numpy import ndarray

from imgtools import converter_to_rgb
from imgtools import restore_padding
from imgtools import join_channels
from imgtools import up_sample
from imgtools import inv_quantize
from imgtools import calculate_inv_dct
from imgtools import dpcm_decoder

from file_worker import load_q_matrix


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

    q_matrix_y = load_q_matrix("q_matrix_y.csv")
    q_matrix_cbcr = load_q_matrix("q_matrix_cbcr.csv")

    de_DPCM = (
        dpcm_decoder(data[0]),
        dpcm_decoder(data[1]),
        dpcm_decoder(data[2])
    )
    
    de_quantized = (
        inv_quantize(de_DPCM[0], q_matrix_y),
        inv_quantize(de_DPCM[1], q_matrix_cbcr),
        inv_quantize(de_DPCM[2], q_matrix_cbcr)
    )

    inv_dct = calculate_inv_dct(
        de_quantized[0],
        de_quantized[1],
        de_quantized[2],
        8
    )

    up_sampled = up_sample(inv_dct[0], inv_dct[1], inv_dct[2])

    image_r, image_g, image_b = converter_to_rgb(up_sampled[0], up_sampled[1], up_sampled[2])

    image_rgb_padded = join_channels(image_r, image_g, image_b)

    image_rgb = restore_padding(image_rgb_padded, width, height)

    return image_rgb
