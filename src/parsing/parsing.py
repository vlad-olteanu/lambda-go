from .yacc import parser

def parse(src):
    return parser.parse(src)
