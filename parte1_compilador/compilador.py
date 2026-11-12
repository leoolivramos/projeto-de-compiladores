import sys
import os
from .lexico import AnalisadorLexico, ErroLexico
from .sintatico import AnalisadorSintatico, ErroSintatico
from .semantico import ErroSemantico


def compilar(caminho_entrada: str, caminho_saida: str = "codigo_objeto.txt") -> str:
    if not os.path.exists(caminho_entrada):
        print(f"Erro: arquivo '{caminho_entrada}' nao encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(caminho_entrada, "r", encoding="utf-8") as f:
        codigo_fonte = f.read()

    try:
        lexer = AnalisadorLexico(codigo_fonte)
        tokens = lexer.obter_todos_tokens()

        parser = AnalisadorSintatico(tokens)
        gerador = parser.analisar()

        gerador.salvar(caminho_saida)
        print(f"Compilacao concluida! Codigo objeto salvo em: {caminho_saida}")
        return gerador.codigo_texto()

    except (ErroLexico, ErroSintatico, ErroSemantico) as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 -m parte1_compilador.compilador <entrada.php> [saida.txt]")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else "codigo_objeto.txt"
    compilar(entrada, saida)
