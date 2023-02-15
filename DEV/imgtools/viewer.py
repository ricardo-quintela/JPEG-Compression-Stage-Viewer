"""Contém funções que permitem a visualização
de imagens
"""

from numpy import ndarray
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pyplot import figure, subplot, imshow, axis, title, show

def show_img(
    img: ndarray,
    colormap: LinearSegmentedColormap = None,
    name: str = None,
    fig_number: int = None,
    sub_plot_config: tuple = None
    ):
    """Retorna uma figura com a imagem fornecida como parâmetro
    e caso seja fornecido um colormap, aplica-o à mesma

    Args:
        img (ndarray): a matriz da imagem
        colormap (LinearSegmentedColormap, optional): o colormap para mostrar na
        imagem. Defaults to None.
        name (str, optional): o título do plot. Default a None.
        fig_numb (int, optional): o numero da figura. Default a None
        sub_plot_config (tuple, optional): a configuração do subplot (linhas, colunas, indice[1, ...]). Default a None
    """

    if fig_number and sub_plot_config:
        if len(sub_plot_config) != 3:
            print("Subplot config is a wrong format")
            return

        figure(fig_number)
        subplot(sub_plot_config[0], sub_plot_config[1], sub_plot_config[2])

    else:
        figure()

    axis("off")

    # colocar um título no plot
    if name is not None:
        title(name)

    # aplicar um colormap caso seja dado
    if colormap is not None:
        imshow(img, colormap)
        
        if fig_number is None:
            show()
        return

    # caso não seja passado colormap
    imshow(img)

    if fig_number is None:
        show()
