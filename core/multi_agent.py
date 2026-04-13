# betaroot/core/multi_agent.py
import asyncio
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .cycle_engine import CycleEngine
from .memory_system import BetaRootMemorySystem
from .consolidation_engine import ConsolidationEngine
from .governance import GovernanceEngine, Action
from .symbolic_patterns import SymbolicPatternEngine


@dataclass
class AgentMessage:
    id: str
    sender: str
    receiver: str
    content: Any
    timestamp: str
    action_type: str


class BaseAgent:
    def __init__(self, name: str, memory: BetaRootMemorySystem, governance: GovernanceEngine):
        self.name = name
        self.memory = memory
        self.governance = governance
        self.message_queue: List[AgentMessage] = []

    async def send_message(self, receiver: str, content: Any, action_type: str):
        msg = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.name,
            receiver=receiver,
            content=content,
            timestamp=datetime.now().isoformat(),
            action_type=action_type
        )
        self.message_queue.append(msg)
        print(f"📨 {self.name} → {receiver} | {action_type}")


class ObserverAgent(BaseAgent):
    """يراقب الترددات والحالة الخارجية"""
    async def observe(self):
        action = Action("analyze_frequency")
        if not self.governance.check(action):
            return None

        # محاكاة قراءة التردد
        freq_status = {"current": 8.1, "base": 7.83, "pressure": 0.65, "needs_correction": True}
        
        await self.send_message("Planner", freq_status, "observation")
        return freq_status


class PlannerAgent(BaseAgent):
    """يخطط ويطبق الأنماط الرمزية"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_engine = SymbolicPatternEngine()

    async def plan(self, observation: Dict):
        action = Action("apply_symbolic_patterns")
        if not self.governance.check(action):
            return None

        # تطبيق أنماط سببية
        content = str(observation)
        pattern_result = self.pattern_engine.apply_pattern(content)

        plan = {
            "action": "correct_frequency" if observation.get("needs_correction") else "consolidate",
            "pattern_used": pattern_result.pattern_name if pattern_result else "None",
            "priority": 0.9 if observation.get("needs_correction") else 0.6
        }

        await self.send_message("Executor", plan, "plan")
        return plan


class ExecutorAgent(BaseAgent):
    """ينفذ الخطة ويحفظ في الذاكرة"""
    async def execute(self, plan: Dict):
        action = Action(plan["action"])
        if not self.governance.check(action):
            return {"success": False, "reason": "blocked_by_governance"}

        # تنفيذ بسيط
        if plan["action"] == "correct_frequency":
            result = {"success": True, "corrected": True, "message": "تم تصحيح الضغط الترددي"}
        else:
            result = {"success": True, "message": "تم تنفيذ الخطة"}

        # حفظ في الذاكرة
        self.memory.store(
            content=result,
            memory_type=MemoryType.EPISODIC,
            priority=0.85,
            source=self.name
        )

        await self.send_message("Evaluator", result, "execution_result")
        return result


class EvaluatorAgent(BaseAgent):
    """يقيم النتيجة ويطلب الدمج"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consolidator: Optional[ConsolidationEngine] = None

    async def evaluate(self, result: Dict):
        score = 0.9 if result.get("success") else 0.4

        eval_data = {
            "score": score,
            "feedback": "جيد جداً" if score > 0.75 else "يحتاج تحسين",
            "needs_consolidation": score > 0.7
        }

        # إذا كان الأداء جيد → اطلب دمج
        if eval_data["needs_consolidation"] and self.consolidator:
            await self.send_message("Consolidator", eval_data, "request_consolidation")

        return eval_data


class MultiAgentSystem:
    """
    النظام متعدد الوكلاء الكامل
    """
    def __init__(self):
        self.memory = BetaRootMemorySystem()
        self.governance = GovernanceEngine()
        self.consolidator = ConsolidationEngine(self.memory)

        self.agents = {
            "Observer": ObserverAgent("Observer", self.memory, self.governance),
            "Planner": PlannerAgent("Planner", self.memory, self.governance),
            "Executor": ExecutorAgent("Executor", self.memory, self.governance),
            "Evaluator": EvaluatorAgent("Evaluator", self.memory, self.governance),
        }

        self.agents["Evaluator"].consolidator = self.consolidator

    async def run_cycle(self):
        """دورة كاملة متعددة الوكلاء"""
        print(f"\n🔄 بدء دورة Multi-Agent #{self.get_cycle_count()}")

        # 1. Observer
        obs = await self.agents["Observer"].observe()

        # 2. Planner
        plan = await self.agents["Planner"].plan(obs) if obs else None

        # 3. Executor
        result = await self.agents["Executor"].execute(plan) if plan else None

        # 4. Evaluator
        if result:
            await self.agents["Evaluator"].evaluate(result)

        print("✅ انتهت الدورة بنجاح")

    def get_cycle_count(self):
        # يمكن تحسينه ليكون عداد حقيقي
        return len(self.memory.episodic)

    async def start(self, cycles: int = 5, interval: int = 15):
        for i in range(cycles):
            await self.run_cycle()
            await asyncio.sleep(interval)


# ====================== تشغيل سريع ======================
if __name__ == "__main__":
    system = MultiAgentSystem()
    asyncio.run(system.start(cycles=3, interval=10))
