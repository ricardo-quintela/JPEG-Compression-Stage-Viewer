"""
'Trabalho Prático nº 1'
'Compressão de Imagem'

Criado por:
    André Filipe Costa Colaço - 2020220301 
    João Rafael do Rosário Henriques - 2020216586
    Ricardo Quintela Martins Santos Rosa - 2020220508
"""

import argparse
from os.path import basename

from imgtools import show_img
from imgtools import read_bmp
from imgtools import create_colormap, separate_channels
from imgtools import converter_to_ycbcr
from imgtools import add_padding
from imgtools import down_sample
from imgtools import calculate_dct
from imgtools import quantize
from imgtools import dpcm_encoder

from codec import main_codec_function

from file_worker import lex, synt, semantic, read_config, load_grammar, load_q_matrix

from matplotlib.pyplot import close


def main(): 
    """Função principal onde todas as outras serão chamadas
    e será tratada a interação com o utilizador

    Argumentos:

    -i PATH -> Escolher a imagem

        -m {r g b r g b} -> Escolher um colormap para usar na visualização da imagem
            -r -> Escolher o formato RGB
            -y -> Escolher o formato YCbCr
            -c {canal} -> Selecionar um canal: int [1,3]

    -a PATH -> Ficheiro de config que tem comandos para diferentes plots
    """

    # fechar todos os plots a correr no backend do matplotlib
    close("all")
    
    # criar um parser de argumentos da consola
    parser = argparse.ArgumentParser()

    # selecionar imagem
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "-i", "--image",
        help="show the image on the given path",
        type=str,
        metavar="PATH"
    )

    action_group.add_argument(
        "-a", "--config",
        help="use a configuration file with commands to run multiple plot instances",
        type=str,
        metavar="PATH"
    )

    # selecionar ação
    color_group = parser.add_argument_group()
    color_group.add_argument(
        "-c", "--channel",
        help="select a color channel: {1, 2, 3}",
        type=int
    )
    color_group.add_argument(
        "-m", "--colormap",
        help="provide a colormap for the image",
        type=float,
        metavar="",
        nargs=6
    )

    # nome do plot
    parser.add_argument(
        "-n", "--name",
        type=str,
        help="give a name to the plot",
        metavar="NAME"
    )

    # encode geral
    parser.add_argument(
        "-e", "--encode",
        type=str,
        help="encode image using JPEG codec and display steps",
        action="store_true"
    )


    # modelos de cor
    color_model_group = parser.add_mutually_exclusive_group()
    color_model_group.add_argument(
        "-y", "--ycbcr",
        help="convert the image channels to the YCbCr color model",
        action="store_true"
    )
    color_model_group.add_argument(
        "-r", "--rgb",
        help="convert the image channels to the RGB color model (default)",
        action="store_true"
    )

    transformations_group = parser.add_argument_group()
    transformations_group.add_argument(
        "-p", "--padding",
        help="add padding to the image unitl a certain value",
        type=int
    )

    transformations_group.add_argument(
        "-s", "--downsample",
        help="downsample the image by a given set of values {0, 1, 2, 4}",
        type=int,
        nargs=3,
        metavar=""
    )

    transformations_group.add_argument(
        "-d", "--dct",
        help="calculate the dct of the image (must be multiples of 8, 0 to apply on the whole channel)",
        type=int
    )

    transformations_group.add_argument(
        "-q", "--quantize",
        help="quantize the image with a defined quality factor [0,100]",
        type=int
    )

    transformations_group.add_argument(
        "-f", "--dcpm",
        help="encode the DC coeficients of the image",
        action="store_true"
    )

    args = parser.parse_args()

    #  verificar se argumentos são usados com seus parents corretos
    if args.image and args.channel and not args.colormap:
        parser.print_usage()
        print(
            f"{basename(__file__)}: error: channel argument can only be user with a colormap")
        return

    #  verificar se argumentos são usados com seus parents corretos
    if args.image and args.ycbcr and not args.colormap:
        parser.print_usage()
        print(
            f"{basename(__file__)}: error: ycbcr argument can only be user with a colormap")
        return

    # verificar se as cores passadas estão no formato certo
    if args.colormap is not None and len(args.colormap) % 3 != 0:
        parser.print_usage()
        print(f"{basename(__file__)}: error: invalid RGB color format")
        return
    
    # verificação da correção lograítmica
    if args.dct:
        log_correction = True
    else:
        log_correction = False

    # agrupar as cores
    if args.colormap is not None:
        colors = (args.colormap[0:3], args.colormap[3:])

        if args.channel is None:
            parser.print_usage()
            print(
                f"{basename(__file__)}: error: colormap argument requires the selection of a color channel")
            return
        

    # utilizar encode geral
    if args.encode:

        # tratamento de parâmetros em falta
        if args.image is None or args.quantize is None:
            print(f"{basename(__file__)}: error: an image path must be given as well as a quality factor")
            return
        
        # ler a imagem
        image = read_bmp(args.image)
        if image is None:
            return

        main_codec_function(image, args.quantize)
        return




    # o utilizador escolhe ver a imagem
    if args.image:

        # ler a imagem
        image = read_bmp(args.image)
        if image is None:
            return

        if args.name:
            name = args.name
        else:
            name = None

        # add padding to the image
        if args.padding:
            image, *_ = add_padding(image, args.padding)

        # utilizador quer usar um colormap
        if args.colormap:

            # criar o colormap
            colormap = create_colormap(colors[0], colors[1], "colormap")
            if colormap is None:
                return

            # converter a imagem para ycbcr
            if args.ycbcr:
                channels = converter_to_ycbcr(image)

            if not args.ycbcr:
                # separar os canais
                channels = separate_channels(image)

                # ocorreu um erro
                if channels is None:
                    return

            # fazer downsampling da imagem
            if args.channel and args.downsample is not None:
                channels = down_sample(channels[0], channels[1], channels[2], args.downsample)

                # ocorreu um erro
                if channels is None:
                    return

            # calcular a dct
            if args.channel and args.dct is not None:
                dct_block = None if args.dct == 0 else args.dct
                log_correction = True

                channels = calculate_dct(channels[0], channels[1], channels[2], dct_block)

                # ocorreu um erro
                if channels is None:
                    return

            # quantizar os canais
            if args.channel and args.quantize:
                q_matrix_y = load_q_matrix("q_matrix_y.csv")
                q_matrix_cbcr = load_q_matrix("q_matrix_cbcr.csv")

                if args.quantize > 100 or args.quantize < 0:
                    print(f"{basename(__file__)}: error: quality factor must be a percentage value")
                    return

                channels = (
                    quantize(channels[0], q_matrix_y, args.quantize),
                    quantize(channels[1], q_matrix_cbcr, args.quantize),
                    quantize(channels[2], q_matrix_cbcr, args.quantize)
                )

                # ocorreu um erro
                if channels[0] is None or channels[1] is None or channels[2] is None:
                    return

                log_correction = True


            # codificar os coeficientes DC os canais
            if args.channel and args.dcpm:

                channels = (
                    dpcm_encoder(channels[0]),
                    dpcm_encoder(channels[1]),
                    dpcm_encoder(channels[2])
                )

                # ocorreu um erro
                if channels[0] is None or channels[1] is None or channels[2] is None:
                    return

                log_correction = True


            # selecionar o canal dependendo da escolha do utilizador
            if args.channel == 1:
                selected_channel = channels[0]
            if args.channel == 2:
                selected_channel = channels[1]
            if args.channel == 3:
                selected_channel = channels[2]


            # mostrar a imagem com o colormap
            show_img(selected_channel, colormap, name=name, log_correction=log_correction)


        # mostrar a imagem sem colormap
        else:
            show_img(image, name=name, log_correction=log_correction)


    # usar um ficheiro de configuração
    if args.config:
        grammar = load_grammar("grammar.json")
        if grammar is None:
            return

        config = read_config(args.config)
        if config is None:
            return

        tokens = lex(config)
        if not synt(tokens, grammar):
            return

        semantic(tokens)


if __name__ == "__main__":
    main()
