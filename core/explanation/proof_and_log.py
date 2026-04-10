# betaroot/core/explanation/proof_and_log.py
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class InferenceType(Enum):
    SYMBOLIC = "symbolic"
    PROBABILISTIC = "probabilistic"
    HYBRID = "hybrid"

@dataclass
class ProofNode:
    """عقدة في شجرة الإثبات: تمثل متغيرًا، قيمته، درجة يقينه، وسبب استنتاجه"""
    variable: str
    value: Any
    confidence: float
    inference_type: InferenceType
    justification: str  # معرف القاعدة أو "bayesian_posterior"
    children: List['ProofNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "variable": self.variable, "value": self.value,
            "confidence": self.confidence, "type": self.inference_type.value,
            "justification": self.justification,
            "children": [c.to_dict() for c in self.children],
            "metadata": self.metadata
        }

    def format_arabic(self, indent: int = 0, max_depth: int = 8) -> str:
        if indent > max_depth:
            return "  " * indent + "⋮ (تم اقتطاع الشجرة)"
        prefix = "  " * indent
        emoji = {"symbolic": "🔷", "probabilistic": "🟠", "hybrid": "🟣"}.get(self.inference_type.value, "⚪")
        line = f"{prefix}{emoji} {self.variable} = {self.value} ({self.confidence:.2%}) ← {self.justification}"
        parts = [line]
        for child in self.children:
            parts.append(child.format_arabic(indent + 1, max_depth))
        return "\n".join(parts)

@dataclass
class LogEntry:
    timestamp: datetime
    action: str  # add, update, retract, revise, observe, infer
    variable: str
    old_value: Any
    new_value: Any
    confidence_delta: float
    source: str
    reason: Optional[str] = None

class ChangeLog:
    """سجل التغييرات الزمني: يتتبع كل تعديل على الحقائق أو المعتقدات"""
    def __init__(self, max_entries: int = 5000):
        self.entries: List[LogEntry] = []
        self.max_entries = max_entries

    def add(self, action: str, variable: str, old_val: Any, new_val: Any,
            conf_delta: float, source: str, reason: str = None):
        entry = LogEntry(datetime.now(), action, variable, old_val, new_val, conf_delta, source, reason)
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)

    def filter(self, variable=None, action=None, source=None, limit=100) -> List[LogEntry]:
        res = self.entries
        if variable: res = [e for e in res if e.variable == variable]
        if action: res = [e for e in res if e.action == action]
        if source: res = [e for e in res if e.source == source]
        return res[-limit:]

    def to_markdown(self, limit=50) -> str:
        lines = ["## 📜 سجل التغييرات (Change Log)",
                 "| الوقت | الإجراء | المتغير | من ← إلى | Δ يقين | المصدر | السبب |",
                 "|-------|---------|---------|-----------|--------|--------|-------|"]
        for e in reversed(self.filter(limit=limit)):
            ts = e.timestamp.strftime("%H:%M:%S")
            conf = f"{e.confidence_delta:+.2f}" if e.confidence_delta != 0 else "—"
            lines.append(f"| {ts} | {e.action} | {e.variable} | {e.old_value} → {e.new_value} | {conf} | {e.source} | {e.reason or '—'} |")
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps([
            {"timestamp": e.timestamp.isoformat(), "action": e.action, "variable": e.variable,
             "old_value": e.old_value, "new_value": e.new_value, "confidence_delta": e.confidence_delta,
             "source": e.source, "reason": e.reason} for e in self.entries
        ], ensure_ascii=False, indent=2)
