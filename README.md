# Visualizador de Etapas de Compressão JPEG

<p align='center'>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8-yellow" />
  </a>&nbsp;&nbsp;
</p>

Welcome to the repository dedicated to our Multimedia project during our undergraduate studies,
focusing on the exploration of the JPEG compression method.
This interactive program provides a detailed view of the codec, allowing users to customize their experience through an intuitive scripting language.

## Key Features:

### Interactivity:

- Explore each phase of the JPEG codec interactively.
- Instruct the program with a simple scripting language.

### Detailed Visualization:

- Visually observe the impact of each stage on image quality.
- Combine stages to understand compression decisions.

### Side-by-Side Comparison:

- Compare various stages of the JPEG codec for a comparative analysis.
- Gain insights into different compression settings.

## Contents

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
  
## Requirements

[**Python 3.8**](https://www.python.org/downloads/) or above

Libraries:  
`python -m pip install -r requirements.txt`

# Usage

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


# Scripting the behaviour of the program

A configuration file in a basic scripting language can be used to visualize different steps of the compression
algorithm side by side.

To use:
`main.py -a path/to/config_file`

Example of a configuration file structure:

```
plot "RGB Channels"
-i "img/barn_mountains.bmp" -m 0 0 0 1 0 0 -c 1 -r -n "R Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 0 1 0 -c 2 -r -n "G Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 0 0 1 -c 3 -r -n "B Channel"
end
plot "YCbCr Channels"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 1 -y -p 32 -n "Y Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 2 -y -p 32 -n "Cb Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 3 -y -p 32 -n "Cr Channel"
end
plot "YCbCr Channels whith 422 Downsampling"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 1 -y -s 4 2 2 -p 32 -n "Y Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 2 -y -s 4 2 2 -p 32 -n "Cb Channel"
-i "img/barn_mountains.bmp" -m 0 0 0 1 1 1 -c 3 -y -s 4 2 2 -p 32 -n "Cr Channel"
end
plot Original
-i "img/barn_mountains.bmp"
end
```

## Flags

| Command | Arguments                                  | Action                                                                                                 |
| ------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `-i`    | PATH                                        | Selects an image file to use                                                                         |
| `-m`    | FLOAT FLOAT FLOAT FLOAT FLOAT FLOAT \[0,1\] | Creates a color map for image visualization                                                          |
| `-c`    | INT {1,2,3}                                 | Selects one of the image channels                                                                    |
| `-y`    |                                             | Selects YcbCr color mode                                                                            |
| `-r`    |                                             | Selects RGB color mode                                                                              |
| `-s`    | INT INT INT {0,1,2,4}                       | Subsamples image channels according to a configuration                                               |
| `-n`    | STRING                                      | Name of the image subplot                                                                           |
| `-p`    | INT                                         | Adds padding to the provided image                                                                  |
| `-d`    | INT                                         | Performs DCT on blocks of the given size or on the entire image if not provided                      |
| `-q`    | INT                                         | Quantizes the image using quantization matrices                                                      |
| `-f`    |                                             | Applies DPCM encoding                                                                              |
| `-e`    |                                             | Encodes the image and displays intermediate steps                                                   |
| `plot`  | STRING                                      | Initiates a `plot` code block with the provided name in `STRING`                                      |
| `end`   |                                             | Ends a code block                                                                                   |
