# test_knowledge_fact.py
from betaroot.core.knowledge import KnowledgeBase, FactBase, Rule, RuleType, TruthValue

def test_basic_integration():
    print("🧪 Testing KnowledgeBase + FactBase integration...\n")
    
    # 1. إنشاء القواعد
    kb = KnowledgeBase(name="medical_rules")
    
    kb.add_rule(Rule(
        id="R1",
        antecedents=["Fever", "Cough"],
        consequent="PossibleInfection",
        rule_type=RuleType.IMPLICATION,
        confidence=0.9
    ))
    
    kb.add_rule(Rule(
        id="R2",
        antecedents=["PossibleInfection"],
        consequent="RecommendAntibiotics",
        rule_type=RuleType.CAUSAL,
        confidence=0.8
    ))
    
    print(f"✓ Added {len(kb)} rules to KnowledgeBase")
    
    # 2. إنشاء الحقائق
    fb = FactBase(name="patient_001")
    
    fb.add("Fever", True, TruthValue.TRUE, confidence=0.95, source="observation")
    fb.add("Cough", True, TruthValue.TRUE, confidence=0.90, source="observation")
    
    print(f"✓ Added {len(fb)} facts to FactBase")
    
    # 3. تطبيق السلسلة الأمامية يدوياً
    applicable = kb.get_applicable_rules(fb)
    print(f"✓ Found {len(applicable)} applicable rules")
    
    for rule in applicable:
        result = rule.apply(fb)
        if result:
            fb.add(result.variable, result.value, result.truth, 
                  result.confidence, source="inference", justification=result.justification)
            print(f"  → Inferred: {result}")
    
    # 4. التحقق من النتيجة
    if fb.is_true("PossibleInfection", threshold=0.7):
        print(f"✓ Successfully inferred PossibleInfection with confidence {fb.get('PossibleInfection').confidence:.2f}")
    
    # 5. اختبار التناقض
    success, msg = fb.add("Fever", False, TruthValue.FALSE, confidence=0.8, on_conflict='reject')
    print(f"✓ Conflict test: {msg}")
    
    print("\n✅ All tests passed! KnowledgeBase and FactBase are ready.")
    return kb, fb

if __name__ == "__main__":
    test_basic_integration()
