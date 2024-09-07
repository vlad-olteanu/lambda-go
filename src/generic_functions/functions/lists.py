from ..generic_function import GenericFunction
from typing import Mapping
from utils import list_to_tuple
from code_generation.types import expand_type
generic_functions: Mapping[str, type] = {}


def generic(cls):
    generic_functions[cls.get_fn_name()] = cls
    return cls


@generic
class Concat(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        return argument_types+[argument_types[0]]

    @staticmethod
    def expand(fn_type):
        if fn_type[0] is str and fn_type[1] is str:
            return "concatStr(arg0, arg1)"
        return "append(arg0, arg1...)"


@generic
class Len(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 1:
            raise Exception(f"{cls.get_fn_name()} expected 1 argument")
        return argument_types+[int]

    @staticmethod
    def expand(fn_type):
        return "len(arg0)"


@generic
class Append(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        if list_to_tuple(argument_types[0][0]) != list_to_tuple(argument_types[1]):
            raise Exception(f"Element type does not match list type: {list_to_tuple(argument_types[0])} {list_to_tuple(argument_types[1])}")
        return argument_types+[argument_types[0]]

    @staticmethod
    def expand(_):
        return "append(arg0, arg1)"

@generic
class Idx(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        if not isinstance(argument_types[0], list):
            raise Exception(f"{cls.get_fn_name()} expected a list as the first argument")
        if argument_types[1] is not int:
            raise Exception(f"{cls.get_fn_name()} expected an int as the second argument")
        return argument_types+[argument_types[0][0]]

    @staticmethod
    def expand(_):
        return "arg0[arg1]"

@generic
class Map(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        fn_type, list_type = argument_types[0], argument_types[1]
        if not isinstance(list_type, list) or len(list_type) != 1:
            raise Exception(
                f"Map expects the second argument to be a list, not {list_type}")
        if not isinstance(fn_type, list) or len(fn_type) != 2:
            raise Exception(
                f"Map expects the first argument to be a single argument function, not {fn_type}")
        if not list_to_tuple(list_type[0]) == list_to_tuple(fn_type[0]):
            raise Exception(
                f"Map expects the function's argument type to match the list's element type")
        return argument_types+[[fn_type[1]]]

    @staticmethod
    def expand(fn_type: list):
        """
        func map_1(fn func(int) string, l1 []int) []string {
            ret := []string{}
            for _, e := range l1 {
                ret = append(ret, fn(e))
            }
            return ret
        }
        """

        return "\n".join([
            f"func () {expand_type(fn_type[-1])}" +"{"+
            f"  ret := {expand_type(fn_type[-1])}"+"{}",
            """
                for _, e := range arg1 {
                    ret = append(ret, arg0(e))
                }
                return ret
            }()
            """
        ])


@generic
class Filter(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 2:
            raise Exception(f"{cls.get_fn_name()} expected 2 arguments")
        fn_type, list_type = argument_types[0], argument_types[1]
        if not isinstance(list_type, list) or len(list_type) != 1:
            raise Exception(
                f"Filter expects the second argument to be a list, not {list_type}")
        if not isinstance(fn_type, list) or len(fn_type) != 2:
            raise Exception(
                f"Filter expects the first argument to be a single argument function, not {fn_type}")
        if not list_to_tuple(list_type[0]) == list_to_tuple(fn_type[0]):
            raise Exception(
                f"Filter expects the function's argument type to match the list's element type")
        if fn_type[1] is not bool:
            raise Exception(
                "Filter expects a function whose return value is a bool")
        return argument_types+[list_type]

    @staticmethod
    def expand(fn_type: list):
        """ 
        func filter_1(fn func(int) bool, l1 []int) []int {
            ret := []int{}
            for _, e := range l1 {
                if fn(e) {
                    ret = append(ret, e)
                }
            }
            return ret
        }
        """

        return "\n".join([

            f"func () {expand_type(fn_type[1])}" +"{"+
            f"  ret := {expand_type(fn_type[1])}"+"{}",
            """
                for _, e := range arg1 {
                    if arg0(e) {
                        ret = append(ret, e)
                    }
                }
                return ret
            }()
            """
        ])


@generic
class Reduce(GenericFunction):
    @classmethod
    def get_type(cls, argument_types: list, metadata: dict):
        if len(argument_types) != 3:
            raise Exception(f"{cls.get_fn_name()} expected 3 arguments")

        fn_type, list_type, acc_type = argument_types[0], argument_types[1], argument_types[2]
        if not isinstance(list_type, list) or len(list_type) != 1:
            raise Exception(
                f"Reduce expects the second argument to be a list, not {list_type}"
            )

        if not isinstance(fn_type, list) or len(fn_type) != 3:
            raise Exception(
                f"Reduce expects the first argument to be a 2 argument function, not {fn_type}"
            )

        if list_to_tuple(fn_type[0]) != list_to_tuple(list_type[0]):
            raise Exception(
                f"Reduce expects the function's first argument type to match the list's element type"
            )

        if list_to_tuple(fn_type[1]) != list_to_tuple(acc_type):
            raise Exception(
                f"Reduce expects the function's second argument type to match the accumulator's type"
            )

        if list_to_tuple(fn_type[2]) != list_to_tuple(acc_type):
            raise Exception(
                f"Reduce expects the function's return value type to match the accumulator's type"
            )

        return argument_types+[acc_type]

    @staticmethod
    def expand(fn_type: list):
        """ 
        func reduce_1(fn func(int) func(int) int, l []int, acc int) int {
            for _, e := range l {
                acc = fn(e)(acc)
            }
            return acc
        }
        """

        return "\n".join([
            f"func () {expand_type(fn_type[2])}" +"""{
                for _, e := range arg1 {
                    arg2 = arg0(e)(arg2)
                }
                return arg2
            }()
            """
        ])

