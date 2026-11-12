class ErroSemantico(Exception):
    def __init__(self, mensagem: str, linha: int = 0, coluna: int = 0):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        pos = f" na linha {linha}, coluna {coluna}" if linha > 0 else ""
        super().__init__(f"Erro semantico{pos}: {mensagem}")


class Simbolo:
    def __init__(self, nome: str, endereco: int, linha: int):
        self.nome = nome
        self.endereco = endereco
        self.linha = linha

    def __repr__(self):
        return f"Simbolo(nome='{self.nome}', end={self.endereco}, L:{self.linha})"


class TabelaSimbolos:
    def __init__(self):
        self.simbolos: dict[str, Simbolo] = {}
        self.prox_endereco = 0

    # cadastra nova variavel e aloca endereco sequencial (0, 1, 2...)
    def declarar(self, nome: str, linha: int = 0, coluna: int = 0) -> Simbolo:
        if nome in self.simbolos:
            linha_ant = self.simbolos[nome].linha
            raise ErroSemantico(
                f"Variavel '{nome}' ja declarada na linha {linha_ant}",
                linha,
                coluna,
            )
        simb = Simbolo(nome, self.prox_endereco, linha)
        self.simbolos[nome] = simb
        self.prox_endereco += 1
        return simb

    # verifica se a variavel existe na tabela antes do uso
    def buscar(self, nome: str, linha: int = 0, coluna: int = 0) -> Simbolo:
        if nome not in self.simbolos:
            raise ErroSemantico(
                f"Variavel '{nome}' nao foi declarada",
                linha,
                coluna,
            )
        return self.simbolos[nome]

    def listar(self) -> list[Simbolo]:
        return list(self.simbolos.values())
