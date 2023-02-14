"""Contém funções para análise lexical do
ficheiro de configuração
"""

from re import finditer

def lex(buffer: str):
    
    # encontrar plots
    plot_tokens = list(finditer(r"plot [a-zA-Z0-9]+\n", buffer))

    end_tokens = list(finditer(r"end\n", buffer))

    if len(plot_tokens) != len(end_tokens):
        print("ERRO NO PARSER (numero de plots e ends diferentes)")
        return

    # DEBUG
    for i in range(len(plot_tokens)):
        print(plot_tokens[i].group()[:-1], plot_tokens[i].span(), end_tokens[i].group()[:-1], end_tokens[i].span())


    for i in range(len(plot_tokens)):

        if not end_tokens[i].start() > plot_tokens[i].end():
            print("ERRO NO PARSER (bloco de plot desemparelhado)")
            return

        







if __name__ == "__main__":
    s = """plot nome1
-i caminho -m color1 color2 -c canal
-i caminho -m color1 color2 -c canal
-i caminho -m color1 color2 -c canal
end
plot nome2
-i caminho -m color1 color2 -c canal
-i caminho -m color1 color2 -c canal
-i caminho -m color1 color2 -c canal
end
"""

    lex(s)
