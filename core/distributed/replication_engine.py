# core/distributed/replication_engine.py

import copy

class ReplicationEngine:

    def replicate(self, node):
        new_engine = copy.deepcopy(node.engine)

        return Node(
            id=f"{node.id}_child",
            engine=new_engine
        )
