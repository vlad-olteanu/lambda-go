from ..generic_function import GenericFunction
from typing import Mapping

generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


class BinaryLogical(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) == 1:
            return [argument_types[0], argument_types[0], bool]
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        return argument_types+[bool]

class BinaryLogicalBool(GenericFunction):
    @staticmethod
    def get_type(_):
        return [bool, bool, bool]

@generic
class Neq(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 != arg1"


@generic
class Eq(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 == arg1"


@generic
class Gt(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 > arg1"


@generic
class Gte(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 >= arg1"


@generic
class Lt(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 < arg1"


@generic
class Lte(BinaryLogical):
    @staticmethod
    def expand(_):
        return "arg0 <= arg1"


@generic
class And(BinaryLogicalBool):
    @staticmethod
    def expand(_):
        return "arg0 && arg1"


@generic
class Or(BinaryLogicalBool):
    @staticmethod
    def expand(_):
        return "arg0 || arg1"
