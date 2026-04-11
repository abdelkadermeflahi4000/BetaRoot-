# betaroot/core/reasoning_engine.py

from typing import Dict, Any, List


class ReasoningEngine:
    def __init__(self, knowledge_base, causal_graph=None, explanation_generator=None):
        self.kb = knowledge_base
        self.graph = causal_graph
        self.explainer = explanation_generator

    # ----------------------------------
    # Main API
    # ----------------------------------
    def reason(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Example query:
        {
            "subject": "smoking",
            "predicate": "causes"
        }
        """

        # 1. Retrieve relevant facts
        facts = self._retrieve_facts(query)

        if not facts:
            return self._reject("No knowledge available")

        # 2. Validate consistency (already handled at insert, but double check)
        if not self._check_consistency(facts):
            return self._reject("Inconsistent knowledge")

        # 3. Build causal chain
        causal_chain = self._build_causal_chain(query, facts)

        # 4. Generate answer
        answer = self._generate_answer(facts)

        # 5. Generate explanation
        explanation = self._generate_explanation(query, facts, causal_chain)

        return {
            "answer": answer,
            "reasoning_path": facts,
            "causal_chain": causal_chain,
            "explanation": explanation,
            "confidence": 1.0,
            "consistent": True
        }

    # ----------------------------------
    # Step 1: Retrieve facts
    # ----------------------------------
    def _retrieve_facts(self, query):
        results = []

        for fact in self.kb.get_all_facts():
            if (
                fact.get("subject") == query.get("subject")
                and fact.get("predicate") == query.get("predicate")
            ):
                results.append(fact)

        return results

    # ----------------------------------
    # Step 2: Consistency check
    # ----------------------------------
    def _check_consistency(self, facts: List[Dict]) -> bool:
        values = set()

        for f in facts:
            values.add(f.get("value"))

        # إذا كان هناك أكثر من قيمة → تناقض
        return len(values) <= 1

    # ----------------------------------
    # Step 3: Causal Chain
    # ----------------------------------
    def _build_causal_chain(self, query, facts):
        chain = []

        for f in facts:
            chain.append({
                "from": f.get("subject"),
                "relation": f.get("predicate"),
                "to": f.get("value")
            })

        # لاحقًا: نربطها بـ graph traversal
        return chain

    # ----------------------------------
    # Step 4: Answer
    # ----------------------------------
    def _generate_answer(self, facts):
        return facts[0].get("value")

    # ----------------------------------
    # Step 5: Explanation
    # ----------------------------------
    def _generate_explanation(self, query, facts, chain):
        if self.explainer:
            return self.explainer.generate(query, facts, chain)

        # fallback بسيط
        explanation = f"{query['subject']} {query['predicate']} {facts[0]['value']}"

        return explanation

    # ----------------------------------
    # Reject
    # ----------------------------------
    def _reject(self, reason):
        return {
            "answer": None,
            "reasoning_path": [],
            "causal_chain": [],
            "explanation": reason,
            "confidence": 0.0,
            "consistent": False
        }
