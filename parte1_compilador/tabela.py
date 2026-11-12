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
    INPP = "#INPP"
    PARA = "#PARA"
    ID_VISTO = "#ID_VISTO"
    DECL_UNICA = "#DECL_UNICA"
    DECL_PRIMEIRA = "#DECL_PRIMEIRA"
    DECL_SEGUINTE = "#DECL_SEGUINTE"
    ATRIB_ID = "#ATRIB_ID"
    ECHO_ID = "#ECHO_ID"
    EMIT_IMPR = "#EMIT_IMPR"
    EMIT_LEIT = "#EMIT_LEIT"
    IF_COND = "#IF_COND"
    ELSE_INI = "#ELSE_INI"
    IF_FIM = "#IF_FIM"
    WHILE_INI = "#WHILE_INI"
    WHILE_COND = "#WHILE_COND"
    WHILE_FIM = "#WHILE_FIM"
    EMIT_REL = "#EMIT_REL"
    OP_EQ = "#OP_EQ"
    OP_NE = "#OP_NE"
    OP_GE = "#OP_GE"
    OP_LE = "#OP_LE"
    OP_GT = "#OP_GT"
    OP_LT = "#OP_LT"
    EMIT_SOMA = "#EMIT_SOMA"
    EMIT_SUBT = "#EMIT_SUBT"
    EMIT_MULT = "#EMIT_MULT"
    EMIT_DIV = "#EMIT_DIV"
    UNARIO_MENOS = "#UNARIO_MENOS"
    UNARIO_NENHUM = "#UNARIO_NENHUM"
    APLICA_UNARIO = "#APLICA_UNARIO"
    FATOR_ID = "#FATOR_ID"
    FATOR_NUM = "#FATOR_NUM"


# gramatica fatorada com acoes semanticas e de geracao de codigo
PRODUCOES = {
    1: [TokenType.TAG_OPEN, AcaoSemantica.INPP, NaoTerminal.CMDS, TokenType.TAG_CLOSE, AcaoSemantica.PARA],
    2: [TokenType.ID, AcaoSemantica.ID_VISTO, NaoTerminal.RESTO_ID, NaoTerminal.MAIS_CMDS],
    3: [TokenType.ECHO, TokenType.ID, AcaoSemantica.ECHO_ID, TokenType.PONTO, TokenType.PHP_EOL, AcaoSemantica.EMIT_IMPR, NaoTerminal.MAIS_CMDS],
    4: [NaoTerminal.CMD_COND, NaoTerminal.CMDS],
    5: [],  # lambda

    # resto_id: atribuicao (=) ou declaracao (, ou ;)
    6: [TokenType.ATRIB, NaoTerminal.EXP_IDENT, AcaoSemantica.ATRIB_ID],
    7: [AcaoSemantica.DECL_PRIMEIRA, TokenType.VIRGULA, TokenType.ID, AcaoSemantica.DECL_SEGUINTE, NaoTerminal.MAIS_VAR],
    8: [AcaoSemantica.DECL_UNICA],

    9: [TokenType.VIRGULA, TokenType.ID, AcaoSemantica.DECL_SEGUINTE, NaoTerminal.MAIS_VAR],
    10: [],  # lambda

    11: [TokenType.PONTO_VIRGULA, NaoTerminal.CMDS],

    # if / else e while
    12: [TokenType.IF, TokenType.ABRE_PAR, NaoTerminal.CONDICAO, TokenType.FECHA_PAR, AcaoSemantica.IF_COND, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE, NaoTerminal.PFALSA, AcaoSemantica.IF_FIM],
    13: [TokenType.WHILE, AcaoSemantica.WHILE_INI, TokenType.ABRE_PAR, NaoTerminal.CONDICAO, TokenType.FECHA_PAR, AcaoSemantica.WHILE_COND, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE, AcaoSemantica.WHILE_FIM],
    14: [TokenType.ELSE, AcaoSemantica.ELSE_INI, TokenType.ABRE_CHAVE, NaoTerminal.CMDS, TokenType.FECHA_CHAVE],
    15: [],  # lambda

    # leitura ou expressao
    16: [TokenType.FLOATVAL, TokenType.ABRE_PAR, TokenType.READLINE, TokenType.ABRE_PAR, TokenType.FECHA_PAR, TokenType.FECHA_PAR, AcaoSemantica.EMIT_LEIT],
    17: [NaoTerminal.EXPRESSAO],

    # condicao e relacionais
    18: [NaoTerminal.EXPRESSAO, NaoTerminal.RELACAO, NaoTerminal.EXPRESSAO, AcaoSemantica.EMIT_REL],
    19: [TokenType.EQ, AcaoSemantica.OP_EQ],
    20: [TokenType.NE, AcaoSemantica.OP_NE],
    21: [TokenType.GE, AcaoSemantica.OP_GE],
    22: [TokenType.LE, AcaoSemantica.OP_LE],
    23: [TokenType.GT, AcaoSemantica.OP_GT],
    24: [TokenType.LT, AcaoSemantica.OP_LT],

    # expressoes aritmeticas
    25: [NaoTerminal.TERMO, NaoTerminal.OUTROS_TERMOS],
    26: [TokenType.MAIS, NaoTerminal.TERMO, AcaoSemantica.EMIT_SOMA, NaoTerminal.OUTROS_TERMOS],
    27: [TokenType.MENOS, NaoTerminal.TERMO, AcaoSemantica.EMIT_SUBT, NaoTerminal.OUTROS_TERMOS],
    28: [],  # lambda

    29: [NaoTerminal.OP_UN, NaoTerminal.FATOR, AcaoSemantica.APLICA_UNARIO, NaoTerminal.MAIS_FATORES],
    30: [TokenType.MENOS, AcaoSemantica.UNARIO_MENOS],
    31: [AcaoSemantica.UNARIO_NENHUM],

    32: [TokenType.MULT, NaoTerminal.FATOR, AcaoSemantica.EMIT_MULT, NaoTerminal.MAIS_FATORES],
    33: [TokenType.DIV, NaoTerminal.FATOR, AcaoSemantica.EMIT_DIV, NaoTerminal.MAIS_FATORES],
    34: [],  # lambda

    35: [TokenType.ID, AcaoSemantica.FATOR_ID],
    36: [TokenType.NUM, AcaoSemantica.FATOR_NUM],
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
