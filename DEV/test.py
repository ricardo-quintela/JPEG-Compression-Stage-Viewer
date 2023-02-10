"""Tests the codec
"""

import unittest

import numpy as np
import matplotlib.colors as clr

# imgtools
from imgtools import read_bmp
from imgtools import create_colormap
from imgtools import add_padding

class TestImgToolsReader(unittest.TestCase):
    """Tests the imgtools reader package
    """

    def test_read_file(self):
        """Test if a bmp image can be read
        """
        np.testing.assert_array_equal(
            read_bmp("test/test_img.bmp"),
            np.array([[[255,255,255]]], dtype=np.uint8)
        )

    def test_read_error(self):
        """Test if an error occurs when opening a file that doesn't exist
        """
        self.assertEqual(read_bmp("test/test_img_none.bmp"), None)

    def test_read_no_bmp(self):
        """Test if an error occurs when opening a file that
        isn't in a bmp format
        """
        self.assertEqual(read_bmp("test/test_img_none.png"), None)

class TestImgToolsColor(unittest.TestCase):
    """Tests the imgtools color module
    """

    def test_create_colormap(self):
        """Tests if a user can create a colormap
        with correct parameters
        """
        self.assertEqual(
            create_colormap((0,0,0), (1,1,1), "white"),
            clr.LinearSegmentedColormap.from_list("white", [(0,0,0), (1,1,1)], 256)
        )

    def test_colormap_invalid_color_type1(self):
        """Tests if passing an invalid first color returns None
        """
        self.assertEqual(
            create_colormap(1, (1,1,1), "white"),
            None
        )

    def test_colormap_invalid_color_type2(self):
        """Tests if passing an invalid second color returns None
        """
        self.assertEqual(
            create_colormap((0,0,0), 0, "white"),
            None
        )

    def test_colormap_invalid_color_range1(self):
        """Tests if passing a first color outside of the
        [0,1] range returns None
        """
        self.assertEqual(
            create_colormap((255,255,255), (1,1,1), "white"),
            None
        )

    def test_colormap_invalid_color_range2(self):
        """Tests if passing a second color outside of the
        [0,1] range returns None
        """
        self.assertEqual(
            create_colormap((0,0,0), (255,255,255), "white"),
            None
        )

    def test_colormap_invalid_rgb_quantization(self):
        """Tests if passing an invalid rgb quantization type
        returns None
        """
        self.assertEqual(
            create_colormap((0,0,0), (1,1,1), "white", "test"),
            None
        )

class TestImgtoolsExtender(unittest.TestCase):
    """Tests the imgtools extender module
    """

    def test_add_padding(self):
        """Tests if an image can be extended keeping the color of the last
        row in the extended area
        """
        np.testing.assert_array_equal(
            add_padding(np.zeros((4,5,3), dtype=np.uint8), 32)[0],
            np.zeros((32,32,3), dtype=np.uint8)
        )

    def test_add_padding_old_size(self):
        """Tests if an image that has been extended returns the correct old size
        """
        self.assertTupleEqual(
            add_padding(np.zeros((4,5,3), dtype=np.uint8), 32)[1:],
            (4,5)
        )


if __name__ == "__main__":
    unittest.main()
