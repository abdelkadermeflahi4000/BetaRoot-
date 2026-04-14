# core/distributed/distributed_engine.py

class DistributedEngine:

    def __init__(self):
        self.nodes = []
        self.selection = SelectionEngine()
        self.replication = ReplicationEngine()
        self.exchange = KnowledgeExchange()

    def add_node(self, node):
        self.nodes.append(node)

    def run(self):
        # تشغيل كل العقد
        for node in self.nodes:
            node.run_cycle()

        # تبادل المعرفة
        for i in range(len(self.nodes)-1):
            self.exchange.exchange(self.nodes[i], self.nodes[i+1])

        # اختيار الأفضل
        best_nodes = self.selection.select_best(self.nodes)

        # التكاثر
        for node in best_nodes:
            child = self.replication.replicate(node)
            self.nodes.append(child)

        print(f"[NETWORK SIZE] {len(self.nodes)}")
