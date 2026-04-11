from betaroot.agents.reasoning_agent import ReasoningAgent
from betaroot.agents.learning_agent import LearningAgent
from betaroot.agents.critic_agent import CriticAgent
from betaroot.agents.explorer_agent import ExplorerAgent


class Coordinator:
    def __init__(self, kb, engine, learner):
        self.reasoning = ReasoningAgent(engine)
        self.learning = LearningAgent(learner)
        self.critic = CriticAgent()
        self.explorer = ExplorerAgent()
        self.kb = kb

    def execute(self, task):
        print("\n🧠 Multi-Agent Execution Started\n")

        # 1. Reason
        result = self.reasoning.execute(task)

        # 2. Critic check
        evaluation = self.critic.evaluate(result)

        if evaluation["status"] == "valid":
            return result

        # 3. Explore if weak
        print("🔍 Exploring missing knowledge...")
        exploration = self.explorer.explore(task, self.kb)

        # 4. Ask questions if needed
        questions = result.get("questions", [])

        return {
            "status": "needs_learning",
            "questions": questions,
            "exploration": exploration
        }
