from .tokens import Token, TokenType
from .tabela import NaoTerminal, AcaoSemantica, PRODUCOES, TABELA_M
from .semantico import TabelaSimbolos, ErroSemantico
from .gerador import GeradorCodigo


class ErroSintatico(Exception):
    def __init__(self, mensagem: str, linha: int = 0, coluna: int = 0):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        pos = f" na linha {linha}, coluna {coluna}" if linha > 0 else ""
        super().__init__(f"Erro sintatico{pos}: {mensagem}")


class AnalisadorSintatico:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.pilha = []
        self.tabela_simbolos = TabelaSimbolos()
        self.gerador = GeradorCodigo()

        # controle semantico e traducao
        self.id_atual = ""
        self.ultimo_id = ""
        self.ultimo_num = ""
        self.linha_id = 0
        self.col_id = 0
        self.op_rel = ""
        self.unario_neg = False
        self.pilha_desvios = []

    def _token_atual(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def analisar(self) -> GeradorCodigo:
        # inicia pilha com EOF ($) na base e PROG no topo
        self.pilha = [TokenType.EOF, NaoTerminal.PROG]

        while self.pilha:
            topo = self.pilha.pop()
            token = self._token_atual()

            # marcador de acao semantica / geracao de codigo
            if isinstance(topo, str) and topo.startswith("#"):
                self._executar_acao(topo)

            # topo e terminal: verifica match com o token da entrada
            elif isinstance(topo, TokenType):
                if topo == token.tipo:
                    if topo == TokenType.ID:
                        self.ultimo_id = token.lexema
                        self.linha_id = token.linha
                        self.col_id = token.coluna
                    elif topo == TokenType.NUM:
                        self.ultimo_num = token.lexema
                    self.pos += 1
                else:
                    raise ErroSintatico(
                        f"Esperado '{topo.name}', encontrado '{token.lexema}' ({token.tipo.name})",
                        token.linha,
                        token.coluna,
                    )

            # topo e nao-terminal: consulta a tabela preditiva M
            elif isinstance(topo, str):
                chave = (topo, token.tipo)
                if chave in TABELA_M:
                    num_prod = TABELA_M[chave]
                    producao = PRODUCOES[num_prod]
                    # empilha os simbolos ao contrario para o primeiro ficar no topo
                    for simbolo in reversed(producao):
                        self.pilha.append(simbolo)
                else:
                    raise ErroSintatico(
                        f"Token inesperado '{token.lexema}' ({token.tipo.name}) em '{topo}'",
                        token.linha,
                        token.coluna,
                    )

        return self.gerador

    def _executar_acao(self, acao: str):
        if acao == AcaoSemantica.INPP:
            self.gerador.emitir("INPP")

        elif acao == AcaoSemantica.PARA:
            self.gerador.emitir("PARA")

        elif acao == AcaoSemantica.ID_VISTO:
            self.id_atual = self.ultimo_id

        elif acao in (AcaoSemantica.DECL_UNICA, AcaoSemantica.DECL_PRIMEIRA):
            self.tabela_simbolos.declarar(self.id_atual, self.linha_id, self.col_id)
            self.gerador.emitir("ALME 1")

        elif acao == AcaoSemantica.DECL_SEGUINTE:
            self.tabela_simbolos.declarar(self.ultimo_id, self.linha_id, self.col_id)
            self.gerador.emitir("ALME 1")

        elif acao == AcaoSemantica.ATRIB_ID:
            simb = self.tabela_simbolos.buscar(self.id_atual, self.linha_id, self.col_id)
            self.gerador.emitir(f"ARMZ {simb.endereco}")

        elif acao == AcaoSemantica.EMIT_LEIT:
            self.gerador.emitir("LEIT")

        elif acao == AcaoSemantica.ECHO_ID:
            simb = self.tabela_simbolos.buscar(self.ultimo_id, self.linha_id, self.col_id)
            self.gerador.emitir(f"CRVL {simb.endereco}")

        elif acao == AcaoSemantica.EMIT_IMPR:
            self.gerador.emitir("IMPR")

        elif acao == AcaoSemantica.FATOR_ID:
            simb = self.tabela_simbolos.buscar(self.ultimo_id, self.linha_id, self.col_id)
            self.gerador.emitir(f"CRVL {simb.endereco}")

        elif acao == AcaoSemantica.FATOR_NUM:
            self.gerador.emitir(f"CRCT {self.ultimo_num}")

        elif acao == AcaoSemantica.UNARIO_MENOS:
            self.unario_neg = True

        elif acao == AcaoSemantica.UNARIO_NENHUM:
            self.unario_neg = False

        elif acao == AcaoSemantica.APLICA_UNARIO:
            if self.unario_neg:
                self.gerador.emitir("INVE")
                self.unario_neg = False

        elif acao == AcaoSemantica.EMIT_SOMA:
            self.gerador.emitir("SOMA")
        elif acao == AcaoSemantica.EMIT_SUBT:
            self.gerador.emitir("SUBT")
        elif acao == AcaoSemantica.EMIT_MULT:
            self.gerador.emitir("MULT")
        elif acao == AcaoSemantica.EMIT_DIV:
            self.gerador.emitir("DIVI")

        elif acao == AcaoSemantica.OP_EQ:
            self.op_rel = "CPIG"
        elif acao == AcaoSemantica.OP_NE:
            self.op_rel = "CDES"
        elif acao == AcaoSemantica.OP_GE:
            self.op_rel = "CPAI"
        elif acao == AcaoSemantica.OP_LE:
            self.op_rel = "CPMI"
        elif acao == AcaoSemantica.OP_GT:
            self.op_rel = "CPMA"
        elif acao == AcaoSemantica.OP_LT:
            self.op_rel = "CPME"

        elif acao == AcaoSemantica.EMIT_REL:
            self.gerador.emitir(self.op_rel)

        # controle de desvios do while
        elif acao == AcaoSemantica.WHILE_INI:
            self.pilha_desvios.append(("WHILE_INI", self.gerador.endereco_atual()))

        elif acao == AcaoSemantica.WHILE_COND:
            pos_dsvf = self.gerador.emitir("DSVF 0")
            self.pilha_desvios.append(("WHILE_COND", pos_dsvf))

        elif acao == AcaoSemantica.WHILE_FIM:
            _, pos_dsvf = self.pilha_desvios.pop()
            _, ini_while = self.pilha_desvios.pop()
            self.gerador.emitir(f"DSVI {ini_while}")
            self.gerador.remendar(pos_dsvf, self.gerador.endereco_atual())

        # controle de desvios do if / else
        elif acao == AcaoSemantica.IF_COND:
            pos_dsvf = self.gerador.emitir("DSVF 0")
            self.pilha_desvios.append(("IF", pos_dsvf))

        elif acao == AcaoSemantica.ELSE_INI:
            pos_dsvi = self.gerador.emitir("DSVI 0")
            _, pos_dsvf = self.pilha_desvios.pop()
            self.gerador.remendar(pos_dsvf, self.gerador.endereco_atual())
            self.pilha_desvios.append(("ELSE", pos_dsvi))

        elif acao == AcaoSemantica.IF_FIM:
            _, pos_desvio = self.pilha_desvios.pop()
            self.gerador.remendar(pos_desvio, self.gerador.endereco_atual())
