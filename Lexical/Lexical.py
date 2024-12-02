from Token.Token import Token, TokenType  
import string 

class Lexical:
    def __init__(self, filename):
        self.filename = filename
        self.line = 1
        self.tokens = []
        try:
            self.source_file = open(filename, 'r')
        except FileNotFoundError:
            raise RuntimeError("Falha ao abrir arquivo fonte")

    def __del__(self):
        if hasattr(self, 'source_file') and not self.source_file.closed:
            self.source_file.close()

    def analise(self):
        """
        Função principal para analise Lexical
        """
        while True:
            self.del_espaco_comentario()
            ch = self.source_file.read(1)
            if not ch:
                self.tokens.append(Token("endfile", "endfile"))
                break
            self.source_file.seek(self.source_file.tell() - 1)
            token = self.get_next_token()
            self.tokens.append(token)

    def del_espaco_comentario(self):
        """
        Pular espaços em branco e ignorar comentarios
        """
        while True:
            ch = self.source_file.read(1)
            if not ch:
                break

            if ch == '{':
                open_line = self.line
                closed = False
                while True:
                    ch = self.source_file.read(1)
                    if not ch:
                        raise RuntimeError(f"Error: Comentario aberto na linha {open_line} não fechado")
                    if ch == '}':
                        closed = True
                        break
                    if ch == '\n':
                        self.line += 1
                if not closed:
                    raise RuntimeError(f"Error: Comentario aberto na linha {open_line} não fechado")
            elif ch.isspace():
                if ch == '\n':
                    self.line += 1
                continue
            else:
                self.source_file.seek(self.source_file.tell() - 1) 
                break

    def get_next_token(self):
        """
        Identificar e retornar tokens do arquivo fonte
        """
        self.del_espaco_comentario()

        ch = self.source_file.read(1)
        if not ch: 
            return Token("endfile", "endfile")

        lexeme = ""

        # Identificador e Palavra chave
        if self.is_letter(ch):
            if ch == '_':
                raise RuntimeError(f"Identificadores não podem começar com '_'. Identificador inválido na linha: {self.line}")
            lexeme += ch
            while True:
                ch = self.source_file.read(1)
                if not ch or not (self.is_letter(ch) or self.is_digit(ch) or ch == '_'):
                    break
                lexeme += ch
            if ch:
                self.source_file.seek(self.source_file.tell() - 1) 

            keywords = {
                "programa": "sprograma", "se": "sse", "entao": "sentao", "senao": "ssenao",
                "enquanto": "senquanto", "faca": "sfaca", "inicio": "sinicio", "fim": "sfim",
                "escreva": "sescreva", "leia": "sleia", "var": "svar", "inteiro": "sinteiro",
                "booleano": "sbooleano", "verdadeiro": "sverdadeiro", "falso": "sfalso",
                "procedimento": "sprocedimento", "funcao": "sfuncao", "div": "sdiv",
                "e": "se", "ou": "sou", "nao": "snao"
            }
            if lexeme in keywords:
                return Token(keywords[lexeme], lexeme)
            else:
                return Token("sidentificador", lexeme)

        # Numeros
        if self.is_digit(ch):
            lexeme += ch
            while True:
                ch = self.source_file.read(1)
                if not ch or not self.is_digit(ch):
                    break
                lexeme += ch
            if ch:
                self.source_file.seek(self.source_file.tell() - 1) 
            return Token("snumero", lexeme)

        if ch == ':':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("satribuicao", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("sdoispontos", lexeme)

        if ch == '<':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("smenorig", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("smenor", lexeme)

        if ch == '>':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("smaiorig", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("smaior", lexeme)

        if ch == '!':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("sdif", lexeme)
            raise RuntimeError(f"Error: Operador invalido '!' na linha: {self.line}")

        # Operadores e pontuação
        single_char_tokens = {
            ';': "sponto_virgula", '.': "sponto", ',': "svirgula", '(': "sabre_parenteses",
            ')': "sfecha_parenteses", '+': "smais", '-': "smenos", '*': "smult", '=': "sig"
        }
        if ch in single_char_tokens:
            return Token(single_char_tokens[ch], ch)

        # Simbolo desconhecido
        raise RuntimeError(f"Simbolo desconhecido '{ch}' na linha: {self.line}")

    def is_letter(self, ch):
        """
        Checar caractere letra
        """
        return ch.isalpha()

    def is_digit(self, ch):
        """
        Checar caractere digito
        """
        return ch.isdigit()

    def get_tokens(self):
        """
        Retornar lista de caracteres
        """
        return self.tokens

    def get_current_line(self):
        """
        Retornar linha
        """
        return self.line
