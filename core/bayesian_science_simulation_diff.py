--- bayesian_science_simulation.py (原始)


+++ bayesian_science_simulation.py (修改后)
"""
Bayesian Unified Framework Simulation
This script simulates the unified mathematical vessel combining:
1. Formal Logic (Deductive reasoning as P(E|H) = 1 or 0)
2. Inductive Reasoning (Bayesian Updating)
3. Scientific Method (Iterative hypothesis testing)

Based on Bayesian Confirmation Theory.
"""

class BayesianScientificMethod:
    def __init__(self, hypothesis_name, prior_probability):
        """
        Initialize a scientific inquiry process.

        :param hypothesis_name: Name of the hypothesis (H)
        :param prior_probability: Initial belief P(H) before evidence
        """
        self.hypothesis = hypothesis_name
        self.current_prior = prior_probability
        self.history = []

    def deductive_prediction(self, hypothesis_true, logical_entailment_strength):
        """
        Simulates Deductive Reasoning (Logic).
        Calculates P(E|H) - The Likelihood.

        In pure logic, if H entails E, P(E|H) = 1.
        Here we allow for 'noisy' logic (experimental error) but default to strict logic.

        :param hypothesis_true: Boolean, is the hypothesis actually true in this world?
        :param logical_entailment_strength: Float (0.0 to 1.0).
                                            1.0 = Strict Modus Ponens (H implies E definitely).
                                            < 1.0 = Probabilistic relationship.
        :return: P(E|H) and P(E|not H)
        """
        if hypothesis_true:
            # If H is true, and H logically entails E
            likelihood_given_h = logical_entailment_strength
            # If H is true but we're observing evidence, what would ~H predict?
            # This is the false negative rate scenario
            likelihood_given_not_h = 1.0 - logical_entailment_strength
        else:
            # If H is false, what is the chance of seeing E anyway? (False positive rate)
            # Usually low in good experiments
            likelihood_given_h = 1.0 - logical_entailment_strength
            likelihood_given_not_h = logical_entailment_strength

        return likelihood_given_h, likelihood_given_not_h

    def observe_evidence(self, evidence_name, likelihood_given_h, likelihood_given_not_h):
        """
        Simulates the Observation/Experiment phase and Bayesian Update.
        Calculates P(H|E) using Bayes' Theorem.

        Formula: P(H|E) = [P(E|H) * P(H)] / [P(E|H) * P(H) + P(E|~H) * P(~H)]
        """
        prior_h = self.current_prior
        prior_not_h = 1.0 - prior_h

        # Calculate Marginal Probability of Evidence P(E)
        prob_evidence = (likelihood_given_h * prior_h) + (likelihood_given_not_h * prior_not_h)

        if prob_evidence == 0:
            # Avoid division by zero; evidence was impossible under any hypothesis
            posterior = 0.0
        else:
            # Apply Bayes' Theorem
            numerator = likelihood_given_h * prior_h
            posterior = numerator / prob_evidence

        # Record history
        self.history.append({
            "evidence": evidence_name,
            "prior": prior_h,
            "likelihood_H": likelihood_given_h,
            "likelihood_not_H": likelihood_given_not_h,
            "posterior": posterior
        })

        # Update current belief for next iteration
        self.current_prior = posterior

        return posterior

    def run_scientific_cycle(self, experiments):
        """
        Runs the full Scientific Method loop:
        Observation -> Hypothesis -> Deduction -> Experiment -> Conclusion (Update)

        :param experiments: List of dicts containing experiment details
        """
        print(f"--- Starting Scientific Inquiry for Hypothesis: '{self.hypothesis}' ---")
        print(f"Initial Prior Belief P(H): {self.current_prior:.4f}\n")

        for i, exp in enumerate(experiments):
            print(f"Cycle {i+1}:")
            print(f"  Experiment: {exp['name']}")

            # 1. Deductive Phase: What does logic predict?
            # We assume the 'ground_truth' is known to the simulator to generate realistic data
            h_is_true = exp['ground_truth_h_is_true']
            logic_strength = exp['logical_entailment_strength']

            p_e_given_h, p_e_given_not_h = self.deductive_prediction(h_is_true, logic_strength)

            # Adjust for experimental noise if specified
            if 'noise' in exp:
                # Noise might make a true prediction look false or vice versa slightly
                # But here we stick to the core Bayesian update based on the model's expectation
                pass

            print(f"  Logical Prediction (Likelihood P(E|H)): {p_e_given_h:.4f}")
            print(f"  Alternative Prediction (P(E|~H)):      {p_e_given_not_h:.4f}")

            # 2. Inductive Phase: Update belief based on observed evidence
            # In this simulation, the "Observation" is consistent with the ground truth defined above
            new_belief = self.observe_evidence(
                evidence_name=exp['name'],
                likelihood_given_h=p_e_given_h,
                likelihood_given_not_h=p_e_given_not_h
            )

            print(f"  Result: Belief updated from {self.history[-1]['prior']:.4f} to {new_belief:.4f}")

            if new_belief > 0.99:
                print("  >> Status: Hypothesis Confirmed with near certainty.")
            elif new_belief < 0.01:
                print("  >> Status: Hypothesis Falsified (Rejected).")
            print("-" * 30)

        return self.current_prior

