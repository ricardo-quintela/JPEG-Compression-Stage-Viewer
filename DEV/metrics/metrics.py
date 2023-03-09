
from numpy import sum as npsum, ndarray, float32, round as npround, max as npmax

from imgtools import show_img
from imgtools import create_colormap
from imgtools import converter_to_ycbcr
from imgtools import add_padding

from math import sqrt, log10

def MSE(imagem_original: ndarray, imagem_reconstruida: ndarray) -> float:
    '''ola ola
    
    '''
    
    imagem_original,_,_ = add_padding(imagem_original, 32)
    imagem_reconstruida,_,_ = add_padding(imagem_reconstruida, 32)

    imagem_O = converter_to_ycbcr(imagem_original)
    imagem_R = converter_to_ycbcr(imagem_reconstruida)
    
    E = abs(imagem_O[0].astype(float32) - imagem_R[0])
    
    show_img(
        E,
        create_colormap((0,0,0), (1,1,1))
    )
    
    imagem_original = npround(imagem_original).astype(float32)
    
    return npsum(abs(imagem_original - imagem_reconstruida)**2) / (imagem_original.shape[0]*imagem_original.shape[1])


def RMSE(MSE_value: float):
    return sqrt(MSE_value)

def SNR(MSE_value: float, imagem_original: ndarray):
    
    power = npsum((imagem_original.astype(float32))**2) / (imagem_original.shape[0]*imagem_original.shape[1])
    
    return log10(power/MSE_value) * 10

def PSNR(MSE_value: float, imagem_original: ndarray):
    
    max = npmax(imagem_original.astype(float32)) ** 2
    
    return log10(max/MSE_value) * 10
