"""Contém funções para análise lexical do
ficheiro de configuração
"""

from typing import List
from re import finditer, split, sub

from .token import Token


def lex(buffer: str) -> List[Token]:
    """Cria tokens a partir de expressões regulares
    encontradas num buffer fornecido

    Args:
        buffer (str): o buffer que contém o texto a ser analisado

    Returns:
        List[Token]: uma lista de tokens pela ordem que aparecem
    """

    number = r"([01]|0.[0-9]+|.[0-9]+)"

    # encontrar plots
    plot_matches = finditer(r"plot [a-zA-Z0-9]+\n", buffer)
    end_matches = finditer(r"end\n", buffer)
    image_matches = finditer(r"-i \"([^\s]| )+\"|-i [^\s\"]+", buffer)
    colormap_matches = finditer(
        r"-m " + f"{number} "*5 + number,
        buffer
    )
    channel_matches = finditer(r"-c [123]", buffer)
    ycc_matches = finditer(r"-y", buffer)
    rgb_matches = finditer(r"-r", buffer)


    tokens = list()

    # tokens PLOT
    for match in plot_matches:
        value = split(r"\s", match.group())[1]

        tokens.append(
            Token("PLOT", match.start(), value)
        )

    # tokens END
    for match in end_matches:
        tokens.append(
            Token("END", match.start())
        )

    # tokens IMAGE
    for match in image_matches:
        value = split(r"-i ", sub(r"\"", "", match.group()))[1]

        tokens.append(
            Token("IMAGE", match.start(), value)
        )

    # tokens COLORMAP
    for match in colormap_matches:
        numbers = split(r" ", match.group())[1:]

        value = (
            (float(numbers[0]), float(numbers[1]), float(numbers[2])),
            (float(numbers[3]), float(numbers[4]), float(numbers[5])),
        )


        tokens.append(
            Token("COLORMAP", match.start(), value)
        )

    # tokens CHANNEL
    for match in channel_matches:
        value = int(split(r" ", match.group())[1])

        tokens.append(
            Token("CHANNEL", match.start(), value)
        )

    # tokens YCC
    for match in ycc_matches:
        tokens.append(
            Token("YCC", match.start())
        )

    # tokens RGB
    for match in rgb_matches:
        tokens.append(
            Token("RGB", match.start())
        )

    # ordenar os tokens
    tokens.sort()

    return tokens
