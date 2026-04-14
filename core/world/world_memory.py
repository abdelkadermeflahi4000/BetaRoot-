# core/world/world_memory.py

class WorldMemory:

    def __init__(self):
        self.history = []

    def store(self, state, action, result):
        self.history.append({
            "state": state,
            "action": action,
            "result": result
        })
