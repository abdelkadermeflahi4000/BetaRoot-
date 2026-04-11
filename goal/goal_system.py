# betaroot/goal/goal_system.py
"""
Goal System Module for BetaRoot
Provides goal-driven cognition: formulation, decomposition, planning,
progress tracking, conflict resolution, and self-reflection.

Philosophy:
- Goals drive learning & reasoning, not vice versa
- Every goal must be measurable, revisable, and explainable
- Progress is inferred from Memory & Reasoning state, not hard-coded
- Conflicts are resolved via priority × urgency × trust

Author: BetaRoot Team
Date: April 2026
"""
import uuid
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

logger = logging.getLogger(__name__)


# ==========================================
# 📐 1. تعريفات الأهداف (Goal Types & Status)
# ==========================================
class GoalType(Enum):
    KNOWLEDGE_ACQUISITION = "acquire_knowledge"  # جمع/تحديث معرفة
    INFERENCE = "solve_query"                   # الإجابة على استعلام معقد
    OPTIMIZATION = "improve_accuracy"           # تحسين CPDs/قواعد/ثقة
    EXPLORATION = "explore_hypothesis"          # اختبار فرضية جديدة
    MAINTENANCE = "system_health"               # فحص اتساق، تنظيف ذاكرة
    SELF_REFLECTION = "evaluate_reasoning"      # تقييم جودة الاستدلال السابق

