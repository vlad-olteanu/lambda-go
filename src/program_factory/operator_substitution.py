from language import Program
from language.functions import Function
from language.operators import Operator
from language.identifiers import Identifier


def substitute_operators(program: Program) -> Program:
    program.functions = [
        substitute_operators_fn(fn) for fn in program.functions
    ]
    return program


def substitute_operators_fn(fn: Function) -> Function:
    if fn.condition:
        fn.condition = substitute_operators_expression(fn.condition)
    fn.expression = substitute_operators_expression(fn.expression)
    return fn


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


def operator_to_fn(operator: Operator) -> Identifier:
    OPERATORS = {
        "+": "add",
        "++": "concat",
        "-": "sub",
        "*": "mul",
        "/": "div",
        "%": "mod",
        "==": "eq",
    }
    if operator.str_value not in OPERATORS:
        raise Exception(f"Unknown operator: {operator}")
    return Identifier(OPERATORS[operator.str_value])
