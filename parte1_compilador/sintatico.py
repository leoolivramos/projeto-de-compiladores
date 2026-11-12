from .tokens import Token, TokenType
from .tabela import NaoTerminal, PRODUCOES, TABELA_M


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

    def _token_atual(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def analisar(self):
        # inicia pilha com EOF ($) na base e PROG no topo
        self.pilha = [TokenType.EOF, NaoTerminal.PROG]

        while self.pilha:
            topo = self.pilha.pop()
            token = self._token_atual()

            # topo e terminal: verifica match com o token da entrada
            if isinstance(topo, TokenType):
                if topo == token.tipo:
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
        parser.analisar()
        print("Analise sintatica concluida com sucesso!")
    except (ErroLexico, ErroSintatico) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
