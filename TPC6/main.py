import ply.lex as lex

class PLexer():

    states = (('comment', 'exclusive'),)

    tokens = (
        "PROGRAM",
        "FUNCTION",
        "INT",
        "NUMBER",
        "RANGE",
        "IF",
        "ELSE",
        "FOR",
        "IN",
        "WHILE",
        "OPEN_BRACKET",
        "CLOSE_BRACKET",
        "OPEN_CURLY_BRACKET",
        "CLOSE_CURLY_BRACKET",
        "OPEN_PARENTHESES",
        "CLOSE_PARENTHESES",
        "MULTIPLY",
        "DIVIDE",
        "PLUS",
        "MINUS",
        "MORE",
        "LESS",
        "EQUAL",
        "NAME",
        "SEMI_COLON",
        "COMMA",
        "INLINE_COMMENT",
        "COMMENT",
        "OPEN_MULTILINE_COMMENT",
        "CLOSE_MULTILINE_COMMENT"
    )


    def __init__(self):
        self.lexer: lex.Lexer = lex.lex(module=self)

        self.args = 0
        self.open_curly = False
        self.open_brackets = False

        self.reserved_words = {
            "function": "FUNCTION",
            "program": "PROGRAM",
            "while": "WHILE",
            "for": "FOR",
            "in": "IN",
            "range": "RANGE",
            "if": "IF",
            "else": "ELSE",
            "int": "INT",
        }

    t_NUMBER = r'\d+'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MORE = r'\>'
    t_LESS = "<"
    t_EQUAL = r'\='
    t_comment_COMMENT = r"[^(\/\*)]+"
    t_INLINE_COMMENT = "//.*"
    t_SEMI_COLON = ";"
    t_COMMA = ","
    t_RANGE = r'\.\.'
    t_ANY_ignore = ' \t\n'

    def t_OPEN_MULTILINE_COMMENT(self, t):
            r"\/\*"
            t.lexer.begin('comment')
            return t

    def t_comment_CLOSE_MULTILINE_COMMENT(self, t):
        r"\*\/"
        t.lexer.begin('INITIAL')
        return t

    def t_NAME(self, t):
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        t.type = self.reserved_words.get(t.value, "NAME")
        return t

    def t_OPEN_BRACKET(self, t):
        r"\["
        self.open_brackets = True
        return t

    def t_CLOSE_BRACKET(self, t):
        r"\]"
        if self.open_brackets == False:
            print("Unexpected ]")
            return t
        self.open_brackets = False
        return t

    def t_OPEN_PARENTHESES(self, t):
        r"\("
        self.args += 1
        return t

    def t_CLOSE_PARENTHESES(self, t):
        r"\)"
        if self.args == 0:
            print("Unexpected )")
            return t
        self.args -= 1
        return t

    def t_OPEN_CURLY_BRACKET(self, t):
        r"\{"
        self.open_curly = True
        return t

    def t_CLOSE_CURLY_BRACKET(self, t):
        r"\}"
        if self.open_curly == False:
            print("Unexpected }")
            return t
        self.open_curly = False
        return t

    def t_ANY_error(self, t):
        print("Illegal token found", t.value[0])
        t.lexer.skip(1)
        return t

    def read(self, data):
        self.lexer.input(data)

def main():
    
    lexer = PLexer()
    
    try:
        file = input("Enter the file name: ")
        with open(file, "r") as file:
            lexer.read(file.read())
    except FileNotFoundError:
        print("File not found")
        return

    while tok := lexer.lexer.token():
        print(tok)


main()