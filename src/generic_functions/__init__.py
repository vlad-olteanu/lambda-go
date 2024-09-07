from .functions.arithmetic import generic_functions as arithmetic_functions
from .functions.logical import generic_functions as logical_functions
from .functions.lists import generic_functions as list_functions
from .functions.strings import generic_functions as string_functions
from .functions.type_casts import generic_functions as cast_functions
from .functions.dicts import generic_functions as dict_functions

generic_functions = {
    **arithmetic_functions,
    **logical_functions,
    **list_functions,
    **string_functions,
    **cast_functions,
    **dict_functions,
}


def is_generic_fn(name: str) -> bool:
    return name in generic_functions


def get_generic_fn_type(name: str, argument_types: list, metadata: dict):
    if not is_generic_fn(name):
        raise Exception(f"{name} is not a generic fn")
    return generic_functions[name].get_type(argument_types, metadata)


def expand(name: str, fn_type: list):
    if not is_generic_fn(name):
        raise Exception(f"{name} is not a generic fn")
    return generic_functions[name].expand(fn_type)
