# Trabalho prático 1 de Multimédia

## Compressão de Imagem

<p align='center'>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8-yellow" />
  </a>&nbsp;&nbsp;
</p>

Repositório para desenvolvimento e trabalho em grupo  

## Conteúdo

```
mult_tp1
├── ARCH
├── DEV
│   └── test
│   └── img
├── PM
│   ├── docs
│   └── group
├── PROC
├── PROD
├── QA
│   └── docs
└── REQ
```
  
## Requisitos

[**Python 3.8**](https://www.python.org/downloads/) ou superior

Bibliotecas:  
`python -m pip install -r requirements.txt`

# Modo de uso

```
usage: main.py [-h] (-i PATH | -a PATH) [-c CHANNEL] [-m     ] [-n NAME] [-e] [-y | -r]
               [-p PADDING] [-s  ] [-d DCT] [-q QUANTIZE] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --image PATH
                        show the image on the given path
  -a PATH, --config PATH
                        use a configuration file with commands to run multiple plot instances
  -n NAME, --name NAME  give a name to the plot
  -e, --encode          encode image using JPEG codec and display steps
  -y, --ycbcr           convert the image channels to the YCbCr color model
  -r, --rgb             convert the image channels to the RGB color model (default)

  -c CHANNEL, --channel CHANNEL
                        select a color channel: {1, 2, 3}
  -m      , --colormap
                        provide a colormap for the image

  -p PADDING, --padding PADDING
                        add padding to the image unitl a certain value
  -s   , --downsample
                        downsample the image by a given set of values {0, 1, 2, 4}
  -d DCT, --dct DCT     calculate the dct of the image (must be multiples of 8, 0 to apply on
                        the whole channel)
  -q QUANTIZE, --quantize QUANTIZE
                        quantize the image with a defined quality factor [0,100]
  -f, --dcpm            encode the DC coeficients of the image
```


# Ficheiro de configuração

Um ficheiro de configuração tem blocos de comandos que o programa interpreta.  

Exemplo da estrutura de um ficheiro de configuração:

```
plot "Canais RGB"
-i "img/barn_mountains.bmp" -m 0 0 0 1 0 0 -c 1 -r -n "Canal R"
-i "img/barn_mountains.bmp" -m 0 0 0 0 1 0 -c 2 -r -n "Canal G"
-i "img/barn_mountains.bmp" -m 0 0 0 0 0 1 -c 3 -r -n "Canal B"
end
plot "Canais YCbCr"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 1 -y -p 32 -n "Canal Y"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 2 -y -p 32 -n "Canal Cb"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 3 -y -p 32 -n "Canal Cr"
end
plot "Canais YCbCr com Downsampling 422"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 1 -y -s 4 2 2 -p 32 -n "Canal Y"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 2 -y -s 4 2 2 -p 32 -n "Canal Cb"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 3 -y -s 4 2 2 -p 32 -n "Canal Cr"
end
plot Original
-i "img/barn_mountains.bmp"
end

```

## Flags

| Comando | Argumentos                                  | Ação                                                                                                  |
| ------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `-i`    | PATH                                        | Seleciona uma ficheiro de imagem para utilizar                                                        |
| `-m`    | FLOAT FLOAT FLOAT FLOAT FLOAT FLOAT \[0,1\] | Cria um mapa de cor para utilizar na visualização da imagem                                           |
| `-c`    | INT {1,2,3}                                 | Seleciona um dos canais da imagem                                                                     |
| `-y`    |                                             | Seleciona o modo de cor YcbCr                                                                         |
| `-r`    |                                             | Seleciona o modo de cor RGB                                                                           |
| `-s`    | INT INT INT {0,1,2,4}                       | Faz a subamostragem dos canais da imagem segundo uma configuração                                     |
| `-n`    | STRING                                      | Nome do subplot da imagem                                                                             |
| `-p`    | INT                                         | Adiciona um preenchimento à imagem fornecida                                                          |
| `-d`    | INT                                         | Calcula a dct em blocos de valor igual ao inteiro fornecido ou na imagem toda caso não seja fornecido |
| `-q`    | INT                                         | Quantiza a imagem com as matrizes de quantização                                                      |
| `-f`    |                                             | Aplica codificação DPCM                                                                               |
| `-e`    |                                             | Faz a codificação da imagem e apresenta passos intermédios                                            |
| `plot`  | STRING                                      | Inicia um bloco de código do tipo `plot` com o nome fornecido na `STRING`                             |
| `end`   |                                             | Termina um bloco de código                                                                            |
