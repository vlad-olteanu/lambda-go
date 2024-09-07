from dataclasses import dataclass
from utils import expression_to_str
from language.identifiers import Identifier

@dataclass
class FunctionDefinition:
    name: Identifier
    parameters: list
    condition: list
    expression: list

    def __str__(self):
        condition = f"| {expression_to_str(self.condition)}" if self.condition else ""
        parameters = expression_to_str(self.parameters)
        expression = expression_to_str(self.expression)
        return f"{self.name} {parameters} {condition} = {expression}"


@dataclass
class FunctionTypeDeclaration:
    name: Identifier
    type: list

    def __str__(self)->str:
        def type_elem_to_str(e)->str:
            if isinstance(e, list):
                return "[" + ", ".join([type_elem_to_str(x) for x in e]) + "]"
            return str(e)
        return f"{self.name}::{'->'.join(type_elem_to_str(e) for e in self.type)}"
