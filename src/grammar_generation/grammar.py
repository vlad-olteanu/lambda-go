from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class Grammar:
    productions: List[List[str]]
    symbols: Set[str]
    terminals: Set[str]
    non_terminals: Set[str]