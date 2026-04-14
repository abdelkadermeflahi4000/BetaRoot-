# core/self/recursive_engine.py

class RecursiveSelf:

    def __init__(self, stack, layers):
        self.stack = stack
        self.layers = layers

    def run(self, state):

        # L1
        l1 = self.layers.layer1_awareness(state)
        self.stack.update("L1", "data", l1)

        # L2
        l2 = self.layers.layer2_reflection(l1)
        self.stack.update("L2", "data", l2)

        # L3
        l3 = self.layers.layer3_meta(l2)
        self.stack.update("L3", "data", l3)

        # L4 (Recursive)
        l4 = self.layers.layer4_recursive(l3)
        self.stack.update("L4", "data", l4)

        return {
            "L1": l1,
            "L2": l2,
            "L3": l3,
            "L4": l4
        }
