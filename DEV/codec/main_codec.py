from numpy import ndarray

from . import encode, decode

from metrics import SNR, PSNR, MSE, RMSE

def main_codec_function(img: ndarray, fator_qualidade: int):
    """Serve como main quando não queremos utilizar flags específicas.
    Aqui chama-se uma função de encode que faz todo o processo para o trabalho de MULTIMÉDIA
    com o chamado hardcode. De seguida aplica o decode e apresenta alguns valores para analisar a qualidade 
    da codificação.
    
    Args:
        img (str): caminho para aa imagem
        fator_qualidade (int): fator de qualidade segundo o qual vai-se fazer a codificação
    
    """
    
    imagem_codificada, comprimento, largura = encode(img, fator_qualidade)
    imagem_descodificada = decode(imagem_codificada, comprimento, largura, fator_qualidade)
    
    MSE_value = MSE(img, imagem_descodificada)
    
    print("MSE: " + str(MSE_value))
    print("RMSE: " + str(RMSE(MSE_value)))
    print("SNR: " + str(SNR(MSE_value, imagem_codificada)))
    print("PSNR: " + str(PSNR(MSE_value, imagem_codificada)))
    
    
    