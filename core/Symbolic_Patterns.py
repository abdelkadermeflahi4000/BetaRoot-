# betaroot/core/symbolic_patterns.py
from __future__ import annotations
from typing import Dict, Any, List, Optional, Protocol
from dataclasses import dataclass, field
from enum import Enum
import hashlib

from .unary_logic import UnaryState, RepresentationLevel


class PatternLayer(Enum):
    BASIC = 1          # 32 نمط أساسي
    CAUSAL = 2         # 63 نمط سببي
    COGNITIVE = 3      # 63 نمط معرفي


@dataclass
class SymbolicPattern:
    id: str
    name: str
    layer: PatternLayer
    description: str
    category: str
    apply_func: callable

    def __hash__(self):
        return hash(self.id)

    def apply(self, state: UnaryState) -> UnaryState:
        """تطبيق النمط على حالة آحادية"""
        result = self.apply_func(state)
        # الحفاظ على مبدأ Only 1
        result.parent_states.append(state)
        result.metadata['applied_pattern'] = self.id
        return result


class SymbolicPatternEngine:
    """
    محرك الأنماط الرمزية الكامل (158 نمط)
    """
    def __init__(self):
        self.patterns: Dict[str, SymbolicPattern] = {}
        self._register_all_patterns()

    def _register_all_patterns(self):
        """تسجيل كل الـ 158 نمط"""
        self._register_basic_patterns()      # 32
        self._register_causal_patterns()     # 63
        self._register_cognitive_patterns()  # 63

    def _register_basic_patterns(self):
        """Layer 1: Basic Patterns (32)"""
        basic = [
            # Being & Representation (8)
            ("pure_being", "Pure Being", "Being & Representation", lambda s: s),
            ("first_rep", "First Representation", "Being & Representation", lambda s: UnaryState(RepresentationLevel.FIRST_ORDER, s.content)),
            # ... (يمكنك إضافة الباقي)
            # Movement & Rest (8)
            # Expansion & Contraction (8)
            # Combination & Separation (8)
        ]
        for pid, name, cat, func in basic:
            self.patterns[pid] = SymbolicPattern(
                id=pid, name=name, layer=PatternLayer.BASIC,
                description=cat, category=cat, apply_func=func
            )

    def _register_causal_patterns(self):
        """Layer 2: Causal Patterns (63)"""
        # Direct Causation (21) + Indirect (21) + Complex (21)
        # مثال:
        self.patterns["direct_single_single"] = SymbolicPattern(
            id="direct_single_single",
            name="Direct Single → Single",
            layer=PatternLayer.CAUSAL,
            description="علاقة سببية مباشرة من كيان واحد إلى كيان واحد",
            category="Direct Causation",
            apply_func=lambda s: UnaryState(RepresentationLevel.SYMBOLIC, {"cause": s.content, "effect": "result"})
        )
        # ... باقي الأنماط السببية

    def _register_cognitive_patterns(self):
        """Layer 3: Cognitive Patterns (63)"""
        # Logical Inference (21) + Analysis & Synthesis (21) + Perception (21)
        self.patterns["modus_ponens"] = SymbolicPattern(
            id="modus_ponens",
            name="Modus Ponens",
            layer=PatternLayer.COGNITIVE,
            description="إذا P → Q و P صحيح → Q صحيح",
            category="Logical Inference",
            apply_func=lambda s: s  # يمكن توسيعه لاحقاً
        )
        # ... باقي الأنماط المعرفية

    def get_pattern(self, pattern_id: str) -> Optional[SymbolicPattern]:
        return self.patterns.get(pattern_id)

    def apply(self, state: UnaryState, pattern_id: str) -> UnaryState:
        """التطبيق الرئيسي"""
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            raise ValueError(f"نمط غير موجود: {pattern_id}")
        return pattern.apply(state)

    def apply_multiple(self, state: UnaryState, pattern_ids: List[str]) -> UnaryState:
        """تطبيق سلسلة من الأنماط"""
        current = state
        for pid in pattern_ids:
            current = self.apply(current, pid)
        return current

    def list_patterns(self, layer: Optional[PatternLayer] = None) -> List[SymbolicPattern]:
        if layer is None:
            return list(self.patterns.values())
        return [p for p in self.patterns.values() if p.layer == layer]

    def search_by_category(self, category: str) -> List[SymbolicPattern]:
        return [p for p in self.patterns.values() if p.category == category]
