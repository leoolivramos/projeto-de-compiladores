class GeradorCodigo:
    def __init__(self):
        # lista de instrucoes da maquina hipotetica
        self.instrucoes: list[str] = []

    def emitir(self, inst: str) -> int:
        idx = len(self.instrucoes)
        self.instrucoes.append(inst.strip())
        return idx

    # corrige o endereco de destino de um DSVF ou DSVI (backpatching)
    def remendar(self, idx: int, destino: int):
        op = self.instrucoes[idx].split()[0]
        self.instrucoes[idx] = f"{op} {destino}"

    def endereco_atual(self) -> int:
        return len(self.instrucoes)

    def codigo_texto(self) -> str:
        return "\n".join(self.instrucoes) + "\n"

    def salvar(self, caminho: str):
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(self.codigo_texto())
