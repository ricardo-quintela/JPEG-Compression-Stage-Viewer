"""Contém funções para codificar imagens usando codificação diferencial DPCM
"""

from numpy import ndarray, array

def dpcm_encoder(channel: ndarray) -> ndarray:
    """Codifica os coeficientes DC do canal fornecido

    Args:
        channel (ndarray): o canal a ser codificado

    Returns:
        ndarray: o canal codificado
    """

    aux_channel = array(channel)

    for i in range(aux_channel.shape[0] - 8, -1, -8):
        for j in range(aux_channel.shape[1] - 8, -1, -8):

            if i == 0 and j == 0:
                break

            if j != 0:
                aux_channel[i, j] = aux_channel[i, j] - aux_channel[i, j-8]
                continue

            aux_channel[i, j] = aux_channel[i, j] - aux_channel[i-8, aux_channel.shape[1] - 9]

    return aux_channel


def dpcm_decoder(channel: ndarray) -> ndarray:
    """Descodifica os coeficientes DC de um canal previamente codificado

    Args:
        channel (ndarray): o canal a descodificar

    Returns:
        ndarray: o canal descodificado
    """

    aux_channel = array(channel)


    for i in range(0 , aux_channel.shape[0], 8):
        for j in range(0, aux_channel.shape[1], 8):

            if j == 0 and i == 0:
                continue

            if j != 0:
                aux_channel[i, j] = aux_channel[i, j] + aux_channel[i, j-8]
                continue

            if i + 8 >= aux_channel.shape[0]:
                break

            aux_channel[i, j] = aux_channel[i, j] + aux_channel[i+8, aux_channel.shape[1] - 9]

    return aux_channel
