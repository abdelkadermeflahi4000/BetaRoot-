# betaroot/core/explanation_generator.py

from typing import List, Dict, Any


class ExplanationGenerator:
    def generate(self, query: Dict[str, Any], facts: List[Dict], causal_chain: List[List[str]]) -> str:
        """
        يولد شرح ذكي مبني على:
        - facts
        - causal chain
        """

        if not facts:
            return "No explanation available."

        explanation_parts = []

        # ----------------------------------
        # 1. Direct explanation
        # ----------------------------------
        main_fact = facts[0]
        explanation_parts.append(
            f"According to the knowledge base, '{main_fact['subject']}' {main_fact['predicate']} '{main_fact['value']}'."
        )

        # ----------------------------------
        # 2. Causal chain explanation
        # ----------------------------------
        if causal_chain:
            explanation_parts.append("\nCausal reasoning:")

            for path in causal_chain:
                chain_text = " → ".join(path)
                explanation_parts.append(f"- {chain_text}")

        # ----------------------------------
        # 3. Logical justification
        # ----------------------------------
        explanation_parts.append("\nLogical validation:")

        if len(facts) == 1:
            explanation_parts.append(
                "No contradictions found. The fact is consistent with existing knowledge."
            )
        else:
            explanation_parts.append(
                "Multiple supporting facts found. No contradictions detected."
            )

        # ----------------------------------
        # 4. Counterfactual insight (optional)
        # ----------------------------------
        explanation_parts.append("\nCounterfactual insight:")

        explanation_parts.append(
            f"If '{query['subject']}' did not occur, the resulting effects in the causal chain would likely not happen."
        )

        return "\n".join(explanation_parts)
