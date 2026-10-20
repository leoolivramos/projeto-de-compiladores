from enum import Enum, auto


class TokenType(Enum):
    # tags
    TAG_OPEN = auto()       # <?php
    TAG_CLOSE = auto()      # ?>

    # palavras reservadas
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    ECHO = auto()
    PHP_EOL = auto()
    FLOATVAL = auto()
    READLINE = auto()

    # variavel e numero
    ID = auto()             # $id
    NUM = auto()            # int ou float

    # atribuicao e ponto
    ATRIB = auto()          # =
    PONTO = auto()          # .

    # aritmeticos
    MAIS = auto()           # +
    MENOS = auto()          # -
    MULT = auto()           # *
    DIV = auto()            # /

    # relacionais
    EQ = auto()             # ==
    NE = auto()             # !=
    GE = auto()             # >=
    LE = auto()             # <=
    GT = auto()             # >
    LT = auto()             # <

    # pontuacao
    PONTO_VIRGULA = auto()  # ;
    VIRGULA = auto()        # ,
    ABRE_PAR = auto()       # (
    FECHA_PAR = auto()      # )
    ABRE_CHAVE = auto()     # {
    FECHA_CHAVE = auto()    # }

    EOF = auto()            # fim do arquivo


class Token:
    def __init__(self, tipo: TokenType, lexema: str, linha: int, coluna: int):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo.name}, '{self.lexema}', L:{self.linha}, C:{self.coluna})"
