from .code_formatting import format_code
from language import Program, Identifier
from language.functions import Function, FunctionDefinition
from .function_headers_footers import get_fn_header, get_fn_footer
from .expressions import expand_expression
from utils import fn_type_to_str


def expand_functions(program: Program) -> str:
    return format_code(
        "\n".join([expand_fn(program, fn) for fn in program.functions])
    )


def expand_fn(p: Program, fn: Function) -> str:
    ret = []
    ret.append(f"// {fn.name}::{fn_type_to_str(fn.type)}")
    ret.append(get_fn_header(fn.name, fn.type))
    ret += [expand_fn_definition(fn_def, fn.type) for fn_def in fn.definitions]
    ret.append(get_fn_footer(fn.type))
    return "\n".join(ret)


def expand_fn_definition(fn_def: FunctionDefinition, fn_type: list) -> str:
    ret = []
    condition = fn_def.condition
    if condition is not None:
        ret.append(f"if {expand_expression(condition)} "+"{")

    additional_calls = "".join([
        f"(arg{i})" for i in range(len(fn_def.parameters), len(fn_type)-1)
    ])
    ret.append(f"return {expand_expression(fn_def.expression)}{additional_calls}")

    if condition is not None:
        ret.append("}")

    return "\n".join(ret)
