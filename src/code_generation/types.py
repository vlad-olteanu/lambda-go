from language import EnvVariable
from utils import tuple_to_list


def expand_type(t) -> str:
    def elem(e) -> str:
        # if isinstance(e, tuple):
        #     e = tuple_to_list(e)
        if e is any:
            return "interface{}"
        if e is None:
            return ""
        if isinstance(e, EnvVariable):
            return "string"
        if hasattr(e, "name"):
            return e.name
        if e is dict:
            return "map[string]interface{}"
        if e is float:
            return "float64"
        if e is str:
            return "string"
        if isinstance(e, list):
            # it's a function type
            if len(e) > 1:
                return expand_type(e)
            # it's a list type
            return "[]"+expand_type(e[0])
        return e.__name__
    if isinstance(t, list) and len(t) > 1:
        # it's a function type
        return " ".join([f"func({elem(e)})" for e in t[:-1]]) + " " + elem(t[-1])
    return elem(t)
