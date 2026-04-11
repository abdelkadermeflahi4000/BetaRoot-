from betaroot.core.knowledge_base import KnowledgeBase
from betaroot.core.reasoning_engine import ReasoningEngine

kb = KnowledgeBase()

kb.add_fact({
    "subject": "smoking",
    "predicate": "causes",
    "value": "lung_damage",
    "confidence": 1.0
})

kb.add_fact({
    "subject": "lung_damage",
    "predicate": "causes",
    "value": "cancer",
    "confidence": 1.0
})

engine = ReasoningEngine(kb, causal_graph=kb.graph)

query = {
    "subject": "smoking",
    "predicate": "causes"
}

result = engine.reason(query)

print("\n=== ANSWER ===")
print(result["answer"])

print("\n=== EXPLANATION ===")
print(result["explanation"])
