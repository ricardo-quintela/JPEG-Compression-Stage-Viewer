
from numpy import sum as npsum, ndarray, float64, round as npround

from imgtools import show_img
from imgtools import create_colormap

def MSE(imagem_original: ndarray, imagem_reconstruida: ndarray) -> float:
    '''ola ola
    
    '''
    
    E = abs(imagem_original - imagem_reconstruida)
    
    show_img(
        E[0],
        create_colormap((0,0,0), (1,1,1))
    )
    
    imagem_original = npround(imagem_original).astype(float64)
    
    return npsum((imagem_original - imagem_reconstruida)**2) / (imagem_original.shape[0]*imagem_original.shape[1])