# ==========================================
# Scenario Simulation
# ==========================================

if __name__ == "__main__":
    # Scenario: Testing the hypothesis "All Swans are White"
    # H: All Swans are White.

    # We define a series of observations (Experiments)
    # In a real logical entailment: If H is true, observing a Swan MUST yield White (P=1).
    # If we see a Black Swan, P(E|H) becomes 0 (Falsification).

    experiments_log = [
        {
            "name": "Observation 1: Swan in Europe",
            "ground_truth_h_is_true": True, # Let's assume for the sake of the model that H is effectively true in this limited context initially
            "logical_entailment_strength": 1.0, # Strict logic: If all swans are white, this one must be white.
            "description": "We observe a white swan."
        },
        {
            "name": "Observation 2: Swan in Asia",
            "ground_truth_h_is_true": True,
            "logical_entailment_strength": 1.0,
            "description": "We observe another white swan."
        },
        {
            "name": "Observation 3: Swan in Australia (The Critical Test)",
            # Here we simulate the discovery of a Black Swan.
            # If H="All swans are white", and we see a Black Swan:
            # P(E|H) = 0 (Because H forbids black swans).
            # This should drive the Posterior to 0 immediately.
            "ground_truth_h_is_true": False, # In reality, H is false because black swans exist
            "logical_entailment_strength": 1.0, # The logic is still strict
            "description": "We observe a BLACK swan. This contradicts H."
        },
        {
            "name": "Observation 4: Revised Hypothesis Test",
            # Now testing H_new: "Most swans are white, but some are black"
            # We reset the simulation below for this part, but here let's see the collapse of the first one.
            "ground_truth_h_is_true": False,
            "logical_entailment_strength": 1.0,
            "description": "Further confirmation of diversity."
        }
    ]

    # Run Simulation 1: The Classic "Black Swan" Falsification
    print("\n=== SIMULATION 1: Falsification via Deductive Contradiction ===")
    scientist_1 = BayesianScientificMethod("All Swans are White", 0.90)
    scientist_1.run_scientific_cycle(experiments_log)

    print("\n\n=== SIMULATION 2: Gradual Confirmation (Inductive Strengthening) ===")
    # Scenario: Testing "This coin is biased towards Heads (80%)"
    # Here logic isn't binary (0 or 1) but probabilistic likelihoods.
    # H: Coin bias = 0.8 Heads.
    # E: Observed sequence of Heads.

    # Custom cycle for probabilistic induction
    scientist_2 = BayesianScientificMethod("Coin is Biased (80% Heads)", 0.50)

    # Simulate 5 tosses resulting in Heads
    # If H is true, P(Head|H) = 0.8
    # If H is false (fair coin), P(Head|~H) = 0.5
    probabilistic_experiments = []
    for i in range(5):
        probabilistic_experiments.append({
            "name": f"Coin Toss {i+1} (Result: Heads)",
            "ground_truth_h_is_true": True, # The coin IS biased in our simulation reality
            "logical_entailment_strength": 0.8 # This represents P(E|H) directly in a probabilistic context
        })

    # We need a custom runner for probabilistic likelihoods where P(E|~H) is fixed differently
    print(f"Starting Prior for Coin Bias: {scientist_2.current_prior:.4f}")
    for i, exp in enumerate(probabilistic_experiments):
        lh = 0.8  # Likelihood if hypothesis is true
        lnh = 0.5 # Likelihood if hypothesis is false (null hypothesis: fair coin)

        post = scientist_2.observe_evidence(exp['name'], lh, lnh)
        print(f"Step {i+1}: Observed Heads. New Belief = {post:.4f}")

    print("\nConclusion:")
    print("Simulation 1 demonstrated how Deductive Logic (P(E|H)=0) leads to immediate Falsification (Popper).")
    print("Simulation 2 demonstrated how Inductive Reasoning (Bayesian Updating) gradually increases certainty.")
    print("Both operate within the same mathematical vessel: P(H|E) = P(E|H)*P(H) / P(E)")