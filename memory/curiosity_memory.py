class CuriosityMemory:
    def __init__(self):
        self.events = []

    def store(self, tokens, curiosity_score):
        self.events.append({
            "tokens": tokens,
            "curiosity": curiosity_score
        })

    def retrieve_high_curiosity(self, threshold=0.5):
        return [
            e for e in self.events
            if e["curiosity"] > threshold
        ]
