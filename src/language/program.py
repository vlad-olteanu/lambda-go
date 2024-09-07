from dataclasses import dataclass
from typing import List

from .identifiers import Identifier
from .functions import Function
from .functions import HardFunction


@dataclass
class Program:
    functions: List[Function]
    hard_functions: List[HardFunction]

    def __str__(self):
        return "\n".join([
            f"{e}\n" for e in
            self.functions 
        ])

    def has_function(self, identifier: Identifier) -> bool:
        return identifier in {fn.name for fn in self.functions+self.hard_functions}

    def get_fn_type(self, name: Identifier) -> list:
        if not self.has_function(name):
            raise Exception(f"Function not found: {name}")
        return [fn.type for fn in self.functions+self.hard_functions if fn.name == name][0]
