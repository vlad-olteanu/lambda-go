from language import ListLiteral, EnvVariable
from .types import expand_type


def expand_expression(expression: list) -> str:
    def elem(e):
        if isinstance(e, list):# and len(e) > 1:
            return expand_expression(e)
        if isinstance(e, ListLiteral):
            return expand_list_literal(e)
        if isinstance(e, dict):
            return expand_dict(e)
        if isinstance(e, bool):
            return str(e).lower()
        if isinstance(e, EnvVariable):
            return expand_env_var(e)
        return str(e)
    if not isinstance(expression, list):
        return elem(expression)
    return "".join([elem(expression[0])]+[f"({elem(e)})" for e in expression[1:]])


def expand_list_literal(list_literal: ListLiteral) -> str:
    def expand_list_literal_rec(list_literal: ListLiteral) -> str:
        def expand_elem(e) -> str:
            if isinstance(e, ListLiteral):
                return expand_list_literal_rec(e)
            if hasattr(e, "name"):
                return e.name
            if isinstance(e, dict):
                return expand_dict(e)
            if isinstance(e, list):
                return expand_expression(e)
            return str(e)
        return "{"+", ".join([expand_elem(e) for e in list_literal.list])+"}"

    return expand_type(list_literal.type) + expand_list_literal_rec(list_literal)


def expand_dict(d: dict):
    kv_pairs = []

    for k, v in d.items():
        k = f"\"{k}\": "
        if isinstance(v, dict):
            v = expand_dict(v)
        elif isinstance(v, EnvVariable):
            v = expand_env_var(v)
        elif isinstance(v, list):
            v = expand_expression(v)
        else:
            v = str(v)
        kv_pairs.append(k + v + ", ")

    return "map[string]interface{}"+"{\n"+"\n".join(kv_pairs)+"\n}"


def expand_env_var(e: EnvVariable) -> str:
    return f"get_env(\"{e.name}\")"
