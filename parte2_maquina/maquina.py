import sys
import os


class ErroExecucao(Exception):
    def __init__(self, mensagem: str, pc: int = -1):
        pos = f" (instrucao {pc})" if pc >= 0 else ""
        super().__init__(f"Erro de execucao{pos}: {mensagem}")


class MaquinaHipotetica:
    def __init__(self, tam_memoria: int = 1000):
        # memoria de codigo (C) e pilha de dados (M)
        self.codigo: list[tuple[str, str | None]] = []
        self.memoria: list[float] = [0.0] * tam_memoria
        self.pc = 0
        self.sp = -1
        self.saidas: list[float] = []

    def carregar_texto(self, texto: str):
        self.codigo.clear()
        for linha in texto.strip().splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = linha.split(maxsplit=1)
            op = partes[0].upper()
            arg = partes[1] if len(partes) > 1 else None
            self.codigo.append((op, arg))

    def carregar_arquivo(self, caminho: str):
        with open(caminho, "r", encoding="utf-8") as f:
            self.carregar_texto(f.read())

    def executar(self, entradas_teste: list[float] | None = None):
        self.pc = 0
        self.sp = -1
        self.saidas.clear()
        fila_entradas = list(entradas_teste) if entradas_teste is not None else None

        # ciclo principal de execucao
        while 0 <= self.pc < len(self.codigo):
            op, arg = self.codigo[self.pc]

            if op == "INPP":
                self.sp = -1
                self.pc += 1

            elif op == "PARA":
                break

            elif op == "ALME":
                self.sp += int(arg)
                self.pc += 1

            elif op == "DESM":
                self.sp -= int(arg)
                self.pc += 1

            elif op == "CRCT":
                self.sp += 1
                self.memoria[self.sp] = float(arg)
                self.pc += 1

            elif op == "CRVL":
                self.sp += 1
                self.memoria[self.sp] = self.memoria[int(arg)]
                self.pc += 1

            elif op == "ARMZ":
                self.memoria[int(arg)] = self.memoria[self.sp]
                self.sp -= 1
                self.pc += 1

            # operacoes aritmeticas
            elif op == "SOMA":
                self.memoria[self.sp - 1] += self.memoria[self.sp]
                self.sp -= 1
                self.pc += 1

            elif op == "SUBT":
                self.memoria[self.sp - 1] -= self.memoria[self.sp]
                self.sp -= 1
                self.pc += 1

            elif op == "MULT":
                self.memoria[self.sp - 1] *= self.memoria[self.sp]
                self.sp -= 1
                self.pc += 1

            elif op == "DIVI":
                if self.memoria[self.sp] == 0:
                    raise ErroExecucao("Divisao por zero", self.pc)
                self.memoria[self.sp - 1] /= self.memoria[self.sp]
                self.sp -= 1
                self.pc += 1

            elif op == "INVE":
                self.memoria[self.sp] = -self.memoria[self.sp]
                self.pc += 1

            # comparacoes relacionais (1 = verdadeiro, 0 = falso)
            elif op == "CPME":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] < self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            elif op == "CPMA":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] > self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            elif op == "CPIG":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] == self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            elif op == "CDES":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] != self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            elif op == "CPMI":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] <= self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            elif op == "CPAI":
                self.memoria[self.sp - 1] = 1.0 if self.memoria[self.sp - 1] >= self.memoria[self.sp] else 0.0
                self.sp -= 1
                self.pc += 1

            # desvios
            elif op == "DSVI":
                self.pc = int(arg)

            elif op == "DSVF":
                cond = self.memoria[self.sp]
                self.sp -= 1
                if cond == 0.0:
                    self.pc = int(arg)
                else:
                    self.pc += 1

            # leitura e impressao
            elif op == "LEIT":
                self.sp += 1
                if fila_entradas is not None:
                    val = float(fila_entradas.pop(0))
                else:
                    val = float(input("Digite um valor: "))
                self.memoria[self.sp] = val
                self.pc += 1

            elif op == "IMPR":
                val = self.memoria[self.sp]
                self.saidas.append(val)
                print(int(val) if val.is_integer() else val)
                self.sp -= 1
                self.pc += 1

            else:
                raise ErroExecucao(f"Instrucao desconhecida '{op}'", self.pc)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 -m parte2_maquina.maquina <codigo_objeto.txt>")
        sys.exit(1)

    caminho = sys.argv[1]
    if not os.path.exists(caminho):
        print(f"Erro: arquivo '{caminho}' nao encontrado.", file=sys.stderr)
        sys.exit(1)

    try:
        vm = MaquinaHipotetica()
        vm.carregar_arquivo(caminho)
        vm.executar()
    except (ErroExecucao, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExecucao interrompida.")
        sys.exit(0)
