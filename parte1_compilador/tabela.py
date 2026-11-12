from .tokens import TokenType


class NaoTerminal:
    PROG = "PROG"
    CMDS = "CMDS"
    RESTO_ID = "RESTO_ID"
    MAIS_VAR = "MAIS_VAR"
    MAIS_CMDS = "MAIS_CMDS"
    CMD_COND = "CMD_COND"
    PFALSA = "PFALSA"
    EXP_IDENT = "EXP_IDENT"
    CONDICAO = "CONDICAO"
    RELACAO = "RELACAO"
    EXPRESSAO = "EXPRESSAO"
    OUTROS_TERMOS = "OUTROS_TERMOS"
    TERMO = "TERMO"
    OP_UN = "OP_UN"
    MAIS_FATORES = "MAIS_FATORES"
    FATOR = "FATOR"


class AcaoSemantica:
    ID_VISTO = "#ID_VISTO"
    DECL_UNICA = "#DECL_UNICA"
    DECL_PRIMEIRA = "#DECL_PRIMEIRA"
    DECL_SEGUINTE = "#DECL_SEGUINTE"
    VERIFICA_ATRIB = "#VERIFICA_ATRIB"
    VERIFICA_ID = "#VERIFICA_ID"


# gramatica fatorada com marcadores de checagem semantica
PRODUCOES = {
    1: [TokenType.TAG_OPEN, NaoTerminal.CMDS, TokenType.TAG_CLOSE],
    2: [TokenType.ID, AcaoSemantica.ID_VISTO, NaoTerminal.RESTO_ID, NaoTerminal.MAIS_CMDS],
    3: [TokenType.ECHO, TokenType.ID, AcaoSemantica.VERIFICA_ID, TokenType.PONTO, TokenType.PHP_EOL, NaoTerminal.MAIS_CMDS],
    4: [NaoTerminal.CMD_COND, NaoTerminal.CMDS],
    5: [],  # lambda

    # resto_id: decide entre atribuicao (=) ou declaracao de variaveis (, ou ;)
    6: [TokenType.ATRIB, NaoTerminal.EXP_IDENT, AcaoSemantica.VERIFICA_ATRIB],
    7: [AcaoSemantica.DECL_PRIMEIRA, TokenType.VIRGULA, TokenType.ID, AcaoSemantica.DECL_SEGUINTE, NaoTerminal.MAIS_VAR],
    8: [AcaoSemantica.DECL_UNICA],  # declaracao simples: $a;

    9: [TokenType.VIRGULA, TokenType.ID, AcaoSemantica.DECL_SEGUINTE, NaoTerminal.MAIS_VAR],
    10: [],  # lambda

    11: [TokenType.PONTO_VIRGULA, NaoTerminal.CMDS],

    # estruturas condicionais e repeticao
    12: [TokenType.IF, TokenType.ABRE_PAR, NaoTerminal.CONDICAO, TokenType.FECHA_PAR, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE, NaoTerminal.PFALSA],
    13: [TokenType.WHILE, TokenType.ABRE_PAR, NaoTerminal.CONDICAO, TokenType.FECHA_PAR, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE],
    14: [TokenType.ELSE, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE],
    15: [],  # lambda

    # atribuicao de leitura ou expressao
    16: [TokenType.FLOATVAL, TokenType.ABRE_PAR, TokenType.READLINE, TokenType.ABRE_PAR, TokenType.FECHA_PAR, TokenType.FECHA_PAR],
    17: [NaoTerminal.EXPRESSAO],

    # condicao e operadores relacionais
    18: [NaoTerminal.EXPRESSAO, NaoTerminal.RELACAO, NaoTerminal.EXPRESSAO],
    19: [TokenType.EQ],
    20: [TokenType.NE],
    21: [TokenType.GE],
    22: [TokenType.LE],
    23: [TokenType.GT],
    24: [TokenType.LT],

    # expressoes aritmeticas
    25: [NaoTerminal.TERMO, NaoTerminal.OUTROS_TERMOS],
    26: [TokenType.MAIS, NaoTerminal.TERMO, NaoTerminal.OUTROS_TERMOS],
    27: [TokenType.MENOS, NaoTerminal.TERMO, NaoTerminal.OUTROS_TERMOS],
    28: [],  # lambda

    29: [NaoTerminal.OP_UN, NaoTerminal.FATOR, NaoTerminal.MAIS_FATORES],
    30: [TokenType.MENOS],
    31: [],  # lambda

    32: [TokenType.MULT, NaoTerminal.FATOR, NaoTerminal.MAIS_FATORES],
    33: [TokenType.DIV, NaoTerminal.FATOR, NaoTerminal.MAIS_FATORES],
    34: [],  # lambda

    35: [TokenType.ID, AcaoSemantica.VERIFICA_ID],
    36: [TokenType.NUM],
    37: [TokenType.ABRE_PAR, NaoTerminal.EXPRESSAO, TokenType.FECHA_PAR],
}


