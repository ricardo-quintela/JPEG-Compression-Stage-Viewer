"""Contém funções que permitem a visualização
de imagens
"""

from numpy import ndarray
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pyplot import figure, imshow, axis, title, show

def show_img(
    img: ndarray,
    colormap: LinearSegmentedColormap = None,
    name: str = None
    ):
    """Retorna uma figura com a imagem fornecida como parâmetro
    e caso seja fornecido um colormap, aplica-o à mesma

    Args:
        img (ndarray): a matriz da imagem
        colormap (LinearSegmentedColormap, optional): o colormap para mostrar na
        imagem. Defaults to None.
        name (str, optional): o título do plot. Default a None.
    """

    figure()
    axis("off")

    # colocar um título no plot
    if name is not None:
        title(name)

    # aplicar um colormap caso seja dado
    if colormap is not None:
        imshow(img, colormap)
        show()
        return

    # caso não seja passado colormap
    imshow(img)
    show()
