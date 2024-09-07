from language import Program
from language.functions import Function, FunctionDefinition
from language.operators import Operator
from language.identifiers import Identifier


def substitute_operators(fn_def: FunctionDefinition) -> FunctionDefinition:
    if fn_def.condition:
        fn_def.condition = substitute_operators_expression(fn_def.condition)
    fn_def.expression = substitute_operators_expression(fn_def.expression)
    return fn_def


def substitute_operators_expression(expression: list) -> list:
    for i, e in enumerate(expression):
        if isinstance(e, Operator):
            if i == 0:
                raise Exception(
                    "Unmatched operator at start of expression: "+" ".join(expression))
            if i == len(expression)-1:
                raise Exception(
                    "Unmatched operator at end of expression: "+" ".join(expression))
            if isinstance(expression[i-1], Operator):
                raise Exception("Consecutive operators: "+" ".join(expression))
            if isinstance(expression[i+1], Operator):
                raise Exception("Consecutive operators: "+" ".join(expression))
            expression[i-1:i + 2] = [
                operator_to_fn(e), expression[i-1], expression[i+1]
            ]
        if isinstance(e, list):
            expression[i] = substitute_operators_expression(e)
    return expression


def operator_to_fn(operator: Operator) -> Identifier:
    OPERATORS = {
        "+": "add",
        "-": "sub",
        "*": "mul",
        "/": "div",
        "%": "mod",
        "==": "eq",
        "!=": "neq",
        ">": "gt",
        ">=": "gte",
        "<": "lt",
        "<=": "lte",
        "++": "concat"
    }
    if operator.str_value not in OPERATORS:
        raise Exception(f"Unknown operator: {operator}")
    return Identifier(OPERATORS[operator.str_value])
