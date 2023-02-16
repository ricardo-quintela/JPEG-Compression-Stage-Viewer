from typing import Tuple

from numpy import ndarray

def sub_sample(
        y_channel: ndarray,
        cb_channel: ndarray,
        cr_channel: ndarray,
        scale: Tuple[int, int, int]
    ) -> Tuple[ndarray, ndarray, ndarray]:
    """Faz a subamostragem da imagem com a escala fornecida

    Args:
        y_channel (ndarray): o canal Y
        cb_channel (ndarray): o canal cb
        cr_channel (ndarray): o canal cr
        scale (Tuple[int, int, int]): a escala para a sub-amostragem {0,1,2,4}

    Returns:
        Tuple[ndarray, ndarray, ndarray]: os canais com a respetiva asubamostragem
    """
    pass
