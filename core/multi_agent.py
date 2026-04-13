# betaroot/core/multi_agent.py
import asyncio
import uuid
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

from .cycle_engine import CycleEngine
from .memory_system import BetaRootMemorySystem, MemoryType, Priority
from .consolidation_engine import ConsolidationEngine
from .governance import GovernanceEngine, Action
from .symbolic_patterns import SymbolicPatternEngine
from .frequency_resonance import FrequencyResonance


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
        print(f"📨 [{self.name}] → [{receiver}] | {action_type}")


class ObserverAgent(BaseAgent):
    """الوكيل المراقب — يقرأ الترددات ويحسب الضغط الخاطئ"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resonance = FrequencyResonance()

    async def observe(self):
        action = Action("analyze_frequency")
        if not self.governance.check(action):
            return None

        # قراءة التردد الحالي (محاكاة أو قراءة حقيقية لاحقاً)
        freq_status = self.resonance.calculate_wrong_pressure(
            f_current=7.83 + 0.25 * (self.memory.get_stats()["episodic_count"] % 8),  # تغيير ديناميكي
            tech_intensity=0.65,
            contamination=0.55
        )

        # حفظ الملاحظة في الذاكرة
        self.memory.store(
            content=freq_status,
            memory_type=MemoryType.EPISODIC,
            priority=Priority.HIGH if freq_status["correction_needed"] else Priority.MEDIUM,
            source="ObserverAgent",
            tags=["frequency", "schumann"]
        )

        await self.send_message("Planner", freq_status, "frequency_observation")
        return freq_status


class PlannerAgent(BaseAgent):
    """الوكيل المخطط — يطبق الأنماط السببية المتقدمة"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_engine = SymbolicPatternEngine()

    async def plan(self, observation: Dict):
        action = Action("apply_symbolic_patterns")
        if not self.governance.check(action):
            return None

        # تطبيق الأنماط السببية المتقدمة
        content = str(observation)
        pattern_result = self.pattern_engine.apply_pattern(content)

        # إذا كان هناك ضغط ترددي → نفعّل نمط Resonance_Causation
        if observation.get("correction_needed", False):
            plan = {
                "action": "correct_frequency",
                "pattern": "Resonance_Causation",
                "priority": 0.95,
                "suggested_pattern": pattern_result.pattern_name if pattern_result else "None"
            }
        else:
            plan = {
                "action": "consolidate_memory",
                "pattern": pattern_result.pattern_name if pattern_result else "Repetition_Recognition",
                "priority": 0.7
            }

        await self.send_message("Executor", plan, "execution_plan")
        return plan


class ExecutorAgent(BaseAgent):
    """الوكيل المنفذ — ينفذ ويحفظ"""
    async def execute(self, plan: Dict):
        action = Action(plan["action"])
        if not self.governance.check(action):
            return {"success": False, "reason": "blocked_by_governance"}

        if plan["action"] == "correct_frequency":
            result = {
                "success": True,
                "corrected": True,
                "message": "تم تفعيل تصحيح ترددي باستخدام Resonance_Causation"
            }
        else:
            result = {
                "success": True,
                "message": f"تم تنفيذ {plan.get('pattern', 'unknown')}"
            }

        # حفظ النتيجة في الذاكرة
        self.memory.store(
            content=result,
            memory_type=MemoryType.EPISODIC,
            priority=Priority.HIGH,
            source="ExecutorAgent",
            tags=["execution", plan.get("pattern", "")]
        )

        await self.send_message("Evaluator", result, "execution_result")
        return result


class EvaluatorAgent(BaseAgent):
    """الوكيل المقيّم — يقيّم ويطلب دمج"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consolidator: Optional[ConsolidationEngine] = None

    async def evaluate(self, result: Dict):
        score = 0.92 if result.get("success") else 0.35

        eval_data = {
            "score": score,
            "feedback": "ممتاز - يستحق الدمج" if score > 0.8 else "متوسط",
            "needs_consolidation": score > 0.75
        }

        if eval_data["needs_consolidation"] and self.consolidator:
            await self.send_message("Consolidator", eval_data, "request_consolidation")

        return eval_data


class MultiAgentSystem:
    """النظام متعدد الوكلاء الكامل مع ربط Frequency Resonance"""
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
        print(f"\n🔄 Multi-Agent Cycle #{len(self.memory.episodic) // 2 + 1}")

        obs = await self.agents["Observer"].observe()
        if not obs:
            return

        plan = await self.agents["Planner"].plan(obs)
        if not plan:
            return

        result = await self.agents["Executor"].execute(plan)
        if result:
            await self.agents["Evaluator"].evaluate(result)

        print("✅ انتهت الدورة بنجاح")

    async def start(self, cycles: int = 8, interval: int = 12):
        print("🌍 BetaRoot Multi-Agent System مع Frequency Resonance بدأ العمل...\n")
        for _ in range(cycles):
            await self.run_cycle()
            await asyncio.sleep(interval)


# ====================== تشغيل سريع ======================
if __name__ == "__main__":
    system = MultiAgentSystem()
    asyncio.run(system.start(cycles=6, interval=10))
