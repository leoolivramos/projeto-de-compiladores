from .tokens import Token, TokenType


class ErroLexico(Exception):
    def __init__(self, mensagem: str, linha: int, coluna: int):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(f"Erro lexico na linha {linha}, coluna {coluna}: {mensagem}")


class AnalisadorLexico:
    PALAVRAS_CHAVE = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "echo": TokenType.ECHO,
        "PHP_EOL": TokenType.PHP_EOL,
        "floatval": TokenType.FLOATVAL,
        "readline": TokenType.READLINE,
    }

    def __init__(self, codigo_fonte: str):
        self.fonte = codigo_fonte
        self.pos = 0
        self.tam = len(codigo_fonte)
        self.linha = 1
        self.coluna = 1

    def _char_atual(self) -> str:
        if self.pos >= self.tam:
            return ""
        return self.fonte[self.pos]

    def _espiar(self, deslocamento: int = 1) -> str:
        idx = self.pos + deslocamento
        if idx >= self.tam:
            return ""
        return self.fonte[idx]

    def _avancar(self) -> str:
        ch = self._char_atual()
        self.pos += 1
        if ch == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return ch

    def _pular_espacos_e_comentarios(self):
        while self.pos < self.tam:
            ch = self._char_atual()

            # espacos e quebras de linha
            if ch in (" ", "\t", "\r", "\n"):
                self._avancar()
                continue

            # comentario //
            if ch == "/" and self._espiar(1) == "/":
                self._avancar()
                self._avancar()
                while self.pos < self.tam and self._char_atual() != "\n":
                    self._avancar()
                continue

            # comentario /* ... */
            if ch == "/" and self._espiar(1) == "*":
                l_ini, c_ini = self.linha, self.coluna
                self._avancar()
                self._avancar()
                while self.pos < self.tam:
                    if self._char_atual() == "*" and self._espiar(1) == "/":
                        self._avancar()
                        self._avancar()
                        break
                    self._avancar()
                else:
                    raise ErroLexico("Comentario em bloco nao fechado", l_ini, c_ini)
                continue

            break

    def proximo_token(self) -> Token:
        self._pular_espacos_e_comentarios()

        if self.pos >= self.tam:
            return Token(TokenType.EOF, "$", self.linha, self.coluna)

        l_tok = self.linha
        c_tok = self.coluna
        ch = self._char_atual()

        # tag <?php
        if ch == "<" and self._espiar(1) == "?":
            if self.fonte[self.pos : self.pos + 5] == "<?php":
                for _ in range(5):
                    self._avancar()
                return Token(TokenType.TAG_OPEN, "<?php", l_tok, c_tok)

        # tag ?>
        if ch == "?" and self._espiar(1) == ">":
            self._avancar()
            self._avancar()
            return Token(TokenType.TAG_CLOSE, "?>", l_tok, c_tok)

        # variavel com $
        if ch == "$":
            lexema = self._avancar()
            prox = self._char_atual()
            if not (prox.isalpha() or prox == "_"):
                raise ErroLexico(f"Identificador invalido apos '$': '{prox}'", l_tok, c_tok)
            while self._char_atual().isalnum() or self._char_atual() == "_":
                lexema += self._avancar()
            return Token(TokenType.ID, lexema, l_tok, c_tok)

        # numero (inteiro ou real)
        if ch.isdigit():
            lexema = ""
            while self._char_atual().isdigit():
                lexema += self._avancar()
            if self._char_atual() == "." and self._espiar(1).isdigit():
                lexema += self._avancar()
                while self._char_atual().isdigit():
                    lexema += self._avancar()
            return Token(TokenType.NUM, lexema, l_tok, c_tok)

        # palavras-chave
        if ch.isalpha() or ch == "_":
            lexema = ""
            while self._char_atual().isalnum() or self._char_atual() == "_":
                lexema += self._avancar()
            if lexema in self.PALAVRAS_CHAVE:
                return Token(self.PALAVRAS_CHAVE[lexema], lexema, l_tok, c_tok)
            raise ErroLexico(f"Identificador ou palavra inesperada: '{lexema}'", l_tok, c_tok)

        # relacionais e atribuicao
        if ch == "=":
            self._avancar()
            if self._char_atual() == "=":
                self._avancar()
                return Token(TokenType.EQ, "==", l_tok, c_tok)
            return Token(TokenType.ATRIB, "=", l_tok, c_tok)

        if ch == "!":
            self._avancar()
            if self._char_atual() == "=":
                self._avancar()
                return Token(TokenType.NE, "!=", l_tok, c_tok)
            raise ErroLexico("Esperado '=' apos '!'", l_tok, c_tok)

        if ch == ">":
            self._avancar()
            if self._char_atual() == "=":
                self._avancar()
                return Token(TokenType.GE, ">=", l_tok, c_tok)
            return Token(TokenType.GT, ">", l_tok, c_tok)

        if ch == "<":
            self._avancar()
            if self._char_atual() == "=":
                self._avancar()
                return Token(TokenType.LE, "<=", l_tok, c_tok)
            return Token(TokenType.LT, "<", l_tok, c_tok)

        # operadores
        if ch == "+":
            self._avancar()
            return Token(TokenType.MAIS, "+", l_tok, c_tok)
        if ch == "-":
            self._avancar()
            return Token(TokenType.MENOS, "-", l_tok, c_tok)
        if ch == "*":
            self._avancar()
            return Token(TokenType.MULT, "*", l_tok, c_tok)
        if ch == "/":
            self._avancar()
            return Token(TokenType.DIV, "/", l_tok, c_tok)

        # pontuacao
        if ch == ";":
            self._avancar()
            return Token(TokenType.PONTO_VIRGULA, ";", l_tok, c_tok)
        if ch == ",":
            self._avancar()
            return Token(TokenType.VIRGULA, ",", l_tok, c_tok)
        if ch == ".":
            self._avancar()
            return Token(TokenType.PONTO, ".", l_tok, c_tok)
        if ch == "(":
            self._avancar()
            return Token(TokenType.ABRE_PAR, "(", l_tok, c_tok)
        if ch == ")":
            self._avancar()
            return Token(TokenType.FECHA_PAR, ")", l_tok, c_tok)
        if ch == "{":
            self._avancar()
            return Token(TokenType.ABRE_CHAVE, "{", l_tok, c_tok)
        if ch == "}":
            self._avancar()
            return Token(TokenType.FECHA_CHAVE, "}", l_tok, c_tok)

        invalido = self._avancar()
        raise ErroLexico(f"Caractere invalido: '{invalido}'", l_tok, c_tok)

    def obter_todos_tokens(self) -> list[Token]:
        tokens = []
        while True:
            t = self.proximo_token()
            tokens.append(t)
            if t.tipo == TokenType.EOF:
                break
        return tokens


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python3 -m parte1_compilador.lexico <arquivo.php>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        codigo = f.read()

    try:
        scanner = AnalisadorLexico(codigo)
        for token in scanner.obter_todos_tokens():
            print(token)
    except ErroLexico as e:
        print(e, file=sys.stderr)
        sys.exit(1)
