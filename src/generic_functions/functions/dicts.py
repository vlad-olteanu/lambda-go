from ..generic_function import GenericFunction
from typing import Mapping

from code_generation.types import expand_type

generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


@generic
class DictDeepGet(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 3:
            raise Exception(f"{fn_name} expected 3 arguments")
        [dict_type, path_type, default_value_type] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        if path_type is not str:
            raise Exception(
                f"{fn_name} expected str as the 2nd argument, not {path_type}")
        return argument_types+[default_value_type]

    @staticmethod
    def expand(fn_type):
        # cast interface{} to return type
        return f"dictDeepGet(arg0, arg1, arg2).({expand_type(fn_type[-1])})"


@generic
class DictGetDefault(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 3:
            raise Exception(f"{fn_name} expected 3 arguments")
        [dict_type, path_type, default_value_type] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        if path_type is not str:
            raise Exception(
                f"{fn_name} expected str as the 2nd argument, not {path_type}")
        return argument_types+[default_value_type]

    @staticmethod
    def expand(fn_type):
        # cast interface{} to return type
        return f"dictGetDefault(arg0, arg1, arg2).({expand_type(fn_type[-1])})"

@generic
class DictGet(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) !=2:
            raise Exception(f"{fn_name} expected 2 arguments")
        [dict_type, path_type] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        if path_type is not str:
            raise Exception(
                f"{fn_name} expected str as the 2nd argument, not {path_type}")
        return argument_types+[any]

    @staticmethod
    def expand(fn_type):
        # cast interface{} to return type
        return f"dictGet(arg0, arg1).({expand_type(fn_type[-1])})"

@generic
class DictSet(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 3:
            raise Exception(f"{fn_name} expected 3 arguments")
        [dict_type, path_type, _] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        if path_type is not str:
            raise Exception(
                f"{fn_name} expected str as the 2nd argument, not {path_type}")
        return argument_types+[dict]

    @staticmethod
    def expand(_):
        return "dictSet(arg0, arg1, arg2)"

@generic
class DictDeepSet(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 3:
            raise Exception(f"{fn_name} expected 3 arguments")
        [dict_type, path_type, _] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        if path_type is not str:
            raise Exception(
                f"{fn_name} expected str as the 2nd argument, not {path_type}")
        return argument_types+[dict]

    @staticmethod
    def expand(_):
        return "dictDeepSet(arg0, arg1, arg2)"


@generic
class DictKeys(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        fn_name = cls.get_fn_name()
        if len(argument_types) != 1:
            raise Exception(f"{fn_name} expected 1 argument")
        [dict_type] = argument_types
        if dict_type is not dict:
            raise Exception(
                f"{fn_name} expected dict as the 1st argument, not {dict_type}")
        return argument_types+[[str]]

    @staticmethod
    def expand(_):
        return "dictKeys(arg0)"
