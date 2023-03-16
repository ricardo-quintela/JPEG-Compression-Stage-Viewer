"""Calcula as métricas relativas à compressão da imagem.
"""

from numpy import sum as npsum, ndarray, float32, round as npround, max as npmax

from imgtools import show_img
from imgtools import create_colormap
from imgtools import converter_to_ycbcr
from imgtools import add_padding

from math import sqrt, log10

def MSE(imagem_original: ndarray, imagem_reconstruida: ndarray) -> float:
    """Calcula a diferença média quadrada de entre os píxeis da imagem original
    e da imagem reconstruída e apresenta as diferenças numa imagem preto e branco.

    Args:
        imagem_original (ndarray): a imagem original
        imagem_reconstruida (ndarray): a imagem reconstruida

    Returns:
        float: as diferenças entre a imagem original e reconstruida
    """

    imagem_original_com_padding,_,_ = add_padding(imagem_original, 32)
    imagem_reconstruida_com_padding,_,_ = add_padding(imagem_reconstruida, 32)

    imagem_O = converter_to_ycbcr(imagem_original_com_padding)
    imagem_R = converter_to_ycbcr(imagem_reconstruida_com_padding)
    
    differences = abs(imagem_O[0].astype(float32) - imagem_R[0])
    
    show_img(
        imagem_reconstruida,
        fig_number=11,
        sub_plot_config=(1,1,1),
        plot_title="Imagem Reconstruída"
    )
    
    show_img(
        differences,
        create_colormap((0,0,0), (1,1,1)),
        fig_number=12,
        sub_plot_config=(1,1,1),
        plot_title="Diferenças Original-Reconstruído"
    )
    

    imagem_original = npround(imagem_original).astype(float32)
    
    return npsum((imagem_original - imagem_reconstruida)**2) / (imagem_original.shape[0]*imagem_original.shape[1])

def RMSE(MSE_value: float) -> float:
    """Calcula a raíz da diferença média quadrada de entre os píxeis da imagem original
    e da imagem reconstruída.

    Args:
        MSE_value (float): diferença média quadrada de entre os píxeis da imagem original
    e da imagem reconstruída

    Returns:
        float: valor da raíz da diferença entre a imagem original e reconstruida
    """
    return sqrt(MSE_value)

def SNR(MSE_value: float, imagem_original: ndarray) -> float:
    """Calcula a relação entre o original e o erro.

    Args:
        MSE_value (float): diferença média quadrada de entre os píxeis da imagem original
    e da imagem reconstruída
        imagem_original (ndarray): a imagem original

    Returns:
        float: relação entre o original e o erro
    """
    
    power = npsum((imagem_original.astype(float32))**2) / (imagem_original.shape[0]*imagem_original.shape[1])
    
    return log10(power/MSE_value) * 10

def PSNR(MSE_value: float, imagem_original: ndarray) -> float:
    """Calcula o rácio entre o quadrado do pico do sinal correcto (valor mais alto 
    da imagem original) e o ruído (MSE).

    Args:
        MSE_value (float): diferença média quadrada de entre os píxeis da imagem original
    e da imagem reconstruída
        imagem_original (ndarray): a imagem original

    Returns:
        float: rácio entre o quadrado do pico do sinal correcto e o ruído
    """
    
    max = npmax(imagem_original.astype(float32)) ** 2
    
    return log10(max/MSE_value) * 10
