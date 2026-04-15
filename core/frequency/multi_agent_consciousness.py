# core/frequency/multi_agent_consciousness.py
import numpy as np
import asyncio
from typing import List, Dict
from .agent import FrequencyAgent
from .consciousness import ConsciousnessLayer
from ..core_engine import BetaRootCoreEngine  # ربط مع النواة

class MultiAgentFrequencyConsciousness:
    """
    طبقة الوعي الجماعي الترددي
    Emergence حقيقي من تفاعل عدة وكلاء تردديين
    """

    def __init__(self, num_agents: int = 8):
        self.agents: List[FrequencyAgent] = [
            FrequencyAgent(i, n_oscillators=16) for i in range(num_agents)
        ]
        self.consciousness = ConsciousnessLayer()
        self.global_phases_history = []
        self.core = BetaRootCoreEngine()  # ربط مع BetaRoot

    async def run_global_cycle(self, external_signal: np.ndarray = None):
        """دورة جماعية واحدة — Emergence"""
        individual_levels = []
        
        # كل وكيل يتطور
        for agent in self.agents:
            level = agent.step(external_signal)
            individual_levels.append(level)

        # حساب التزامن العالمي
        all_phases = np.concatenate([a.state.phases for a in self.agents])
        global_sync = 1 / (1 + np.std(all_phases))
        
        # حساب التنوع العالمي
        all_freqs = np.concatenate([a.state.freqs for a in self.agents])
        global_diversity = np.var(all_freqs)

        # حساب مستوى الوعي الجماعي
        C_global = self.consciousness.compute_consciousness(
            global_sync, global_diversity, np.mean(individual_levels)
        )

        self.global_phases_history.append(all_phases.mean())

        # قرار جماعي
        if C_global > 0.72:
            decision = "resonate_and_act"   # وعي عالي → تنفيذ
        elif C_global > 0.45:
            decision = "explore"
        else:
            decision = "stabilize"          # وعي منخفض → تصحيح

        return {
            "global_consciousness": round(C_global, 4),
            "avg_individual": round(np.mean(individual_levels), 4),
            "global_sync": round(global_sync, 4),
            "decision": decision,
            "num_agents": len(self.agents),
            "timestamp": asyncio.get_event_loop().time()
        }

    async def integrate_with_betaroot(self, user_query: str):
        """ربط الوعي الجماعي مع BetaRoot Orchestrator"""
        # تشغيل دورة ترددية
        consciousness_report = await self.run_global_cycle()

        # إرسال التقرير إلى Core Engine
        await self.core.evolve({
            "consciousness_level": consciousness_report["global_consciousness"],
            "decision": consciousness_report["decision"],
            "query": user_query
        })

        return consciousness_report
