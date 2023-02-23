"""Contém funções relacionadas com a Transformada 
de Coseno Discreta
"""

from typing import Tuple
from numpy import ndarray, zeros, r_

from scipy.fftpack import dct, idct


def calculate_dct(
        Y_channel: ndarray,
        Cb_channel: ndarray,
        Cr_channel: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula a DCT de um canal completo

    Args:
        Y_channel (ndarray): o canal Y
        Cb_channel (ndarray): o canal cb
        Cr_channel (ndarray): o canal cr

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a DCT calculada 
    """

    Y_dct = dct(dct(Y_channel, norm="ortho").T, norm="ortho").T
    Cb_dct = dct(dct(Cb_channel, norm="ortho").T, norm="ortho").T
    Cr_dct = dct(dct(Cr_channel, norm="ortho").T, norm="ortho").T

    return Y_dct, Cb_dct, Cr_dct


def calculate_inv_dct(
        Y_dct: ndarray,
        Cb_dct: ndarray,
        Cr_dct: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula o inverso da DCT de um canal completo

    Args:
        Y_dct (ndarray): o canal Y com a dct
        Cb_dct (ndarray): o canal Cb com a dct
        Cr_dct (ndarray): o canal Cr com a dct

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais originais (sem a dct)
    """

    Y_channel = idct(idct(Y_dct, norm="ortho").T, norm="ortho").T
    Cb_channel = idct(idct(Cb_dct, norm="ortho").T, norm="ortho").T
    Cr_channel = idct(idct(Cr_dct, norm="ortho").T, norm="ortho").T

    return Y_channel, Cb_channel, Cr_channel


def calculate_dct_8x8(
        Y_channel: ndarray,
        Cb_channel: ndarray,
        Cr_channel: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula a DCT em blocos 8x8 de um canal completo

    Args:
        Y_channel (ndarray): o canal Y
        Cb_channel (ndarray): o canal Cb
        Cr_channel (ndarray): o canal Cr

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a DCT em blocos 8x8 calculada     
    """

    size = Y_channel.shape
    Y_DCT8 = zeros(size)
    Cb_DCT8 = zeros(size)
    Cr_DCT8 = zeros(size)

    for i in r_[:size[0]:8]:
        for j in r_[:size[1]:8]:
            Y_DCT8[i:(i+8), j:(j+8)],
            Cb_DCT8[i:(i+8), j:(j+8)],
            Cr_DCT8[i:(i+8), j:(j+8)] = calculate_dct(Y_channel[i:(i+8), j:(j+8)],
                                                      Cb_channel[i:(
                                                          i+8), j:(j+8)],
                                                      Cr_channel[i:(i+8), j:(j+8)])

    return Y_DCT8, Cb_DCT8, Cr_DCT8


def calculate_inv_dct_8x8(
        Y_DCT8: ndarray,
        Cb_DCT8: ndarray,
        Cr_DCT8: ndarray
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula o inverso da DCT em blocos 8x8 de um canal completo

    Args:
        Y_DCT8 (ndarray): o canal Y
        Cb_DCT8 (ndarray): o canal cb
        Cr_DCT8 (ndarray): o canal cr

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais originais (sem a dct 8x8)
    """

    size = Y_DCT8.shape
    Y_channel = zeros(size)
    Cb_channel = zeros(size)
    Cr_channel = zeros(size)

    for i in r_[:size[0]:8]:
        for j in r_[:size[1]:8]:
            Y_DCT8[i:(i+8), j:(j+8)],
            Cb_channel[i:(i+8), j:(j+8)],
            Cr_channel[i:(i+8), j:(j+8)] = calculate_inv_dct(Y_DCT8[i:(i+8), j:(j+8)],
                                                             Cb_DCT8[i:(i+8), j:(j+8)], Cr_DCT8[i:(i+8), j:(j+8)])

    return Y_channel, Cb_channel, Cr_channel
