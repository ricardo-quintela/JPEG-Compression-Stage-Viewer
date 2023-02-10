"""Contém funções para fins de leitura de imagem
"""

from os.path import isfile

from matplotlib.pyplot import imread
from numpy import ndarray


def read_bmp(path: str) -> ndarray:
    """Lê um arquivo BMP

    Args:
        path (str): O caminho para o arquivo BMP

    Returns:
        ndarray: Uma matriz com os valores de pixel de imagem em formato RGB
            ou None se o arquivo for inválido ou ocorrer um erro
    """

    if not path.endswith(".bmp"):
        print("File format is not of type 'bmp'")
        return

    if not isfile(path):
        print("Given path is not a file")
        return

    return imread(path)
