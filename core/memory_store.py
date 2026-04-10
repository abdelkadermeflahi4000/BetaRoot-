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
