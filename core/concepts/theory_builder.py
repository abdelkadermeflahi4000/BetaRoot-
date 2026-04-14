# core/concepts/theory_builder.py

class TheoryBuilder:

    def build(self, concepts, relations):
        return {
            "concepts": concepts,
            "relations": relations,
            "rules": self.extract_rules(relations)
        }

    def extract_rules(self, relations):
        rules = []

        for r in relations:
            rules.append(f"{r['from']} -> {r['to']}")

        return rules
