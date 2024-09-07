from language.identifiers import Identifier
from dataclasses import dataclass
from utils import fn_type_to_str

@dataclass
class HardFunction:
    name: Identifier
    type: list
    generic_name: str
    "The name of the generic fn the hard function was extracted from"

    def __str__(self)->str:
        return f"{self.generic_name}::{fn_type_to_str(self.type)}"