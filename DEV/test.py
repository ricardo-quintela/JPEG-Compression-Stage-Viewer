"""Tests the codec
"""

import unittest

import numpy as np
import matplotlib.colors as clr

# imgtools
from imgtools import read_bmp
from imgtools import create_colormap, separate_channels, join_channels
from imgtools import add_padding, restore_padding
from imgtools import converter_to_rgb, converter_to_ycbcr
from imgtools import down_sample, up_sample
from imgtools import calculate_dct, calculate_inv_dct

# file_worker
from file_worker import read_config
from file_worker import Token
from file_worker import lex


class TestImgToolsReader(unittest.TestCase):
    """Testa o pacote do leitor de imgtools"""

    def test_read_file(self):
        """Testa se uma imagem BMP pode ser lida"""
        np.testing.assert_array_equal(
            read_bmp("test/test_img.bmp"), np.array([[[255, 255, 255]]], dtype=np.uint8)
        )

    def test_read_error(self):
        """Testa se ocorre um erro ao abrir um arquivo que não existe"""
        self.assertEqual(read_bmp("test/test_img_none.bmp"), None)

    def test_read_no_bmp(self):
        """Testa se ocorre um erro ao abrir um arquivo que
        não está em um formato BMP
        """
        self.assertEqual(read_bmp("test/test_img_none.png"), None)


class TestImgToolsColor(unittest.TestCase):
    """Testa o módulo de cor de imgtools"""

    def test_create_colormap(self):
        """Testa se um usuário pode criar um color
        com parâmetros corretos
        """
        self.assertEqual(
            create_colormap((0, 0, 0), (1, 1, 1), "white"),
            clr.LinearSegmentedColormap.from_list("white", [(0, 0, 0), (1, 1, 1)], 256),
        )

    def test_colormap_invalid_color_type1(self):
        """Testa se passar uma primeira cor inválida retorna None"""
        self.assertEqual(create_colormap(1, (1, 1, 1), "white"), None)

    def test_colormap_invalid_color_type2(self):
        """Testa se passar uma segunda cor inválida retorna None"""
        self.assertEqual(create_colormap((0, 0, 0), 0, "white"), None)

    def test_colormap_invalid_color_range1(self):
        """Testa se passar uma primeira cor fora do intervalo
        [0,1] retorna None
        """
        self.assertEqual(create_colormap((255, 255, 255), (1, 1, 1), "white"), None)

    def test_colormap_invalid_color_range2(self):
        """Testa se passar uma segunda cor fora do
        intervalo [0,1] retorna None
        """
        self.assertEqual(create_colormap((0, 0, 0), (255, 255, 255), "white"), None)

    def test_colormap_invalid_rgb_quantization(self):
        """Testa se passar um tipo de quantização RGB inválido
        retorna None
        """
        self.assertEqual(create_colormap((0, 0, 0), (1, 1, 1), "white", "test"), None)

    def test_separate_channels(self):
        """Testa se uma imagem fornecida é separada nos 3 canais
        de RGB que a compõem
        """
        np.testing.assert_array_equal(
            separate_channels(np.ones((1, 1, 3), dtype=np.uint8)),
            (np.array([[1]]), np.array([[1]]), np.array([[1]])),
        )

    def test_separate_channels_wrong_format(self):
        """Testa se é retornado None através da imagem de
        formato errado fornecida
        """
        self.assertEqual(separate_channels(np.ones((1, 1), dtype=np.uint8)), None)

    def test_separate_channels_wrong_channels(self):
        """Testa se é retornado None através da imagem com menos canais
        fornecida
        """
        self.assertEqual(separate_channels(np.ones((1, 1, 2), dtype=np.uint8)), None)

    def test_join_channels(self):
        """Testa se os 3 canais RGB de uma imagem podem ser unidos
        para reconstruir a imagem original
        """
        np.testing.assert_array_equal(
            join_channels(
                np.array([[255]], dtype=np.uint8),
                np.array([[255]], dtype=np.uint8),
                np.array([[255]], dtype=np.uint8),
            ),
            np.array([[[255, 255, 255]]], dtype=np.uint8),
        )

    def test_join_channels_not_equal(self):
        """Testa se fornecer 3 canais com formatos diferentes
        retorna None
        """
        self.assertEqual(
            join_channels(
                np.array([[255]], dtype=np.uint8),
                np.array([[255, 255, 255]], dtype=np.uint8),
                np.array([[[255]]], dtype=np.uint8),
            ),
            None,
        )

    def test_join_channels_wrong_shape(self):
        """Testa se fornecer 3 canais com o formato errado retorna
        None
        """
        self.assertEqual(
            join_channels(
                np.array([[[255, 255, 255]]], dtype=np.uint8),
                np.array([[255, 255, 255]], dtype=np.uint8),
                np.array([[255, 255]], dtype=np.uint8),
            ),
            None,
        )


