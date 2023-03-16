from .decoder import decode
from .encoder import encode

from metrics import SNR, PSNR, MSE, RMSE

from imgtools import read_bmp

from matplotlib.pyplot import show

def main_codec_function(img: str, fator_qualidade: int, downsampling: tuple):
    """Serve como main quando não queremos utilizar flags específicas.
    Aqui chama-se uma função de encode que faz todo o processo para o trabalho de MULTIMÉDIA
    com o chamado hardcode. De seguida aplica o decode e apresenta alguns valores para analisar a qualidade 
    da codificação.
    
    Args:
        img (str): caminho para a imagem
        fator_qualidade (int): fator de qualidade segundo o qual vai-se fazer a codificação
        downsampling (tuple): o fator de subamostragem
    
    """

    imagem_original = read_bmp(img)

    y_codificada, cb_codificada, cr_codificada, comprimento, largura = encode(imagem_original, fator_qualidade, downsampling)

    imagem_codificada = (
        y_codificada,
        cb_codificada,
        cr_codificada
    )

    imagem_descodificada = decode(imagem_codificada, comprimento, largura, fator_qualidade)

    MSE_value = MSE(imagem_original, imagem_descodificada)

    print("MSE: " + str(MSE_value))
    print("RMSE: " + str(RMSE(MSE_value)))
    print("SNR: " + str(SNR(MSE_value, imagem_original)))
    print("PSNR: " + str(PSNR(MSE_value, imagem_original)))

    show()
    