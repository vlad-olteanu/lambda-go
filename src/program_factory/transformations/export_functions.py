from language import Program, Identifier, ListLiteral
from language.functions import Function, FunctionDefinition
from ..type_inference import get_type
from utils import get_hard_fn_name

def export_functions(fn: Function)->Function:
    fn.name = Identifier(fn.name.name.capitalize())
    return fn

def export_functions_in_defs(fn_def: FunctionDefinition, fn: Function, p: Program) -> FunctionDefinition:
    fn_names = [fn.name.name for fn in p.functions]
    if fn_def.condition:
        fn_def.condition = substitute_expression(
            p, fn_names, fn_def.condition
        )
    fn_def.expression = substitute_expression(
        p, fn_names, fn_def.expression
    )
    return fn_def


def substitute_expression(program: Program, fn_names: list, expression: list) -> list:
    for i, e in enumerate(expression):
        if isinstance(e, Identifier):
            if e.name.capitalize() in fn_names:
                expression[i] = Identifier(e.name.capitalize())
        if isinstance(e, list):
            expression[i] = substitute_expression(program, fn_names, e)
    return expression
