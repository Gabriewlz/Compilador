class TokenType:
    """
    Enumeração dos tipos de tokens disponíveis.
    """
    SPROGRAMA = "sprograma"
    SINICIO = "sinicio"
    SFIM = "sfim"
    SPROCEDIMENTO = "sprocedimento"
    SFUNCAO = "sfuncao"
    SSE = "sse"
    SENTAO = "sentao"
    SSENAO = "ssenao"
    SENQUANTO = "senquanto"
    SFACA = "sfaca"
    SATRIBUICAO = "satribuicao"
    SESCREVA = "sescreva"
    SLEIA = "sleia"
    SVAR = "svar"
    SINTEIRO = "sinteiro"
    SBOLEANO = "sbooleano"
    SIDENTIFICADOR = "sidentificador"
    SNUMERO = "snumero"
    SPONTO = "sponto"
    SPONTO_VIRGULA = "sponto_virgula"
    SVIRGULA = "svirgula"
    SABRE_PARENTESES = "sabre_parenteses"
    SFECHA_PARENTESES = "sfecha_parenteses"
    SMAIOR = "smaior"
    SMAIORIG = "smaiorig"
    SIG = "sig"
    SMENOR = "smenor"
    SMENORIG = "smenorig"
    SDIF = "sdif"
    SMAIS = "smais"
    SMENOS = "smenos"
    SMULT = "smult"
    SDIV = "sdiv"
    SE = "se"
    SOU = "sou"
    SNAO = "snao"
    SDOISPONTOS = "sdoispontos"
    SVERDADEIRO = "sverdadeiro"
    SFALSO = "sfalso"
    ENDFILE = "endfile"
    TOKEN_UNKNOWN = "TOKEN_UNKNOWN"


class Token:
    """
    Classe que representa um token gerado pelo analisador léxico.
    """
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def get_type(self):
        """
        Retorna o tipo do token.
        """
        return self.token_type

    def get_type_string(self):
        """
        Retorna o tipo do token como uma string.
        """
        return self.token_type

    def get_lexeme(self):
        """
        Retorna o lexema associado ao token.
        """
        return self.lexeme

    def __repr__(self):
        """
        Converte o token para uma string para depuração.
        """
        return f"Token(lexeme='{self.lexeme}', type='{self.token_type}')"


# Mapa global que associa lexemas a tokens
LEXEMA_TO_TOKEN = {
    "programa": TokenType.SPROGRAMA,
    "inicio": TokenType.SINICIO,
    "fim": TokenType.SFIM,
    "procedimento": TokenType.SPROCEDIMENTO,
    "funcao": TokenType.SFUNCAO,
    "se": TokenType.SSE,
    "entao": TokenType.SENTAO,
    "senao": TokenType.SSENAO,
    "enquanto": TokenType.SENQUANTO,
    "faca": TokenType.SFACA,
    ":=": TokenType.SATRIBUICAO,
    "escreva": TokenType.SESCREVA,
    "leia": TokenType.SLEIA,
    "var": TokenType.SVAR,
    "inteiro": TokenType.SINTEIRO,
    "booleano": TokenType.SBOLEANO,
    "identificador": TokenType.SIDENTIFICADOR,
    "numero": TokenType.SNUMERO,
    ".": TokenType.SPONTO,
    ";": TokenType.SPONTO_VIRGULA,
    ",": TokenType.SVIRGULA,
    "(": TokenType.SABRE_PARENTESES,
    ")": TokenType.SFECHA_PARENTESES,
    ">": TokenType.SMAIOR,
    ">=": TokenType.SMAIORIG,
    "=": TokenType.SIG,
    "<": TokenType.SMENOR,
    "<=": TokenType.SMENORIG,
    "!=": TokenType.SDIF,
    "+": TokenType.SMAIS,
    "-": TokenType.SMENOS,
    "*": TokenType.SMULT,
    "div": TokenType.SDIV,
    "e": TokenType.SE,
    "ou": TokenType.SOU,
    "nao": TokenType.SNAO,
    ":": TokenType.SDOISPONTOS,
    "verdadeiro": TokenType.SVERDADEIRO,
    "falso": TokenType.SFALSO,
}


def get_token(lexeme):
    """
    Função para criar um Token com base em um lexema.
    """
    token_type = LEXEMA_TO_TOKEN.get(lexeme, TokenType.TOKEN_UNKNOWN)
    return Token(token_type, lexeme)
