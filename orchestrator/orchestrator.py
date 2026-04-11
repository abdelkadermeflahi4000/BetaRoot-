# betaroot/orchestrator/orchestrator.py

from typing import Dict, Any
from betaroot.core.reasoning_engine import ReasoningEngine
from betaroot.core.question_generator import QuestionGenerator


class Orchestrator:
    def __init__(self, kb):
        self.engine = ReasoningEngine(kb, causal_graph=kb.graph)
        self.qgen = QuestionGenerator()

    def run(self, task: Dict[str, Any]):
        """
        Main loop (Agent Loop)
        """

        print("\n🚀 Starting reasoning loop...\n")

        # 1. Reason
        result = self.engine.reason(task)

        # 2. If incomplete → ask questions
        if not result["consistent"] or not result["answer"]:
            print("⚠️ Missing knowledge → generating questions...")

            questions = result.get("questions", [])

            return {
                "status": "need_input",
                "questions": questions
            }

        # 3. If good → return result
        return {
            "status": "done",
            "result": result
        }
