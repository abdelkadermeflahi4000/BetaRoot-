# betaroot/core/governance.py
from typing import Dict, Any
from dataclasses import dataclass

class Action:
    def __init__(self, name: str, params: Dict = None):
        self.name = name
        self.params = params or {}

class GovernanceEngine:
    """
    محرك الحوكمة — يحمي النظام من السلوكيات الخطرة
    """

    ALLOWED_ACTIONS = {
        "read_memory",
        "store_memory",
        "analyze_frequency",
        "consolidate_memory",
        "run_cycle",
        "generate_explanation",
        "update_from_github"
    }

    def __init__(self):
        self.safety_level = "strict"  # strict / medium / experimental

    def check(self, action: Action) -> bool:
        """التحقق من الإذن قبل التنفيذ"""
        if action.name not in self.ALLOWED_ACTIONS:
            print(f"⛔ Action blocked by governance: {action.name}")
            return False

        # قواعد إضافية حسب مستوى السلامة
        if self.safety_level == "strict":
            if "modify_self" in action.name or "execute_code" in action.name:
                print(f"⛔ Self-modification blocked in strict mode")
                return False

        return True

    def log_action(self, action: Action, approved: bool):
        status = "✅ Approved" if approved else "⛔ Blocked"
        print(f"GOVERNANCE | {status} | Action: {action.name}")
