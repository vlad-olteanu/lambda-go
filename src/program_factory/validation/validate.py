from language import Program


def validate_functions(program: Program, validation_fn, layers_passed=1):
    for fn in p.functions:
        validation_fn(*[fn, program][:layers_passed])


def validate_fn_definitions(program: Program, validation_fn, layers_passed=1):
    for fn in program.functions:
        for fn_def in fn.definitions:
            validation_fn(*[fn_def, fn, program][:layers_passed])
