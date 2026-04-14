# core/distributed/node_identity.py

import random

class NodeIdentity:

    def __init__(self):
        self.signature = random.randint(1000, 9999)

    def mutate(self):
        self.signature += random.randint(-10, 10)
