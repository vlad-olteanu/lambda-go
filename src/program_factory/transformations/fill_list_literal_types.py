from language import Program, Identifier, ListLiteral
from language.functions import Function, FunctionDefinition
from ..type_inference import get_type
from utils import get_hard_fn_name


def fill_list_literal_types(fn_def: FunctionDefinition, fn: Function, p: Program) -> FunctionDefinition:
    parameter_types = {p: t for p, t in zip(fn_def.parameters, fn.type)}
    if fn_def.condition:
        fn_def.condition = substitute_expression(
            p, parameter_types, fn_def.condition
        )
    fn_def.expression = substitute_expression(
        p, parameter_types, fn_def.expression
    )
    return fn_def


def substitute_expression(program: Program, parameter_types: dict, expression: list) -> list:
    for i, e in enumerate(expression):
        if isinstance(e, ListLiteral):
            e.type = get_type(e, program, parameter_types)
            expression[i] = e
        if isinstance(e, list):
            expression[i] = substitute_expression(program, parameter_types, e)
        if isinstance(e, dict):
            expression[i] = substitute_dict(program, parameter_types, e)
    return expression

def substitute_dict(program: Program, parameter_types: dict, d: dict) -> dict:
    d = dict(d)
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = substitute_dict(program, parameter_types, v)
        elif isinstance(v, list):
            d[k] = substitute_expression(program, parameter_types, v) 
        elif isinstance(e, ListLiteral):
            e.type = get_type(e, program, parameter_types)
    return d
