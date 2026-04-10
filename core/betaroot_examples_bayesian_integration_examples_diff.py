--- betaroot/examples/bayesian_integration_examples.py (原始)


+++ betaroot/examples/bayesian_integration_examples.py (修改后)
"""
BetaRoot Bayesian Integration Examples
======================================
This file demonstrates practical applications of the Bayesian Engine
integrated with BetaRoot's symbolic causal graphs.

Examples:
1. Rain-Sprinkler-Grass (Classic Causal Network)
2. Medical Diagnosis (Symptoms → Diseases)
3. Scientific Method Simulation (Hypothesis Testing with Bayesian Updates)
"""

import sys
sys.path.insert(0, '/workspace/betaroot/core')

from bayesian_engine import BayesianEngine, HybridSymbolicProbabilisticSolver
import networkx as nx


def example_1_rain_sprinkler():
    """
    Classic example: Rain and Sprinkler causing Wet Grass.
    Demonstrates diagnostic inference: Given wet grass, what caused it?
    """
    print("="*60)
    print("EXAMPLE 1: Rain-Sprinkler-Grass Network")
    print("="*60)

    # Build causal graph
    G = nx.DiGraph()
    G.add_edges_from([('Rain', 'GrassWet'), ('Sprinkler', 'GrassWet')])

    # Define Conditional Probability Distributions (CPDs)
    cpd_config = {
        'Rain': {
            'values': [0, 1],  # 0=No, 1=Yes
            'evidence': [],
            'values_given_parents': [[0.8], [0.2]]  # P(Rain=No)=0.8, P(Rain=Yes)=0.2
        },
        'Sprinkler': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.7], [0.3]]  # P(Sprinkler=No)=0.7, P(Sprinkler=Yes)=0.3
        },
        'GrassWet': {
            'values': [0, 1],
            'evidence': ['Rain', 'Sprinkler'],
            # Columns: R=0,S=0 | R=1,S=0 | R=0,S=1 | R=1,S=1
            'values_given_parents': [
                [1.0, 0.1, 0.2, 0.01],   # P(GrassWet=No | ...)
                [0.0, 0.9, 0.8, 0.99]    # P(GrassWet=Yes | ...)
            ]
        }
    }

    engine = BayesianEngine(G)
    engine.build_network(cpd_config)

    # Query 1: Prior probability of rain
    print("\n[Query 1] What is the prior probability of rain?")
    print(engine.explain_inference(['Rain']))

    # Query 2: Diagnostic inference - Given wet grass, probability of rain?
    print("\n[Query 2] The grass is wet. What is the probability it rained?")
    print(engine.explain_inference(['Rain'], evidence={'GrassWet': 1}))

    # Query 3: Explaining away effect
    print("\n[Query 3] The grass is wet AND the sprinkler was on. Probability of rain?")
    print("(Notice how knowing the sprinkler was on reduces the probability of rain)")
    print(engine.explain_inference(['Rain'], evidence={'GrassWet': 1, 'Sprinkler': 1}))

    return engine