class TestImgtoolsExtender(unittest.TestCase):
    """Testa o módulo de extensor de imgtools"""

    def test_add_padding(self):
        """Testa se uma imagem pode ser estendida mantendo a cor do último
        Linha na área estendida
        """
        np.testing.assert_array_equal(
            add_padding(np.zeros((4, 5, 3), dtype=np.uint8), 32)[0],
            np.zeros((32, 32, 3), dtype=np.uint8),
        )

    def test_add_padding_old_size(self):
        """Testa se uma imagem que foi estendida retorna o tamanho antigo correto"""
        self.assertTupleEqual(
            add_padding(np.zeros((4, 5, 3), dtype=np.uint8), 32)[1:], (4, 5)
        )

    def test_restore_padding(self):
        """Testa se uma imagem que foi previamente estendida é restaurada corretamente
        para o tamanho original
        """
        np.testing.assert_array_equal(
            restore_padding(np.zeros((32, 32, 3), dtype=np.uint8), 4, 5),
            np.zeros((4, 5, 3), dtype=np.uint8),
        )


class TestImgtoolsConverter(unittest.TestCase):
    """Testa o módulo converter do package imgtools"""

    def test_convert_to_ycbcr(self):
        """Testa se uma imagem no modelo de cor RGB é corretamente
        convertida para o modelo YCbCr
        """

        np.testing.assert_array_almost_equal(
            converter_to_ycbcr(np.ones((1, 1, 3), dtype=np.uint8) * 255),
            (
                np.array([[255.0]], dtype=np.float64),
                np.array([[128.0]], dtype=np.float64),
                np.array([[128.0]], dtype=np.float64),
            ),
        )

    def test_convert_to_rgb(self):
        """Testa se as componentes de uma imagem
        no modelo de cor YCbCr são corretamente
        convertidas para o modelo RGB
        """

        np.testing.assert_array_equal(
            converter_to_rgb(
                np.array([[255.0]], dtype=np.float64),
                np.array([[128.0]], dtype=np.float64),
                np.array([[128.0]], dtype=np.float64),
            ),
            (
                np.array([[255]], dtype=np.uint8),
                np.array([[255]], dtype=np.uint8),
                np.array([[255]], dtype=np.uint8),
            ),
        )


class TestFileworkerReader(unittest.TestCase):
    """Testa o módulo reader do package file_worker"""

    def test_read_config(self):
        """Testa se é possível ler um ficheiro de configuração"""
        self.assertEqual(read_config("test/test_config.cfg"), "Test config")

    def test_read_config_path_dir(self):
        """Testa se fornecendo um diretório como caminho
        a função retorna None
        """
        self.assertEqual(read_config("test/"), None)

    def test_read_config_bad_extension(self):
        """Testa se fornecendo um ficheiro que não está no formato
        cfg a função retorna None
        """
        self.assertEqual(read_config("test/test_config.txt"), None)

    def test_read_config_file_not_found(self):
        """Testa se fornecendo um ficheiro que não está no formato
        cfg a função retorna None
        """
        self.assertEqual(read_config("test/test_configNOT.cfg"), None)


class TestFileworkerToken(unittest.TestCase):
    """Testa o modulo token do package file_worker"""

    def test_sort_tokens(self):
        """Testa se um array de tokens pode ser
        ordenado com base na sua posição
        """
        tokens = [
            Token("TEST4", 4),
            Token("TEST2", 2),
            Token("TEST3", 3),
            Token("TEST1", 1),
        ]
        tokens.sort()

        self.assertListEqual(
            tokens,
            [
                Token("TEST1", 1),
                Token("TEST2", 2),
                Token("TEST3", 3),
                Token("TEST4", 4),
            ],
        )


class TestFileworkerFileParser(unittest.TestCase):
    """Testa o modulo file parser do package file worker"""

    def test_lex(self):
        """Testa se são apanhados os tokens corretamente"""
        tokens = [str(i) for i in lex(read_config("test/test_config2.cfg"))]

        self.assertListEqual(
            tokens,
            [
                "PLOT",
                "IMAGE",
                "COLORMAP",
                "CHANNEL",
                "YCC",
                "IMAGE",
                "COLORMAP",
                "CHANNEL",
                "RGB",
                "SUBSAMPLE",
                "END",
            ],
        )


