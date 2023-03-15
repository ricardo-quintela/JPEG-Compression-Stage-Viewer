from matplotlib.pyplot import show, close

from imgtools import read_bmp
from imgtools import separate_channels
from imgtools import create_colormap
from imgtools import show_img
from imgtools import add_padding
from imgtools import converter_to_ycbcr
from imgtools import down_sample
from imgtools import calculate_dct
from imgtools import quantize
from imgtools import dpcm_encoder

from file_worker import load_q_matrix

def encode(path: str, fator_qualidade: int):
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


    show_img(image_r, map_r, fig_number=10, name="Canal vermelho")
    show_img(image_g, map_g, fig_number=11, name="Canal verde")
    show_img(image_b, map_b, fig_number=12, name="Canal azul")
    show_img(image, fig_number=4, name="Imagem original")

    # Exercício 4 e 5

    image_padded = add_padding(image, 32)[0]
    image_y, image_cb, image_cr = converter_to_ycbcr(image_padded)

    map_gr = create_colormap((0,0,0), (1,1,1), "grayscale")

    show_img(image_y, map_gr, fig_number=13, name="Canal luma")
    show_img(image_cb, map_gr, fig_number=14, name="Canal crominância azul em relação a luma")
    show_img(image_cr, map_gr, fig_number=15, name="Canal crominância vermenlha em relação a luma")

    
    # Exercicio 6
    y_resized, cb_resized, cr_resized = down_sample(image_y, image_cb, image_cr, (4,2,2))
    
    show_img(y_resized, map_gr, fig_number=16, name="Y resized")
    show_img(cb_resized, map_gr, fig_number=17, name="Cb resized")
    show_img(cr_resized, map_gr, fig_number=18, name="Cr resized")
    
    # Exercicio 7
    y_dct_without_blocks, cb_dct_without_blocks, cr_dct_without_blocks = calculate_dct(y_resized, cb_resized, cr_resized)
    y_dct_blocks_8, cb_dct_blocks_8, cr_dct_blocks_8 = calculate_dct(y_resized, cb_resized, cr_resized, 8)
    y_dct_blocks_64, cb_dct_blocks_64, cr_dct_blocks_64 = calculate_dct(y_resized, cb_resized, cr_resized, 64)
    
    show_img(y_dct_without_blocks, map_gr, fig_number=19, name="Y resized")
    show_img(cb_dct_without_blocks, map_gr, fig_number=20, name="Cb resized")
    show_img(cr_dct_without_blocks, map_gr, fig_number=21, name="Cr resized")
    show_img(y_dct_blocks_8, map_gr, fig_number=22, name="Y resized")
    show_img(cb_dct_blocks_8, map_gr, fig_number=23, name="Cb resized")
    show_img(cr_dct_blocks_8, map_gr, fig_number=24, name="Cr resized")
    show_img(y_dct_blocks_64, map_gr, fig_number=25, name="Y resized")
    show_img(cb_dct_blocks_64, map_gr, fig_number=26, name="Cb resized")
    show_img(cr_dct_blocks_64, map_gr, fig_number=27, name="Cr resized")
    
    # Exercicio 8
    q_matrix_y = load_q_matrix("q_matrix_y.csv")
    q_matrix_cbcr = load_q_matrix("q_matrix_cbcr.csv")
    
    y_quantizated = quantize(y_dct_blocks_8, q_matrix_y, fator_qualidade)
    cb_quantizated = quantize(cb_dct_blocks_8, q_matrix_cbcr, fator_qualidade)
    cr_quantizated = quantize(cr_dct_blocks_8, q_matrix_cbcr, fator_qualidade)
    
    show_img(y_quantizated, map_gr, fig_number=28, name="Y quantizated", log_correction=True)
    show_img(cb_quantizated, map_gr, fig_number=29, name="Cb quantizated", log_correction=True)
    show_img(cr_quantizated, map_gr, fig_number=30, name="Cr quantizated", log_correction=True)
    
    # Exercicio 9
    y_with_dcpm = dpcm_encoder(y_quantizated)
    cb_with_dcpm = dpcm_encoder(cb_quantizated)
    cr_with_dcpm = dpcm_encoder(cr_quantizated)
    
    show_img(y_with_dcpm, map_gr, fig_number=31, name="Y DCPM", log_correction=True)
    show_img(cb_with_dcpm, map_gr, fig_number=32, name="Cb DCPM", log_correction=True)
    show_img(cr_with_dcpm, map_gr, fig_number=33, name="Cr DCPM", log_correction=True)
        
    show()

    return y_with_dcpm, cb_with_dcpm, cr_with_dcpm, image.shape[0], image.shape[1]
