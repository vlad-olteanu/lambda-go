from language import Program

from .build_from_statements import build_program_from_statements
from .transformations.transform import transform_functions, transform_fn_definitions
from .transformations.operator_substitution import substitute_operators
from .transformations.fn_type_substitution import substitute_fn_types
from .transformations.fn_type_substitution import substitute_cast_types
from .transformations.generic_fn_substitution import substitute_generic_fns
from .transformations.argument_name_substitution import substitute_argument_names
from .transformations.fill_list_literal_types import fill_list_literal_types
from .transformations.replace_otherwise import replace_otherwise
from .transformations.export_functions import export_functions, export_functions_in_defs

from .validation.validate import validate_functions, validate_fn_definitions
from .validation.check_fn_def_types import check_fn_def_type


def build_program(statements) -> Program:
    p = build_program_from_statements(statements)
    p = transform_fn_definitions(p, replace_otherwise)
    p = transform_fn_definitions(p, fill_list_literal_types, layers_passed=3)
    p = transform_fn_definitions(p, substitute_operators)
    p = transform_functions(p, substitute_fn_types)
    p = transform_fn_definitions(p, substitute_cast_types)
    p = transform_fn_definitions(p, substitute_generic_fns, layers_passed=3)
    p = transform_fn_definitions(p, substitute_argument_names)
    p = transform_functions(p, export_functions)
    p = transform_fn_definitions(p, export_functions_in_defs, layers_passed=3)

    validate_fn_definitions(p, check_fn_def_type, layers_passed=3)

    return p
