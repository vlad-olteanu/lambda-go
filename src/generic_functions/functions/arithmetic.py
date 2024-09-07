from ..generic_function import GenericFunction
from typing import Mapping

generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


class BinaryArithmetic(GenericFunction):
    @classmethod
    def get_type(cls, argument_types, _):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 2:
            raise Exception(f"{fn_name} expected 2 arguments")
        allowed_argument_types = {int, float}
        for t in argument_types:
            if isinstance(t, list) or t not in allowed_argument_types:
                raise Exception(f"{t} is not allowed for {fn_name}")
        if argument_types[0] is not argument_types[1]:
            raise Exception(
                f"{fn_name} doesn't support {argument_types[0].__name__} and {argument_types[1].__name__}. Cast them before the operation.")
        if float in argument_types:
            return [float, float, float]
        return [int, int, int]


@generic
class Add(BinaryArithmetic):
    @staticmethod
    def expand(_):
        return "arg0 + arg1"


@generic
class Sub(BinaryArithmetic):
    @staticmethod
    def expand(_):
        return "arg0 - arg1"


@generic
class Mul(BinaryArithmetic):
    @staticmethod
    def expand(_):
        return "arg0 * arg1"


@generic
class Div(BinaryArithmetic):
    @staticmethod
    def expand(_):
        return "arg0 / arg1"


@generic
class Mod(GenericFunction):
    @classmethod
    def get_type(cls, argument_types, _):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        allowed_argument_types = {int}
        for t in argument_types:
            if isinstance(t, list) or t not in allowed_argument_types:
                raise Exception(f"{t} is not allowed for {cls.get_fn_name()}")
        return argument_types+[int]

    @staticmethod
    def expand(_):
        return r"arg0 % arg1"
