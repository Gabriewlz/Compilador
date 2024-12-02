/* Variáveis globais para manipulação de instruções */
let memoria = [];        /* Variavel que representa a regiao de memoria (memoria = M[]) */
let stackPointer = -1;   /* Ponteiro da região de STACK (stackPointer = s) */
let pc = 0;              /* Program Counter */
let pcAnterior = 0;
let debugFlag = 0;
let step = false;
let statusBreakpoint = 0
let dev = false

if (!dev) {
  console.log = () => { }
  console.table = () => { }
}


/**
 * Função executada para reiniciar a execucao da VM
 */
function reset() {
  window.location.reload(true);  /* Recarrega a página ao clicar no botão reset */
}

/**
 * Função executada quando clicar no botão PLAY
 */
async function rodarCodigo() {
  let stackWindow = document.getElementById("stack");  /* Obtem o objeto para escrever na GUI de stack */
  while (pc < codigo.length)                                   /* Para cada linha do codigo */ {
    let line = codigo[pc]
    let elementos = line.trim().split(" ")              /* Remove os espacos extras do fim e começo e quebra a linha a cada espaco armanzenando cada elemento na variavel elemento*/
    let funcao = elementos.shift()                      /* Recupera e remove o primeiro elemento da linha (instrução ou label) */
    let linhaAnterior = document.getElementById("line-" + pcAnterior);
    let linha = document.getElementById("line-" + pc)     /* Pega o objeto que representa a linha que esta sendo executada */
    pcAnterior = pc;

    if (debugFlag == 1)                                  /* Se a flag de debug for igual a 1, indica que o código esta sendo executado com a opção de debug */ {
      linhaAnterior.classList.remove("highlight");      /* Remove o highlight da linha */
      linha.classList.add("highlight");                 /* Aplica a classe highlight a linha que esta sendo executada */
      if (breakpoints[pc] == true)                       /* Se existir um breakpoint ativo */ {
        statusBreakpoint = 1;                            /* Ativa a flag para execução com breakpoint */
      }

      if (statusBreakpoint == 1)                         /* Caso a flag de breakpoint ainda estiver ativa, continua com o step */ {
        if (step == false)                               /* Após executar a instrução parada sai do while */ {
          return;
        }
        else {
          step = false;
        }
      }
    }

    elementos.forEach((e, index, arr) =>                /* Para cada elemento restante, ou seja, argumentos ou a instrução NULL */ {
      if (e.length != 0)                                /* Se não existirem argumentos */ {
        if (e.match(/^[0-9]+$/) == null) {              /* Se elemento nao for um numero (ou seja, um parametro), o armazaena na tabela pois eh um label */
          arr[index] = tabela[e];                       /* Armazena o Label na tabela */
        }
        else {
          arr[index] = +e;                              /* Caso for um número, converte o elemento de string para numero */
        }
      }
    })

    if (!(funcao in tabela))                            /* Se a função nao for label, ou seja, é uma instrução, executa a funcao passando os respectivos parametros */ {
      if (funcao === "RD")                               /* Se a função lida for READ */ {
        /* Garante que o popup só pegara numeros inteiros */
        do {
          var answer = prompt("Digite o valor de INPUT (Numeros - true/false): ")

          sleep = (ms) => {
            return new Promise(resolve => setTimeout(resolve, ms));
          }
          await sleep(0.5)

          if (answer === "true")
            answer = parseInt("1")
          else if (answer === "false")
            answer = parseInt("0")
          else
            answer = parseInt(answer)  /* Abre um pop up para inserir o dado */

        } while (isNaN(answer));                                        /* Garante que o dado sempre será um numero inteiro */

        if (!isNaN(answer))                                /* Se o dado inserido não for vazio (ou seja, inseriu algo valido *****TRATAR NUMEROS*****) */ {
          instrucoes["RD"](+answer)                     /* Executa a função de READ */
        }
      }
      else {
        if (funcao === "HLT")                             /* Termina a execução do programa ao encontrar um HLT, saí do while */
          return
        else {

          instrucoes[funcao](...elementos)
        }             /* Caso a função NÃO FOR READ, executa ela normal passando os argumentos */
      }
    }
    pc++;                                               /* Incrementa o valor de PC a cada instrução */

    /* Atualiza a janela de stack -> Lado direito da GUI */
    stackWindow.value += "PC: " + pc;
    stackWindow.value += "\r\n";
    stackWindow.value += "SP: " + stackPointer;
    stackWindow.value += "\r\n";
    stackWindow.value += "FUNCAO: " + funcao + "\r\n";
    stackWindow.value += "MEMORY: " + memoria;
    stackWindow.value += "\r\n";
    stackWindow.value += "---------------------------";
    stackWindow.value += "\r\n";
    stackWindow.scrollTop = stackWindow.scrollHeight;
  }
}

function ativarDebug()  /* Acionada quando clicar no botão de debug */ {
  debugFlag = 1;  /* Quando executar o código com a opção debug, seta a variavel global para 1 */
  rodarCodigo();  /* E roda o código */
}

function setStep()     /* Acionada quando clicar no botão de step */ {
  step = true;    /* Avisa que o step esta ativo */
  rodarCodigo();  /* Executa o código */
}

function setContinue() /* Acionada quando clicar no botão de continue */ {
  step = false;           /* Desativa o modo step */
  statusBreakpoint = 0;   /* Desativa o modo breakpoint */
  rodarCodigo();          /* E roda o código */
}