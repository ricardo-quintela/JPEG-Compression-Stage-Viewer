"""Contém funções relacionadas à manipulação de cores
e mapas de cor
Contém as funções para a conversão entre modelo RGB e YCbCr
e vice-versa
"""

from typing import Tuple

from matplotlib.colors import LinearSegmentedColormap
from numpy import ndarray, zeros, array, linalg, round as npround, uint8, float32

def create_colormap(
        first_color: Tuple[float, float, float],
        second_color: Tuple[float, float, float],
        name:str = "colormap",
        rgb_quantization: int = 256,
    ) -> LinearSegmentedColormap:

    """Cria um colorido de segmento linear com os valores de cores RGB fornecidos\n
    o mapa de cor será nomeado com o nome dado

    Args:
        first_color (Tuple[float, float, float]): a primeira cor
        second_color (Tuple[float, float, float]): a cor final
        name (str, optional): o nome do colormap. Default a "colormap"
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
    """Separa a imagem fornecida nos seus 3 canais RGB ou YCbCr

    Args:
        img (ndarray): a matriz da imagem

    Returns:
        Tuple[ndarray, ndarray, ndarray]: as matrizes dos canais RGB ou YCbCr da imagem
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


def join_channels(ch1: ndarray, ch2: ndarray, ch3: ndarray) -> ndarray:
    """Reconstroi uma imagem com os canais RGB ou YcbCr fornecidos

    Args:
        ch1 (ndarray): o primeiro canal
        ch2 (ndarray): o segundo canal
        ch3 (ndarray): o terceiro canal

    Returns:
        ndarray: a imagem reconstruida com os canais RGB ou YCbCr ou None caso ocorra um erro
    """

    # canais da imagem não são iguais
    if ch1.shape * 3 != ch1.shape + ch2.shape + ch3.shape:
        print("Given channels have different shapes")
        return

    # canais da imagem estão no formato errado
    if len(ch1.shape) != 2:
        print("Given channel is in the wrong format")
        return

    img = zeros((ch1.shape[0],ch1.shape[1],3), dtype=uint8)


    try:
        img[:,:,0] = ch1
        img[:,:,1] = ch2
        img[:,:,2] = ch3
    except ValueError:
        print("Could not join the channels")
        return

    return img



def converter_to_ycbcr(img: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    """Converte uma imagem no modelo RGB para o modelo YCbCr
    \n
    As componentes serão valores de vírgula flutuante

    Args:
        img (ndarray): a matriz da imagem

    Returns:
        Tuple[ndarray, ndarray, ndarray]: a componente luma (Y),
        e as componentes cromáticas (Cb, Cr)
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

    # round everthing to int type
    Y = npround(Y).astype(uint8)
    Cb = npround(Cb).astype(uint8)
    Cr = npround(Cr).astype(uint8)


    Y[Y > 255] = 255
    Y[Y < 0] = 0
    Cb[Cb > 255] = 255
    Cb[Cb < 0] = 0
    Cr[Cr > 255] = 255
    Cr[Cr < 0] = 0

    return Y, Cb, Cr


def converter_to_rgb(Y: ndarray, Cb: ndarray, Cr: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    """Converte uma imagem no modelo YCbCr para o modelo RGB
    \n
    As compontentes convertidas estarão no intervalo [0,1]

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

    Y  = Y.astype(float32)
    Cb = Cb.astype(float32)
    Cr = Cr.astype(float32)

    # calculate the different channels R,G,B
    R = T_inverse[0,0]*Y + T_inverse[0,1]*(Cb-128) + T_inverse[0,2]*(Cr-128)
    G = T_inverse[1,0]*Y + T_inverse[1,1]*(Cb-128) + T_inverse[1,2]*(Cr-128)
    B = T_inverse[2,0]*Y + T_inverse[2,1]*(Cb-128) + T_inverse[2,2]*(Cr-128)


    # make sure everything is in the [0,255] range
    # R *= 255
    # G *= 255
    # B *= 255

    R[R > 255] = 255
    R[R < 0] = 0
    G[G > 255] = 255
    G[G < 0] = 0
    B[B > 255] = 255
    B[B < 0] = 0

    # round everthing to int type
    R = npround(R).astype(uint8)
    G = npround(G).astype(uint8)
    B = npround(B).astype(uint8)

    return R, G, B

