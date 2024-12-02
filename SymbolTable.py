class SymbolInfo:
    def __init__(self, name, scope_level, type_, memory_address):
        self.name = name
        self.scope_level = scope_level
        self.type = type_
        self.memory_address = memory_address


class Node:
    def __init__(self, symbol_info):
        self.symbol_info = symbol_info
        self.next = None


class SymbolTable:
    def __init__(self):
        self.top = None

    def push(self, name, scope_level, type_, memory_address):
        """
        Adiciona um novo símbolo à pilha da tabela de símbolos.
        """
        symbol_info = SymbolInfo(name, scope_level, type_, memory_address)
        new_node = Node(symbol_info)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """
        Remove o símbolo do topo da pilha.
        """
        if self.top is not None:
            temp = self.top
            self.top = self.top.next
            del temp  # Libera o nó removido da memória

    def is_empty(self):
        """
        Verifica se a tabela de símbolos está vazia.
        """
        return self.top is None

    def peek(self):
        """
        Retorna o símbolo do topo da pilha sem removê-lo.
        """
        if self.top is not None:
            return self.top.symbol_info
        return None

    def contains_var(self, name):
        """
        Verifica se uma variável foi declarada no escopo atual (até encontrar "L").
        """
        aux = self.top
        while aux is not None:
            if aux.symbol_info and aux.symbol_info.scope_level == "L":
                if aux.symbol_info.name == name:
                    return True
                break
            if aux.symbol_info and aux.symbol_info.name == name:
                return True
            aux = aux.next
        return False

    def contains(self, name):
        """
        Verifica se o identificador existe na tabela de símbolos.
        """
        aux = self.top
        while aux is not None and aux.symbol_info is not None:
            if aux.symbol_info.name == name:
                return True
            aux = aux.next
        return False

    def cut_stack(self):
        """
        Remove todos os símbolos até encontrar "L" no escopo.
        """
        count = 0
        while self.top is not None and self.top.symbol_info.scope_level != "L":
            if self.top.symbol_info.type in ["inteiro", "booleano"]:
                count += 1
            self.pop()
        if self.top is not None:
            self.top.symbol_info.scope_level = ""
        return count

    def assign_type_to_variables(self, new_type):
        """
        Atribui um tipo às variáveis no escopo atual.
        """
        current = self.top
        while current is not None:
            if current.symbol_info.type == "var":
                current.symbol_info.type = new_type
            current = current.next

    def assign_type_to_function(self, new_type):
        """
        Atribui um tipo às funções no escopo atual.
        """
        current = self.top
        while current is not None:
            if current.symbol_info.type == "function":
                current.symbol_info.type = new_type
            current = current.next

    def get_type(self, name):
        """
        Retorna o tipo do identificador.
        """
        current = self.top
        while current is not None:
            if current.symbol_info.name == name:
                return current.symbol_info.type
            current = current.next
        return ""

    def get_address(self, name):
        """
        Retorna o endereço de memória do identificador.
        """
        current = self.top
        while current is not None:
            if current.symbol_info.name == name:
                return current.symbol_info.memory_address
            current = current.next
        return ""

    def is_procedure_or_program(self, name):
        """
        Verifica se o identificador é um procedimento ou programa.
        """
        current = self.top
        while current is not None:
            if (
                current.symbol_info.name == name
                and current.symbol_info.type in ["procedimento", "programa"]
            ):
                return True
            current = current.next
        return False

    def print_stack(self):
        """
        Imprime a pilha da tabela de símbolos.
        """
        current = self.top
        while current is not None:
            info = current.symbol_info
            print(
                f"Name: {info.name}, Scope Level: {info.scope_level}, "
                f"Type: {info.type}, Memory Address: {info.memory_address}"
            )
            current = current.next

    def to_postfix(self, input_tokens):
        """
        Converte uma expressão infixa para pós-fixa (notação polonesa reversa).
        """
        operators = []
        output = []

        def precedence(op):
            if op in ["+u", "-u", "nao"]:
                return 5
            if op in ["*", "div"]:
                return 4
            if op in ["+", "-"]:
                return 3
            if op in ["=", "!=", "<", ">", "<=", ">="]:
                return 2
            if op == "e":
                return 1
            if op == "ou":
                return 0
            return -1

        def is_operator(token):
            return token in [
                "+", "-", "*", "div", "=", "!=", "<", ">", "<=", ">=", "nao", "e", "ou", "+u", "-u"
            ]

        for token in input_tokens:
            if not is_operator(token) and token not in ["(", ")"]:
                output.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                if operators:
                    operators.pop()
            elif is_operator(token):
                while (
                    operators
                    and operators[-1] != "("
                    and precedence(operators[-1]) >= precedence(token)
                ):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        return output