class TestImgtoolsSampler(unittest.TestCase):
    """Testa o módulo sampler do package Imagetools"""

    def test_scale_y_421(self):
        """Testa se o canal Y é corretamente escalado
        com o modo 410 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 1),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_421(self):
        """Testa se o canal cr é corretamente escalado
        com o modo 411 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 1),
            )[1],
            np.ones((32, 8), dtype=np.float32),
        )

    def test_scale_cr_421(self):
        """Testa se o canal cb é corretamente escalado
        com o modo 411 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 1),
            )[2],
            np.ones((32, 16), dtype=np.float32),
        )

    def test_scale_y_411(self):
        """Testa se o canal Y é corretamente escalado
        com o modo 411 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 1, 1),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_411(self):
        """Testa se o canal Cr é corretamente escalado
        com o modo 411 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 1, 1),
            )[1],
            np.ones((32, 8), dtype=np.float32),
        )

    def test_scale_cr_411(self):
        """Testa se o canal Cb é corretamente escalado
        com o modo 411 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 1, 1),
            )[2],
            np.ones((32, 8), dtype=np.float32),
        )

    def test_scale_y_422(self):
        """Testa se o canal Y é corretamente escalado
        com o modo 422 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 2),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_422(self):
        """Testa se o canal Cb é corretamente escalado
        com o modo 422 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 2),
            )[1],
            np.ones((32, 16), dtype=np.float32),
        )

    def test_scale_cr_422(self):
        """Testa se o canal Cr é corretamente escalado
        com o modo 422 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 2),
            )[2],
            np.ones((32, 16), dtype=np.float32),
        )

    def test_scale_y_420(self):
        """Testa se o canal Y é corretamente escalado
        com o modo 420 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 0),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_420(self):
        """Testa se o canal Cb é corretamente escalado
        com o modo 420 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 0),
            )[1],
            np.ones((16, 16), dtype=np.float32),
        )

    def test_scale_cr_420(self):
        """Testa se o canal Cr é corretamente escalado
        com o modo 420 de subsampling
        """

        np.testing.assert_array_equal(
            down_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                np.ones((32, 32), dtype=np.float32),
                (4, 2, 0),
            )[2],
            np.ones((16, 16), dtype=np.float32),
        )

    def test_scale_y_420_up(self):
        """Testa se o canal Y é corretamente escalado
        com o modo 420 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_420_up(self):
        """Testa se o canal Cb é corretamente escalado
        com o modo 420 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
            )[1],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cr_420_up(self):
        """Testa se o canal Cr é corretamente escalado
        com o modo 420 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
                np.ones((16, 16), dtype=np.float32),
            )[2],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_y_422_up(self):
        """Testa se o canal y é corretamente escalado
        com o modo 422 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
            )[0],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cb_422_up(self):
        """Testa se o canal Cb é corretamente escalado
        com o modo 422 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
            )[1],
            np.ones((32, 32), dtype=np.float32),
        )

    def test_scale_cr_422_up(self):
        """Testa se o canal Cr é corretamente escalado
        com o modo 422 de upsampling
        """

        np.testing.assert_array_equal(
            up_sample(
                np.ones((32, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
                np.ones((16, 32), dtype=np.float32),
            )[2],
            np.ones((32, 32), dtype=np.float32),
        )


class TestImgtoolsDct(unittest.TestCase):
    """testa o modulo Dct do package Imgtools
    """

    def test_calculate_dct(self):
        """Testa se a dct é calculada corretamente numa imagem completamente
        branca no modelo YCbCr em blocos 8x8
        """

        result_array_y = np.zeros((64,64), dtype=np.float32)
        result_array_y[0,0] = 2040
        result_array_cbcr = np.zeros((64,64), dtype=np.float32)
        result_array_cbcr[0,0] = 1024

        np.testing.assert_array_almost_equal(
            calculate_dct(
                np.ones((64,64), dtype=np.float32) * 255,
                np.ones((64,64), dtype=np.float32) * 128,
                np.ones((64,64), dtype=np.float32) * 128,
                8,
            ),
            (result_array_y, result_array_cbcr, result_array_cbcr),
            decimal=0
        )


if __name__ == "__main__":
    unittest.main()
