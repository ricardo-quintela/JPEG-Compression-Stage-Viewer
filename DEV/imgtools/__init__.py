"""Contém ferramentas para trabalhar com imagens
"""

# reader
from .reader import read_bmp

# color
from .color import create_colormap, separate_channels, join_channels

# extender
from .extender import add_padding, restore_padding

# viewer
from .viewer import show_img

# converter
from .converter import converter_to_rgb, converter_to_ycbcr
