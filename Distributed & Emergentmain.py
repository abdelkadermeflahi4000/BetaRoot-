# main.py

engine = DistributedEngine()

node1 = Node("A", BetaRootEngine([]))
node2 = Node("B", BetaRootEngine([]))

engine.add_node(node1)
engine.add_node(node2)

while True:
    engine.run()
