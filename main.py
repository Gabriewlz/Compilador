import sys
from Lexical.Lexical import Lexical
from Token.Token import Token, TokenType
from SymbolTable import SymbolTable


# Variáveis globais
lexer = Lexical("code.txt")
Token = lexer.get_next_token()
symbol_table = SymbolTable()  # Instancia a tabela de símbolos
label = 1
memory_position = 1



# Arquivo de saída para resultados
output_file = open("output.txt", "w")
assembly_file = open("assembly.txt", "w")


def get_next_token():
    """
    Atualiza o Token atual com o próximo da análise léxica.
    """
    global Token
    Token = lexer.get_next_token()


def gera(label, instruction, attribute1, attribute2):
    """
    Gera código de saída para o arquivo assembly, adicionando 'L' apenas a rótulos e removendo espaços extras.
    """
    with open("assembly.txt", "a") as assembly_file:  # Abre em modo append
        # Formatação do label, adicionando 'L' apenas se for um número
        formatted_label = f"L{label.strip()}" if label.strip().isdigit() else label.strip()
        
        # Para qualquer instrução que tenha um número (como 'CALL', 'JMP', 'JMPF'), 
        # garante que 'L' seja adicionado ao número.
        if instruction in ["CALL", "JMP", "JMPF"] and attribute1.strip().isdigit():  # Verifica se é 'CALL', 'JMP', ou 'JMPF' e se o atributo é numérico
            formatted_attr1 = f"L{attribute1.strip()}"
        else:
            formatted_attr1 = attribute1.strip()
        
        # Formatação do attribute2
        formatted_attr2 = attribute2.strip() if attribute2.strip() else ""  # Garante que não haja espaços extras
        
        # Formando a linha com 2 espaços entre o 'CALL' e o rótulo 'L<num>'
        if instruction == "CALL":
            line = f"{formatted_label}{instruction}  {formatted_attr1} {formatted_attr2}"  # Sem espaço antes de CALL, com 2 espaços entre CALL e L<num>
        else:
            line = f"{formatted_label} {instruction} {formatted_attr1} {formatted_attr2}".strip()
        
        # Escrevendo a linha no arquivo
        assembly_file.write(line + "\n")



def gera_expressao(postfix):
    """
    Gera código para uma expressão em notação pós-fixada.
    """
    for elem in postfix:
        if elem == "nao":
            gera("", "NEG", "", "")
        elif elem == "e":
            gera("", "AND", "", "")
        elif elem == "ou":
            gera("", "OR", "", "")
        elif elem == "+":
            gera("", "ADD", "", "")
        elif elem == "-":
            gera("", "SUB", "", "")
        elif elem == "*":
            gera("", "MULT", "", "")
        elif elem == "div":
            gera("", "DIVI", "", "")  # Corrigido para 'DIVI' conforme instruções
        elif elem == "=":
            gera("", "CEQ", "", "")
        elif elem == "!=":
            gera("", "CDIF", "", "")
        elif elem == "<":
            gera("", "CME", "", "")
        elif elem == ">":
            gera("", "CMA", "", "")
        elif elem == "<=":
            gera("", "CMEQ", "", "")
        elif elem == ">=":
            gera("", "CMAQ", "", "")
        elif elem == "-u":
            gera("", "INV", "", "")  # Inversão de sinal
        elif elem == "verdadeiro":
            gera("", "LDC", "1", "")  # Constante '1' para verdadeiro
        elif elem == "falso":
            gera("", "LDC", "0", "")  # Constante '0' para falso
        elif symbol_table.contains(elem):
            symbol_type = symbol_table.get_type(elem)
            if symbol_type in ["funcao inteiro", "funcao booleano"]:
                gera("", "LDV", "0", "")
            else:
                gera("", "LDV", symbol_table.get_address(elem), "")
        else:
            gera("", "LDC", elem, "")  # Constante genérica


