
from numpy import sum as npsum, ndarray, float64, round as npround

from imgtools import show_img
from imgtools import create_colormap
from imgtools import converter_to_ycbcr

from math import sqrt, log10

def MSE(imagem_original: ndarray, imagem_reconstruida: ndarray) -> float:
    '''ola ola
    
    '''
    
    imagem_O = converter_to_ycbcr(imagem_original)
    imagem_R = converter_to_ycbcr(imagem_reconstruida)
    
    
    E = abs(imagem_O[0] - imagem_R[0])
    
    show_img(
        E,
        create_colormap((0,0,0), (1,1,1))
    )
    
    imagem_original = npround(imagem_original).astype(float64)
    
    return npsum((imagem_original - imagem_reconstruida)**2) / (imagem_original.shape[0]*imagem_original.shape[1])


def RMSE(MSE: float):
    return sqrt(MSE)

def SNR(MSE: float, imagem_original: ndarray):
    
    P = npsum((imagem_original)**2) / (imagem_original.shape[0]*imagem_original.shape[1])
    
    return log10(P/MSE) * 10

def PSNR(MSE: float, imagem_original: ndarray):
    
    aux = max(imagem_original)
    
    return log10(aux/MSE) * 10