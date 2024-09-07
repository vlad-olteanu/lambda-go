"""
Replace the expressions argument names with arg0, arg1, arg2 etc.
"""
from language import Program, Identifier, ListLiteral
from language.functions import Function, FunctionDefinition


def substitute_argument_names(fn_def: FunctionDefinition) -> FunctionDefinition:
    new_parameter_names = {p: Identifier(
        f"arg{i}") for i, p in enumerate(fn_def.parameters)}
    fn_def.parameters = substitute_expression(
        new_parameter_names, fn_def.parameters
    )
    if fn_def.condition:
        fn_def.condition = substitute_expression(
            new_parameter_names, fn_def.condition
        )
    fn_def.expression = substitute_expression(
        new_parameter_names, fn_def.expression
    )
    return fn_def


def substitute_expression(new_parameter_names: dict, expression: list) -> list:
    new_expression = [*expression]
    for i, e in enumerate(new_expression):
        if isinstance(e, Identifier):
            if isinstance(e, Identifier):
                if e in new_parameter_names:
                    new_expression[i] = new_parameter_names[e]
        if isinstance(e, ListLiteral):
            e.list = substitute_expression(new_parameter_names, e.list)
        if isinstance(e, list):
            new_expression[i] = substitute_expression(new_parameter_names, e)
        if isinstance(e, dict):
            new_expression[i] = substitute_dict(new_parameter_names, e)
        if isinstance(e, ListLiteral):
            new_expression[i] = substitute_list_literal(new_parameter_names, e)
    return new_expression


def substitute_dict(new_parameter_names: dict, d: dict) -> dict:
    d = dict(d)
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = substitute_dict(new_parameter_names, v)
        elif isinstance(v, list):
            d[k] = substitute_expression(new_parameter_names, v)
        elif isinstance(v, Identifier) and v in new_parameter_names:
            d[k] = new_parameter_names[v]
    return d


def substitute_list_literal(new_parameter_names: dict, ll: ListLiteral) -> ListLiteral:
    l = ll.list
    for i, e in enumerate(l):
        if isinstance(e, ListLiteral):
            l[i] = substitute_list_literal(new_parameter_names, e)
        elif isinstance(e, Identifier) and e in new_parameter_names:
            l[i] = new_parameter_names[e]
        elif isinstance(e, dict):
            l[i] = substitute_dict(new_parameter_names, e)
    return ll
