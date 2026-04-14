# core/self/identity_stack.py

class IdentityStack:

    def __init__(self):
        self.layers = {
            "L1": {},
            "L2": {},
            "L3": {},
            "L4": {}
        }

    def update(self, layer, key, value):
        self.layers[layer][key] = value

    def get(self, layer):
        return self.layers[layer]
