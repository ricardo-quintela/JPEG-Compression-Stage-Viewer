"""Contém funções para análise lexical do
ficheiro de configuração
"""

from typing import List
from re import finditer, split, sub

from matplotlib.pyplot import show

from .stoken import Token
from imgtools import read_bmp, separate_channels, show_img, converter_to_ycbcr, add_padding, create_colormap


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
    plot_matches = finditer(r"plot [a-zA-Z0-9_]+\n", buffer)
    end_matches = finditer(r"end\n", buffer)
    image_matches = finditer(r"-i \"([^\s]| )+\"|-i [^\s\"]+", buffer)
    colormap_matches = finditer(
        r"-m " + f"{number} "*5 + number,
        buffer
    )
    channel_matches = finditer(r"-c [123]", buffer)
    padding_matches = finditer(r"-p [1-9][0-9]*", buffer)
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

    # tokens PADDING
    for match in padding_matches:
        value = int(split(r" ", match.group())[1])

        tokens.append(
            Token("PADDING", match.start(), value)
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


def synt(buffer: List[Token], productions: dict) -> bool:
    """Faz a análise sintática do buffer de tokens recolhidos
    pela análise lexical

    Args:
        buffer (List[Token]): o buffer que contém os tokens

    Returns:
        bool: True se a AST for contruida com sucesso, False caso contrário
    """

    # pilha de tokens
    stack = list()


    # iterar pela pilha (stack)
    i = len(buffer) - 1
    while i >= 0:

        # stack temporária
        stack_ind = -1
        stack_comp = list()
        
        # adicionar o token à stack
        stack.append(buffer[i].name)
        i -= 1

        # percorrer a stack atual e tentar reduzir as produçoes
        while stack_ind > -len(stack) - 1:
            
            # preencher stack temporaria
            stack_comp.append(stack[stack_ind])
            stack_ind -= 1

            # procurar por uma produção que satisfaça um reduce
            # se não for encontrada faz-se shift do proximo token
            for production in productions:

                # encontrou-se uma produção para fazer reduce
                if stack_comp in productions[production]:

                    # reduce da produção
                    j = len(stack) + stack_ind + 1
                    while j < len(stack):
                        stack.pop(j)
                    stack.append(production)

                    # reset à stack temporária
                    stack_comp = list()
                    stack_ind = -1
                    break


    # sucesso no parsing
    if stack == ["PROGRAM"]:
        return True
    
    # falhou
    print("ERRO: não foi possível fazer o parsing do ficheiro de configuração")
    return False


def semantic(buffer: List[Token]):
    """Faz a análise semântica dos tokens fornecidos

    Args:
        buffer (List[Token]): a lista de tokens depois da análise sintática
    """

    blocks = list()

    block_index = 0
    command_index = 0
    for token in buffer:

        if token == "PLOT":
            blocks.append([[token, 0]])
            continue

        if token != "END":
            
            if token == "IMAGE":
                blocks[block_index].append({token.name: token.value})
                blocks[block_index][0][1] += 1
                command_index += 1
                continue

            blocks[block_index][command_index][token.name] = token.value

        else:
            block_index += 1
            command_index = 0

    # interpretar comandos
    for i, block in enumerate(blocks):

        if block[0][0] == "PLOT":

            plot_size = block[0][1]+block[0][1]%2

            for j, command in enumerate(block[1:]):
                image = read_bmp(command["IMAGE"])

                if "COLORMAP" in command:
                    colormap = create_colormap(command["COLORMAP"][0], command["COLORMAP"][1], "colormap")
                    channel = command["CHANNEL"]
                else:
                    colormap = None

                if "PADDING" in command:
                    image = add_padding(image, command["PADDING"])[0]

                if "YCC" in command:
                    image = converter_to_ycbcr(image)[channel-1]

                if not "YCC" in command and "CHANNEL" in command:
                    image = separate_channels(image)[channel-1]

                
                show_img(image, colormap, block[0][0].value, i+1, (int(plot_size/2), int(plot_size/2), j+1))

    show()


            


if __name__ == "__main__":

    from file_reader import load_grammar, read_config

    tk = lex(read_config("../ex_1_5_config.cfg"))

    if synt(tk, load_grammar("../grammar.json")):
        semantic(tk)

