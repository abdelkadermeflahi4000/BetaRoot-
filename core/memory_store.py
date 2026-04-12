from dataclasses import dataclass
from typing import List


@dataclass
class Fact:
    subject: str
    predicate: str
    object: str


@dataclass
class Rule:
    category: str
    consequence: str


class MemoryStore:
    def __init__(self):
        self.facts: List[Fact] = []
        self.rules: List[Rule] = []

    def add_fact(self, subject, predicate, obj):
        self.facts.append(Fact(subject, predicate, obj))

    def add_rule(self, category, consequence):
        self.rules.append(Rule(category, consequence))

    def get_facts(self):
        return self.facts

    def get_rules(self):
        return self.rules

def add_biophoton_tokens(self, tokens):
    for token in tokens:
        self.add_fact(
            content=f"freq_bin={token['freq_bin']}, amp={token['amplitude']:.3f}",
            fact_type="biophoton",
            mode="alpha",  # exploratory by default
            confidence=0.5
        )
