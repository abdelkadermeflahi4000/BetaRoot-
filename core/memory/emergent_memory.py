# core/memory/emergent_memory.py

class EmergentMemory:

    def __init__(self):
        self.events = []
        self.patterns = {}

    def store(self, action):
        self.events.append(action)

    def extract_patterns(self):
        for action in self.events:
            self.patterns[action] = self.patterns.get(action, 0) + 1

        return self.patterns
