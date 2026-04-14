# core/concepts/concept_memory.py

class ConceptMemory:

    def __init__(self):
        self.concepts = {}

    def add(self, name, data):
        self.concepts[name] = data

    def get_all(self):
        return self.concepts
