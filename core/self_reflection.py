# betaroot/core/self_reflection.py
"""
Self-Reflection Module for BetaRoot
Implements meta-cognition: self-evaluation, bias detection, and systematic improvement.

Philosophy:
- "Trust but Verify": Every inference is logged and later evaluated
- "Bias is a Signal, Not a Failure": Detect patterns, adjust parameters, log changes
- "Safe Improvement": All suggestions are dry-run first, require explicit approval or auto-apply under strict thresholds

Author: BetaRoot Team
Date: April 2026
"""
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)


# ==========================================
# 📐 1. تعريفات التقييم والتحيز (Enums & Dataclasses)
# ==========================================
class BiasType(Enum):
    OVERCONFIDENCE = "overconfidence"
    UNDERCONFIDENCE = "underconfidence"
    SOURCE_BIAS = "source_bias"
    CONFIRMATION_BIAS = "confirmation_bias"
    RECENCY_BIAS = "recency_bias"
    LOGICAL_FALLACY = "logical_fallacy"

class ImprovementAction(Enum):
    ADJUST_CERTAINTY_THRESHOLD = "adjust_threshold"
    UPDATE_SOURCE_TRUST = "update_source_trust"
    PRUNE_UNRELIABLE_KNOWLEDGE = "prune_knowledge"
    REPRIORITIZE_GOALS = "reprioritize_goals"
    RECALIBRATE_CONFIDENCE = "recalibrate_confidence"
    FLAG_FOR_HUMAN_REVIEW = "flag_for_review"

@dataclass
class ReflectionReport:
    """تقرير شامل عن جلسة التقييم الذاتي"""
    timestamp: datetime = field(default_factory=datetime.now)
    evaluation_score: float = 0.0  # 0.0 (ضعيف) → 1.0 (ممتاز)
    calibration_error: float = 0.0  # متوسط الفرق بين الثقة والدقة الفعلية
    biases_detected: List[Dict[str, Any]] = field(default_factory=list)
    reasoning_quality: str = "unknown"  # excellent, good, acceptable, poor
    suggested_actions: List[Dict[str, Any]] = field(default_factory=list)
    meta Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "evaluation_score": self.evaluation_score,
            "calibration_error": self.calibration_error,
            "reasoning_quality": self.reasoning_quality,
            "biases_count": len(self.biases_detected),
            "actions_count": len(self.suggested_actions),
            "metadata": self.meta
        }

@dataclass
class ImprovementPlan:
    """خطة تحسين قابلة للتنفيذ بأمان"""
    actions: List[Dict[str, Any]]
    expected_impact: str
    risk_level: str  # low, medium, high
    dry_run_result: Dict[str, Any] = field(default_factory=dict)


# ==========================================
# 🔍 2. محرك كشف التحيز (BiasDetector)
# ==========================================
class BiasDetector:
    """
    يحلل سجلات الاستدلال والذاكرة لاكتشاف الأنماط المنحازة
    
    المدخلات:
    - inference_logs: قائمة بنتائج الاستدلال السابقة {query, confidence, actual_outcome, source, reasoning_steps}
    - memory_trust_dist: توزيع الثقة حسب المصادر
    """
    
    @staticmethod
    def detect_overconfidence(inference_logs: List[Dict], threshold: float = 0.15) -> List[Dict]:
        """كشف المبالغة في الثقة (الثقة المعلنة > الدقة الفعلية)"""
        biased_items = []
        for log in inference_logs:
            conf = log.get("confidence", 0.5)
            actual = log.get("actual_accuracy", 0.5)
            if conf - actual > threshold:
                biased_items.append({
                    "type": BiasType.OVERCONFIDENCE.value,
                    "severity": (conf - actual) / threshold,
                    "instance": log["query"],
                    "confidence": conf, "actual": actual
                })
        return biased_items

    @staticmethod
    def detect_source_bias(trust_scores: Dict[str, float], min_samples: int = 5) -> List[Dict]:
        """كشف تحيز المصدر (مصدر معين دائماً عالي/منخفض الثقة دون مبرر)"""
        biases = []
        if len(trust_scores) < min_samples: return biases
        mean_trust = statistics.mean(trust_scores.values())
        std_trust = statistics.stdev(trust_scores.values()) if len(trust_scores) > 1 else 0.0
        
        for source, trust in trust_scores.items():
            if abs(trust - mean_trust) > 2 * std_trust:
                biases.append({
                    "type": BiasType.SOURCE_BIAS.value,
                    "source": source,
                    "trust": trust,
                    "deviation": trust - mean_trust,
                    "suggestion": "Normalize trust scoring or verify source reliability"
                })
        return biases

    @staticmethod
    def detect_confirmation_bias(inference_logs: List[Dict]) -> List[Dict]:
        """كشف تجاهل الأدلة المضادة (تأكيد معتقدات عالية الثقة رغم أدلة معاكسة)"""
        biases = []
        for log in inference_logs:
            if log.get("confidence", 0) > 0.9 and log.get("contradictory_evidence_count", 0) > 0:
                if not log.get("revised", False):
                    biases.append({
                        "type": BiasType.CONFIRMATION_BIAS.value,
                        "instance": log["query"],
                        "confidence": log["confidence"],
                        "contradictions": log["contradictory_evidence_count"],
                        "suggestion": "Force belief revision or trigger human review"
                    })
        return biases


