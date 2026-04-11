from betaroot.core.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# --------------------------
# ✅ 1. Fact صحيح
# --------------------------
fact1 = {
    "subject": "smoking",
    "predicate": "causes",
    "value": "cancer",
    "confidence": 1.0,
}

kb.add_fact(fact1)


# --------------------------
# ❌ 2. Fact متناقض
# --------------------------
fact2 = {
    "subject": "smoking",
    "predicate": "causes",
    "value": "no_cancer",
    "confidence": 1.0,
}

kb.add_fact(fact2)


# --------------------------
# ❌ 3. Fact ضعيف confidence
# --------------------------
fact3 = {
    "subject": "water",
    "predicate": "boils_at",
    "value": "100C",
    "confidence": 0.0,
}

kb.add_fact(fact3)
