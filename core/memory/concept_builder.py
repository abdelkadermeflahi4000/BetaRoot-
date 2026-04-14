# core/memory/concept_builder.py

class ConceptBuilder:

    def build(self, patterns):
        concepts = {}

        for action, count in patterns.items():
            if count > 3:
                concept_name = f"C_{action}"
                concepts[concept_name] = {
                    "base": action,
                    "strength": count
                }

        return concepts
