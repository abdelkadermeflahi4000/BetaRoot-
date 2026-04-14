# core/distributed/communication_layer.py

class CommunicationLayer:

    def __init__(self):
        self.nodes = []

    def register(self, node):
        self.nodes.append(node)

    def broadcast(self, sender, data):
        for node in self.nodes:
            if node != sender:
                node.engine.receive(data)
