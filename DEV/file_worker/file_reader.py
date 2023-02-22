"""Contém funções para efetuar o parsing de ficheiros
de configuração
"""

from os.path import isdir
from json import loads
from json.decoder import JSONDecodeError

def read_config(path: str) -> str:
    """Lê um ficheiro de configuração

    Args:
        path (str): o caminho do ficheiro de configuração

    Returns:
        str: o conteúdo do ficheiro de configuração
    """

    # não é um ficheiro
    if isdir(path):
        print("Given path is not a file")
        return

    # extensão errada
    if not path.endswith(".cfg"):
        print("Given file is not a configuration file")

    # ler o ficheiro
    try:
        with open(path, "r", encoding="utf-8") as conf_file:
            return conf_file.read()

    # ficheiro não existe
    except FileNotFoundError:
        print("Given file does not exist")
        return

    # ocorreu outro erro
    except IOError:
        print("An error has occured while opening the file")
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
        print("Given path is not a file")
        return

    # extensão errada
    if not path.endswith(".json"):
        print("Given file is not a JSON file")

    # ler o ficheiro
    try:
        with open(path, "r", encoding="utf-8") as conf_file:
            return loads(conf_file.read())

    except JSONDecodeError:
        print("An erros has occured while loading the grammar")
        return

    # ficheiro não existe
    except FileNotFoundError:
        print("Given file does not exist")
        return

    # ocorreu outro erro
    except IOError:
        print("An error has occured while reading the grammar file")
        return
