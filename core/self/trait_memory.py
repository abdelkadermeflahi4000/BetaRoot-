# core/self/trait_memory.py

class TraitMemory:

    def __init__(self):
        self.traits = {}

    def add(self, trait):
        self.traits[trait["name"]] = trait

    def get_all(self):
        return self.traits
