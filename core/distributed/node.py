# core/distributed/node.py

class Node:

    def __init__(self, id, engine):
        self.id = id
        self.engine = engine
        self.fitness = 0

    def run_cycle(self):
        self.engine.run_cycle()
        self.fitness += len(self.engine.state.history)
