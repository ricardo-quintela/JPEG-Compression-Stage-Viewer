"""
'Trabalho Prático nº 1'
'Compressão de Imagem'

Criado por:
    André Filipe Costa Colaço - 2020220301 
    João Rafael do Rosário Henriques - 2020216586
    Ricardo Quintela Martins Santos Rosa - 2020220508
"""

from codec import encode, decode


def main():
    img, num_lines, num_col = encode('./img/barn_mountains.bmp')
    decode(img, num_lines, num_col)


if __name__ == "__main__":
    main()