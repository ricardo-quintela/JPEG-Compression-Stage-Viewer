from matplotlib.pyplot import show, close
from numpy import zeros, float64, uint8, round as npround

from imgtools import read_bmp
from imgtools import separate_channels
from imgtools import create_colormap
from imgtools import show_img
from imgtools import add_padding
from imgtools import converter_to_ycbcr
from imgtools import down_sample

def encode(path: str):
    """Codifica o arquivo de imagem no caminho fornecido para um formato JPEG

    Args:
        path (str): the path to the file
    """
    
    close("all")
    image = read_bmp(path)

    # Exercicio 3
    image_r, image_g, image_b = separate_channels(image)

    map_r = create_colormap((0,0,0), (1,0,0), "red")
    map_g = create_colormap((0,0,0), (0,1,0), "green")
    map_b = create_colormap((0,0,0), (0,0,1), "blue")


    show_img(image_r, map_r, fig_numb=1, name="Canal vermelho")
    show_img(image_g, map_g, fig_numb=2, name="Canal verde")
    show_img(image_b, map_b, fig_numb=3, name="Canal azul")
    show_img(image, fig_numb=4, name="Imagem original")

    # Exercício 4 e 5

    image_padded = add_padding(image, 32)[0]
    image_y, image_cb, image_cr = converter_to_ycbcr(image_padded)

    map_gr = create_colormap((0,0,0), (1,1,1), "grayscale")

    show_img(image_y, map_gr, fig_numb=6, name="Canal luma")
    show_img(image_cb, map_gr, fig_numb=7, name="Canal crominância azul em relação a luma")
    show_img(image_cr, map_gr, fig_numb=8, name="Canal crominância vermenlha em relação a luma")

    
    # Exercicio 6
    y_resized, cb_resized, cr_resized = down_sample(image_y, image_cb, image_cr, (4,2,2))
    
    # Exercicio 7
    
    show()

    return image_y, image_cb, image_cr, image.shape[0], image.shape[1]
