from betaroot.core.knowledge_base import KnowledgeBase
from betaroot.core.reasoning_engine import ReasoningEngine

kb = KnowledgeBase()

# إضافة بيانات
kb.add_fact({
    "subject": "smoking",
    "predicate": "causes",
    "value": "cancer",
    "confidence": 1.0
})

engine = ReasoningEngine(kb)

query = {
    "subject": "smoking",
    "predicate": "causes"
}

result = engine.reason(query)

print(result)
