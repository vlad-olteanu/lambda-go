from ..generic_function import GenericFunction
from typing import Mapping

generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


@generic
class StartsWith(GenericFunction):
    @staticmethod
    def get_type(_, __):
        return [str, str, bool]

    @staticmethod
    def expand(_, __):
        return "startsWith(arg0, arg1)"


@generic
class Contains(GenericFunction):
    @staticmethod
    def get_type(_, __):
        return [str, str, bool]

    @staticmethod
    def expand(_):
        return "contains(arg0, arg1)"


@generic
class ReMatch(GenericFunction):
    @staticmethod
    def get_type(_, __):
        return [str, str, bool]

    @staticmethod
    def expand(_):
        return "reMatch(arg0, arg1)"
