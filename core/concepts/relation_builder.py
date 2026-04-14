# core/concepts/relation_builder.py

class RelationBuilder:

    def build(self, concepts):
        relations = []

        keys = list(concepts.keys())

        for i in range(len(keys) - 1):
            c1 = keys[i]
            c2 = keys[i+1]

            relations.append({
                "from": c1,
                "to": c2,
                "type": "sequence"
            })

        return relations
