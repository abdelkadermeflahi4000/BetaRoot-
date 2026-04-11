from betaroot.core.knowledge_base import KnowledgeBase
from betaroot.core.reasoning_engine import ReasoningEngine
from betaroot.core.self_learning import SelfLearningEngine

kb = KnowledgeBase()

# فقط fact واحد (ناقص)
kb.add_fact({
    "subject": "smoking",
    "predicate": "causes",
    "value": "cancer",
    "confidence": 1.0
})

engine = ReasoningEngine(kb, causal_graph=kb.graph)
learner = SelfLearningEngine(kb, engine)

query = {
    "subject": "smoking",
    "predicate": "causes"
}

# النظام سيسأل
result = engine.reason(query)

print("Questions:")
for q in result["questions"]:
    print("-", q)

# نعطيه جواب خارجي
external_answers = {
    "What intermediate steps connect 'smoking' to 'cancer'?": "lung_damage"
}

# يبدأ التعلم
learning_result = learner.learn(query, external_answers)

print("\nLearned:")
print(learning_result)
