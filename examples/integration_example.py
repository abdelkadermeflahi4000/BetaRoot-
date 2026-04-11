# integration_example.py
import networkx as nx
from betaroot.core.knowledge import KnowledgeBase, FactBase, Rule, RuleType, TruthValue
from betaroot.core.inference.forward_chainer import ForwardChainer
from betaroot.core.inference.backward_chainer import BackwardChainer
from betaroot.core.bayesian_engine import BayesianEngine  # Votre module existant

def hybrid_inference_demo():
    # 1. Base de connaissances (règles symboliques + structure causale)
    kb = KnowledgeBase("medical_kb")
    kb.add_rule(Rule("R1", ["Fever", "Cough"], "PossibleInfection", RuleType.IMPLICATION, 0.9))
    kb.add_rule(Rule("R2", ["PossibleInfection", "HighWBC"], "BacterialInfection", RuleType.CAUSAL, 0.85))
    
    # 2. Base de faits (observations)
    fb = FactBase("patient_01")
    fb.add("Fever", True, TruthValue.TRUE, 0.95, "observation")
    fb.add("Cough", True, TruthValue.TRUE, 0.90, "observation")
    
    # 3. Chaînage avant (déduction automatique)
    print("🔍 Forward Chaining...")
    forward = ForwardChainer(kb, fb)
    new_facts = forward.run()
    for f in new_facts:
        print(f"  → Déduit: {f}")
        
    # 4. Chaînage arrière (vérification d'hypothèse)
    print("\n🎯 Backward Chaining pour 'BacterialInfection'...")
    backward = BackwardChainer(kb, fb)
    proof = backward.prove("BacterialInfection")
    print(backward.explain_proof(proof))
    
    # 5. Passage au Bayésien si la preuve est partielle/inconnue
    if proof.status.value == "unknown" or proof.confidence < 0.7:
        print("\n🔄 Preuve symbolique insuffisante → Fallback Bayésien")
        
        # Construction du graphe causal pour pgmpy (comme dans votre code existant)
        G = nx.DiGraph()
        G.add_edges_from(kb.causal_graph.edges())
        
        # Votre configuration CPD existante
        cpd_config = {
            "Fever": {"values": [0,1], "evidence": [], "values_given_parents": [[0.1],[0.9]]},
            "Cough": {"values": [0,1], "evidence": [], "values_given_parents": [[0.2],[0.8]]},
            "PossibleInfection": {"values": [0,1], "evidence": ["Fever","Cough"], 
                                  "values_given_parents": [[1.0,0.3,0.3,0.05],[0.0,0.7,0.7,0.95]]},
            "HighWBC": {"values": [0,1], "evidence": [], "values_given_parents": [[0.85],[0.15]]},
            "BacterialInfection": {"values": [0,1], "evidence": ["PossibleInfection","HighWBC"],
                                   "values_given_parents": [[1.0,0.4,0.3,0.01],[0.0,0.6,0.7,0.99]]}
        }
        
        engine = BayesianEngine(G)
        engine.build_network(cpd_config)
        
        # Requête bayésienne avec les faits observés
        evidence = {k: v.value for k,v in fb.facts.items() if v.truth == TruthValue.TRUE}
        result = engine.query(["BacterialInfection"], evidence=evidence)
        print(f"   Résultat Bayésien: {result}")

if __name__ == "__main__":
    hybrid_inference_demo()
