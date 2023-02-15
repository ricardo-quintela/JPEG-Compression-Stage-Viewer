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
from codec import encode, decode

from file_worker import lex, synt, semantic, read_config, load_grammar



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

    args = parser.parse_args()


    #  verificar se argumentos são usados com seus parents corretos
    if args.image and args.channel and not args.colormap:
        parser.print_usage()
        print(f"{basename(__file__)}: error: channel argument can only be user with a colormap")
        return

    #  verificar se argumentos são usados com seus parents corretos
    if args.image and args.ycbcr and not args.colormap:
        parser.print_usage()
        print(f"{basename(__file__)}: error: ycbcr argument can only be user with a colormap")
        return


    # verificar se as cores passadas estão no formato certo
    if args.colormap is not None and len(args.colormap) % 3 != 0:
        parser.print_usage()
        print(f"{basename(__file__)}: error: invalid RGB color format")
        return

    # agrupar as cores
    if args.colormap is not None:
        colors = (args.colormap[0:3], args.colormap[3:])

        if args.channel is None:
            parser.print_usage()
            print(f"{basename(__file__)}: error: colormap argument requires the selection of a color channel")
            return

    # o utilizador escolhe ver a imagem
    if args.image:

        # ler a imagem
        image = read_bmp(args.image)
        if image is None:
            return

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
                if channels is None:
                    return

            # selecionar o canal dependendo da escolha do utilizador
            if args.channel == 1:
                selected_channel = channels[0]
            if args.channel == 2:
                selected_channel = channels[1]
            if args.channel == 3:
                selected_channel = channels[2]

            # mostrar a imagem com o colormap
            show_img(selected_channel, colormap)

        # mostrar a imagem sem colormap
        else:
            show_img(image)

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
