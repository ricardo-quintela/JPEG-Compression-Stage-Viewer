"""Contém ferramentas para verificar comandos num ficheiro
de configuração
"""

# file_parser
from .file_reader import read_config, load_grammar, load_q_matrix

# lex_analysis
from .analysis import lex, synt, semantic

# token
from .stoken import Token
