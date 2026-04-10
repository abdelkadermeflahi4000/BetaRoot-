--- betaroot/core/bayesian_engine.py (原始)


+++ betaroot/core/bayesian_engine.py (修改后)
"""
Bayesian Engine for BetaRoot
----------------------------
This module integrates Probabilistic Causal Inference into the BetaRoot symbolic core.
It converts causal graphs (DAGs) into Bayesian Networks and performs exact inference.

Philosophy:
- Symbolic Logic (Unary) is the default (Certainty = 1.0 or 0.0).
- Bayesian Inference is the fallback for uncertainty, providing calculated probabilities
  rather than hallucinations.
"""

import networkx as nx
from typing import Dict, List, Optional, Tuple, Any
try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
except ImportError:
    raise ImportError("pgmpy is required for Bayesian inference. Install via: pip install pgmpy")

class BayesianEngine:
    """
    Handles the construction and inference of Bayesian Networks
    based on BetaRoot's causal graph structure.
    """

    def __init__(self, causal_graph: nx.DiGraph):
        """
        Initialize the engine with a NetworkX DiGraph representing causal relations.

        Args:
            causal_graph: A directed acyclic graph where nodes are variables
                          and edges represent causal dependencies.
        """
        self.causal_graph = causal_graph
        self.bn_model: Optional[BayesianNetwork] = None
        self.inference_engine: Optional[VariableElimination] = None
        self.cpds: Dict[str, TabularCPD] = {}

        # Validate DAG
        if not nx.is_directed_acyclic_graph(causal_graph):
            raise ValueError("The provided causal graph must be a Directed Acyclic Graph (DAG).")

    def build_network(self, cpd_definitions: Dict[str, Dict]) -> None:
        """
        Constructs the Bayesian Network model and loads Conditional Probability Distributions (CPDs).

        Args:
            cpd_definitions: A dictionary defining the CPD for each node.
                             Format: {
                                'NodeName': {
                                    'values': [0, 1], # e.g., [No, Yes]
                                    'evidence': ['Parent1', 'Parent2'],
                                    'values_given_parents': [[...], [...]] # Columns for each evidence combo
                                }
                             }
        """
        # 1. Define the structure
        edges = list(self.causal_graph.edges())
        self.bn_model = BayesianNetwork(edges)

        # 2. Add CPDs
        for node, config in cpd_definitions.items():
            evidence = config.get('evidence', [])
            values = config.get('values', [0, 1])
            cardinality = len(values)

            # Calculate number of columns needed (product of parents' cardinalities)
            # Assuming binary parents for simplicity in this demo, can be generalized
            n_states_parents = 1
            for parent in evidence:
                # Assume parents are binary if not specified, or retrieve from a global schema
                n_states_parents *= 2

            values_matrix = config.get('values_given_parents')

            if not values_matrix:
                raise ValueError(f"Missing probability table for node {node}")

            cpd = TabularCPD(
                variable=node,
                variable_card=cardinality,
                values=values_matrix,
                evidence=evidence,
                evidence_card=[2] * len(evidence) # Assuming binary parents
            )
            self.bn_model.add_cpds(cpd)
            self.cpds[node] = cpd

        # Validate the model
        if not self.bn_model.check_model():
            raise ValueError("The constructed Bayesian Network model is invalid.")

        # Initialize Inference Engine
        self.inference_engine = VariableElimination(self.bn_model)

    def query(self, query_vars: List[str], evidence: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """
        Perform exact inference using Variable Elimination.

        Args:
            query_vars: List of variables to compute probability for.
            evidence: Dictionary of observed evidence {Variable: Value}.

        Returns:
            Dictionary mapping variable states to their probabilities.
        """
        if not self.inference_engine:
            raise RuntimeError("Bayesian Network not built yet. Call build_network() first.")

        result = self.inference_engine.query(variables=query_vars, evidence=evidence)

        # Format output as a simple dictionary
        prob_dict = {}

        # In newer pgmpy, result is a DiscreteFactor directly when querying single var
        # or a list of factors for multiple vars
        if len(query_vars) == 1:
            var = query_vars[0]
            # result is the factor for that variable
            values = result.values
            state_names = [0, 1]  # Default binary states

            for i, val in enumerate(values):
                prob_dict[f"{var}={state_names[i]}"] = float(val)
        else:
            # For multiple variables, iterate through result factors
            for factor in result:
                var = factor.variables[0]
                values = factor.values
                state_names = [0, 1]
                for i, val in enumerate(values):
                    prob_dict[f"{var}={state_names[i]}"] = float(val)

        return prob_dict

    def explain_inference(self, query_vars: List[str], evidence: Optional[Dict[str, Any]] = None) -> str:
        """
        Generates a textual explanation of the inference result.
        """
        probs = self.query(query_vars, evidence)
        explanation = "Bayesian Inference Result:\n"

        if evidence:
            ev_str = ", ".join([f"{k}={v}" for k, v in evidence.items()])
            explanation += f"Given evidence: [{ev_str}]\n"
        else:
            explanation += "Without specific evidence (Prior probabilities):\n"

        for q_var in query_vars:
            explanation += f"\nProbabilities for {q_var}:\n"
            for state, prob in probs.items():
                if state.startswith(f"{q_var}="):
                    explanation += f"  - {state}: {prob:.4f}\n"

        return explanation

class HybridSymbolicProbabilisticSolver:
    """
    Combines BetaRoot's Unary Logic with Bayesian Inference.
    Strategy: Try symbolic deduction first. If confidence < 1.0 or unknown, use Bayesian.
    """

    def __init__(self, causal_graph: nx.DiGraph, unary_logic_engine=None):
        self.graph = causal_graph
        self.bayesian_engine = BayesianEngine(causal_graph)
        self.unary_engine = unary_logic_engine # Placeholder for existing BetaRoot logic

    def solve(self, hypothesis: str, evidence: Dict, cpd_data: Dict) -> Dict:
        """
        Attempt to solve using logic, fallback to probability.
        """
        result = {
            "method": "",
            "confidence": 0.0,
            "result": None,
            "explanation": ""
        }

        # 1. Try Unary Logic (Simulated here)
        # In real BetaRoot, this would call unary_logic.py
        # If logic proves it 100% (True/False), we stop there.
        logical_result = self._try_unary_deduction(hypothesis, evidence)

        if logical_result['certainty'] == 1.0:
            result['method'] = "Symbolic Unary Logic"
            result['confidence'] = 1.0
            result['result'] = logical_result['value']
            result['explanation'] = "Deduced with absolute certainty via symbolic logic."
            return result

        # 2. Fallback to Bayesian Inference
        # Build network dynamically if not already done
        if not self.bayesian_engine.bn_model:
            self.bayesian_engine.build_network(cpd_data)

        # Map hypothesis to variable name (simplified)
        query_var = hypothesis
        bayes_probs = self.bayesian_engine.query([query_var], evidence)

        # Find max probability
        max_state = max(bayes_probs, key=bayes_probs.get)
        max_prob = bayes_probs[max_state]

        result['method'] = "Bayesian Probabilistic Inference"
        result['confidence'] = max_prob
        result['result'] = max_state
        result['explanation'] = self.bayesian_engine.explain_inference([query_var], evidence)

        return result

    def _try_unary_deduction(self, hypothesis: str, evidence: Dict) -> Dict:
        """
        Mock implementation of Unary Logic check.
        Returns certainty=1.0 only if logically proven, else 0.0
        """
        # Placeholder: In real integration, this calls BetaRoot's existing logic core
        # For now, assume logic fails to prove everything to demonstrate Bayesian fallback
        return {"certainty": 0.0, "value": None}

# Example Usage: Rain-Sprinkler-Grass Network
if __name__ == "__main__":
    # 1. Create Causal Graph (as BetaRoot would)
    G = nx.DiGraph()
    G.add_edges_from([('Rain', 'GrassWet'), ('Sprinkler', 'GrassWet')])

    # 2. Define CPDs (Conditional Probability Distributions)
    # P(Rain) = 0.2
    # P(Sprinkler) = 0.3
    # P(GrassWet | Rain, Sprinkler) defined by table

    cpd_config = {
        'Rain': {
            'values': [0, 1], # 0=No, 1=Yes
            'evidence': [],
            'values_given_parents': [[0.8], [0.2]] # P(R=0), P(R=1)
        },
        'Sprinkler': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.7], [0.3]] # P(S=0), P(S=1)
        },
        'GrassWet': {
            'values': [0, 1],
            'evidence': ['Rain', 'Sprinkler'],
            # Columns order: R=0,S=0 | R=1,S=0 | R=0,S=1 | R=1,S=1
            # P(G=0 | ...)
            'values_given_parents': [
                [1.0, 0.1, 0.2, 0.01], # P(G=0 | ...)
                [0.0, 0.9, 0.8, 0.99]  # P(G=1 | ...)
            ]
        }
    }

    # 3. Initialize Engine
    engine = BayesianEngine(G)
    engine.build_network(cpd_config)

    # 4. Query: Given Grass is Wet (1), what is probability of Rain (1)?
    print("--- Bayesian Inference Demo ---")
    print(engine.explain_inference(['Rain'], evidence={'GrassWet': 1}))

    # 5. Hybrid Solver Demo
    print("\n--- Hybrid Solver Demo ---")
    solver = HybridSymbolicProbabilisticSolver(G)
    # Simulate a case where logic fails (certainty < 1)
    res = solver.solve('Rain', {'GrassWet': 1}, cpd_config)
    print(f"Method: {res['method']}")
    print(f"Confidence: {res['confidence']:.4f}")
    print(f"Result: {res['result']}")