from dataclasses import dataclass, field
from frozendict import frozendict

@dataclass(frozen=True, unsafe_hash=True)
class Identifier:
    name: str
    metadata: dict = field(default_factory=frozendict)

    def __str__(self):
        return self.name
