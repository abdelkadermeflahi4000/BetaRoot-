import time


class EpisodicMemory:
    def __init__(self):
        self.episodes = []

    def record(self, event):
        self.episodes.append({
            "timestamp": time.time(),
            "event": event
        })

    def get_all(self):
        return self.episodes
