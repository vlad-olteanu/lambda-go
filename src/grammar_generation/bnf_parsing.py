from typing import List, Set
from .grammar import Grammar
from utils import chain, remove_duplicates
import re


def parse_bnf(text: str) -> Grammar:
    """
        grammar file content => (productions, symbols, terminals)
    """
    # remove comments
    text = re.sub("#.*", "", text)
    productions = text.split("\n\n")
    productions = [p.strip() for p in productions]
    productions = [p for p in productions if len(p) > 0]

    def production_str_to_productions(production: str) -> List[List[str]]:
        """
            "A ::= B C | C D"  => [["A", "B", "C"], ["A", "C", "D"]]
        """
        left_side, right_side = [s.strip() for s in production.split("::=")]
        right_sides = [[e.strip() for e in s.split()]
                    for s in right_side.split("|")]
        productions = [[left_side]+right_side for right_side in right_sides]
        return productions
    
    def remove_epsilon(production):
        return [e for e in production  if e!="EPSILON"]

    productions = chain([production_str_to_productions(p) for p in productions])
    productions = [remove_epsilon(p) for p in productions]
    symbols = set(chain(productions))
    non_terminals = set([p[0] for p in productions])
    terminals = [s for s in symbols if s not in non_terminals]

    return Grammar(productions, symbols, terminals, non_terminals)
