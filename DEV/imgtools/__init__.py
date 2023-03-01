"""Contém ferramentas para trabalhar com imagens
"""

# reader
from .reader import read_bmp

# color
from .color import create_colormap, separate_channels, join_channels, converter_to_rgb, converter_to_ycbcr

# extender
from .extender import add_padding, restore_padding, down_sample, up_sample

# viewer
from .viewer import show_img

# dct
from .dct import calculate_dct, calculate_inv_dct

# quantization
from .quantization import quantize, inv_quantize
