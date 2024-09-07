from language.functions import FunctionDefinition
from language import Identifier


def replace_otherwise(fn_def: FunctionDefinition) -> FunctionDefinition:
    condition = fn_def.condition
    if condition is None:
        return fn_def
    if len(condition) == 1 and condition[0] == Identifier("otherwise"):
        fn_def.condition = None
    return fn_def
