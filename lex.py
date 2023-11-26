import sys

class Token:
    EOF, STRING_LITERAL, ID, INT_LITERAL, \
    ASSIGN, L, G, EQ, NEQ, \
    PLUS, MINUS, ASTERISK, SLASH, DSLASH, \
    PERCENT, LBR, RBR, LCBR, RCBR, LSBR, \
    RSBR, LE, GE, SEMI, COMMA, \
    WHILE, RETURN, SUB, IF, ELSE, \
    OR, AND, NOT, DOG, DOL = range(35)

    token_names = {
        EOF: "EOF",
        ID: "ID",
        INT_LITERAL: "INT_LITERAL",
        STRING_LITERAL: "STRING_LITERAL",
        ASSIGN: "ASSIGN '='",
        L: "L '<'",
        G: "G '>'",
        EQ: "EQ '=='",
        PLUS: "PLUS '+'",
        MINUS: "MINUS '-'",
        ASTERISK: "ASTERISK '*'",
        SLASH: "SLASH '/'",
        DSLASH: "DSLASH '//'",
        PERCENT: "PERCENT '%'",
        LBR: "LBR '('",
        RBR: "RBR ')'",
        LCBR: "LCBR '{'",
        RCBR: "RCBR '}'",
        LSBR: "LSBR '['",
        RSBR: "RSBR ']'",
        LE: "LE '<='",
        GE: "GE '>='",
        SEMI: "SEMI ';'",
        COMMA: "COMMA ','",
        WHILE: "WHILE",
        RETURN: "RETURN",
        3: "SUB",
        IF: "IF",
        DOG: "@",
        DOL: "$"
    }

    KEYWORDS = {
        'while': WHILE,
        'return': RETURN,
        'sub': SUB,
        'if': IF,
        'else': ELSE,
        'or': OR,
        'and': AND,
        'not': NOT,
    }

    def __init__(self, token, value, lineno, pos):
        self.name = token
        self.value = value
        self.lineno = lineno
        self.pos = pos

    def __repr__(self):
        return f'({self.token_names[self.name]}, {self.value}, ({self.lineno}, {self.pos}))'


