# core/distributed/selection_engine.py

class SelectionEngine:

    def select_best(self, nodes):
        nodes = sorted(nodes, key=lambda n: n.fitness, reverse=True)
        return nodes[:2]  # أفضل عقدتين
