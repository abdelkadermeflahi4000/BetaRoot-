--- betaroot/BAYESIAN_INTEGRATION.md (原始)


+++ betaroot/BAYESIAN_INTEGRATION.md (修改后)
# BetaRoot Bayesian Integration

This directory contains the Bayesian inference engine integrated with BetaRoot's symbolic AI core.

## Architecture

### Core Module: `bayesian_engine.py`

The main integration module providing:

1. **BayesianEngine Class**
   - Converts NetworkX causal graphs (DAGs) into Bayesian Networks
   - Performs exact inference using Variable Elimination
   - Supports Conditional Probability Distributions (CPDs)
   - Provides explainable inference results

2. **HybridSymbolicProbabilisticSolver Class**
   - Combines BetaRoot's Unary Logic with Bayesian Inference
   - Strategy: Try symbolic deduction first (certainty = 1.0 or 0.0)
   - Fallback to Bayesian inference when logic cannot prove certainty
   - Maintains transparency by reporting which method was used

## Key Features

### 1. Causal Graph to Bayesian Network Conversion
```python
import networkx as nx
from bayesian_engine import BayesianEngine

# Create causal graph
G = nx.DiGraph()
G.add_edges_from([('Rain', 'GrassWet'), ('Sprinkler', 'GrassWet')])

# Initialize engine
engine = BayesianEngine(G)
engine.build_network(cpd_config)
```

### 2. Exact Probabilistic Inference
```python
# Diagnostic inference: P(Cause | Effect)
result = engine.query(['Rain'], evidence={'GrassWet': 1})
# Returns: {'Rain=0': 0.5576, 'Rain=1': 0.4424}
```

### 3. Explainable Results
```python
explanation = engine.explain_inference(['Rain'], evidence={'GrassWet': 1})
print(explanation)
# Output includes evidence, probabilities, and interpretation
```

### 4. Hybrid Symbolic-Probabilistic Solving
```python
from bayesian_engine import HybridSymbolicProbabilisticSolver

solver = HybridSymbolicProbabilisticSolver(G)
result = solver.solve('Hypothesis', {'Evidence': 1}, cpd_data)

# Result includes:
# - method: "Symbolic Unary Logic" or "Bayesian Probabilistic Inference"
# - confidence: 1.0 for logic, <1.0 for Bayesian
# - explanation: Full trace of reasoning
```

## Examples

See `examples/bayesian_integration_examples.py` for:

1. **Rain-Sprinkler-Grass**: Classic causal network demonstrating diagnostic inference and "explaining away"
2. **Medical Diagnosis**: Multi-disease symptom network for diagnostic reasoning
3. **Hybrid Solver**: Car trouble diagnosis showing symbolic→Bayesian fallback
4. **Scientific Method**: Hypothesis testing with Bayesian updates

## Installation Requirements

Add to `requirements.txt`:
```
pgmpy>=0.1.20
networkx>=3.0
```

Install:
```bash
pip install pgmpy networkx
```

## Mathematical Foundation

The implementation uses the **Factorization Theorem** for Bayesian Networks:

$$P(X_1, X_2, ..., X_n) = \prod_{i=1}^n P(X_i \mid Pa(X_i))$$

Where:
- $Pa(X_i)$ are the parent variables of $X_i$ in the causal graph
- $P(X_i \mid Pa(X_i))$ are stored in Conditional Probability Tables (CPTs)

Inference is performed using **Variable Elimination**, an exact algorithm that:
1. Eliminates non-query variables by summing them out
2. Preserves the joint distribution over query variables given evidence
3. Computes posterior probabilities efficiently

## Integration with BetaRoot Philosophy

This module aligns with BetaRoot's core principles:

- **No Hallucinations**: Bayesian inference provides calculated probabilities, not guesses
- **Explainability**: Every result includes the reasoning path and confidence level
- **Symbolic First**: Unary logic takes precedence; Bayesian is a fallback for uncertainty
- **Causal Transparency**: The DAG structure makes causal assumptions explicit

## Future Enhancements (Roadmap)

1. **Structure Learning**: Automatically learn causal graph from data
2. **Parameter Learning**: Update CPDs from observations (MLE/Bayesian estimation)
3. **Sequential Updating**: Implement proper Bayesian updating where posterior becomes prior
4. **Visualization**: Generate graphical representations of networks with probabilities
5. **Advanced Inference**: Support for continuous variables (hybrid networks)

## Usage in Scientific Research

This integration enables BetaRoot to:
- Model complex scientific hypotheses with uncertainty
- Perform diagnostic reasoning in medicine and engineering
- Simulate the scientific method (hypothesis → prediction → test → update)
- Combine symbolic knowledge with statistical evidence

## License

Part of the BetaRoot open-source project.