# tabela preditiva LL(1): (NaoTerminal, TokenType) -> numero da producao
TABELA_M = {
    # PROG
    (NaoTerminal.PROG, TokenType.TAG_OPEN): 1,

    # CMDS
    (NaoTerminal.CMDS, TokenType.ID): 2,
    (NaoTerminal.CMDS, TokenType.ECHO): 3,
    (NaoTerminal.CMDS, TokenType.IF): 4,
    (NaoTerminal.CMDS, TokenType.WHILE): 4,
    (NaoTerminal.CMDS, TokenType.FECHA_CHAVE): 5,
    (NaoTerminal.CMDS, TokenType.TAG_CLOSE): 5,

    # RESTO_ID
    (NaoTerminal.RESTO_ID, TokenType.ATRIB): 6,
    (NaoTerminal.RESTO_ID, TokenType.VIRGULA): 7,
    (NaoTerminal.RESTO_ID, TokenType.PONTO_VIRGULA): 8,

    # MAIS_VAR
    (NaoTerminal.MAIS_VAR, TokenType.VIRGULA): 9,
    (NaoTerminal.MAIS_VAR, TokenType.PONTO_VIRGULA): 10,

    # MAIS_CMDS
    (NaoTerminal.MAIS_CMDS, TokenType.PONTO_VIRGULA): 11,

    # CMD_COND
    (NaoTerminal.CMD_COND, TokenType.IF): 12,
    (NaoTerminal.CMD_COND, TokenType.WHILE): 13,

    # PFALSA
    (NaoTerminal.PFALSA, TokenType.ELSE): 14,
    (NaoTerminal.PFALSA, TokenType.ID): 15,
    (NaoTerminal.PFALSA, TokenType.ECHO): 15,
    (NaoTerminal.PFALSA, TokenType.IF): 15,
    (NaoTerminal.PFALSA, TokenType.WHILE): 15,
    (NaoTerminal.PFALSA, TokenType.FECHA_CHAVE): 15,
    (NaoTerminal.PFALSA, TokenType.TAG_CLOSE): 15,

    # EXP_IDENT
    (NaoTerminal.EXP_IDENT, TokenType.FLOATVAL): 16,
    (NaoTerminal.EXP_IDENT, TokenType.MENOS): 17,
    (NaoTerminal.EXP_IDENT, TokenType.ID): 17,
    (NaoTerminal.EXP_IDENT, TokenType.NUM): 17,
    (NaoTerminal.EXP_IDENT, TokenType.ABRE_PAR): 17,

    # CONDICAO
    (NaoTerminal.CONDICAO, TokenType.MENOS): 18,
    (NaoTerminal.CONDICAO, TokenType.ID): 18,
    (NaoTerminal.CONDICAO, TokenType.NUM): 18,
    (NaoTerminal.CONDICAO, TokenType.ABRE_PAR): 18,

    # RELACAO
    (NaoTerminal.RELACAO, TokenType.EQ): 19,
    (NaoTerminal.RELACAO, TokenType.NE): 20,
    (NaoTerminal.RELACAO, TokenType.GE): 21,
    (NaoTerminal.RELACAO, TokenType.LE): 22,
    (NaoTerminal.RELACAO, TokenType.GT): 23,
    (NaoTerminal.RELACAO, TokenType.LT): 24,

    # EXPRESSAO
    (NaoTerminal.EXPRESSAO, TokenType.MENOS): 25,
    (NaoTerminal.EXPRESSAO, TokenType.ID): 25,
    (NaoTerminal.EXPRESSAO, TokenType.NUM): 25,
    (NaoTerminal.EXPRESSAO, TokenType.ABRE_PAR): 25,

    # OUTROS_TERMOS
    (NaoTerminal.OUTROS_TERMOS, TokenType.MAIS): 26,
    (NaoTerminal.OUTROS_TERMOS, TokenType.MENOS): 27,
    (NaoTerminal.OUTROS_TERMOS, TokenType.PONTO_VIRGULA): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.EQ): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.NE): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.GE): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.LE): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.GT): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.LT): 28,
    (NaoTerminal.OUTROS_TERMOS, TokenType.FECHA_PAR): 28,

    # TERMO
    (NaoTerminal.TERMO, TokenType.MENOS): 29,
    (NaoTerminal.TERMO, TokenType.ID): 29,
    (NaoTerminal.TERMO, TokenType.NUM): 29,
    (NaoTerminal.TERMO, TokenType.ABRE_PAR): 29,

    # OP_UN
    (NaoTerminal.OP_UN, TokenType.MENOS): 30,
    (NaoTerminal.OP_UN, TokenType.ID): 31,
    (NaoTerminal.OP_UN, TokenType.NUM): 31,
    (NaoTerminal.OP_UN, TokenType.ABRE_PAR): 31,

    # MAIS_FATORES
    (NaoTerminal.MAIS_FATORES, TokenType.MULT): 32,
    (NaoTerminal.MAIS_FATORES, TokenType.DIV): 33,
    (NaoTerminal.MAIS_FATORES, TokenType.MAIS): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.MENOS): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.PONTO_VIRGULA): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.EQ): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.NE): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.GE): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.LE): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.GT): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.LT): 34,
    (NaoTerminal.MAIS_FATORES, TokenType.FECHA_PAR): 34,

    # FATOR
    (NaoTerminal.FATOR, TokenType.ID): 35,
    (NaoTerminal.FATOR, TokenType.NUM): 36,
    (NaoTerminal.FATOR, TokenType.ABRE_PAR): 37,
}
