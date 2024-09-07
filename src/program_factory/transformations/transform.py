from language import Program
from language.functions import Function, FunctionDefinition


def transform_functions(program: Program, transform_fn) -> Program:
    program.functions = [
        transform_fn(fn) for fn in program.functions
    ]
    return program


def transform_fn_definitions(program: Program, transform_fn, layers_passed=1) -> Program:
    def transform_function(fn: Function) -> Function:
        fn.definitions = [
            transform_fn(*[fn_def, fn, program][:layers_passed])
            for fn_def in fn.definitions
        ]
        return fn
    program.functions = [
        transform_function(fn) for fn in program.functions
    ]
    return program
