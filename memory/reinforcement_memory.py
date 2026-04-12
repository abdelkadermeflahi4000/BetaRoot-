class ReinforcementMemory:
    def __init__(self):
        self.history = []

    def store(self, input_data, output, reward):
        self.history.append({
            "input": input_data,
            "output": output,
            "reward": reward
        })

    def get_last(self, n=10):
        return self.history[-n:]
