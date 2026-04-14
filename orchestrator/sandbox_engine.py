# orchestrator/sandbox_engine.py
import asyncio
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, Callable

from ..core.governance import GovernanceEngine, Action

@dataclass
class SandboxProposal:
    id: str
    module: str
    parameter: str
    new_value: Any
    reason: str
    risk_score: float          # 0.0 → 1.0
    proposed_by: str           # "frequency_correction", "agent_fusion", "self_reflection"
    timestamp: str

class SandboxEngine:
    """
    Sandbox آمن لـ Self-Modification
    يمنع التعديلات الخطرة ويختبرها قبل التطبيق
    """

    def __init__(self, governance: GovernanceEngine):
        self.governance = governance
        self.approved_changes: Dict[str, SandboxProposal] = {}
        self.rejected_changes: List[SandboxProposal] = []
        self.test_results: Dict[str, Dict] = {}

    def calculate_risk(self, proposal: SandboxProposal) -> float:
        """حساب درجة الخطر"""
        risk = 0.0
        if proposal.module in ["resonance", "core_engine"]:
            risk += 0.4
        if abs(proposal.new_value) > 1.0 and isinstance(proposal.new_value, (int, float)):
            risk += 0.3
        if "k_conscious" in proposal.parameter or "k_tech" in proposal.parameter:
            risk += 0.25
        if proposal.proposed_by == "frequency_correction":
            risk -= 0.2  # تصحيح ترددي = أقل خطراً
        return min(1.0, max(0.0, risk))

    async def propose_change(self, module: str, parameter: str, new_value: Any, reason: str, proposed_by: str = "self_evolution") -> Dict:
        """اقتراح تعديل + تقييم في Sandbox"""
        proposal_id = hashlib.sha256(f"{module}{parameter}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        proposal = SandboxProposal(
            id=proposal_id,
            module=module,
            parameter=parameter,
            new_value=new_value,
            reason=reason,
            risk_score=0.0,  # سيتم حسابها
            proposed_by=proposed_by,
            timestamp=datetime.now().isoformat()
        )

        proposal.risk_score = self.calculate_risk(proposal)

        # فحص الحوكمة
        action = Action.EVOLVE if proposal.risk_score < 0.6 else Action.MAINTAIN_STABILITY
        if not self.governance.check(action):
            self.rejected_changes.append(proposal)
            return {
                "status": "rejected",
                "reason": "Governance blocked high-risk change",
                "risk_score": proposal.risk_score,
                "proposal_id": proposal_id
            }

        # اختبار في Sandbox (محاكاة)
        test_result = await self._run_sandbox_test(proposal)
        self.test_results[proposal_id] = test_result

        if test_result["passed"]:
            self.approved_changes[proposal_id] = proposal
            # تطبيق التعديل الفعلي (في الإصدارات المتقدمة يمكن تنفيذه ديناميكياً)
            self._apply_change(proposal)
            return {
                "status": "approved",
                "proposal_id": proposal_id,
                "risk_score": proposal.risk_score,
                "test_result": test_result,
                "applied": True
            }
        else:
            self.rejected_changes.append(proposal)
            return {
                "status": "rejected",
                "reason": "Sandbox test failed",
                "test_result": test_result,
                "proposal_id": proposal_id
            }

    async def _run_sandbox_test(self, proposal: SandboxProposal) -> Dict:
        """محاكاة اختبار التعديل في بيئة معزولة"""
        await asyncio.sleep(0.3)  # محاكاة وقت الاختبار
        
        # اختبارات أمان بسيطة
        stability_test = proposal.risk_score < 0.75
        consistency_test = True
        performance_test = proposal.new_value is not None

        return {
            "passed": stability_test and consistency_test and performance_test,
            "stability": stability_test,
            "consistency": consistency_test,
            "performance_impact": "low" if performance_test else "high",
            "message": "All sandbox checks passed" if stability_test else "Stability risk detected"
        }

    def _apply_change(self, proposal: SandboxProposal):
        """تطبيق التعديل الآمن (محاكاة)"""
        print(f"🛠️ Sandbox applied change → {proposal.module}.{proposal.parameter} = {proposal.new_value}")
        print(f"   Reason: {proposal.reason} | Risk: {proposal.risk_score:.2f}")

    def get_sandbox_report(self) -> Dict:
        """تقرير Sandbox كامل"""
        return {
            "approved_count": len(self.approved_changes),
            "rejected_count": len(self.rejected_changes),
            "last_approved": list(self.approved_changes.values())[-1].__dict__ if self.approved_changes else None,
            "high_risk_rejected": len([p for p in self.rejected_changes if p.risk_score > 0.7])
        }
