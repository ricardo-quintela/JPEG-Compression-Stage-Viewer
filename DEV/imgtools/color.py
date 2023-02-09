"""Contains functions related to color manipulation
and colormaps
"""

from typing import Tuple

from matplotlib.colors import LinearSegmentedColormap

def create_colormap(
        first_color: Tuple[float, float, float],
        second_color: Tuple[float, float, float],
        name:str,
        rgb_quantization: int = 256,
    ) -> LinearSegmentedColormap:

    """Creates a linear segment colormap with the given RGB color values\n
    the colormap will be named with the given name

    Args:
        first_color (Tuple[float, float, float]): the first color
        second_color (Tuple[float, float, float]): the final color
        name (str): the name of the colormap
        rgb_quantization (int, optional): the RGB quantization levels. Defaults to 256.

    Returns:
        LinearSegmentedColormap: A LinearSegmentedColormap object or None if an error occurs
    """

    # try to create a colormap
    try:
        cmap = LinearSegmentedColormap.from_list(
            name,
            [first_color, second_color],
            rgb_quantization
        )

    # if the color arguments are in a wrong format
    except ValueError:
        print("Invalid color argument or rgb quantization value")
        return

    # first color contains invalid values
    if not (0 <= first_color[0] <= 1 or 0 <= first_color[1] <= 1 or 0 <= first_color[2] <= 1):
        print("Color values must be mapped from the range [0,1]")
        return

    # second color contains invalid values
    if not (0 <= second_color[0] <= 1 or 0 <= second_color[1] <= 1 or 0 <= second_color[2] <= 1):
        print("Color values must be mapped from the range [0,1]")
        return

    return cmap
