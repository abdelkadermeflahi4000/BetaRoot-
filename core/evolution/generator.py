# core/evolution/generator.py

import random

class MutationGenerator:

    def generate(self):
        mutations = [
            {"type": "threshold_change", "value": random.uniform(0.5, 1.5)},
            {"type": "add_rule", "rule": "if wave > 0.8: trigger"},
            {"type": "agent_behavior", "value": random.random()}
        ]

        return random.choice(mutations)