def infer_type(postfix_expr):
    """
    Infere o tipo da expressão pós-fixada.
    """
    type_stack = []

    def is_operator(Token):
        return Token in ["+", "-", "*", "div", "=", "!=", "<", ">", "<=", ">=", "e", "ou", "nao", "+u", "-u"]

    def is_number(Token):
        return Token.isdigit()

    for Token in postfix_expr:
        if not is_operator(Token):
            if is_number(Token):
                type_stack.append("inteiro")
            elif Token in ["verdadeiro", "falso"]:
                type_stack.append("booleano")
            else:
                token_type = symbol_table.get_type(Token)
                if token_type in ["inteiro", "booleano"]:
                    type_stack.append(token_type)
                elif token_type == "funcao inteiro":
                    type_stack.append("inteiro")
                elif token_type == "funcao booleano":
                    type_stack.append("booleano")
                else:
                    raise RuntimeError(f"Tipo inválido para o Token '{Token}'. Linha: {lexer.get_current_line()}")
        else:
            if Token in ["+", "-", "*", "div"]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "inteiro" or left != "inteiro":
                    raise RuntimeError(f"Operadores aritméticos requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("inteiro")
            elif Token in ["+u", "-u"]:
                if not type_stack:
                    raise RuntimeError("Operandos insuficientes.")
                operand = type_stack.pop()
                if operand != "inteiro":
                    raise RuntimeError(f"Operadores unários requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("inteiro")
            elif Token in ["=", "!="]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != left:
                    raise RuntimeError(f"Operadores de igualdade requerem operandos do mesmo tipo. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token in ["<", ">", "<=", ">="]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "inteiro" or left != "inteiro":
                    raise RuntimeError(f"Operadores relacionais requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token in ["e", "ou"]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "booleano" or left != "booleano":
                    raise RuntimeError(f"Operadores lógicos requerem booleanos. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token == "nao":
                if not type_stack:
                    raise RuntimeError("Operandos insuficientes.")
                operand = type_stack.pop()
                if operand != "booleano":
                    raise RuntimeError(f"Operador 'nao' requer booleano. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")

    if len(type_stack) != 1:
        raise RuntimeError(f"Erro: expressão malformada. Linha: {lexer.get_current_line()}")

    return type_stack[0]


'''
                  SINTATICO
'''


def get_next_token():
    """
    Atualiza o Token atual com o próximo da análise léxica.
    """
    global Token
    Token = lexer.get_next_token()

    # Adicione este print para depurar
    # print(f"Token retornado: {Token} (tipo: {type(Token)})")

def analise_expressao_simples(infix_expression):
    """
    Analisa uma expressão simples e atualiza o vetor de expressão infix.
    """
    global Token  # Certifique-se de que a variável global `Token` é usada
    if Token.token_type in ["smais", "smenos"]:
        # Adiciona operador unário ao vetor de expressão infix
        infix_expression.append("+u" if Token.token_type == TokenType.SMAIS else "-u")
        get_next_token()
    term_analysis(infix_expression)
    while Token.token_type in ["smais", "smenos", "sou"]:
        # Adiciona operador ao vetor de expressão infix
        infix_expression.append(Token.lexeme)
        get_next_token()
        term_analysis(infix_expression)


def function_call_analysis():
    """
    Analisa a chamada de uma função e gera o código correspondente.
    """
    address = symbol_table.get_address(Token.lexeme)
    gera("", "CALL", address, "")
    get_next_token()


def procedure_call_analysis(address):
    """
    Analisa a chamada de um procedimento e gera o código correspondente.
    """
    gera("", "CALL", address, "")


def atrib_analysis(expected_type):
    """
    Analisa uma atribuição, verifica tipos e gera o código correspondente.
    """
    get_next_token()
    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)
    expression_type = infer_type(postfix)

    if expression_type != expected_type:
        raise RuntimeError(f"Atribuição de tipos diferentes na linha: {lexer.get_current_line()}")

    gera_expressao(postfix)


def factor_analysis(infix_expression):
    """
    Analisa um fator e atualiza o vetor de expressão infix.
    """
    global Token  # Certifique-se de que está usando a variável global 'Token'

    if Token.token_type == "sidentificador":
        if symbol_table.contains(Token.lexeme):
            if symbol_table.get_type(Token.lexeme) in ["funcao inteiro", "funcao booleano"]:
                infix_expression.append(Token.lexeme)
                function_call_analysis()
            elif not symbol_table.is_procedure_or_program(Token.lexeme):
                infix_expression.append(Token.lexeme)
                get_next_token()
            else:
                raise RuntimeError(f"Procedimento usado indevidamente na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Variável não declarada na linha: {lexer.get_current_line()}")
    elif Token.token_type == "snumero":
        infix_expression.append(Token.lexeme)
        get_next_token()
    elif Token.token_type == "snao":
        get_next_token()
        infix_expression.append("nao")
        factor_analysis(infix_expression)
    elif Token.token_type == "sabre_parenteses":
        get_next_token()
        infix_expression.append("(")
        expression_analysis(infix_expression)
        if Token.token_type == "sfecha_parenteses":
            infix_expression.append(")")
            get_next_token()
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
    elif Token.token_type in ["sverdadeiro", "sfalso"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador', 'numero', 'nao' ou '(' na linha: {lexer.get_current_line()}")



def term_analysis(infix_expression):
    """
    Analisa um termo e atualiza o vetor de expressão infix.
    """
    global Token
    factor_analysis(infix_expression)
    while Token.token_type in ["smult", "sdiv", "se"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
        factor_analysis(infix_expression)


def expression_analysis(infix_expression):
    """
    Analisa uma expressão e atualiza o vetor de expressão infix.
    """
    global Token
    analise_expressao_simples(infix_expression)
    if Token.token_type in ["smaior", "smaiorig", "sig", "smenor", "smenorig", "sdif"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
        analise_expressao_simples(infix_expression)


def analise_leia():
    """
    Analisa o comando de leitura (read) e gera o código correspondente.
    """
    global Token
    get_next_token()
    if Token.token_type == "sabre_parenteses":
        get_next_token()
        if Token.token_type == "sidentificador":
            if symbol_table.contains(Token.lexeme) and symbol_table.get_type(Token.lexeme) == "inteiro":
                # Gera código para leitura da variável
                gera("", "RD", "", "")
                gera("", "STR", symbol_table.get_address(Token.lexeme), "")
                get_next_token()
                if Token.token_type == "sfecha_parenteses":
                    get_next_token()
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Variável não declarada ou tipo incompatível na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se '(' na linha: {lexer.get_current_line()}")


def analise_escreva():
    """
    Analisa o comando de escrita (write) e gera o código correspondente.
    """
    global Token
    get_next_token()
    if Token.token_type == "sabre_parenteses":
        get_next_token()
        if Token.token_type == "sidentificador":
            if symbol_table.contains(Token.lexeme) and symbol_table.get_type(Token.lexeme) == "inteiro":
                # Gera código para escrita da variável
                gera("", "LDV", symbol_table.get_address(Token.lexeme), "")
                gera("", "PRN", "", "")
                get_next_token()
                if Token.token_type == "sfecha_parenteses":
                    get_next_token()
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Variável não declarada ou tipo incompatível na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se '(' na linha: {lexer.get_current_line()}")


def atrib_chproc():
    """
    Analisa uma atribuição ou chamada de procedimento e gera o código correspondente.
    """
    global Token
    if symbol_table.contains(Token.lexeme):
        var_type = symbol_table.get_type(Token.lexeme)
        address = symbol_table.get_address(Token.lexeme)
        flag = 0

        get_next_token()
        if var_type == "funcao inteiro":
            var_type = "inteiro"
            flag = 1
        elif var_type == "funcao booleano":
            var_type = "booleano"
            flag = 1

        if Token.token_type == "satribuicao" and var_type in ["inteiro", "booleano", "funcao inteiro", "funcao booleano"]:
            atrib_analysis(var_type)
            if var_type in ["inteiro", "booleano"]:
                if flag == 1:
                    gera("", "STR", "0", "")
                else:
                    gera("", "STR", address, "")
        elif var_type == "procedimento":
            procedure_call_analysis(address)
        else:
            raise RuntimeError(f"Tipo inválido na atribuição/chamada de procedimento na linha {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Variável não declarada na linha {lexer.get_current_line()}")


def analise_se():
    """
    Analisa a estrutura condicional (if-else) e gera o código correspondente.
    """
    global Token, label
    get_next_token()

    # Análise da expressão condicional
    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)

    gera_expressao(postfix)

    expression_type = infer_type(postfix)
    if expression_type != "booleano":
        raise RuntimeError(f"Expressão inválida. Linha: {lexer.get_current_line()}")

    aux_label1 = label
    gera("", "JMPF", str(label), "")
    label += 1

    # Bloco 'entao'
    if Token.token_type == "sentao":
        get_next_token()
        comando_simples()

        if Token.token_type == "ssenao":
            aux_label2 = label
            gera("", "JMP", str(label), "")
            label += 1

            gera(str(aux_label1), "NULL", "", "")

            get_next_token()
            comando_simples()

            gera(str(aux_label2), "NULL", "", "")
        else:
            gera(str(aux_label1), "NULL", "", "")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'entao' na linha: {lexer.get_current_line()}")



def analise_enquanto():
    """
    Analisa a estrutura de repetição (while) e gera o código correspondente.
    """
    global Token, label
    get_next_token()

    aux_label1 = label
    gera(str(label), "NULL", "", "")
    label += 1

    # Análise da expressão condicional
    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)
    expression_type = infer_type(postfix)

    if expression_type != "booleano":
        raise RuntimeError(f"Expressão inválida. Linha: {lexer.get_current_line()}")

    gera_expressao(postfix)

    if Token.token_type == "sfaca":
        aux_label2 = label
        gera("", "JMPF", str(label), "")
        label += 1

        get_next_token()
        comando_simples()

        gera("", "JMP", str(aux_label1), "")
        gera(str(aux_label2), "NULL", "", "")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'faca' ou operador lógico na linha: {lexer.get_current_line()}")


def comando_simples():
    """
    Analisa um comando simples e direciona para a análise específica.
    """
    global Token
    if Token.token_type == "sidentificador":
        atrib_chproc()
    elif Token.token_type == "sse":
        analise_se()
    elif Token.token_type == "senquanto":
        analise_enquanto()
    elif Token.token_type == "sleia":
        analise_leia()
    elif Token.token_type == "sescreva":
        analise_escreva()
    else:
        analise_comando()


def analise_comando():
    """
    Analisa a estrutura de comandos compostos (início-fim).
    """
    global Token
    if Token.token_type == "sinicio":
        get_next_token()
        comando_simples()

        while Token.token_type != "sfim":
            if Token.token_type == "sponto_virgula":
                get_next_token()
                if Token.token_type != "sfim":
                    comando_simples()
            else:
                raise RuntimeError(f"Erro! ';' faltante na linha: {lexer.get_current_line()}")

        get_next_token()
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'inicio' ou ';' inadequado na linha: {lexer.get_current_line()}")


def analise_func():
    """
    Analisa uma declaração de função e gera o código correspondente.
    """
    global Token, label, memory_position
    get_next_token()

    if Token.token_type == "sidentificador":
        if not symbol_table.contains(Token.lexeme):
            symbol_table.push(Token.lexeme, "L", "function", str(label))

            # Gera a marcação da função
            gera(str(label), "NULL", "", "")
            label += 1

            get_next_token()
            if Token.token_type == "sdoispontos":
                get_next_token()
                if Token.token_type in ["sinteiro", "sbooleano"]:
                    symbol_table.assign_type_to_function(f"funcao {Token.lexeme}")
                    get_next_token()
                    if Token.token_type == "sponto_virgula":
                        analise_bloco()
                    else:
                        raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Tipo inválido na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Erro de Sintaxe! Espera-se ':' na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Função já declarada na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")

    # Gerenciar desalocação de memória
    count = symbol_table.cut_stack()
    if count > 0:
        dalloc_start_position = memory_position - count
        gera("", "DALLOC", str(dalloc_start_position), str(count))
        memory_position = dalloc_start_position

    gera("", "RETURN", "", "")


def analise_proc():
    """
    Analisa uma declaração de procedimento e gera o código correspondente.
    """
    global Token, label, memory_position
    get_next_token()

    if Token.token_type == "sidentificador":
        if not symbol_table.contains(Token.lexeme):
            symbol_table.push(Token.lexeme, "L", "procedimento", str(label))
            gera(str(label), "NULL", "", "")
            label += 1

            get_next_token()
            if Token.token_type == "sponto_virgula":
                analise_bloco()
            else:
                raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Procedimento já declarado na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")

    # Gerenciar desalocação de memória
    count = symbol_table.cut_stack()
    if count > 0:
        dalloc_start_position = memory_position - count
        gera("", "DALLOC", str(dalloc_start_position), str(count))
        memory_position = dalloc_start_position

    gera("", "RETURN", "", "")


def analise_subrotina():
    """
    Analisa declarações de sub-rotinas (procedimentos e funções).
    """
    global Token, label
    flag = 0
    aux_label = None

    if Token.token_type in ["sprocedimento", "sfuncao"]:
        aux_label = label
        gera("", "JMP", str(label), "")
        label += 1
        flag = 1

    while Token.token_type in ["sprocedimento", "sfuncao"]:
        if Token.token_type == "sprocedimento":
            analise_proc()
        else:
            analise_func()

        if Token.token_type == "sponto_virgula":
            get_next_token()
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")

    if flag == 1:
        gera(str(aux_label), "NULL", "", "")


def analise_tipo():
    """
    Analisa o tipo das variáveis declaradas e verifica sua validade.
    """
    if Token.token_type not in ["sinteiro", "sbooleano"]:
        raise RuntimeError(f"Erro de Sintaxe! Tipo inválido na linha: {lexer.get_current_line()}")
    else:
        symbol_table.assign_type_to_variables(Token.lexeme)
    get_next_token()


def analise_variaveis():
    """
    Analisa a declaração de variáveis, verifica duplicidade e aloca memória.
    """
    global memory_position
    count = 0
    while True:
        if Token.token_type == "sidentificador":
            if not symbol_table.contains_var(Token.lexeme):
                symbol_table.push(Token.lexeme, "", "var", str(memory_position + count))
                count += 1
                get_next_token()

                if Token.token_type in ["svirgula", "sdoispontos"]:
                    if Token.token_type == "svirgula":
                        get_next_token()
                        if Token.token_type == "sdoispontos":
                            raise RuntimeError(
                                f"Erro de Sintaxe! Padrão indevido na linha: {lexer.get_current_line()}"
                            )
                    elif Token.token_type == "sdoispontos":
                        break
                else:
                    raise RuntimeError(
                        f"Erro de Sintaxe! Esperava-se ',' ou ':' na linha: {lexer.get_current_line()}"
                    )
            else:
                raise RuntimeError(
                    f"Variável já declarada na linha: {lexer.get_current_line()}"
                )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Esperava-se 'identificador' na linha: {lexer.get_current_line()}"
            )

    gera("", "ALLOC", str(memory_position), str(count))
    memory_position += count
    get_next_token()
    analise_tipo()


def declaracao_variaveis():
    """
    Analisa a seção de declaração de variáveis.
    """
    if Token.token_type == "svar":
        get_next_token()
        if Token.token_type == "sidentificador":
            while Token.token_type == "sidentificador":
                # Analisa cada variável
                analise_variaveis()
                if Token.token_type == "sponto_virgula":
                    get_next_token()  # Avança o Token após o ponto e vírgula
                else:
                    raise RuntimeError(
                        f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}"
                    )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}"
            )


def analise_bloco():
    """
    Analisa um bloco completo, incluindo variáveis, sub-rotinas e comandos.
    """
    get_next_token()
    declaracao_variaveis()
    analise_subrotina()
    analise_comando()


def main():
    try:
        global Token  # Certifique-se de que a variável global Token está acessível

        # Verifica se o programa inicia com 'programa'
        if Token.token_type == "sprograma":
            get_next_token()
            if Token.token_type == "sidentificador":
                symbol_table.push(Token.lexeme, "", "programa", "")
                get_next_token()
                if Token.token_type == "sponto_virgula":
                    # Geração inicial de código
                    gera("", "START", "", "")
                    gera("", "ALLOC", "0", "1")

                    # Analisa o bloco principal do programa
                    analise_bloco()

                    if Token.token_type == "sponto":
                        # Realiza desalocação de memória ao final do programa
                        count = symbol_table.cut_stack()
                        dalloc_start_position = memory_position - count
                        gera("", "DALLOC", str(dalloc_start_position), str(count))

                        get_next_token()
                        if Token.token_type == "endfile":
                            print("Compilado com sucesso!")
                            with open("output.txt", "a") as output_file:
                                output_file.write("\nCompilado com sucesso!\n\n")

                            # Imprime a tabela de símbolos no console
                            symbol_table.print_stack()

                            # Gera código final de desalocação e halt
                            gera("", "DALLOC", "0", "1")
                            gera("", "HLT", "", "")
                        else:
                            raise RuntimeError(
                                f"Símbolos inválidos após o fim do programa na linha: {lexer.get_current_line()}"
                            )
                    else:
                        raise RuntimeError(
                            f"Espera-se '.' na linha: {lexer.get_current_line()}"
                        )
                else:
                    raise RuntimeError(
                        f"Espera-se ';' na linha: {lexer.get_current_line()}"
                    )
            else:
                raise RuntimeError(
                    f"Espera-se 'identificador' na linha: {lexer.get_current_line()}"
                )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Espera-se 'programa' na linha: {lexer.get_current_line()}"
            )

    except Exception as e:
        # Em caso de erro, exibe a mensagem e registra no arquivo de saída
        print(f"Erro: {e}")
        with open("output.txt", "w") as output_file:
            output_file.write(f"Linha: {lexer.get_current_line()}\nErro: {e}\n")
        
        # Limpa o conteúdo do arquivo assembly em caso de erro
        with open("assembly.txt", "w") as assembly_file:
            assembly_file.truncate()

    # Finaliza os arquivos ao encerrar
    finally:
        print("Execução finalizada")


# Executa o programa principal
if __name__ == "__main__":
    main()
