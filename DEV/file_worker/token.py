"""Contém a classe token
"""

class Token:
    """Guarda a informação sobre um token
    """

    def __init__(self, name: str, pos: int, index: int, value: object = None) -> None:
        """Construtor da classe token

        Token
        -----
        Um token é uma expressão regular representada por um nome\n
        Um token pode também ter um valor associado

        Args:
            name (str): o nome do token
            pos: (int): a posição do token no buffer
            index: (int): o indice do token
            value (object, optional): o valor do token. Default a None
        """
        self.name = name
        self.pos = pos
        self.index = index
        self.value = value

        self.matches = list()

    def __lt__(self, __o: object) -> bool:
        return self.pos < __o.pos

    def __gt__(self, __o: object) -> bool:
        return self.pos > __o.pos

    def __le__(self, __o: object) -> bool:
        return self.pos <= __o.pos

    def __ge__(self, __o: object) -> bool:
        return self.pos >= __o.pos

    def __eq__(self, __o: object) -> bool:
        return self.name == str(__o)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name} -> {self.value}"
