/* Variáveis Globais da VM */
let codigo = [];    /* Variavel onde em cada posicao representa uma linha do codigo */
let tabela = {};    /* Tabela labels x linha do codigo, utilizada para jumps */
let breakpoints = {};

/* Render Code Window ->> Handler ativado quando importar o código OBJ/TXT */
function openFile() {
  var input = document.createElement('input');
  input.type = 'file';

  input.onchange = e => {
    // getting a hold of the file reference
    var file = e.target.files[0];

    // setting up the reader
    var reader = new FileReader();
    reader.readAsText(file, 'UTF-8');

    // here we tell the reader what to do when it's done reading...
    reader.onload = readerEvent => {
      var content = readerEvent.target.result; // this is the content!
      montarTexto(content);
    }
  }
  input.click();
}

function montarTexto(code)                          /* Recebe o conteudo do arquivo (parametro code) e o trata nessa arrow function (Callback) */ {
  const lines = code.split("\n");                   /* Quebra o conteudo do arquivo em linhas separadas a partir do \n */
  div = document.querySelector(".code-window");     /* Instanciacao do objeto que recebera o conteudo do arquivo - div onde irá aparecer o codigo bruto */
  div.innerHTML = "";                               /* Limpando o conteudo do objeto antes de carregar o codigo nesse objeto */
  ol = document.createElement("ol")                 /* Cria uma lista ordenada (ol) para armazenar cada linha do código */
  ol.classList.add("code-list");                    /* Adiciona uma classe no objeto HTML para o funcionamento do CSS */
  div.appendChild(ol)                               /* Adiciona a lista ordenada na div para exibir o codigo obj */
  let numLinha = 1                                  /* Inicia contagem da linha de texto como 1 */
  lines.forEach((line, index, array) =>             /* Para cada linha do codigo */ {
    let clickou = false;

    /* Cria o dicionário de Labels */
    if (line.includes('NULL'))                      /* Se existe o parametro NULL, eh label */ {
      tabela[line.split(' ')[0]] = numLinha - 1;    /* Salva o numero da linha - 1 na tabela (-1 para executar a proxima instrução)  */
    }

    /*
     * Render code
     * Adicionando elemetos HTML para estetica e
     * renderizaçao do codigo
    **/
    const li = document.createElement("li");        /* Instanciando um item para ser inserido na lista de itens */
    li.setAttribute("id", "line-" + index);

    /* Cria uma div para cada linha (cada uma dessas divs é composta por uma região cinza - esquerda - e uma região branca - direita) */
    const divBreak = document.createElement("div")  /* Cria a barra lateral esquerda para o botão de breakpoint*/
    divBreak.classList.add("break-div")             /* Adiciona uma classe ao CSS para modificar o style do breakpoint */

    const divNumber = document.createElement("div") /* Cria a barra lateral esquerda para exibir o número da linha */
    divNumber.classList.add("number-div")           /* Adiciona uma classe ao CSS para modificar o style da barra criada acima */

    const divLine = document.createElement("div")   /* Cria a linha que sera exibido o código */
    divLine.classList.add("line-div")               /* Adiciona uma classe ao CSS para modificar o style de onde irá ficar o texto */

    /*
     * Escrevedo o botão, número da linha e o conteudo de cada uma delas (codigo)
    **/

    /* BOTÃO */
    const breakButton = document.createElement("button");
    breakButton.setAttribute("id", "break-" + index);
    breakButton.innerHTML = "<i class='fas fa-circle select-trans'></i>";
    breakButton.addEventListener("click", function () {
      numLinha = this.id.split("-")[1];
      if (clickou === false) {
        /* insere tabela o numero da linha */
        breakpoints[numLinha] = true;
        breakButton.innerHTML = "<i class='fas fa-circle break-div'></i>"
        clickou = true;
      }
      else {
        /* remove tabela  */
        breakpoints[numLinha] = false;
        breakButton.innerHTML = "<i class='fas fa-circle select-trans'></i>";
        clickou = false;
      }
    });
    divBreak.appendChild(breakButton);

    /* NUMERO LINHA */
    const numText = document.createTextNode(numLinha) /* Cria um const (variavel) para armazenar o numero da linha */
    divNumber.appendChild(numText)                    /* Escreve na divNumber o numero da linha */

    /* CODIGO */
    const lineText = document.createTextNode(line)    /* Cria um const (variavel) para armazenar o código (linha a linha) */
    divLine.appendChild(lineText)                     /* Escreve na divLine o código */

    breakpoints[numLinha - 1] = false;                  /* Armazena onde tem breakpoints */

    numLinha++;                                       /* Incrementa o número da linha */

    li.appendChild(divBreak);
    li.appendChild(divNumber);                        /* Insere a div de número de linha na lista de itens */
    li.appendChild(divLine);                          /* Insere a div de código na lista de itens */

    ol.appendChild(li);                               /* Insere a linha da lista de itens na lista ordenada (que contera o codigo inteiro) */

    codigo.push(line);                                /* Armazenando o conteudo do arquivo em nossa variavel */
  });
}
/* Aqui finaliza o import do código texto */