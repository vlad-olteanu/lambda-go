from language import Program, Identifier, ListLiteral, EnvVariable
from utils import list_to_tuple, expression_to_str, types_to_str
from generic_functions import get_generic_fn_type, is_generic_fn
from generic_functions.functions.type_casts import TypeCast


def get_type(e, program: Program, parameter_types: dict, follow: list = None):
    if follow is None:
        # The generic functions' type depends on their arguments, pass them into follow
        follow = []
    if isinstance(e, dict):
        return dict
    if isinstance(e, bool):
        return bool
    if isinstance(e, int):
        return int
    if isinstance(e, float):
        return float
    if isinstance(e, str):
        return str
    if isinstance(e, EnvVariable):
        return str
    elif isinstance(e, ListLiteral):
        l = e.list
        if len(l) == 0:
            return [any]
        if isinstance(l, ListLiteral):
            return [get_type(l, program, parameter_types)]
        else:
            return [get_type(l[0], program, parameter_types)]
    elif isinstance(e, list):
        return get_expression_type(e, program, parameter_types)
    elif isinstance(e, TypeCast):
        argument_types = [
            get_type(arg, program, parameter_types)
            for arg in follow
        ]
        return e.get_type(argument_types)
    elif isinstance(e, Identifier):
        if e in parameter_types:
            return parameter_types[e]
        if program.has_function(e):
            return program.get_fn_type(e)
        elif is_generic_fn(e.name):
            return get_generic_function_type(
                e, follow, program, parameter_types
            )
        else:
            raise Exception(f"Could not infer type for identifier: {e}")
    else:
        raise Exception(f"Could not infer type for {e}")


def get_expression_type(expression, program: Program, parameter_types: dict) -> list:
    try:
        if len(expression) == 0:
            raise Exception("Empty expression")

        elem_types = [
            get_type(e, program, parameter_types, expression[i+1:])
            for i, e in enumerate(expression)
        ]

        def reduce(fn_type, arg_types):
            def pre_return(fn_type):
                if len(fn_type) == 1:
                    return fn_type[0]
                return fn_type

            if len(arg_types) == 0:
                return pre_return(fn_type), arg_types

            if not isinstance(fn_type, list):
                raise Exception(
                    f"{types_to_str(fn_type)} is not a function type")

            t1, t2 = fn_type[0], arg_types[0]
            if list_to_tuple(t1) != list_to_tuple(t2):
                raise Exception(
                    f"{types_to_str(fn_type)} does not match arguments {types_to_str(arg_types)}")

            return pre_return(fn_type[1:]), arg_types[1:]

        fn_type = elem_types[0]
        arg_types = elem_types[1:]
        while len(arg_types) > 0:
            fn_type, arg_types = reduce(fn_type, arg_types)

        return fn_type
    except Exception as e:
        raise Exception(
            f"Type inference for: {expression_to_str(expression)} failed: {e}")


def get_generic_function_type(fn_identifier: Identifier, arguments: list, program: Program, parameter_types: dict) -> list:
    """
    The generic function's type is inferred based on the type of its arguments.
    The result type is infered from the arguments' types and the function name.
    """

    fn_name = fn_identifier.name
    metadata = fn_identifier.metadata
    argument_types = [
        get_type(arg, program, parameter_types)
        for arg in arguments
    ]
    return get_generic_fn_type(fn_name, argument_types, metadata)
