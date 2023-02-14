from matplotlib.pyplot import show
from numpy import zeros, uint8

from imgtools import converter_to_rgb
from imgtools import restore_padding
from imgtools import show_img


def decode(data: bytearray, width: int, height: int):
    """Decodifica a matriz de bytes dada em formato jpeg
    para uma imagem

    Args:
        data (bytearray): A matriz de bytes em formato JPEG
        width (int): a largura da imagem original
        height (int): a altura da imagem original
    """

    image_y = data[:,:,0]
    image_cb = data[:,:,1]
    image_cr = data[:,:,2]

    image_r, image_g, image_b = converter_to_rgb(image_y, image_cb, image_cr)

    image_rgb_padded = zeros(data.shape, dtype=uint8)
    image_rgb_padded[:,:,0] = image_r
    image_rgb_padded[:,:,1] = image_g
    image_rgb_padded[:,:,2] = image_b

    image_rgb = restore_padding(image_rgb_padded, width, height)

    show_img(image_rgb, fig_numb=1, name="Imagem decoded")
    show()