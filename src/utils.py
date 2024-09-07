import itertools
import re
import hashlib


def chain(list_of_lists) -> list:
    return list(itertools.chain(*list_of_lists))


def remove_duplicates(l) -> list:
    return list(set(l))


def flatten(l) -> list:
    ret = []
    for e in l:
        if isinstance(e, list):
            ret += flatten(e)
        else:
            ret.append(e)
    return ret


def expression_to_str(expression: list) -> str:
    def expression_elem_to_str(e) -> str:
        if isinstance(e, list):
            return "(" + expression_to_str(e) + ")"
        return str(e)

    expression = [expression_elem_to_str(e) for e in expression]
    return " ".join(expression)


def list_to_tuple(l: list) -> tuple:
    if not isinstance(l, list):
        return l
    ret = []
    for e in l:
        if isinstance(e, list):
            ret.append(list_to_tuple(e))
        else:
            ret.append(e)
    return tuple(ret)


def list_depth(l: list):
    if not isinstance(l, list):
        return 0
    if len(l) == 0:
        return 1
    return 1+list_depth(l[0])


def tuple_to_list(l: tuple) -> list:
    if not isinstance(l, tuple) and not isinstance(l, list):
        return l
    ret = []
    for e in l:
        if isinstance(e, tuple):
            ret.append(tuple_to_list(e))
        else:
            ret.append(e)
    return ret


def types_to_str(t) -> str:
    def elem(e):
        if isinstance(e, tuple):
            e = tuple_to_list(e)
        if hasattr(e, "name"):
            return e.name
        if isinstance(e, list):
            return types_to_str(e)
        return e.__name__
    if not isinstance(t, list):
        return (elem(t))
    return "("+", ".join([elem(e) for e in t])+")"


def fn_type_to_str(t) -> str:
    def elem(e) -> str:
        if hasattr(e, "name"):
            return e.name
        if hasattr(e, "__name__"):
            return e.__name__
        if isinstance(e, list):
            if len(e) == 1:
                return "[" + elem(e[0]) + "]"
            return "(" + fn_type_to_str(e) + ")"
        return str(e)
    return "->".join([elem(e) for e in t])


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def get_hard_fn_name(generic_fn_name: str, fn_type: list) -> str:
    def elem(e):
        if isinstance(e, tuple):
            e = tuple_to_list(e)
        if hasattr(e, "name"):
            return e.name
        if isinstance(e, list):
            return get_hard_fn_name("", e)
        return e.__name__
    if not isinstance(fn_type, list):
        return (elem(fn_type))
    if len(generic_fn_name) > 0:
        generic_fn_name = generic_fn_name+"_"
    return generic_fn_name+md5("BL_"+"_".join([elem(e) for e in fn_type])+"_EL")[:5]


def camelcase_to_snakecase(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
