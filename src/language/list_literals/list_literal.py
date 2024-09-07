from dataclasses import dataclass, field


@dataclass
class ListLiteral:
    list: list
    type: list = field(default=None)

    def __str__(self) -> str:
        return "["+",".join(str(e) for e in self.list)+"]"
