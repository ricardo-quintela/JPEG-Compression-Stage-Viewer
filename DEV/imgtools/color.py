"""Contém funções relacionadas à manipulação de cores
e mapas de cor
"""

from typing import Tuple

from matplotlib.colors import LinearSegmentedColormap
from numpy import ndarray

def create_colormap(
        first_color: Tuple[float, float, float],
        second_color: Tuple[float, float, float],
        name:str,
        rgb_quantization: int = 256,
    ) -> LinearSegmentedColormap:

    """Cria um colorido de segmento linear com os valores de cores RGB fornecidos\n
    o mapa de cor será nomeado com o nome dado

    Args:
        first_color (Tuple[float, float, float]): a primeira cor
        second_color (Tuple[float, float, float]): a cor final
        name (str): o nome do colorido
        rgb_quantization (int, optional): os níveis de quantização de RGB. Default a 256.

    Returns:
        LinearSegmentedColormap: Um objeto LinearSegmentedColormap ou None se ocorrer um erro
    """

    # try to create a colormap
    try:
        cmap = LinearSegmentedColormap.from_list(
            name,
            [first_color, second_color],
            rgb_quantization
        )

    # if the color arguments are in a wrong format
    except ValueError:
        print("Invalid color argument or rgb quantization value")
        return

    # first color contains invalid values
    if not 0 <= first_color[0] <= 1 or not 0 <= first_color[1] <= 1 or not 0 <= first_color[2] <= 1:
        print("Color values must be mapped from the range [0,1]")
        return

    # second color contains invalid values
    if not 0 <= second_color[0] <= 1 or not 0 <= second_color[1] <= 1 or not 0 <= second_color[2] <= 1:
        print("Color values must be mapped from the range [0,1]")
        return


    return cmap


def separate_channels(img: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    """Separa a imagem fornecida nos seus 3 canais de RGB

    Args:
        img (ndarray): a matriz da imagem

    Returns:
        Tuple[ndarray, ndarray, ndarray]: as matrizes dos canais RGB da imagem
        ou None caso a imagem seja incompatível
    """
    # imagem incompatível
    if len(img.shape) != 3:
        print("Given image is incompatible")
        return

    # imagem sem 3 canais
    if img.shape[2] != 3:
        print("Given image doesn't have 3 channels")
        return

    return img[:,:,0], img[:,:,1], img[:,:,2]
