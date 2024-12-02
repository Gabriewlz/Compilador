let junk;
let instrucoes = {
  "LDC": (k) => {   /* Load Constant */
    stackPointer = stackPointer + 1                                               /* Incrementa o ponteiro de pilha (proxima posição de memoria) */
    memoria[stackPointer] = k                                                     /* Insere a constante na pilha recebida como parametro (k) */
  },
  "LDV": (n) => {   /* Load Value */
    stackPointer = stackPointer + 1                                               /* Incrementa o ponteiro da pilha (proxima posição de memória) */
    memoria[stackPointer] = memoria[n]                                            /* Insere o valor recebido (parametro n) na pilha */
  },
  "ADD": () => {    /* Somar */
    memoria[stackPointer - 1] = memoria[stackPointer - 1] + memoria[stackPointer] /* Soma os dois valores superiores apontados pelo stackPointer e armazena na posicao stackPointer-1 */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementra o ponteiro de pilha */
  },
  "SUB": () => {    /* Subtrair */
    memoria[stackPointer - 1] = memoria[stackPointer - 1] - memoria[stackPointer] /* Subtrai (PILHA[stackPointer-1] - PILHA[stackPointer]) os dois valores superiores apontados pelo stackPointer e armazena na posicao stackPointer-1 */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementra o ponteiro de pilha */
  },
  "MULT": () => {   /* Multiplicar */
    memoria[stackPointer - 1] = memoria[stackPointer - 1] * memoria[stackPointer] /* Multiplica os dois valores superiores apontados pelo stackPointer e armazena na posicao stackPointer-1 */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementra o ponteiro de pilha */
  },
  "DIVI": () => {   /* Dividir */
    memoria[stackPointer - 1] = Math.trunc(memoria[stackPointer - 1] / memoria[stackPointer]) /* Divide (PILHA[stackPointer-1] / PILHA[stackPointer]) os dois valores superiores apontados pelo stackPointer e armazena na posicao stackPointer-1 */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementra o ponteiro de pilha */
  },
  "INV": () => {  /* Inverter Sinal */
    memoria[stackPointer] = -memoria[stackPointer]                                /* Inverte o sinal do numero que esta no topo da pilha */
  },
  "AND": () => {  /* Operação Lógica AND - Conjunção */
    if (memoria[stackPointer - 1] == 1 && memoria[stackPointer] == 1) {           /* Se os dois números superiores da pilha forem iguais a 1, salva na posição stackPointer-1 o resultado 1 da opecação lógica AND */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posicao stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "OR": () => {  /* Operação Lógica OR - Disjunção */
    if (memoria[stackPointer - 1] == 1 || memoria[stackPointer] == 1) {           /* Se o primeiro ou o segundo elementos da pilha forem iguais a 1, salva na posicao stackPointer-1 o resultado 1 da operação lógica OR */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "NEG": () => {  /* Operação Lógica NOT - Negação */
    memoria[stackPointer] = 1 - memoria[stackPointer]                             /* Aplica operação lógica NOT na posição stackPointer e salva nesse mesmo lugar o resultado obtido */
  },
  "CME": () => {  /* Compara Menor */
    if (memoria[stackPointer - 1] < memoria[stackPointer]) {                      /* Se o numero na posição stackPointer-1 for MENOR do que o numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "CMA": () => {  /* Compara Maior */
    if (memoria[stackPointer - 1] > memoria[stackPointer]) {                      /* Se o numero na posição stackPointer-1 for MAIOR do que o numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "CEQ": () => {  /* Compara Igual (EQ = Equivalente) */
    if (memoria[stackPointer - 1] == memoria[stackPointer]) {                     /* Se o numero na posição stackPointer-1 for IGUAL ao numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "CDIF": () => { /* Compara Desigual (DIF = Diferente) */
    if (memoria[stackPointer - 1] != memoria[stackPointer]) {                     /* Se o numero na posição stackPointer-1 for DIFERENTE ao numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "CMEQ": () => { /* Compara Menor ou Igual (ME = Menor || Q = Equivalente ) */
    if (memoria[stackPointer - 1] <= memoria[stackPointer]) {                     /* Se o numero na posição stackPointer-1 for MENOR OU IGUAL ao numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "CMAQ": () => { /* Compara Maior ou Igual (MA = Maior || Q = Equivalente ) */
    if (memoria[stackPointer - 1] >= memoria[stackPointer]) {                     /* Se o numero na posição stackPointer-1 for MAIOR OU IGUAL ao numero na posição stackPointer, salva o valor 1 na posição stackPointer-1 */
      memoria[stackPointer - 1] = 1
    }
    else {                                                                        /* Armazena o valor 0 na posição stackPointer-1 caso contrário */
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "START": () => {/* Iniciar programa Principal */
    stackPointer = -1;                                                            /* O inicio do programa acontece quando o stack pointer ainda não aponta para uma região válida de memória */
  },
  "HLT": () => {  /* Parar Execução (HLT = HALT) */
    /* Parar a execução da MVD */
  },
  "STR": (n) => { /* Armazenar Valor região de memória de posição "n" (STR = Store) */
    memoria[n] = memoria[stackPointer]                                           /* Armazena o valor apontado por stackPointer na posição n da memoria de dados */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                              /* Decrementa o stackPointer */
  },
  "JMP": (t) => { /* Desviar PC para "t" */
    pc = t                                                                       /* Salva o endereço "t" como proxima instrução (PC) */
  },
  "JMPF": (t) => { /* Desviar PC para "t" se FALSO */
    if (memoria[stackPointer] == 0) {                                            /* Se o valor apontado por stackPointer foi igual a 0 desvia */
      pc = t                                                                     /* Salva o endereço "t" como proxima instrução (PC) */
    }
    else {
      pc = pc                                                                    /* Caso não atenda a condição aponta para proxima instrução e NAO DESVIA */
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                              /* Decrementa o stackPointer */
  },
  "NULL": () => { /* Operação NULA */
    return;
  },
  "RD": (value) => {   /* Entrada de dados pelo usuário (RD = read) */
    stackPointer = stackPointer + 1                                              /* Incrementa o stackPointer */
    memoria[stackPointer] = value                                                /* Salva o valor lido no INPUT do FRONT END */
  },
  "PRN": () => {  /* Operação PRINT */
    let out = '';                                 /* Recupera o elemeto que recebra o valor */
    out += memoria[stackPointer];                                          /* Escreve o valor no elemento HTML */
    out += "\r\n";
    document.getElementById("output").value += out
    document.getElementById("output").scrollTop = out.scrollHeight;                                            /* "Anda" automaticamente com o scroll */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                              /* Decrementa o stackPointer */
  },
  "ALLOC": (m, n) => {  /* Alocar Memória de tamanho 'n' */
    for (let k = 0; k < n; k++) {                                                                            /* Realiza o processo de ALLOC "n" VEZES */
      stackPointer = stackPointer + 1                                            /* Incrementa o stackPointer */
      memoria[stackPointer] = memoria[m + k]
    }
  },
  "DALLOC": (m, n) => { /* Desalocar Memória de tamanho 'n' */
    for (let k = n - 1; k >= 0; k--) {                                                                            /* Realiza o processo de DESALOCAR "n" VEZES */
      memoria[m + k] = memoria[stackPointer]
      junk = memoria.pop()
      stackPointer = stackPointer - 1                                            /* Decrementa o stackPointer */
    }
  },
  "CALL": (t, l) => {  /* Chamar uma Rotina */
    stackPointer = stackPointer + 1                                              /* Incrementa o stackPointer */
    memoria[stackPointer] = pc + 1                                              /* Salva o PC na pilha de memoria */
    pc = l                                                                     /* Define o procedimento como proxima instrução a ser executada */
  },
  "RETURN": () => { /* Retornar de uma Rotina */
    pc = memoria[stackPointer] - 1                                                     /* Recupera o valor de PC a partir do stackPointer */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */
  },
  "RETURNF": (m, n) => { /* Retornar de uma Rotina */
    /* Salva o topo da pilha (retorno de função) */
    topoPilha = memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1

    /* DALLOC */
    for (let k = n - 1; k >= 0; k--) {                                                                            /* Realiza o processo de DESALOCAR "n" VEZES */
      memoria[m + k] = memoria[stackPointer]
      junk = memoria.pop()
      stackPointer = stackPointer - 1                                            /* Decrementa o stackPointer */
    }

    /* RETURN */
    pc = memoria[stackPointer] - 1                                                    /* Recupera o valor de PC a partir do stackPointer */
    junk = memoria.pop()
    stackPointer = stackPointer - 1                                               /* Decrementa o stackPointer */

    /* Restaura o topo na pilha */
    stackPointer = stackPointer + 1
    memoria[stackPointer] = topoPilha
  },
};