def example_2_medical_diagnosis():
    """
    Medical diagnosis example: Diseases cause symptoms.
    Demonstrates diagnostic reasoning under uncertainty.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Medical Diagnosis Network")
    print("="*60)

    # Build causal graph: Diseases → Symptoms
    G = nx.DiGraph()
    G.add_edges_from([
        ('Flu', 'Fever'),
        ('Flu', 'Cough'),
        ('Allergy', 'Sneezing'),
        ('Allergy', 'Cough'),
        ('Cold', 'Fever'),
        ('Cold', 'Sneezing')
    ])

    # CPDs
    cpd_config = {
        'Flu': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.95], [0.05]]  # 5% prevalence
        },
        'Allergy': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.8], [0.2]]  # 20% prevalence
        },
        'Cold': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.9], [0.1]]  # 10% prevalence
        },
        'Fever': {
            'values': [0, 1],
            'evidence': ['Flu', 'Cold'],
            'values_given_parents': [
                [0.99, 0.3, 0.3, 0.01],   # P(Fever=No | Flu, Cold)
                [0.01, 0.7, 0.7, 0.99]    # P(Fever=Yes | Flu, Cold)
            ]
        },
        'Cough': {
            'values': [0, 1],
            'evidence': ['Flu', 'Allergy'],
            'values_given_parents': [
                [0.95, 0.4, 0.4, 0.1],    # P(Cough=No | Flu, Allergy)
                [0.05, 0.6, 0.6, 0.9]     # P(Cough=Yes | Flu, Allergy)
            ]
        },
        'Sneezing': {
            'values': [0, 1],
            'evidence': ['Allergy', 'Cold'],
            'values_given_parents': [
                [0.95, 0.2, 0.2, 0.05],   # P(Sneezing=No | Allergy, Cold)
                [0.05, 0.8, 0.8, 0.95]    # P(Sneezing=Yes | Allergy, Cold)
            ]
        }
    }

    engine = BayesianEngine(G)
    engine.build_network(cpd_config)

    # Query: Patient has fever and cough. What's the most likely disease?
    print("\n[Query] Patient presents with Fever and Cough.")
    print("What is the probability of Flu?")
    print(engine.explain_inference(['Flu'], evidence={'Fever': 1, 'Cough': 1}))

    print("\nWhat is the probability of Allergy?")
    print(engine.explain_inference(['Allergy'], evidence={'Fever': 1, 'Cough': 1}))

    print("\nWhat is the probability of Cold?")
    print(engine.explain_inference(['Cold'], evidence={'Fever': 1, 'Cough': 1}))

    return engine


def example_3_hybrid_solver():
    """
    Demonstrates the Hybrid Symbolic-Probabilistic Solver.
    Shows fallback from symbolic logic to Bayesian inference.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Hybrid Symbolic-Probabilistic Solver")
    print("="*60)

    # Simple causal graph
    G = nx.DiGraph()
    G.add_edges_from([('BatteryDead', 'CarNotStart'), ('NoGas', 'CarNotStart')])

    cpd_config = {
        'BatteryDead': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.9], [0.1]]
        },
        'NoGas': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.95], [0.05]]
        },
        'CarNotStart': {
            'values': [0, 1],
            'evidence': ['BatteryDead', 'NoGas'],
            'values_given_parents': [
                [1.0, 0.1, 0.1, 0.01],   # P(Start=Yes | ...)
                [0.0, 0.9, 0.9, 0.99]    # P(NotStart=Yes | ...)
            ]
        }
    }

    solver = HybridSymbolicProbabilisticSolver(G)

    # Scenario: Car won't start. What's the cause?
    print("\n[Scenario] The car won't start (CarNotStart=1).")
    print("Attempting to diagnose the cause...\n")

    result = solver.solve('BatteryDead', {'CarNotStart': 1}, cpd_config)
    print(f"Diagnosis for BatteryDead:")
    print(f"  Method: {result['method']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print(f"  Result: {result['result']}")

    result2 = solver.solve('NoGas', {'CarNotStart': 1}, cpd_config)
    print(f"\nDiagnosis for NoGas:")
    print(f"  Method: {result2['method']}")
    print(f"  Confidence: {result2['confidence']:.4f}")
    print(f"  Result: {result2['result']}")

    print("\nNote: Since symbolic logic cannot prove certainty (confidence < 1.0),")
    print("the system automatically falls back to Bayesian inference.")


def example_4_scientific_method():
    """
    Simulates the scientific method using Bayesian updates.
    Hypothesis testing with accumulating evidence.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Scientific Method Simulation")
    print("="*60)
    print("Hypothesis H: 'A new drug is effective'")
    print("Evidence E: Patient recovery observations\n")

    # Simple graph: DrugEffective → PatientRecovers
    G = nx.DiGraph()
    G.add_edge('DrugEffective', 'PatientRecovers')

    # Start with neutral prior (50% belief in hypothesis)
    cpd_config = {
        'DrugEffective': {
            'values': [0, 1],
            'evidence': [],
            'values_given_parents': [[0.5], [0.5]]  # Neutral prior
        },
        'PatientRecovers': {
            'values': [0, 1],
            'evidence': ['DrugEffective'],
            'values_given_parents': [
                [0.7, 0.3],   # P(Recover=No | DrugEff=No/Yes)
                [0.3, 0.7]    # P(Recover=Yes | DrugEff=No/Yes)
            ]
        }
    }

    engine = BayesianEngine(G)
    engine.build_network(cpd_config)

    # Simulate sequential experiments
    print("Initial belief in DrugEffectiveness: 50%")

    # Experiment 1: Patient recovers
    posterior_1 = engine.query(['DrugEffective'], evidence={'PatientRecovers': 1})
    prob_effective_1 = posterior_1['DrugEffective=1']
    print(f"\nExperiment 1: Patient recovered.")
    print(f"Updated belief: {prob_effective_1:.4f} ({prob_effective_1*100:.2f}%)")

    # Experiment 2: Another patient recovers
    # In a real scenario, we'd update the prior, but here we chain evidence
    posterior_2 = engine.query(['DrugEffective'],
                               evidence={'PatientRecovers': 1})
    # Note: For proper sequential updating, we'd need to update the CPD
    # This is a simplified demonstration

    print("\n(Note: For true sequential Bayesian updating, the posterior")
    print("from one experiment becomes the prior for the next.)")

    print("\nThis demonstrates how the scientific method maps to Bayesian inference:")
    print("1. Form hypothesis (define variable)")
    print("2. Set prior belief (initial probability)")
    print("3. Make prediction (conditional probability)")
    print("4. Gather evidence (observe data)")
    print("5. Update belief (compute posterior)")


if __name__ == "__main__":
    # Run all examples
    example_1_rain_sprinkler()
    example_2_medical_diagnosis()
    example_3_hybrid_solver()
    example_4_scientific_method()

    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)