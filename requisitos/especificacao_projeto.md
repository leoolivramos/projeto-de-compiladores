# Requisitos do Trabalho — Compiladores (UFMT)

Este documento reúne a especificação do trabalho prático da disciplina de Compiladores, filtrado para o meu tema sorteado na planilha da turma.

- **Linguagem atribuída**: PHP (versão simplificada)
- **Técnica do analisador sintático**: Descendente Não Recursivo (LL(1) tabelado com pilha)
- **Modalidade**: Individual, com apresentação prática ao final do semestre.

---

## 1. Escopo Geral

O trabalho está dividido em dois projetos independentes que se comunicam via arquivo de texto:

1. **Parte 1 (Compilador + Tradutor)**: Lê um código-fonte em PHP simplificado e gera um arquivo de texto com instruções da linguagem de máquina hipotética.
2. **Parte 2 (Máquina Hipotética / Interpretador)**: Lê o arquivo gerado na Parte 1 e executa as instruções em uma máquina virtual de pilha vista em aula.

---

## 2. Requisitos da Parte 1 — Compilador

O compilador deve cobrir todo o pipeline clássico de compilação sem depender de bibliotecas geradoras de analisadores (como Lex, Flex, Yacc, Bison ou expressões regulares prontas para parsing).

### 2.1. Analisador Léxico
- Implementação manual via Autômato Finito Determinístico (AFD).
- Reconhecimento dos tokens da linguagem: tags `<?php` e `?>`, palavras reservadas (`if`, `else`, `while`, `echo`, `PHP_EOL`, `floatval`, `readline`), variáveis iniciadas por `$` (`$cont`, `$a`, etc.), constantes numéricas (inteiros e floats), operadores relacionais (`==`, `!=`, `>=`, `<=`, `>`, `<`), operadores aritméticos (`+`, `-`, `*`, `/`) e pontuação (`;`, `,`, `(`, `)`, `{`, `}`, `.`, `=`).
- Controle de linha e coluna para apontar erros léxicos no código de entrada.

### 2.2. Analisador Sintático (Descendente Não Recursivo)
- Construção de um autômato com pilha explícita orientado por tabela de análise preditiva $M[\text{Não-Terminal}, \text{Terminal}]$.
- Como a gramática original de PHP apresenta conflito $\text{FIRST}/\text{FIRST}$ entre declaração de variáveis (`$id;` ou `$id,$id;`) e atribuição (`$id = ...`), a gramática foi fatorada à esquerda na regra de comandos para torná-la estritamente LL(1).
- Tratamento de erros sintáticos acusando o token inesperado, a linha e a coluna.

### 2.3. Analisador Semântico e Tabela de Símbolos
- Tabela de símbolos para registrar o identificador, tipo e endereço de memória de cada variável.
- Validação de declaração prévia: emitir erro se uma variável for usada sem ter sido declarada.
- Validação de duplicidade: emitir erro se uma variável for declarada mais de uma vez no mesmo escopo.
- Mapeamento sequencial de memória ($0, 1, 2, \dots$) para alocação na máquina de pilha.

### 2.4. Tradutor para Código Objeto
- Geração das instruções equivalentes da máquina hipotética (`INPP`, `ALME`, `CRCT`, `CRVL`, `ARMZ`, `SOMA`, `SUBT`, `MULT`, `DIVI`, `CPMA`, `CPME`, `DSVF`, `DSVI`, `LEIT`, `IMPR`, `PARA`).
- Resolução de desvios (*backpatching*) para preencher os endereços de pulo em estruturas `if/else` e laços `while`.
- Gravação das instruções geradas em um arquivo de texto de saída.

---

## 3. Requisitos da Parte 2 — Máquina Hipotética

A máquina hipotética funciona como um interpretador baseado em pilha de execução:

- **Memória de instruções**: Vetor que armazena as instruções carregadas do arquivo objeto gerado pelo compilador.
- **Memória de dados**: Pilha linear indexada por um registrador de topo ($SP$).
- **Apontador de programa ($PC$)**: Indica a instrução atual.
- **Ciclo de execução**: Busca a instrução em $PC$, decodifica mnemônico e argumento, atualiza a pilha/memória e avança $PC$ (ou desvia nos casos de `DSVI`/`DSVF`).
- **Comandos suportados**:
  - `INPP`: inicia a execução e reseta apontadores.
  - `PARA`: encerra o programa.
  - `ALME n`: reserva $n$ posições na pilha.
  - `CRCT k`: coloca a constante numérica $k$ no topo da pilha.
  - `CRVL p`: copia o valor do endereço de memória $p$ para o topo.
  - `ARMZ p`: retira o topo da pilha e salva no endereço $p$.
  - Operações aritméticas e relacionais (`SOMA`, `SUBT`, `MULT`, `DIVI`, `CPMA`, `CPME`, `CPIG`, etc.).
  - Controle de fluxo (`DSVI`, `DSVF`).
  - Entrada e saída (`LEIT` para ler do teclado e `IMPR` para imprimir no terminal).

---

## 4. Regras de Entrega e Apresentação

1. O projeto deve conter um `README.md` com instruções detalhadas de como compilar e como executar os códigos.
2. Não é permitido o uso de bibliotecas de terceiros para parsing.
3. É permitido o uso de IA, desde que declarado de forma explícita na documentação qual ferramenta foi utilizada e como auxiliou no desenvolvimento.
4. O projeto será avaliado e apresentado individualmente no final do semestre.
