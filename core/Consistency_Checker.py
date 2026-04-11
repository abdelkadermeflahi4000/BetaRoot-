"""
Consistency Checker for BetaRoot Core

- Ensures all facts are contradiction-free
- Enforces Unary Logic constraints
- Integrates with Knowledge Base + Causal Graph
"""

from typing import List, Dict, Any


class ConsistencyError(Exception):
    """Raised when a contradiction is detected"""
    pass


class ConsistencyChecker:
    def __init__(self, knowledge_base, unary_logic):
        self.kb = knowledge_base
        self.unary = unary_logic

    # -----------------------------
    # Public API
    # -----------------------------
    def validate_fact(self, fact: Dict[str, Any]) -> bool:
        """
        Main entry point

        Returns True if valid, raises ConsistencyError if not
        """
        # 1. Unary validation
        if not self._validate_unary(fact):
            raise ConsistencyError("Unary validation failed")

        # 2. Check contradictions with existing knowledge
        conflicts = self._find_conflicts(fact)

        if conflicts:
            raise ConsistencyError(
                f"Contradiction detected with facts: {conflicts}"
            )

        return True

    # -----------------------------
    # Unary Logic Validation
    # -----------------------------
    def _validate_unary(self, fact: Dict[str, Any]) -> bool:
        """
        Enforce Unary Logic rules:
        - Everything is assumed valid unless contradiction is proven
        - Confidence must be within (0, 1]
        """
        confidence = fact.get("confidence", 1.0)

        if confidence <= 0 or confidence > 1:
            return False

        return True

    # -----------------------------
    # Conflict Detection
    # -----------------------------
    def _find_conflicts(self, new_fact: Dict[str, Any]) -> List[Dict]:
        """
        Detect contradictions against knowledge base

        Example:
        - "X causes Y"
        - "X does NOT cause Y" → conflict
        """
        conflicts = []

        existing_facts = self.kb.get_all_facts()

        for fact in existing_facts:
            if self._is_contradiction(fact, new_fact):
                conflicts.append(fact)

        return conflicts

    def _is_contradiction(self, fact1: Dict, fact2: Dict) -> bool:
        """
        Define contradiction logic

        Simple version:
        - Same subject + predicate
        - Opposite polarity
        """
        if (
            fact1.get("subject") == fact2.get("subject")
            and fact1.get("predicate") == fact2.get("predicate")
        ):
            return fact1.get("value") != fact2.get("value")

        return False
