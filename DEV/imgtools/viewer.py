"""Contém funções que permitem a visualização
de imagens
"""

from numpy import ndarray, log, abs as npabs
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pyplot import figure, subplot, imshow, axis, suptitle, title, show

def show_img(
    img: ndarray,
    colormap: LinearSegmentedColormap = None,
    plot_title: str = None,
    name: str = None,
    fig_number: int = None,
    sub_plot_config: tuple = None,
    log_correction: bool = False
    ):
    """Retorna uma figura com a imagem fornecida como parâmetro
    e caso seja fornecido um colormap, aplica-o à mesma

    Args:
        img (ndarray): a matriz da imagem
        colormap (LinearSegmentedColormap, optional): o colormap para mostrar na
        imagem. Defaults to None.
        plot_title (str, optional): o título principal do plot. Default a None.
        name (str, optional): o título do plot. Default a None.
        fig_numb (int, optional): o numero da figura. Default a None
        sub_plot_config (tuple, optional): a configuração do subplot (linhas, colunas, indice[1, ...]). Default a None
        log_correction (bool, oprional): usar uma correção logarítmica no display da imagem. Default a False
    """

    # usar a correção logarítmica
    if log_correction:
        img_array = log(npabs(img) + 0.0001)

    else:
        img_array = img

    if fig_number and sub_plot_config:
        if len(sub_plot_config) != 3:
            print("Subplot config is a wrong format")
            return    

        figure(fig_number)
        subplot(sub_plot_config[0], sub_plot_config[1], sub_plot_config[2])


    if fig_number is None:
        figure()

    # colocar um título no plot
    if plot_title is not None:
        suptitle(plot_title)

    # colocar um título no plot
    if name is not None:
        title(name)

    axis("off")

    # aplicar um colormap caso seja dado
    if colormap is not None:
        imshow(img_array, colormap, aspect="equal")

        if fig_number is None:
            show()
        return

    # caso não seja passado colormap
    imshow(img_array, aspect="equal")

    if fig_number is None:
        show()
