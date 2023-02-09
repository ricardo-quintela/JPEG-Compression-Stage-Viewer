"""Tests the codec
"""

import unittest

import numpy as np
import matplotlib.colors as clr

# imgtools
from imgtools import read_bmp
from imgtools import create_colormap

class TestImgToolsReader(unittest.TestCase):
    """Tests the imgtools reader package
    """

    def test_read_file(self):
        """Test if a bmp image can be read
        """
        np.testing.assert_array_equal(read_bmp("test/test_img.bmp"), np.array([[[255,255,255]]], dtype=np.uint8))


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


if __name__ == "__main__":
    unittest.main()
