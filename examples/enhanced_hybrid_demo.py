# betaroot/examples/enhanced_hybrid_demo.py
from betaroot.core.knowledge.knowledge_base import KnowledgeBase, Rule, RuleType
from betaroot.core.knowledge.fact_base import FactBase, TruthValue
from betaroot.core.inference.orchestrator import InferenceOrchestrator, InferenceStrategy
from betaroot.core.bayesian_engine import BayesianEngine
import networkx as nx

def medical_diagnosis_demo():
    """عرض متكامل: تشخيص طبي مع استدلال هجين ومراجعة معتقدات"""
    
    # 1. بناء قاعدة المعرفة
    kb = KnowledgeBase()
    
    # قواعد طبية (رمزية + سببية)
    kb.add_rule(Rule(
        id="R1", antecedents=["Fever", "Cough"], 
        consequent="PossibleInfection", rule_type=RuleType.IMPLICATION
    ))
    kb.add_rule(Rule(
        id="R2", antecedents=["PossibleInfection", "HighWhiteBloodCells"],
        consequent="BacterialInfection", rule_type=RuleType.CAUSAL, confidence=0.85
    ))
    kb.add_rule(Rule(
        id="R3", antecedents=["PossibleInfection", "RecentTravel"],
        consequent="ViralInfection", rule_type=RuleType.CAUSAL, confidence=0.70
    ))
    
    # 2. بناء الرسم البياني السببي للاستدلال البيزي
    G = nx.DiGraph()
    G.add_edges_from([
        ('Fever', 'PossibleInfection'),
        ('Cough', 'PossibleInfection'),
        ('PossibleInfection', 'BacterialInfection'),
        ('PossibleInfection', 'ViralInfection'),
        ('HighWhiteBloodCells', 'BacterialInfection'),
        ('RecentTravel', 'ViralInfection')
    ])
    
    # 3. تهيئة المحركات
    fb = FactBase()
    bayesian = BayesianEngine(G)
    # ... تعريف CPDs هنا ...
    
    orchestrator = InferenceOrchestrator(kb, fb, bayesian)
    
    # 4. سيناريو: مريض يدخل بأعراض
    print("🏥 مريض جديد: حمى + سعال")
    fb.add("Fever", True, TruthValue.TRUE, confidence=1.0, source="observation")
    fb.add("Cough", True, TruthValue.TRUE, confidence=1.0, source="observation")
    
    # 5. استدلال تلقائي (السلسلة الأمامية)
    results = orchestrator.infer(
        query=["BacterialInfection", "ViralInfection"],
        strategy=InferenceStrategy.SYMBOLIC_FIRST
    )
    
    for var, res in results.items():
        print(f"   {var}: {res.value} (يقين: {res.confidence:.2f}, طريقة: {res.method})")
    
    # 6. دليل جديد: تحاليل الدم
    print("\n🔬 نتيجة التحاليل: كريات دم بيضاء مرتفعة")
    fb.add("HighWhiteBloodCells", True, TruthValue.TRUE, source="lab_result")
    
    # 7. إعادة الاستدلال مع الأدلة الجديدة
    updated = orchestrator.infer(
        query=["BacterialInfection"],
        strategy=InferenceStrategy.PARALLEL_HYBRID
    )
    
    print(f"\n✅ التشخيص المُحدَّث: BacterialInfection = {updated['BacterialInfection'].value}")
    print(f"   درجة اليقين: {updated['BacterialInfection'].confidence:.2%}")
    
    return orchestrator, fb

if __name__ == "__main__":
    medical_diagnosis_demo()
