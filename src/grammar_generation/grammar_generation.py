import os
from .py_parsing import get_sections
from .bnf_parsing import parse_bnf
from itertools import chain
from typing import List


GRAMMAR_BNF_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "grammar.bnf"
)

LEX_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "tokenization", "lex.py"
)

TOKENS_FILE_PATH = os.path.join(
    os.path.dirname(LEX_FILE_PATH),
    "tokens.py"
)

YACC_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "parsing", "yacc.py"
)

FINAL_COMMANDS_HEADER = "# ==Final Commands=="
FUNCTION_HEADER = "# ==Function=="


def add_function_header(fn_text) -> str:
    return "\n".join([FUNCTION_HEADER, fn_text])


def regenerate_yacc_file(grammar, path):
    if not os.path.exists(path):
        src_text = ""
    else:
        with open(path, "r") as f:
            src_text = f.read()

    import_section, fns, final_commands = get_sections(src_text)
    dst_text = []

    def generate_imports(import_section) -> str:
        if len(import_section.strip()) > 0:
            return import_section
        return "\n".join([
            "import ply.yacc as yacc",
            "from tokenization.tokens import tokens",
            "",
            "",
        ])

    def generate_production_function(production) -> str:
        return "\n".join([
            f"def p_{'_'.join(production)}(s):",
            f"   \"{production[0]} : {' '.join(production[1:])}\"",
            "   pass", "", ""
        ])

    def generate_final_commands(final_commands) -> str:
        if len(final_commands.strip()) > 0:
            return final_commands
        return "\n".join([
            "parser = yacc.yacc()"
        ])

    for production in grammar.productions:
        fn = f"p_{'_'.join(production)}"
        if fn not in fns:
            fns[fn] = generate_production_function(production)

    for fn in fns:
        # remove "p_" prefix
        prod_str = fn[2:]
        all_productions_str = ["_".join(p) for p in grammar.productions]
        if prod_str not in all_productions_str and \
                prod_str not in ["error"]:
            print(f"Warning: Unused parsing function: {fn}")

    dst_text = "".join([
        generate_imports(import_section),
        *[add_function_header(fns[f]) for f in fns],
        f"{FINAL_COMMANDS_HEADER}\n",
        generate_final_commands(final_commands)
    ])

    with open(path, "w") as f:
        f.write(dst_text)


def generate_tokens_file(grammar, path):
    with open(path, "w") as f:
        f.write("\n".join([
            "tokens = [",
            *[f"    \"{terminal}\"," for terminal in grammar.terminals],
            "]"
        ]))


def regenerate_lex_file(grammar, path):
    if not os.path.exists(path):
        src_text = ""
    else:
        with open(path, "r") as f:
            src_text = f.read()

    import_section, fns, final_commands = get_sections(src_text)
    dst_text = []

    def generate_imports(import_section) -> str:
        if len(import_section.strip()) > 0:
            return import_section
        return "\n".join([
            "import ply.lex as lex",
            "from .tokens import tokens",
            "",
            ""
        ])

    def generate_tokenization_function(terminal) -> str:
        return "\n".join([
            f"def t_{terminal}(t):",
            f"   r\"{terminal}\"",
            "   return t", "", ""
        ])

    def generate_final_commands(final_commands) -> str:
        if len(final_commands.strip()) > 0:
            return final_commands
        return "\n".join([
            r"t_ignore  = ' \t'",
            "lexer = lex.lex()"
        ])

    if "t_error" not in fns:
        fns["t_error"] = "\n".join([
            "def t_error(t):",
            "   print(\"Illegal character '%s'\" % t.value[0])",
            "", ""
        ])

    if "t_comment" not in fns:
        fns["t_comment"] = "\n".join([
            "def t_comment(t):",
            "   r\"\\#.*\"",
            "   return None",
            "", ""
        ])

    if "t_newline" not in fns:
        fns["t_newline"] = "\n".join([
            "def t_newline(t):",
            "   r\"\\n+\"",
            "   t.lexer.lineno += len(t.value)",
            "", ""
        ])

    for terminal in grammar.terminals:
        fn = f"t_{terminal}"
        if fn not in fns:
            fns[fn] = generate_tokenization_function(terminal)

    for fn in fns:
        # remove "t_" prefix
        terminal = fn[2:]
        if terminal not in grammar.terminals \
                and terminal not in ["error", "comment", "newline"]:
            print(f"Warning: Unused tokenization function: {fn}")

    dst_text = "".join([
        generate_imports(import_section),
        *[add_function_header(fns[f]) for f in fns],
        f"{FINAL_COMMANDS_HEADER}\n",
        generate_final_commands(final_commands)
    ])

    with open(path, "w") as f:
        f.write(dst_text)


def generate_grammar():
    with open(GRAMMAR_BNF_PATH, "r") as f:
        grammar_text = f.read()
    grammar = parse_bnf(grammar_text)
    generate_tokens_file(grammar, TOKENS_FILE_PATH)
    regenerate_lex_file(grammar, LEX_FILE_PATH)
    regenerate_yacc_file(grammar, YACC_FILE_PATH)
