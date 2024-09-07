"""
Transforms the functions types from identifiers to python types (where applicable)
"""

from language.identifiers import Identifier
from language.program import Program, Function
from language.functions import HardFunction, Function, FunctionDefinition
from frozendict import frozendict
from dataclasses import replace
from utils import list_to_tuple


def subsitute_type_elem(t):
    if isinstance(t, list):
        return substitute_type_list(t)
    type_name = t.name
    type_dict = {t.__name__: t for t in [int, float, str, dict, bool, any]}
    if type_name in type_dict:
        return type_dict[type_name]
    return t


def substitute_type_list(l: list) -> list:
    return [subsitute_type_elem(e) for e in l]


def substitute_fn_types(fn: Function) -> Function:
    fn_type = [subsitute_type_elem(t) for t in fn.type]

    # int->(int->int) => int->int->int
    t = fn_type[-1]
    while isinstance(t, list) and len(t) > 1:
        fn_type = fn_type[:-1]+t
        t = t[-1]

    fn.type = fn_type
    return fn


def substitute_cast_types(fn_def: FunctionDefinition) -> FunctionDefinition:
    if fn_def.condition:
        fn_def.condition = substitute_expression(
            fn_def.condition
        )
    fn_def.expression = substitute_expression(
        fn_def.expression
    )
    return fn_def


def substitute_expression(expression: list) -> list:
    for i, e in enumerate(expression):
        if isinstance(e, Identifier) and e.name == "type_cast":
            metadata = dict(e.metadata)
            metadata["target_type"] = list_to_tuple([subsitute_type_elem(t) for t in e.metadata["target_type"]])
            metadata = frozendict(metadata)
            e = replace(e, metadata=metadata)
            expression[i]  = e
        elif isinstance(e, list):
            expression[i] = substitute_expression(e)
        elif isinstance(e, dict):
            expression[i] = substitute_dict(e)
    return expression


def substitute_dict(d: dict) -> dict:
    d = dict(d)
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = substitute_dict(v)
        elif isinstance(v, list):
            d[k] = substitute_expression(v)
    return d
