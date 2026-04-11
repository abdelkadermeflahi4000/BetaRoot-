from typing import TypedDict


class Fact(TypedDict):
    subject: str
    predicate: str
    value: any
    confidence: float
    source: str
