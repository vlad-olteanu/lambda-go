"""
Checks that the types of the functions' definitons match the declared type
"""

from ..type_inference import get_type
from language import Program
from language.functions import Function, FunctionDefinition
from utils import types_to_str, list_to_tuple


def check_fn_def_type(fn_def: FunctionDefinition, fn: Function, program: Program):
    fn_type = fn.type
    expected_type = fn_type[len(fn_def.parameters):]
    if len(expected_type) == 1:
        expected_type = expected_type[0]

    parameter_types = {p: t for p, t in zip(fn_def.parameters, fn_type)}
    actual_type = get_type(fn_def.expression, program, parameter_types)

    if list_to_tuple(expected_type) != list_to_tuple(actual_type):
        raise Exception(
            f"Type checking {fn.name} {fn_def} failed: Expected type {types_to_str(expected_type)} does not match actual type {types_to_str(actual_type)}"
        )
