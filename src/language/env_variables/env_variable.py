from dataclasses import dataclass


@dataclass
class EnvVariable:
    name: str

    def __str__(self):
        return f"${self.name}"