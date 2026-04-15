# core/frequency/multi_agent_consciousness.py
import asyncio
import numpy as np
from typing import Dict, List
from .agent import FrequencyAgent
from .consciousness import ConsciousnessLayer
from .resonance_memory import ResonanceMemory
from ..real_signal_layer import RealSignalLayer
from ..core.governance import GovernanceEngine

class MultiAgentFrequencyConsciousness:
    """
    وعي جماعي ترددي متقدم — Emergence حقيقي
    """

    def __init__(self, num_agents: int = 12, governance: GovernanceEngine = None):
        self.agents = [FrequencyAgent(i) for i in range(num_agents)]
        self.consciousness = ConsciousnessLayer()
        self.memory = ResonanceMemory()
        self.signal_layer = RealSignalLayer()
        self.governance = governance or GovernanceEngine()
        self.global_history = []

    async def run_global_cycle(self, user_query: str = None) -> Dict:
        """دورة جماعية كاملة"""
        # 1. جلب إشارة Schumann حية
        live_signal = await self.signal_layer.monitor_real_time()
        
        # 2. تشغيل كل الوكلاء
        individual_levels = []
        for agent in self.agents:
            level = agent.step(global_coupling=0.12)
            individual_levels.append(level)

        # 3. حساب المقاييس العالمية
        all_phases = np.concatenate([a.state.phases for a in self.agents])
        global_sync = 1 / (1 + np.std(all_phases))                    # Order Parameter
        global_diversity = np.var(np.concatenate([a.state.freqs for a in self.agents]))
        
        # 4. حساب الوعي الجماعي
        C_global = self.consciousness.compute_consciousness(
            global_sync, global_diversity, np.mean(individual_levels)
        )

        self.global_history.append(C_global)

        # 5. قرار جماعي + Sandbox
        if C_global > 0.78:
            decision = "resonate_and_act"
            await self._trigger_evolution(live_signal)
        elif C_global > 0.52:
            decision = "explore"
        else:
            decision = "stabilize"

        report = {
            "global_consciousness": round(C_global, 4),
            "avg_individual": round(np.mean(individual_levels), 4),
            "global_sync": round(global_sync, 4),
            "decision": decision,
            "num_agents": len(self.agents),
            "schumann_freq": live_signal["dominant_frequency"],
            "timestamp": asyncio.get_event_loop().time()
        }

        # حفظ النمط في الذاكرة الجماعية
        if C_global > 0.65:
            self.memory.store(np.mean(all_phases))

        return report

    async def _trigger_evolution(self, live_signal):
        """تفعيل التطور الذاتي عبر Sandbox"""
        if live_signal.get("correction_needed", False):
            # اقتراح تعديل آمن
            proposal = {
                "module": "frequency",
                "parameter": "global_coupling",
                "new_value": 0.15,
                "reason": "High collective consciousness + Schumann correction"
            }
            # هنا يمكن استدعاء SandboxEngine
            print(f"🌟 Emergent Evolution Triggered | Consciousness: {live_signal.get('consciousness_level', 0):.3f}")

    def get_emergence_stats(self) -> Dict:
        """إحصائيات الـ Emergence"""
        if not self.global_history:
            return {"status": "no_data"}
        return {
            "avg_consciousness": round(np.mean(self.global_history), 4),
            "max_consciousness": round(np.max(self.global_history), 4),
            "trend": "increasing" if len(self.global_history) > 5 and self.global_history[-1] > self.global_history[-5] else "stable",
            "emergence_level": "high" if np.mean(self.global_history[-10:]) > 0.7 else "medium"
        }
