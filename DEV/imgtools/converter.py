"""Contém as funções para a conversão entre modelo RGB e YCbCr
e vice-versa
"""

from typing import Tuple

from numpy import ndarray, array, linalg, round, uint8

def converter_to_YCbCr(img: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    """Converte uma imagem no modelo RGB para o modelo YCbCr

    Args:
        img (ndarray): a matriz da imagem

    Returns:
        Tuple[ndarray, ndarray, ndarray]: a componente luma (Y), e as componentes cromáticas (Cb, Cr)
    """
    
    # array that transforms RGB into YCbCr
    T = array(
        [
            [0.299, 0.587, 0.114],
            [-0.168736, -0.331264, 0.5],
            [0.5, -0.418688, -0.081312],
        ]
    )
    
    # different channels from RGB image
    R = img[:,:,0]
    G = img[:,:,1]
    B = img[:,:,2]
    
    # calculate Y matrix 
    Y = T[0,0] * R + T[0,1] * G + T[0,2] * B
    
    # calculate the chromatic parts of the model
    Cb = (T[1,0] * R + T[1,1] * G + T[1,2] * B) + 128
    Cr = (T[2,0] * R + T[2,1] * G + T[2,2] * B) + 128
    
    return Y, Cb, Cr
    

def converter_to_RGB(Y: ndarray, Cb:ndarray, Cr:ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    """Converte uma imagem no modelo YCbCr para o modelo RGB

    Args:
        Y (ndarray): a componente luma 
        Cb (ndarray): a componente cromática (variação de azul relativamente à luma)
        Cr (ndarray): a componente cromática (variação de vermelho relativamente à luma)

    Returns:
        Tuple[ndarray, ndarray, ndarray]: o canal Red, o canal Green, o canal Blue
    """
    
    # array that transforms RGB into YCbCr
    T = array(
        [
            [0.299, 0.587, 0.114],
            [-0.168736, -0.331264, 0.5],
            [0.5, -0.418688, -0.081312],
        ]
    )
    
    # calculate inverse matrix from T
    T_inverse = linalg.inv(T)
    
    # calculate the different channels R,G,B
    R = T_inverse[0,0] * Y + T_inverse[0,1] * (Cb - 128) + T_inverse[0,2] * (Cr - 128) 
    G = T_inverse[1,0] * Y + T_inverse[1,1] * (Cb - 128) + T_inverse[1,2] * (Cr - 128) 
    B = T_inverse[2,0] * Y + T_inverse[2,1] * (Cb - 128) + T_inverse[2,2] * (Cr - 128) 
    
    # make sure everything is in the [0,255] range
    R[R > 255] = 255
    R[R < 0] = 0
    G[G > 255] = 255
    G[G < 0] = 0
    B[B > 255] = 255
    B[B < 0] = 0
    
    # round everthing to int type
    R = round(R).astype(uint8) 
    G = round(G).astype(uint8) 
    B = round(B).astype(uint8) 
    
    return R, G, B