from typing import Tuple

from numpy import ndarray, shape
from cv2 import resize 

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
    
    width, height = y_channel.shape
    
    if scale[1] == 1:
        width /= 4
    elif scale[1] == 2:
        width /= 2
        
    if scale[2] == 1:
        width /= 4
    elif scale[2] == 2:
        width /= 2
    elif scale[2] == 0:
        if scale[1] == 1:
            width /= 4
            height /= 4
        elif scale[1] == 2:
            width /= 2
            height /= 2

    cb_channel_resized = resize(cb_channel, (int(width), height))
    cr_channel_resized = resize(cr_channel, (int(width), height))
    
    return y_channel, cb_channel_resized, cr_channel_resized