class Lexer:
    def __init__(self, file):
        self.file = file
        self.lineno = 1
        self.pos = 1
        self.state = None
        self.char = None

    def __get_next_char(self):
        self.char = self.file.read(1)
        self.pos += 1
        if self.char == '\n':
            self.lineno += 1
            self.pos = 1

    def error(self, msg):
        print(f'Ошибка лексического анализа ({self.lineno}, {self.pos}): {msg}')
        sys.exit(1)

    def get_next_token(self):
       # match self.state:
            if self.state == None:
                if self.char is None:
                    self.__get_next_char()
                    return self.get_next_token()
                elif self.char in ['\t', '\n', ' ']:
                    self.__get_next_char()
                    return self.get_next_token()
                elif self.char == '':
                    return Token(Token.EOF, "", self.lineno, self.pos)
                elif self.char == '+':
                    self.__get_next_char()
                    return Token(Token.PLUS, "+", self.lineno, self.pos)
                elif self.char == '-':
                    self.__get_next_char()
                    return Token(Token.MINUS, "-", self.lineno, self.pos)
                elif self.char == '*':
                    self.__get_next_char()
                    return Token(Token.ASTERISK, "*", self.lineno, self.pos)
                elif self.char == '%':
                    self.__get_next_char()
                    return Token(Token.PERCENT, "%", self.lineno, self.pos)
                elif self.char == '(':
                    self.__get_next_char()
                    return Token(Token.LBR, "(", self.lineno, self.pos)
                elif self.char == ')':
                    self.__get_next_char()
                    return Token(Token.RBR, ")", self.lineno, self.pos)
                elif self.char == '{':
                    self.__get_next_char()
                    return Token(Token.LCBR, "{", self.lineno, self.pos)
                elif self.char == '@':
                    self.__get_next_char()
                    return Token(Token.DOG, "@", self.lineno, self.pos)
                elif self.char == '}':
                    self.__get_next_char()
                    return Token(Token.RCBR, "}", self.lineno, self.pos)
                elif self.char == '$':
                    self.__get_next_char()
                    return Token(Token.DOL, "$", self.lineno, self.pos)
                elif self.char == '[':
                    self.__get_next_char()
                    return Token(Token.LSBR, "[", self.lineno, self.pos)
                elif self.char == ']':
                    self.__get_next_char()
                    return Token(Token.RSBR, "]", self.lineno, self.pos)
                elif self.char == ';':
                    self.__get_next_char()
                    return Token(Token.SEMI, ";", self.lineno, self.pos)
                elif self.char == ',':
                    self.__get_next_char()
                    return Token(Token.COMMA, ",", self.lineno, self.pos)
                elif self.char == '!':
                    self.__get_next_char()
                    if self.char == '=':
                        self.__get_next_char()
                        return Token(Token.NEQ, "!=", self.lineno, self.pos)
                    else:
                        self.error("Ожидался оператор !=")
                elif self.char == '/':
                    self.state = Token.SLASH
                    return self.get_next_token()
                elif self.char == '=':
                    self.state = Token.ASSIGN
                    return self.get_next_token()
                elif self.char == '<':
                    self.state = Token.L
                    return self.get_next_token()
                elif self.char == '>':
                    self.state = Token.G
                    return self.get_next_token()
                elif self.char == '"':
                    self.state = Token.STRING_LITERAL
                    return self.get_next_token()
                elif self.char.isalpha() or self.char == '_':
                    self.state = Token.ID
                    return self.get_next_token()
                elif self.char.isdigit():
                    self.state = Token.INT_LITERAL
                    return self.get_next_token()
                else:
                    self.error("Неожиданный символ")
            if self.state == Token.SLASH:
                self.__get_next_char()
                if self.char == '/':
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.DSLASH, "//", self.lineno, self.pos)
                else:
                    self.state = None
                    return Token(Token.SLASH, "/", self.lineno, self.pos)
            if self.state == Token.ASSIGN:
                self.__get_next_char()
                if self.char == '=':
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.EQ, "==", self.lineno, self.pos)
                else:
                    self.state = None
                    return Token(Token.ASSIGN, "=", self.lineno, self.pos)
            if self.state == Token.L:
                self.__get_next_char()
                if self.char == '=':
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.LE, "<=", self.lineno, self.pos)
                else:
                    self.state = None
                    return Token(Token.L, "<", self.lineno, self.pos)
            if self.state == Token.G:
                self.__get_next_char()
                if self.char == '=':
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.GE, ">=", self.lineno, self.pos)
                else:
                    self.state = None
                    return Token(Token.G, ">", self.lineno, self.pos)
            if self.state == Token.STRING_LITERAL:
                self.__get_next_char()
                string_literal = ""
                while self.char != '"':
                    if self.char == '':  # если достигнут конец файла
                        self.error('Ожидалась закрывающая кавычка!')
                    string_literal += self.char
                    self.__get_next_char()
                self.__get_next_char()
                self.state = None
                # self.pos минус 2 потому что токен оканчивается за 2 символа
                # до текущего положения чтения (оно сейчас указывает на символ
                # после кавычки, а не на последний символ строки)
                return Token(Token.STRING_LITERAL, string_literal, self.lineno, self.pos - 2)
            if self.state == Token.INT_LITERAL:
                int_literal = ""
                while self.char.isdigit():
                    int_literal += self.char
                    self.__get_next_char()
                if self.char == '.':
                    self.state = Token.INT_LITERAL
                    float_literal = int_literal + '.'
                    self.__get_next_char()
                    f = 'true';
                    while self.char.isdigit():
                        float_literal += self.char
                        self.__get_next_char()
                if self.char.isalpha() or self.char == '_':
                    self.error("Неверная запись идентификатора!")
                if self.state == Token.INT_LITERAL:
                    self.state = None
                    return Token(Token.INT_LITERAL, int_literal, self.lineno, self.pos - 1)
                if f == 'true':
                    self.state = None
                    return Token(Token.INT_LITERAL, float_literal, self.lineno, self.pos - 1)
            if self.state == Token.ID:
                id = self.char
                self.__get_next_char()
                while self.char.isalpha() or self.char.isdigit() or self.char == '_':
                    id += self.char
                    self.__get_next_char()
                self.state = None
                if id in Token.KEYWORDS:
                    return Token(Token.KEYWORDS[id], id, self.lineno, self.pos - 1)
                else:
                    return Token(Token.ID, id, self.lineno, self.pos - 1)

