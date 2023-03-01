"""Contém funções para aplicar quantização em imagens
"""

from numpy import ndarray, zeros, int16, round as npround

def quantize(
        channel: ndarray,
        q_matrix: ndarray
) -> ndarray:
    """Aplica a técnica de quantização ao canal da imagem
    fornecido

    A matriz de quantização tem que ter formato 8x8\n
    A matriz fornecida tem que ser bidimensional e ter
    shape multipla de 8

    Args:
        channel (ndarray): o canal a quantizar
        q_matrix (ndarray): a matriz de quantização a ser usada

    Returns:
        ndarray: o canal da imagem devidamente quantizado
    """

    # garantir que as matrizes têm 2 dimensões
    if len(channel.shape) != 2:
        print("Matrix must be 2 dimentional")
        return

    # verificar se as dimensões das matrizes são multiplas de 8

    if sum(channel.shape) % 8 != 0:
        print("Matrix shape must be multiple of 8")
        return

    if sum(q_matrix.shape) != 16:
        print("Quantization matrix shape must be 8x8")
        return

    # alocar espaço para guardar outras matrizes
    ch_quantized = zeros(channel.shape, dtype=int16)

    # fazer a quantização das matrizes de imagem

    for i in range(0, ch_quantized.shape[0], 8):
        for j in range(0, ch_quantized.shape[1], 8):
            ch_quantized[i:i+8, j:j+8] = npround(
                channel[i:i+8, j:j+8] / q_matrix
            )

    return ch_quantized



def inv_quantize(
        ch_quantized: ndarray,
        q_matrix: ndarray
) -> ndarray:
    """Reverte a técnica de quantização aplicada anteriormente
    ao canal da imagem fornecido

    A matriz de quantização tem que ter formato 8x8\n
    A matriz fornecida têm que ser bidimensional e ter
    shape multipla de 8

    Args:
        ch_quantized (ndarray): o canal para inverter a quantização
        q_matrix (ndarray): a matriz de quantização a ser usada

    Returns:
        ndarray: o canal da imagem devidamente quantizado
    """

    # garantir que as matrizes têm 2 dimensões
    if len(ch_quantized.shape) != 2:
        print("Matrix must be 2 dimentional")
        return

    # verificar se as dimensões das matrizes são multiplas de 8

    if sum(ch_quantized.shape) % 8 != 0:
        print("Matrix shape must be multiple of 8")
        return

    if sum(q_matrix.shape) != 16:
        print("Quantization matrix shape must be 8x8")
        return

    # alocar espaço para guardar outras matrizes
    channel = zeros(ch_quantized.shape, dtype=int16)

    # fazer a quantização das matrizes de imagem

    for i in range(0, channel.shape[0], 8):
        for j in range(0, channel.shape[1], 8):
            channel[i:i+8, j:j+8] = ch_quantized[i:i+8, j:j+8] * q_matrix
            
    return channel
