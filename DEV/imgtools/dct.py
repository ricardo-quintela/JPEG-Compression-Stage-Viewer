"""Contém funções relacionadas com a Transformada 
de Coseno Discreta
"""

from typing import Tuple
from numpy import ndarray, float32, zeros

from scipy.fftpack import dct, idct


def calculate_dct(
    y_channel: ndarray, cb_channel: ndarray, cr_channel: ndarray, block_size: int = None
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula a DCT em blocos de um tamanho fornecido\n
    Caso não seja fornecido é calculada a dct no canal todo\n
    Os blocos têm que ser multiplos de 8\n\n

    Os canais passados têm que ser uma matriz de valores no intervalo [0, 255]

    Args:
        y_channel (ndarray): o canal Y
        cb_channel (ndarray): o canal cb
        cr_channel (ndarray): o canal cr
        block_size (int, optional): o tamanho dos blocos em que a
        dct vai ser calculada. Default a None.

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a DCT calculada
    """

    if block_size is not None and block_size % 8 != 0:
        print("Given block size is not a multiple of 8")
        return

    if block_size is not None and (y_channel.shape[0] * y_channel.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    if block_size is not None and (cb_channel.shape[0] * cb_channel.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    if block_size is not None and (cr_channel.shape[0] * cr_channel.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    # caso não seja passado um tamanho de bloco
    if block_size is None:
        y_dct = dct(dct(y_channel, norm="ortho").T, norm="ortho").T
        cb_dct = dct(dct(cb_channel, norm="ortho").T, norm="ortho").T
        cr_dct = dct(dct(cr_channel, norm="ortho").T, norm="ortho").T

        return y_dct, cb_dct, cr_dct


    # alocar espaço para os arrays onde a dct vai ser calculada
    y_dct = zeros(y_channel.shape, dtype=float32)
    cb_dct = zeros(cb_channel.shape, dtype=float32)
    cr_dct = zeros(cr_channel.shape, dtype=float32)

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, y_dct.shape[0], block_size):
        for j in range(0, y_dct.shape[1], block_size):
            y_dct[i:i+block_size, j:j+block_size] = dct(
                dct(
                    y_channel[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, cb_dct.shape[0], block_size):
        for j in range(0, cb_dct.shape[1], block_size):
            cb_dct[i:i+block_size, j:j+block_size] = dct(
                dct(
                    cb_channel[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, cr_dct.shape[0], block_size):
        for j in range(0, cr_dct.shape[1], block_size):
            cr_dct[i:i+block_size, j:j+block_size] = dct(
                dct(
                    cr_channel[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T


    return y_dct, cb_dct, cr_dct


def calculate_inv_dct(
    y_dct: ndarray, cb_dct: ndarray, cr_dct: ndarray, block_size: int = None
) -> Tuple[ndarray, ndarray, ndarray]:
    """Calcula a inversa da DCT em blocos de um tamanho fornecido\n
    Caso não seja fornecido é calculada a inversa da dct no canal todo
    Os blocos têm que ser multiplos de 8

    Args:
        y_dct (ndarray): o canal Y com a dct calculada
        cb_dct (ndarray): o canal Cb com a dct calculada
        cr_dct (ndarray): o canal Cr com a dct calculada
        block_size (int): o tamanho dos blocos em que a
        dct foi calculada anteriormente
        
    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais originais (sem a dct)
    """

    if block_size is not None and block_size % 8 != 0:
        print("Given block size is not a multiple of 8")
        return

    if block_size is not None and (y_dct.shape[0] * y_dct.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    if block_size is not None and (cb_dct.shape[0] * cb_dct.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    if block_size is not None and (cr_dct.shape[0] * cr_dct.shape[1]) % block_size != 0:
        print("Image channels' shapes are not multiples of the given block size")
        return

    # caso não seja passado um tamanho de bloco
    if block_size is None:
        y_channel = idct(idct(y_dct, norm="ortho").T, norm="ortho").T
        cb_channel = idct(idct(cb_dct, norm="ortho").T, norm="ortho").T
        cr_channel = idct(idct(cr_dct, norm="ortho").T, norm="ortho").T

        return y_channel, cb_channel, cr_channel


    # alocar espaço para os arrays onde a dct vai ser calculada
    y_channel = zeros(y_dct.shape, dtype=float32)
    cb_channel = zeros(cb_dct.shape, dtype=float32)
    cr_channel = zeros(cr_dct.shape, dtype=float32)

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, y_channel.shape[0], block_size):
        for j in range(0, y_channel.shape[1], block_size):
            y_channel[i:i+block_size, j:j+block_size] = idct(
                idct(
                    y_dct[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, cb_channel.shape[0], block_size):
        for j in range(0, cb_channel.shape[1], block_size):
            cb_channel[i:i+block_size, j:j+block_size] = idct(
                idct(
                    cb_dct[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T

    # calcular a dct para o canal Y em blocos de tamanho block_size fornecido
    for i in range(0, cr_channel.shape[0], block_size):
        for j in range(0, cr_channel.shape[1], block_size):
            cr_channel[i:i+block_size, j:j+block_size] = idct(
                idct(
                    cr_dct[i:i+block_size, j:j+block_size],
                    norm="ortho"
                ).T,
                norm="ortho"
            ).T


    return y_channel, cb_channel, cr_channel
