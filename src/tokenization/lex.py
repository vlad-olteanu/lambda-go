import ply.lex as lex
from .tokens import tokens
from language import Operator, Identifier

# ==Function==


def t_FLOAT(t):
    r"[1-9][0-9]*\.[0-9]+"
    t.value = float(t.value)
    return t

# ==Function==


def t_BOOL(t):
    r"(true)|(false)"
    t.value = t.value == "true"
    return t

# ==Function==


def t_ARROW(t):
    r"->"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_MINUS(t):
    r"-"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_CONCAT(t):
    r"\+\+"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_PLUS(t):
    r"\+"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_EQUALITY(t):
    r"=="
    t.value = Operator(t.value)
    return t

# ==Function==


def t_INEQUALITY(t):
    r"!="
    t.value = Operator(t.value)
    return t

# ==Function==


def t_EQUAL(t):
    r"="
    t.value = Operator(t.value)
    return t

# ==Function==


def t_STRING(t):
    r'"[^"\\]*(\\.[^"\\]*)*"'
    return t

# ==Function==


def t_DOUBLE_DOTS(t):
    r"::"
    return t

# ==Function==


def t_INTEGER(t):
    r"[0-9][0-9]*"
    t.value = int(t.value)
    return t

# ==Function==


def t_LBRACKET(t):
    r"\["
    return t

# ==Function==


def t_MOD(t):
    r"%"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.value = Identifier(t.value)
    return t

# ==Function==


def t_LCURLYBRACES(t):
    r"{"
    return t

# ==Function==


def t_MUL(t):
    r"\*"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_COMMA(t):
    r","
    return t

# ==Function==


def t_DOTS(t):
    r":"
    return t

# ==Function==


def t_RPARANTHESIS(t):
    r"\)"
    return t

# ==Function==


def t_DIV(t):
    r"/"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_LPARANTHESIS(t):
    r"\("
    return t

# ==Function==


def t_RCURLYBRACES(t):
    r"\}"
    return t

# ==Function==


def t_PIPE(t):
    r"\|"
    return t

# ==Function==


def t_RBRACKET(t):
    r"\]"
    return t

# ==Function==


def t_comment(s):
    r"\#.*"
    return None

# ==Function==


def t_DOLLLAR(t):
    r"\$"
    return t

# ==Function==


def t_error(t):
    print(f"Illegal character at line {t.lexer.lineno}: \"{t.value[:10]}...\"")
    exit(-1)

# ==Function==


def t_newline(t):
    r"\n"
    t.lexer.lineno += 1

# ==Function==


def t_OR(t):
    r"\|\|"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_AND(t):
    r"&&"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_LESS_OR_EQUAL_THAN(t):
    r"<="
    t.value = Operator(t.value)
    return t

# ==Function==


def t_LESS_THAN(t):
    r"<"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_GREATER_THAN(t):
    r">"
    t.value = Operator(t.value)
    return t

# ==Function==


def t_GREATER_OR_EQUAL_THAN(t):
    r">="
    t.value = Operator(t.value)
    return t

# ==Final Commands==
t_ignore = ' \t'
lexer = lex.lex()
