from .tokens import Token, TokenType
from .tabela import NaoTerminal, AcaoSemantica, PRODUCOES, TABELA_M
from .semantico import TabelaSimbolos, ErroSemantico


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
        self.id_atual = ""
        self.ultimo_id = ""
        self.linha_id = 0
        self.col_id = 0

    def _token_atual(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def analisar(self) -> TabelaSimbolos:
        # inicia pilha com EOF ($) na base e PROG no topo
        self.pilha = [TokenType.EOF, NaoTerminal.PROG]

        while self.pilha:
            topo = self.pilha.pop()
            token = self._token_atual()

            # marcador de acao semantica
            if isinstance(topo, str) and topo.startswith("#"):
                self._executar_acao_semantica(topo)

            # topo e terminal: verifica match com o token da entrada
            elif isinstance(topo, TokenType):
                if topo == token.tipo:
                    if topo == TokenType.ID:
                        self.ultimo_id = token.lexema
                        self.linha_id = token.linha
                        self.col_id = token.coluna
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

        return self.tabela_simbolos

    def _executar_acao_semantica(self, acao: str):
        if acao == AcaoSemantica.ID_VISTO:
            self.id_atual = self.ultimo_id

        elif acao in (AcaoSemantica.DECL_UNICA, AcaoSemantica.DECL_PRIMEIRA):
            self.tabela_simbolos.declarar(self.id_atual, self.linha_id, self.col_id)

        elif acao == AcaoSemantica.DECL_SEGUINTE:
            self.tabela_simbolos.declarar(self.ultimo_id, self.linha_id, self.col_id)

        elif acao == AcaoSemantica.VERIFICA_ATRIB:
            self.tabela_simbolos.buscar(self.id_atual, self.linha_id, self.col_id)

        elif acao == AcaoSemantica.VERIFICA_ID:
            self.tabela_simbolos.buscar(self.ultimo_id, self.linha_id, self.col_id)


if __name__ == "__main__":
    import sys
    from .lexico import AnalisadorLexico, ErroLexico

    if len(sys.argv) < 2:
        print("Uso: python3 -m parte1_compilador.sintatico <arquivo.php>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        codigo = f.read()

    try:
        lexer = AnalisadorLexico(codigo)
        tokens = lexer.obter_todos_tokens()
        parser = AnalisadorSintatico(tokens)
        tab = parser.analisar()
        print("Analise sintatica e semantica concluida com sucesso!")
        print("Tabela de simbolos:", tab.listar())
    except (ErroLexico, ErroSintatico, ErroSemantico) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
