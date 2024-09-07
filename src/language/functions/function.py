from dataclasses import dataclass
from typing import List
from language.identifiers import Identifier
from utils import expression_to_str, fn_type_to_str


@dataclass
class FunctionDefinition:
    parameters: list
    condition: list
    expression: list

    def __str__(self):
        condition = f"| {expression_to_str(self.condition)}" if self.condition else ""
        parameters = expression_to_str(self.parameters)
        expression = expression_to_str(self.expression)
        return f"{parameters} {condition} = {expression}"


@dataclass
class Function:
    name: Identifier
    type: list
    definitions: List[FunctionDefinition]

    def __str__(self):
        type_declaration = f"{self.name}::{fn_type_to_str(self.type)}"
        definitions = [f"{self.name} {fn_def}" for fn_def in self.definitions]
        return "\n".join([type_declaration]+definitions)
