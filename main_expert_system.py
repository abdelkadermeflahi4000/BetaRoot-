# betaroot/main_expert_system.py
import networkx as nx
from betaroot.core.knowledge import KnowledgeBase, FactBase, Rule, RuleType, TruthValue
from betaroot.core.inference.orchestrator import InferenceOrchestrator
from betaroot.core.bayesian_engine import BayesianEngine
from betaroot.ui.cli_expert_system import ExpertSystemCLI

def boot_medical_expert_system():
    print("🚀 جاري تحميل النظام الخبير الطبي...")
    
    # 1. قاعدة المعرفة
    kb = KnowledgeBase("medical_diagnosis")
    kb.add_rule(Rule("R1", ["Fever", "Cough"], "PossibleInfection", RuleType.IMPLICATION, 0.9))
    kb.add_rule(Rule("R2", ["PossibleInfection", "HighWBC"], "BacterialInfection", RuleType.CAUSAL, 0.85))
    
    # 2. قاعدة الحقائق
    fb = FactBase("session_001")
    fb.add("Fever", True, TruthValue.TRUE, 0.95, "observation")
    fb.add("Cough", True, TruthValue.TRUE, 0.90, "observation")
    
    # 3. المحرك الهجين (رمزي + بيزي)
    bayesian = BayesianEngine(kb.causal_graph)
    cpd_config = {
        "Fever": {"values":[0,1],"evidence":[],"values_given_parents":[[0.9],[0.1]]},
        "Cough": {"values":[0,1],"evidence":[],"values_given_parents":[[0.8],[0.2]]},
        "PossibleInfection": {"values":[0,1],"evidence":["Fever","Cough"],
                              "values_given_parents":[[1.0,0.3,0.3,0.05],[0.0,0.7,0.7,0.95]]},
        "HighWBC": {"values":[0,1],"evidence":[],"values_given_parents":[[0.85],[0.15]]},
        "BacterialInfection": {"values":[0,1],"evidence":["PossibleInfection","HighWBC"],
                               "values_given_parents":[[1.0,0.4,0.3,0.01],[0.0,0.6,0.7,0.99]]}
    }
    bayesian.build_network(cpd_config)
    
    orchestrator = InferenceOrchestrator(kb, fb, bayesian)
    
    # 4. تشغيل الواجهة
    cli = ExpertSystemCLI(kb, fb, orchestrator)
    cli.run()

if __name__ == "__main__":
    boot_medical_expert_system()
