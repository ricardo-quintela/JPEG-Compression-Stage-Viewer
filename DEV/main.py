"""
'Trabalho Prático nº 1'
'Compressão de Imagem'

Criado por:
    André Filipe Costa Colaço - 2020220301 
    João Rafael do Rosário Henriques - 2020216586
    Ricardo Quintela Martins Santos Rosa - 2020220508
"""

import argparse

from imgtools import show_img, read_bmp, create_colormap, separate_channels



def main():
    """Função principal onde todas as outras serão chamadas
    e será tratada a interação com o utilizador
    """

    parser = argparse.ArgumentParser()

    image_group = parser.add_mutually_exclusive_group(required=True)
    image_group.add_argument(
        "-i", "--image",
        help="show the image on the given path",
        type=str,
        metavar="PATH"
    )

    color_group = parser.add_argument_group()
    color_group.add_argument(
        "-c", "--channels",
        help="separates the given image in it's RGB channels",
        action="store_true"
    )
    color_group.add_argument(
        "-m", "--colormap",
        help="provide a colormap for the image",
        type=float,
        metavar="",
        nargs=6
    )

    color_channel = parser.add_mutually_exclusive_group()
    color_channel.add_argument(
        "-r", "--red",
        help="select the red channel of the image",
        action="store_true"
    )
    color_channel.add_argument(
        "-g", "--green",
        help="select the green channel of the image",
        action="store_true"
    )
    color_channel.add_argument(
        "-b", "--blue",
        help="select the blue channel of the image",
        action="store_true"
    )

    args = parser.parse_args()


    # verificar se as cores passadas estão no formato certo
    if args.colormap is not None and len(args.colormap) % 3 != 0:
        parser.print_usage()
        print(f"{__file__}: error: invalid RGB color format")
        return

    # agrupar as cores
    if args.colormap is not None:
        colors = (args.colormap[0:3], args.colormap[3:])

        if not (args.red or args.green or args.blue):
            parser.print_usage()
            print(f"{__file__}: error: colormap argument requires the selection of a color channel")
            return



    # o utilizador escolhe ver a imagem
    if args.image is not None:

        # ler a imagem
        image = read_bmp(args.image)
        if image is None:
            return

        # utilizador quer usar um colormap
        if args.colormap:

            # criar o colormap
            colormap = create_colormap(colors[0], colors[1], "colormap")
            if colormap is None:
                return

            # separar os canais
            channels = separate_channels(image)
            if channels is None:
                return

            # selecionar o canal dependendo da escolha do utilizador
            if args.red:
                selected_channel = channels[0]
            if args.green:
                selected_channel = channels[1]
            if args.blue:
                selected_channel = channels[2]

            # mostrar a imagem com o colormap
            show_img(selected_channel, colormap)

        # mostrar a imagem sem colormap
        else:
            show_img(image)


if __name__ == "__main__":
    main()
