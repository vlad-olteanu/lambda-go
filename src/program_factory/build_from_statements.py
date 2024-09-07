from parsing.statements import FunctionDefinition as PFunctionDefinition, FunctionTypeDeclaration
from language import Program
from language.functions import Function, FunctionDefinition
from typing import List, Mapping
from language.identifiers import Identifier


def build_program_from_statements(statements) -> Program:
    fn_definitions = group_function_definitions_by_name(statements)
    type_declarations = get_function_type_declarations(statements)
    check_functions_without_defined_type(
        fn_definitions.keys(), type_declarations
    )
    functions = get_functions(fn_definitions, type_declarations)
    p = Program(
        functions, []
    )
    return p


def group_function_definitions_by_name(statements) -> Mapping[Identifier, List[PFunctionDefinition]]:
    statements = [s for s in statements if isinstance(
        s, PFunctionDefinition)]
    ret = {}
    for s in statements:
        if s.name not in ret:
            ret[s.name] = []
        ret[s.name].append(s)
    return ret


def get_function_type_declarations(statements) -> Mapping[Identifier, FunctionTypeDeclaration]:
    statements = [
        s for s in statements if isinstance(
            s, FunctionTypeDeclaration)
    ]
    ret = {}
    for s in statements:
        if s.name in ret:
            raise Exception(
                f"Can't define {s.name} as {s} because it's already defined as {ret[s.name]}"
            )
        ret[s.name] = s
    return ret


def check_functions_without_defined_type(
    fn_names: List[Identifier],
    fn_type_decls: Mapping[Identifier, FunctionTypeDeclaration]
):
    for fn in fn_names:
        if fn not in fn_type_decls:
            raise Exception(f"{fn} does not have a defined type")


def get_functions(
    fn_definitions: Mapping[Identifier, List[PFunctionDefinition]],
    type_declarations: Mapping[Identifier, FunctionTypeDeclaration]
):
    fns = []
    for fn_name, definitions in fn_definitions.items():
        # turn parsing.statements.FunctionDefinition to program.functions.FunctionDefinition
        definitions = [
            FunctionDefinition(d.parameters, d.condition, d.expression)
            for d in definitions
        ]
        fns.append(
            Function(fn_name, type_declarations[fn_name].type, definitions)
        )

    return fns