class GoalStatus(Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    BLOCKED = "blocked"       # بانتظار تبعية أو مورد
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


# ==========================================
# 🎯 2. تمثيل الهدف (Goal Dataclass)
# ==========================================
@dataclass
class Goal:
    """هدف معرفي قابل للتتبع والقياس"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    description: str = ""
    type: GoalType = GoalType.KNOWLEDGE_ACQUISITION
    status: GoalStatus = GoalStatus.PROPOSED
    priority: float = 0.5  # 0.0 (منخفض) → 1.0 (حرج)
    
    # معايير النجاح (يتم تقييمها تلقائياً أو يدوياً)
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    
    # العلاقات الهرمية والتبعيات
    subgoals: List[str] = field(default_factory=list)  # معرفات الأهداف الفرعية
    dependencies: List[str] = field(default_factory=list)  # يجب اكتمالها أولاً
    
    # التتبع الديناميكي
    progress: float = 0.0  # 0.0 → 1.0
    confidence: float = 0.5  # ثقة النظام في إمكانية إكمال الهدف
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    
    # وسوم وبيانات إضافية للذاكرة والسياق
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def update_state(self, progress: Optional[float] = None, 
                     confidence: Optional[float] = None,
                     status: Optional[GoalStatus] = None,
                     failure_reason: Optional[str] = None) -> None:
        """تحديث حالة الهدف مع تسجيل الطابع الزمني"""
        if progress is not None: self.progress = max(0.0, min(1.0, progress))
        if confidence is not None: self.confidence = max(0.0, min(1.0, confidence))
        if status is not None: self.status = status
        if failure_reason: self.failure_reason = failure_reason
        self.updated_at = datetime.now()
        if self.status == GoalStatus.COMPLETED:
            self.completed_at = self.updated_at

    def calculate_composite_progress(self, subgoals_progress: Dict[str, float]) -> float:
        """حساب التقدم تلقائياً من الأهداف الفرعية"""
        if not subgoals_progress: return self.progress
        relevant = [subgoals_progress.get(sid, 0.0) for sid in self.subgoals]
        self.progress = sum(relevant) / len(relevant) if relevant else 0.0
        return self.progress

    def to_dict(self) -> dict:
        return {
            "id": self.id, "title": self.title, "description": self.description,
            "type": self.type.value, "status": self.status.value,
            "priority": self.priority, "progress": self.progress,
            "confidence": self.confidence, "success_criteria": self.success_criteria,
            "subgoals": self.subgoals, "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "failure_reason": self.failure_reason,
            "tags": self.tags, "meta": self.meta
        }

    @classmethod
    def from_dict(cls,  dict) -> 'Goal':
        data["type"] = GoalType(data["type"])
        data["status"] = GoalStatus(data["status"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        data["completed_at"] = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        return cls(**data)


# ==========================================
# 🧠 3. مدير الأهداف (Goal Manager)
# ==========================================
class GoalManager:
    """
    المحرك المركزي لإدارة الأهداف في BetaRoot
    
    المسؤول عن:
    - صياغة الأهداف وتحليلها إلى مهام فرعية
    - تخطيط مسار التنفيذ باستخدام الذاكرة والاستدلال
    - تتبع التقدم تلقائياً بناءً على حالة النظام
    - كشف وحل التعارضات بين الأهداف المتنافسة
    - الأرشفة والتعلم من النتائج (نجاح/فشل)
    """
    
    def __init__(self, memory_manager=None, reasoning_engine=None, storage_path: Optional[str] = None):
        self.goals: Dict[str, Goal] = {}
        self.active_queue: List[str] = []  # طابور الأهداف النشطة (مرتبة بالأولوية)
        self.memory = memory_manager
        self.reasoning = reasoning_engine
        self.storage_path = Path(storage_path) if storage_path else Path("data/goals")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("GoalManager initialized")
    
    # ========== إنشاء وإدارة الأهداف ==========
    
    def create_goal(self, title: str, description: str, goal_type: GoalType,
                    success_criteria: Dict[str, Any], priority: float = 0.5,
                    tags: List[str] = None, dependencies: List[str] = None) -> Goal:
        """إنشاء هدف جديد وتسجيله في النظام"""
        goal = Goal(
            title=title, description=description, type=goal_type,
            priority=priority, success_criteria=success_criteria,
            tags=tags or [], dependencies=dependencies or []
        )
        
        # التحقق من التبعيات
        for dep_id in goal.dependencies:
            if dep_id not in self.goals:
                raise ValueError(f"Dependency goal '{dep_id}' not found")
            if self.goals[dep_id].status not in (GoalStatus.COMPLETED, GoalStatus.ARCHIVED):
                goal.status = GoalStatus.BLOCKED
                goal.meta["blocked_by"] = dep_id
        
        self.goals[goal.id] = goal
        if goal.status == GoalStatus.PROPOSED:
            self.active_queue.append(goal.id)
            self._sort_queue()
            
        # تسجيل في الذاكرة العرضية
        if self.memory:
            self.memory.store(
                content=goal.to_dict(), memory_type="goal",
                priority="HIGH" if priority > 0.8 else "MEDIUM",
                source="goal_manager", tags=goal.tags
            )
            
        logger.info(f"Goal created: {goal.id} '{title}' (status={goal.status.value})")
        return goal
    
    def decompose_goal(self, parent_id: str, subgoals: List[Goal]) -> bool:
        """تحليل هدف معقد إلى أهداف فرعية قابلة للتنفيذ"""
        parent = self.goals.get(parent_id)
        if not parent:
            raise ValueError(f"Parent goal '{parent_id}' not found")
        
        for sub in subgoals:
            sub.dependencies.append(parent_id)
            self.goals[sub.id] = sub
            parent.subgoals.append(sub.id)
            
        parent.status = GoalStatus.ACTIVE
        parent.updated_at = datetime.now()
        self._sort_queue()
        
        logger.info(f"Goal {parent_id} decomposed into {len(subgoals)} subgoals")
        return True
    
    # ========== التقييم والتقدم ==========
    
    def evaluate_progress(self, goal_id: Optional[str] = None) -> Dict[str, float]:
        """
        تقييم تقدم هدف واحد أو كل الأهداف النشطة
        يستخدم الذاكرة الحالية ومحرك الاستدلال للتحقق من معايير النجاح
        """
        targets = [self.goals[goal_id]] if goal_id and goal_id in self.goals else self.goals.values()
        progress_map = {}
        
        for goal in targets:
            if goal.status in (GoalStatus.COMPLETED, GoalStatus.FAILED, GoalStatus.ARCHIVED):
                continue
                
            # 1. تقييم معايير النجاح
            criteria_met = self._check_criteria(goal)
            
            # 2. تحديث التقدم
            if criteria_met:
                goal.update_state(progress=1.0, confidence=1.0, status=GoalStatus.COMPLETED)
                progress_map[goal.id] = 1.0
                logger.info(f"✅ Goal completed: {goal.id} '{goal.title}'")
            else:
                # تقدير ديناميكي بناءً على الثقة والأولوية
                estimated = min(0.95, goal.confidence * 0.7 + (goal.progress * 0.3))
                goal.update_state(progress=estimated)
                progress_map[goal.id] = estimated
                
                # إذا انخفضت الثقة بشدة، عيّن الحالة إلى BLOCKED أو FAILED
                if goal.confidence < 0.2:
                    goal.update_state(status=GoalStatus.FAILED, failure_reason="Low confidence threshold")
                    progress_map[goal.id] = 0.0
                    
        return progress_map
    
    def _check_criteria(self, goal: Goal) -> bool:
        """التحقق من معايير النجاح باستخدام الذاكرة/الاستدلال"""
        if not goal.success_criteria:
            return False  # بدون معايير، لا يمكن الإعلان عن الاكتمال
            
        # دعم معايير بسيطة (مطابقة قيم في الذاكرة)
        if self.memory:
            for key, expected in goal.success_criteria.items():
                # بحث دلالي أو مباشر في الذاكرة
                results = self.memory.retrieve(key, limit=1)
                if not results or results[0].content.get("value") != expected:
                    return False
        return True
    
    # ========== حل التعارضات والأولوية ==========
    
    def resolve_conflicts(self) -> List[Dict[str, Any]]:
        """كشف الأهداف المتعارضة واقتراح حل"""
        conflicts = []
        active = [g for g in self.goals.values() if g.status == GoalStatus.ACTIVE]
        
        for i, g1 in enumerate(active):
            for g2 in active[i+1:]:
                # تعارض في الموارد/السياق
                if set(g1.tags) & set(g2.tags) and g1.priority != g2.priority:
                    # تعارض في المعايير
                    if self._criteria_conflict(g1, g2):
                        conflicts.append({
                            "goal_a": g1.id, "goal_b": g2.id,
                            "type": "resource_criteria_clash",
                            "suggestion": "Defer lower priority or merge criteria"
                        })
                        
        if conflicts:
            logger.warning(f"Detected {len(conflicts)} goal conflicts")
        return conflicts
    
    def _criteria_conflict(self, g1: Goal, g2: Goal) -> bool:
        """تحقق مما إذا كانت معايير النجاح متعارضة منطقياً"""
        # تبسيط: إذا كانت تتطلب حالات متناقضة لنفس المتغير
        c1_vars = set(g1.success_criteria.keys())
        c2_vars = set(g2.success_criteria.keys())
        common = c1_vars & c2_vars
        for var in common:
            if g1.success_criteria[var] != g2.success_criteria[var]:
                return True
        return False
    
    # ========== الحلقة التشغيلية (Tick) ==========
    
    def tick(self) -> Dict[str, Any]:
        """
        دورة تشغيلية واحدة: تقييم التقدم → حل التعارضات → تحديث الطابور
        يُستدعى دورياً من الـ Main Loop أو الـ Scheduler
        """
        progress = self.evaluate_progress()
        conflicts = self.resolve_conflicts()
        self._sort_queue()
        
        # أهداف جاهزة للتنفيذ (أعلى أولوية)
        next_goals = self.active_queue[:3] if self.active_queue else []
        
        return {
            "progress_updates": progress,
            "conflicts": conflicts,
            "next_actions": next_goals,
            "active_count": len([g for g in self.goals.values() if g.status == GoalStatus.ACTIVE])
        }
    
    def _sort_queue(self):
        """ترتيب طابور الأهداف: أولوية × ثقة × حديثية"""
        def score(gid):
            g = self.goals[gid]
            if g.status != GoalStatus.PROPOSED: return -1
            return (g.priority * 0.6) + (g.confidence * 0.3) + (0.1 * min(1, (datetime.now()-g.created_at).days/30))
            
        self.active_queue.sort(key=lambda gid: score(gid), reverse=True)
    
    # ========== الاستمرارية والتصدير ==========
    
    def save_state(self, filename: Optional[str] = None) -> str:
        """حفظ حالة الأهداف كاملة"""
        filename = filename or f"goals_{datetime.now().strftime('%Y%m%d')}.json"
        path = self.storage_path / filename
        state = {gid: g.to_dict() for gid, g in self.goals.items()}
        path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"Goals state saved to {path}")
        return str(path)
    
    def load_state(self, filename: str) -> None:
        """استعادة حالة أهداف محفوظة"""
        path = self.storage_path / filename
        if not path.exists(): raise FileNotFoundError
        state = json.loads(path.read_text(encoding="utf-8"))
        self.goals = {gid: Goal.from_dict(d) for gid, d in state.items()}
        self.active_queue = [gid for gid, g in self.goals.items() if g.status == GoalStatus.PROPOSED]
        self._sort_queue()
        logger.info(f"Goals state loaded from {path}")
    
    def get_summary(self) -> Dict[str, Any]:
        """ملخص إحصائي سريع لحالة الأهداف"""
        counts = {s.value: 0 for s in GoalStatus}
        for g in self.goals.values():
            counts[g.status.value] += 1
        return {
            "total": len(self.goals),
            "status_distribution": counts,
            "active_priorities": [g.priority for g in self.goals.values() if g.status == GoalStatus.ACTIVE]
        }
