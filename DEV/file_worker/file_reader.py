"""Contém funções para efetuar o parsing de ficheiros
de configuração
"""

from os.path import isdir
from json import loads
from json.decoder import JSONDecodeError
from numpy import loadtxt, uint8, ndarray

def read_config(path: str) -> str:
    """Lê um ficheiro de configuração

    Args:
        path (str): o caminho do ficheiro de configuração

    Returns:
        str: o conteúdo do ficheiro de configuração
    """

    # não é um ficheiro
    if isdir(path):
        print(f"{path} is not a file")
        return

    # extensão errada
    if not path.endswith(".cfg"):
        print(f"File at {path} is not a configuration file")

    # ler o ficheiro
    try:
        with open(path, "r", encoding="utf-8") as conf_file:
            return conf_file.read()

    # ficheiro não existe
    except FileNotFoundError:
        print(f"File at {path} does not exist")
        return

    # ocorreu outro erro
    except IOError:
        print(f"An error has occured while reading the file at {path}")
        return


def load_grammar(path: str) -> dict:
    """Lê um ficheiro de JSON contedo a gramática do parser

    Args:
        path (str): o caminho do ficheiro de gramática

    Returns:
        dict: um dicionário com as produções de gramática
    """

    # não é um ficheiro
    if isdir(path):
        print(f"{path} is not a file")
        return

    # extensão errada
    if not path.endswith(".json"):
        print(f"File at {path} is not a JSON file")

    # ler o ficheiro
    try:
        with open(path, "r", encoding="utf-8") as conf_file:
            return loads(conf_file.read())

    except JSONDecodeError:
        print("An error has occured while loading the grammar")
        return

    # ficheiro não existe
    except FileNotFoundError:
        print(f"File at {path} does not exist")
        return

    # ocorreu outro erro
    except IOError:
        print(f"An error has occured while reading the grammar file at {path}")
        return


def load_q_matrix(path: str) -> ndarray:
    """Lê um ficheiro csv e carrega uma matriz de quantização

    Args:
        path (str): o caminho do ficheiro que contém a matriz de quantização

    Returns:
        ndarray: uma matriz de quantização
    """

    # não é um ficheiro
    if isdir(path):
        print(f"{path} is not a file")
        return

    # extensão errada
    if not path.endswith(".csv"):
        print(f"File at {path} is not a CSV file")

    # ler o ficheiro
    try:
        return loadtxt(path, dtype=uint8, delimiter=",")

    except ValueError:
        print(f"Could not load quantization matrix from file at {path}")

    # ficheiro não existe
    except FileNotFoundError:
        print(f"File at {path} does not exist")
        return

    # ocorreu outro erro
    except IOError:
        print(f"An error has occured while reading the file at {path}")
        return
