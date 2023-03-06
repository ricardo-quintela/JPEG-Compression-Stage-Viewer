"""Contém funções para análise lexical do
ficheiro de configuração
"""

from typing import List
from re import finditer, split, sub

from matplotlib.pyplot import show

from codec import decode

from imgtools import read_bmp
from imgtools import separate_channels
from imgtools import show_img
from imgtools import converter_to_ycbcr
from imgtools import add_padding
from imgtools import create_colormap
from imgtools import down_sample
from imgtools import calculate_dct
from imgtools import quantize
from imgtools import dpcm_encoder

from metrics import MSE
from metrics import RMSE
from metrics import SNR

from .stoken import Token
from .file_reader import load_q_matrix


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
    plot_matches = finditer(r"plot ([a-zA-Z0-9_]+|\"[a-zA-Z0-9_ ]+\")\n", buffer)
    end_matches = finditer(r"end\n", buffer)
    image_matches = finditer(r"-i \"([^\s\"]| )+\"|-i [^\s\"]+", buffer)
    colormap_matches = finditer(
        r"-m " + f"{number} "*5 + number,
        buffer
    )
    channel_matches = finditer(r"-c [123]", buffer)
    name_matches = finditer(r"-n ([a-zA-Z0-9_]+|\"[a-zA-Z0-9_ ]+\")", buffer)
    padding_matches = finditer(r"-p [0-9]+", buffer)
    ycc_matches = finditer(r"-y", buffer)
    rgb_matches = finditer(r"-r", buffer)
    subsample_matches = finditer(r"-s [0-9] [0-9] [0-9]", buffer)
    dct_matches = finditer(r"-d( [0-9]+)?", buffer)
    quantize_matches = finditer(r"-q", buffer)
    dcpm_matches = finditer(r"-f", buffer)


    tokens = list()

    # tokens PLOT
    for match in plot_matches:
        value = split(r"plot |\n", sub(r"\"", "", match.group()))[1]

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

    # tokens NAME
    for match in name_matches:
        value = split(r"-n |\n", sub(r"\"", "", match.group()))[1]

        tokens.append(
            Token("NAME", match.start(), value)
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

    # tokens SUBSAMPLE
    for match in subsample_matches:
        numbers = split(r" ", match.group())[1:]

        value = (
            int(numbers[0]),
            int(numbers[1]),
            int(numbers[2])
        )

        tokens.append(
            Token("SUBSAMPLE", match.start(), value)
        )

    # tokens DCT
    for match in dct_matches:
        if match.group() == "-d":
            value = None
        else:
            value = int(split(r" ", match.group())[1])

        tokens.append(
            Token("DCT", match.start(), value)
        )

    # tokens QUANTIZE
    for match in quantize_matches:
        tokens.append(
            Token("QUANTIZE", match.start())
        )

    # tokens QUANTIZE
    for match in dcpm_matches:
        tokens.append(
            Token("DPCM", match.start())
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
    print("Unable to parse the configuration file")
    return False


def semantic(buffer: List[Token]):
    """Faz a análise semântica dos tokens fornecidos

    Args:
        buffer (List[Token]): a lista de tokens depois da análise sintática
    """

    # juntar os comandos em blocos
    blocks = create_blocks(buffer)

    temp_encoded_img = None

    # interpretar comandos
    for i, block in enumerate(blocks):

        if str(block[0][0]) == "PLOT":

            plot_title = block[0][0].value
            num_plots = block[0][1]

            # calcular o tamanho do plot para ficar bem formatado na janela
            if num_plots == 1:
                plot_size = (1,1)
            elif num_plots == 2:
                plot_size = (1,2)
            else:
                plot_size = (int((num_plots + num_plots % 2) / 2),2)

            encoded_image = semantic_plot(
                block[1:],
                plot_title,
                plot_size,
                i+1
            )

            if temp_encoded_img is None:
                temp_encoded_img = encoded_image

    # mostrar a imagem decodificada
    if temp_encoded_img is not None:
        decoded_image = decode(temp_encoded_img[0], temp_encoded_img[1], temp_encoded_img[2])

        show_img(
            decoded_image,
            plot_title="Decoded Image"
        )

        # print(MSE(read_bmp('img/barn_mountains.bmp'), decoded_image))
        MSE_value = MSE(read_bmp('img/barn_mountains.bmp'), decoded_image)
        print(MSE_value)
        print(RMSE(MSE_value))
        print(SNR(MSE, read_bmp('img/barn_mountains.bmp')))
    
    # mostrar todos os plots
    show()


def create_blocks(buffer: List[Token]) -> List[List]:
    """Junta todos os blocos com os
    respetivos comandos numa lista de listas

    Args:
        buffer (List[Token]): a lista de tokens após a análise lexical

    Returns:
        List[List]: uma lista de listas de blocos
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
                blocks[block_index].append(dict())
                blocks[block_index][0][1] += 1
                command_index += 1

            blocks[block_index][command_index][token.name] = token.value

        else:
            block_index += 1
            command_index = 0

    return blocks



def semantic_plot(block: list, plot_title: str, plot_size: tuple, figure_identifier: int):
    """Interpreta os comandos num bloco "PLOT"

    Args:
        block (list): a lista de comandos do bloco PLOT
        plot_title (str): o titulo do plot
        plot_size (tuple): a configuração de disposição dos plots
        figure_identifier (int): o identificador da figura
    """

    separated_image = None
    command = None
    log_correction = False

    # iterar pelos comandos do bloco
    for j, command in enumerate(block):

        # ler a imagem
        image = read_bmp(command["IMAGE"])
        if image is None:
            return

        # extrair o canal
        channel = command["CHANNEL"] - 1 if "CHANNEL" in command else None

        # extrair o colormap e ter em conta erros
        if "COLORMAP" in command and channel is None:
            print("Color channel must be selected if a colormap is defined")
            return

        elif "COLORMAP" not in command:
            colormap = None

        else:
            colormap = create_colormap(
                command["COLORMAP"][0],
                command["COLORMAP"][1]
            )

        # adicionar padding à imagem
        if "PADDING" in command:
            image, o_width, o_height = add_padding(
                image, command["PADDING"]
            )

        # extrair nome do subplot
        name = command["NAME"] if "NAME" in command else None


        # extrair o colormap e ter em conta erros
        if "RGB" in command and channel is None:
            print("Color channel must be selected if RGB color mode is selected")
            return

        # colormode YCbCr
        if "RGB" in command:
            separated_image = separate_channels(image)


        # extrair o colormap e ter em conta erros
        if "YCC" in command and channel is None:
            print("Color channel must be selected if YCbCr color mode is selected")
            return

        # extrair o colormap e ter em conta erros
        if "YCC" in command and "COLORMAP" not in command:
            print("Colormap must be defined if YCbCr color mode is selected")
            return

        # colormode YCbCr
        if "YCC" in command:
            separated_image = converter_to_ycbcr(image)


        # extrair a subsampling string e ter em conta erros
        if "SUBSAMPLE" in command and channel is None:
            print("Color channel must be selected if downsampling is selected")
            return

        # subamostragem
        if "SUBSAMPLE" in command:

            # caso a imagem ainda não esteja separada
            if separated_image is None:
                separated_image = separate_channels(image)

            separated_image = down_sample(
                separated_image[0],
                separated_image[1],
                separated_image[2],
                command["SUBSAMPLE"]
            )

        # extrair o numero de blocos da dct
        if "DCT" in command and channel is None:
            print("Color channel must be selected if downsampling is selected")
            return

        if "DCT" in command:

            # caso a imagem ainda não esteja separada
            if separated_image is None:
                separated_image = separate_channels(image)

            separated_image = calculate_dct(
                separated_image[0],
                separated_image[1],
                separated_image[2],
                command["DCT"]
            )
            log_correction = True

        # quantizar a imagem e prevenir erros de não ter canal selecionado
        if "QUANTIZE" in command and channel is None:
            print("Color channel must be selected if quantization technique is selected")
            return

        if "QUANTIZE" in command:

            # caso a imagem ainda não esteja separada
            if separated_image is None:
                separated_image = separate_channels(image)

            q_matrix_y = load_q_matrix("q_matrix_y.csv")
            q_matrix_cbcr = load_q_matrix("q_matrix_cbcr.csv")


            separated_image = (
                quantize(separated_image[0], q_matrix_y),
                quantize(separated_image[1], q_matrix_cbcr),
                quantize(separated_image[2], q_matrix_cbcr)
            )
            log_correction = True


        # codificar os coeficientes DC da imagem e prevenir erros de não ter canal selecionado
        if "DPCM" in command and channel is None:
            print("Color channel must be selected if DPCM encoding is selected")
            return

        if "DPCM" in command:

            # caso a imagem ainda não esteja separada
            if separated_image is None:
                separated_image = separate_channels(image)

            # CHAMADA DA FUNCAO
            separated_image = (
                dpcm_encoder(separated_image[0]),
                dpcm_encoder(separated_image[1]),
                dpcm_encoder(separated_image[2])
            )
            log_correction = True




        # mostrar a imagem
        if separated_image is not None:
            image = separated_image[channel]

        show_img(
            image,
            colormap,
            plot_title,
            name,
            figure_identifier,
            (plot_size[0], plot_size[1], j+1),
            log_correction
        )

    # caso tenham sido aplicados niveis de encoding na image
    if command is not None and "YCC" in command and "SUBSAMPLE" in command and "PADDING" in command and "DCT" in command and "QUANTIZE" in command and "DPCM" in command:
        return separated_image, o_width, o_height

    return None
