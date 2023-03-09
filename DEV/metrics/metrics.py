
from numpy import sum as npsum, ndarray, float64, round as npround, max as npmax

from imgtools import show_img
from imgtools import create_colormap
from imgtools import converter_to_ycbcr
from imgtools import add_padding

from math import sqrt, log10

def MSE(imagem_original: ndarray, imagem_reconstruida: ndarray) -> float:
    """Calcula as métricas relativas à compressão da imagem

    Args:
        imagem_original (ndarray): a imagem original
        imagem_reconstruida (ndarray): a imagem reconstruida

    Returns:
        float: as diferenças entre a imagem original e reconstruida
    """

    imagem_original,_,_ = add_padding(imagem_original, 32)
    imagem_reconstruida,_,_ = add_padding(imagem_reconstruida, 32)


    imagem_O = converter_to_ycbcr(imagem_original)
    imagem_R = converter_to_ycbcr(imagem_reconstruida)


    differences = abs(imagem_O[0].astype(float64) - imagem_R[0])

    print("Max difference ", npmax(differences))

    show_img(
        differences,
        create_colormap((0,0,0), (1,1,1))
    )

    imagem_original = npround(imagem_original).astype(float64)

    return npsum((imagem_original - imagem_reconstruida)**2) / (imagem_original.shape[0]*imagem_original.shape[1])


def RMSE(MSE_value: float):
    return sqrt(MSE_value)

def SNR(MSE_value: float, imagem_original: ndarray):

    P = npsum((imagem_original)**2) / (imagem_original.shape[0]*imagem_original.shape[1])

    return log10(P/MSE_value) * 10
