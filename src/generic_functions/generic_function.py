from utils import camelcase_to_snakecase


class GenericFunction:
    @staticmethod
    def expand(fn_type: list):
        raise Exception("Not implemented")

    @staticmethod
    def get_type(argument_types: list):
        raise Exception("Not implemented")

    @classmethod
    def get_fn_name(cls):
        return camelcase_to_snakecase(cls.__name__)