# ==========================================
# 🛠️ 3. محرك التحسين المنهجي (ImprovementEngine)
# ==========================================
class ImprovementEngine:
    """
    يولد خطط تحسين آمنة بناءً على تقارير التقييم
    
    المسؤول عن:
    - تحويل التحيزات إلى إجراءات قابلة للتنفيذ
    - تقدير الأثر والمخاطر
    - دعم وضع Dry-Run قبل التطبيق الفعلي
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "max_threshold_adjustment": 0.1,
            "min_trust_for_auto_update": 0.6,
            "dry_run_always": True
        }
        
    def generate_plan(self, report: ReflectionReport) -> ImprovementPlan:
        """توليد خطة تحسين من تقرير التقييم"""
        actions = []
        risk = "low"
        
        # 1. معالجة فرط الثقة
        overconf = [b for b in report.biases_detected if b["type"] == BiasType.OVERCONFIDENCE.value]
        if overconf:
            avg_severity = statistics.mean(b["severity"] for b in overconf)
            actions.append({
                "action": ImprovementAction.RECALIBRATE_CONFIDENCE.value,
                "target": "global",
                "adjustment": -min(0.1, avg_severity * 0.05),
                "reason": f"Systematic overconfidence detected (severity: {avg_severity:.2f})"
            })
            risk = "medium" if avg_severity > 1.5 else "low"
            
        # 2. معالجة تحيز المصدر
        source_biases = [b for b in report.biases_detected if b["type"] == BiasType.SOURCE_BIAS.value]
        for sb in source_biases:
            if abs(sb["deviation"]) > 0.3:
                actions.append({
                    "action": ImprovementAction.UPDATE_SOURCE_TRUST.value,
                    "target": sb["source"],
                    "adjustment": -sb["deviation"] * 0.2,
                    "reason": f"Source trust deviation: {sb['deviation']:.2f}"
                })
                risk = "medium"
                
        # 3. معالجة تجاهل التناقضات
        confirm_bias = [b for b in report.biases_detected if b["type"] == BiasType.CONFIRMATION_BIAS.value]
        if confirm_bias:
            actions.append({
                "action": ImprovementAction.FLAG_FOR_HUMAN_REVIEW.value,
                "target": "confirmation_bias_instances",
                "count": len(confirm_bias),
                "reason": "High-confidence beliefs resisted contradictory evidence"
            })
            risk = "high"
            
        return ImprovementPlan(
            actions=actions,
            expected_impact="Improved calibration & reduced systematic bias",
            risk_level=risk
        )
    
    def execute_plan(self, plan: ImprovementPlan, 
                    apply_fn: Callable[[Dict], bool],
                    dry_run: bool = True) -> Dict[str, Any]:
        """
        تنفيذ خطة التحسين مع دعم Dry-Run
        
        Args:
            plan: خطة التحسين
            apply_fn: دالة خارجية تطبق التغيير على النظام الفعلي
            dry_run: إذا True، يحاكي التنفيذ دون تغيير الحالة
        """
        results = {"applied": 0, "skipped": 0, "errors": [], "dry_run": dry_run}
        
        for action in plan.actions:
            if dry_run:
                results["applied"] += 1
                logger.info(f"[DRY RUN] Would execute: {action['action']} on {action['target']}")
                continue
                
            try:
                success = apply_fn(action)
                if success:
                    results["applied"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["errors"].append({"action": action["action"], "error": str(e)})
                results["skipped"] += 1
                
        return results


# ==========================================
# 🧠 4. وحدة التقييم الذاتي الرئيسية (SelfReflectionModule)
# ==========================================
class SelfReflectionModule:
    """
    الواجهة الموحدة للتفكير الذاتي في BetaRoot
    
    يربط بين:
    - سجلات الاستدلال (Inference Logs)
    - إحصائيات الذاكرة والثقة
    - محرك كشف التحيز
    - محرك التحسين
    - نظام الأهداف (لإعادة توجيه الأولويات عند الحاجة)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {"reflection_interval_hours": 24, "min_log_size": 50}
        self.bias_detector = BiasDetector()
        self.improvement_engine = ImprovementEngine()
        self.reflection_history: List[ReflectionReport] = []
        self.last_reflection: Optional[datetime] = None
        
        logger.info("SelfReflectionModule initialized")
    
    def evaluate_and_reflect(self, 
                            inference_logs: List[Dict],
                            trust_scores: Dict[str, float] = None,
                            memory_stats: Dict[str, Any] = None) -> ReflectionReport:
        """
        دورة تقييم ذاتي كاملة
        
        Args:
            inference_logs: سجل الاستدلال الحديث
            trust_scores: توزيع الثقة حسب المصادر
            memory_stats: إحصائيات الذاكرة (اختياري)
        """
        if len(inference_logs) < self.config["min_log_size"]:
            logger.debug("Insufficient logs for reflection. Skipping.")
            return None
            
        # 1. كشف التحيزات
        biases = []
        biases.extend(self.bias_detector.detect_overconfidence(inference_logs))
        if trust_scores:
            biases.extend(self.bias_detector.detect_source_bias(trust_scores))
        biases.extend(self.bias_detector.detect_confirmation_bias(inference_logs))
        
        # 2. حساب جودة المعايير (Calibration)
        if inference_logs:
            cal_errors = [abs(log["confidence"] - log.get("actual_accuracy", 0.5)) for log in inference_logs if "confidence" in log]
            avg_cal = statistics.mean(cal_errors) if cal_errors else 0.0
        else:
            avg_cal = 0.0
            
        # 3. تقييم الجودة الشاملة
        eval_score = max(0.0, 1.0 - avg_cal - (len(biases) * 0.1))
        quality = "excellent" if eval_score > 0.85 else "good" if eval_score > 0.7 else "acceptable" if eval_score > 0.5 else "poor"
        
        # 4. توليد خطة التحسين
        report = ReflectionReport(
            evaluation_score=round(eval_score, 3),
            calibration_error=round(avg_cal, 3),
            biases_detected=biases,
            reasoning_quality=quality,
            meta={"log_count": len(inference_logs), "trust_sources": len(trust_scores or {})}
        )
        
        plan = self.improvement_engine.generate_plan(report)
        report.suggested_actions = plan.actions
        
        # 5. حفظ التقرير
        self.reflection_history.append(report)
        self.last_reflection = datetime.now()
        
        logger.info(f"Reflection complete: Score={report.evaluation_score}, Biases={len(biases)}, Quality={quality}")
        return report
    
    def get_trend_analysis(self, window: int = 10) -> Dict[str, Any]:
        """تحليل اتجاه التقييم الذاتي عبر الزمن"""
        recent = self.reflection_history[-window:]
        if not recent:
            return {"trend": "insufficient_data"}
            
        scores = [r.evaluation_score for r in recent]
        cal_errors = [r.calibration_error for r in recent]
        
        return {
            "avg_score": statistics.mean(scores),
            "score_trend": "improving" if scores[-1] > statistics.mean(scores[:-1]) else "declining",
            "avg_calibration_error": statistics.mean(cal_errors),
            "total_reflections": len(self.reflection_history),
            "last_reflection": self.last_reflection.isoformat() if self.last_reflection else None
        }
    
    def export_reflection_log(self, filepath: Optional[str] = None) -> str:
        """تصدير سجل التقييمات للتحليل الخارجي أو المراجعة البشرية"""
        import json
        filepath = filepath or f"reflections_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.reflection_history], f, ensure_ascii=False, indent=2)
        return filepath
