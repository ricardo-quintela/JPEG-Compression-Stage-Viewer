"""Tests the codec
"""

import unittest

import numpy as np
import matplotlib.colors as clr

# imgtools
from imgtools import read_bmp
from imgtools import create_colormap
from imgtools import add_padding, restore_padding

class TestImgToolsReader(unittest.TestCase):
    """Testa o pacote do leitor de imgtools
    """

    def test_read_file(self):
        """Testa se uma imagem BMP pode ser lida
        """
        np.testing.assert_array_equal(
            read_bmp("test/test_img.bmp"),
            np.array([[[255,255,255]]], dtype=np.uint8)
        )

    def test_read_error(self):
        """Testa se ocorre um erro ao abrir um arquivo que não existe
        """
        self.assertEqual(read_bmp("test/test_img_none.bmp"), None)

    def test_read_no_bmp(self):
        """Testa se ocorre um erro ao abrir um arquivo que
        não está em um formato BMP
        """
        self.assertEqual(read_bmp("test/test_img_none.png"), None)

class TestImgToolsColor(unittest.TestCase):
    """Testa o módulo de cor de imgtools
    """

    def test_create_colormap(self):
        """Testa se um usuário pode criar um color
        com parâmetros corretos
        """
        self.assertEqual(
            create_colormap((0,0,0), (1,1,1), "white"),
            clr.LinearSegmentedColormap.from_list("white", [(0,0,0), (1,1,1)], 256)
        )

    def test_colormap_invalid_color_type1(self):
        """Testa se passar uma primeira cor inválida retorna None
        """
        self.assertEqual(
            create_colormap(1, (1,1,1), "white"),
            None
        )

    def test_colormap_invalid_color_type2(self):
        """Testa se passar uma segunda cor inválida retorna None
        """
        self.assertEqual(
            create_colormap((0,0,0), 0, "white"),
            None
        )

    def test_colormap_invalid_color_range1(self):
        """Testa se passar uma primeira cor fora do intervalo
        [0,1] retorna None
        """
        self.assertEqual(
            create_colormap((255,255,255), (1,1,1), "white"),
            None
        )

    def test_colormap_invalid_color_range2(self):
        """Testa se passar uma segunda cor fora do
        intervalo [0,1] retorna None
        """
        self.assertEqual(
            create_colormap((0,0,0), (255,255,255), "white"),
            None
        )

    def test_colormap_invalid_rgb_quantization(self):
        """Testa se passar um tipo de quantização RGB inválido
        retorna None
        """
        self.assertEqual(
            create_colormap((0,0,0), (1,1,1), "white", "test"),
            None
        )

class TestImgtoolsExtender(unittest.TestCase):
    """Testa o módulo de extensor de imgtools
    """

    def test_add_padding(self):
        """Testa se uma imagem pode ser estendida mantendo a cor do último
        Linha na área estendida
        """
        np.testing.assert_array_equal(
            add_padding(np.zeros((4,5,3), dtype=np.uint8), 32)[0],
            np.zeros((32,32,3), dtype=np.uint8)
        )

    def test_add_padding_old_size(self):
        """Testa se uma imagem que foi estendida retorna o tamanho antigo correto
        """
        self.assertTupleEqual(
            add_padding(np.zeros((4,5,3), dtype=np.uint8), 32)[1:],
            (4,5)
        )

    def test_restore_padding(self):
        """Testa se uma imagem que foi previamente estendida é restaurada corretamente
        para o tamanho original
        """
        np.testing.assert_array_equal(
            restore_padding(np.zeros((32,32,3), dtype=np.uint8), 4, 5),
            np.zeros((4,5,3), dtype=np.uint8)
        )


if __name__ == "__main__":
    unittest.main()
