# betaroot/core/self_learning.py

from typing import Dict, Any, List


class SelfLearningEngine:
    def __init__(self, knowledge_base, reasoning_engine):
        self.kb = knowledge_base
        self.engine = reasoning_engine

    # ----------------------------------
    # Run learning cycle
    # ----------------------------------
    def learn(self, query: Dict[str, Any], external_answers: Dict[str, Any]):
        """
        external_answers:
        {
            "What intermediate steps connect 'smoking' to 'cancer'?": "lung_damage"
        }
        """

        result = self.engine.reason(query)

        questions = result.get("questions", [])

        new_facts = []

        for q in questions:
            if q in external_answers:
                answer = external_answers[q]

                fact = self._convert_to_fact(q, answer)

                if fact:
                    self.kb.add_fact(fact)
                    new_facts.append(fact)

        return {
            "learned_facts": new_facts,
            "total_knowledge": len(self.kb.get_all_facts())
        }

    # ----------------------------------
    # Convert Q/A → Fact
    # ----------------------------------
    def _convert_to_fact(self, question: str, answer: Any):
        """
        تحويل السؤال + الجواب إلى fact
        """

        # مثال بسيط (نطوره لاحقًا)
        if "intermediate steps" in question:
            parts = question.split("'")
            if len(parts) >= 3:
                subject = parts[1]
                target = parts[3]

                return {
                    "subject": subject,
                    "predicate": "causes",
                    "value": answer,
                    "confidence": 0.9,
                    "source": "self_learning"
                }

        return None
