from .code_formatting import format_code
from language import Program, Identifier
from language.functions import HardFunction, FunctionDefinition
from .function_headers_footers import get_fn_header, get_fn_footer
from generic_functions import expand

def expand_hard_fns(program: Program) -> str:
    return format_code(
        "\n\n".join([expand_hard_fn(fn) for fn in program.hard_functions])
    )


def expand_hard_fn(fn: HardFunction) -> str:
    ret = []
    ret.append(f"// {fn}")
    ret.append(get_fn_header(fn.name, fn.type))
    ret.append(f"return {get_hard_fn_expression(fn)}")
    ret.append(get_fn_footer(fn.type))
    return "\n".join(ret)


def get_hard_fn_expression(fn: HardFunction) -> str:
    return expand(fn.generic_name, fn.type)

