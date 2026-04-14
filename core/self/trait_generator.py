# core/self/trait_generator.py

import random
import string

class TraitGenerator:

    def generate(self):
        name = "T_" + "".join(random.choices(string.ascii_uppercase, k=4))

        return {
            "name": name,
            "value": random.uniform(0.5, 1.5),
            "type": random.choice(["behavioral", "cognitive", "adaptive"])
        }
