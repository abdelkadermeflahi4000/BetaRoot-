"""
BetaRoot: SymbolicPatternsExtended — 158 نمط رمزي مكتمل

Layer 1 — BASIC    (32 نمط): الوجود، الحركة، الهيكل
Layer 2 — CAUSAL   (63 نمط): العلاقات السببية والفيزيائية
Layer 3 — COGNITIVE (63 نمط): الاستدلال والإدراك والمعرفة

كل نمط = (id, name_en, name_ar, layer, description, transform_tag)
transform_tag يصف ما يفعله النمط بالحالة الآحادية.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Layer(Enum):
    BASIC    = 1
    CAUSAL   = 2
    COGNITIVE = 3


@dataclass
class Pattern:
    pid:         str          # معرف فريد
    name_en:     str
    name_ar:     str
    layer:       Layer
    description: str
    tag:         str          # الوسم الوظيفي للتحويل


# ══════════════════════════════════════════════════════════════
# LAYER 1 — BASIC (32 نمط)
# الكيان الأساسي: الوجود، الحركة، الهيكل، الحدود
# ══════════════════════════════════════════════════════════════

_LAYER1: List[Tuple] = [
    # وجود وتمثيل (1-4)
    ("B01", "Pure_Being",           "الوجود الخالص",         "identity"),
    ("B02", "First_Representation", "التمثيل الأول",          "encode_primary"),
    ("B03", "Second_Representation","التمثيل الثاني",         "encode_secondary"),
    ("B04", "Self_Reference",       "الإشارة الذاتية",        "self_loop"),

    # حركة (5-10)
    ("B05", "Forward_Motion",       "الحركة الأمامية",        "translate_forward"),
    ("B06", "Backward_Motion",      "الحركة الخلفية",         "translate_backward"),
    ("B07", "Circular_Motion",      "الحركة الدائرية",        "rotate"),
    ("B08", "Oscillation",          "التذبذب",                "oscillate"),
    ("B09", "Spiral_Motion",        "الحركة اللولبية",        "spiral"),
    ("B10", "Recursive_Motion",     "الحركة التكرارية",       "recurse"),

    # تحويل الحجم (11-14)
    ("B11", "Expansion",            "التوسع",                 "scale_up"),
    ("B12", "Contraction",          "الانكماش",               "scale_down"),
    ("B13", "Uniform_Scaling",      "التحجيم المتناسب",       "scale_uniform"),
    ("B14", "Asymmetric_Scaling",   "التحجيم غير المتناسب",   "scale_asymmetric"),

    # تركيب وتفكيك (15-18)
    ("B15", "Combination",          "التركيب",                "combine"),
    ("B16", "Separation",           "الفصل",                  "separate"),
    ("B17", "Decomposition",        "التحليل الهيكلي",        "decompose"),
    ("B18", "Recomposition",        "إعادة التركيب",          "recompose"),

    # تحولات هيكلية (19-22)
    ("B19", "Reflection",           "الانعكاس",               "reflect"),
    ("B20", "Symmetry",             "التماثل",                "symmetrize"),
    ("B21", "Transformation",       "التحول",                 "transform"),
    ("B22", "Inversion",            "القلب",                  "invert"),

    # حدود وتدفق (23-26)
    ("B23", "Boundary",             "الحد",                   "bound"),
    ("B24", "Threshold",            "العتبة",                 "threshold"),
    ("B25", "Flow",                 "التدفق",                 "flow"),
    ("B26", "Resistance",           "المقاومة",               "resist"),

    # علاقات (27-30)
    ("B27", "Hierarchy",            "التدرج الهرمي",          "hierarchize"),
    ("B28", "Parallelism",          "التوازي",                "parallelize"),
    ("B29", "Intersection",         "التقاطع",                "intersect"),
    ("B30", "Divergence",           "التشعب",                 "diverge"),

    # توازن وإغلاق (31-32)
    ("B31", "Equilibrium",          "التوازن",                "balance"),
    ("B32", "Closure",              "الإغلاق",                "close"),
]


# ══════════════════════════════════════════════════════════════
# LAYER 2 — CAUSAL (63 نمط)
# السببية: مباشرة، غير مباشرة، فيزيائية، إحصائية، ديناميكية
# ══════════════════════════════════════════════════════════════

_LAYER2: List[Tuple] = [
    # سببية أساسية (1-8)
    ("C01", "Direct_Causation",       "السببية المباشرة",          "cause_direct"),
    ("C02", "Indirect_Causation",     "السببية غير المباشرة",      "cause_indirect"),
    ("C03", "Reciprocal_Causation",   "السببية المتبادلة",         "cause_reciprocal"),
    ("C04", "Feedback_Loop",          "حلقة التغذية الراجعة",      "feedback"),
    ("C05", "Chain_Reaction",         "تفاعل متسلسل",              "chain"),
    ("C06", "Cascading_Failure",      "فشل متتالي",                "cascade_fail"),
    ("C07", "Delay_Causation",        "سببية مؤخرة",               "cause_delayed"),
    ("C08", "Threshold_Effect",       "تأثير العتبة",               "threshold_effect"),

    # تكثيف وتخفيف (9-14)
    ("C09", "Amplification",          "التضخيم",                   "amplify"),
    ("C10", "Attenuation",            "التخفيف",                   "attenuate"),
    ("C11", "Catalysis",              "الحفز",                     "catalyze"),
    ("C12", "Inhibition",             "التثبيط",                   "inhibit"),
    ("C13", "Saturation",             "التشبع",                    "saturate"),
    ("C14", "Deprivation",            "الحرمان",                   "deprive"),

    # قوانين فيزيائية (15-26)
    ("C15", "Rayleigh_Scattering",    "تشتت ريليه",                "scatter_rayleigh"),
    ("C16", "Resonance_Scaling",      "قانون الرنين",              "resonance_scale"),
    ("C17", "Inverse_Square_Law",     "قانون التربيع العكسي",      "inverse_square"),
    ("C18", "Snell_Refraction",       "قانون سنل للانكسار",        "refract_snell"),
    ("C19", "Hooke_Elasticity",       "قانون هوك للمرونة",         "elastic_hooke"),
    ("C20", "Newton_Gravity",         "جاذبية نيوتن",              "gravity_newton"),
    ("C21", "Coulomb_Electric",       "قانون كولوم الكهربي",       "electric_coulomb"),
    ("C22", "Ohm_Resistance",         "قانون أوم للمقاومة",        "resist_ohm"),
    ("C23", "Faraday_Induction",      "حث فاراداي",                "induce_faraday"),
    ("C24", "Bernoulli_Flow",         "تدفق برنولي",               "flow_bernoulli"),
    ("C25", "Archimedes_Buoyancy",    "طفو أرخميدس",               "buoy_archimedes"),
    ("C26", "Conservation_Energy",    "حفظ الطاقة",                "conserve_energy"),

    # ديناميكيات النظام (27-36)
    ("C27", "Exponential_Growth",     "النمو الأسي",               "grow_exponential"),
    ("C28", "Logistic_Growth",        "النمو اللوجستي",            "grow_logistic"),
    ("C29", "Exponential_Decay",      "الاضمحلال الأسي",           "decay_exponential"),
    ("C30", "Power_Law",              "قانون القوة",               "power_law"),
    ("C31", "Phase_Transition",       "الانتقال الطوري",           "phase_transition"),
    ("C32", "Bifurcation",            "التشعب",                    "bifurcate"),
    ("C33", "Strange_Attractor",      "الجاذب الغريب",             "attract_strange"),
    ("C34", "Entropy_Increase",       "زيادة الإنتروبيا",          "entropy_increase"),
    ("C35", "Equilibrium_Shift",      "انزياح التوازن",            "equilibrium_shift"),
    ("C36", "Oscillatory_Decay",      "اضمحلال تذبذبي",            "decay_oscillatory"),

    # حيوية وبيولوجية (37-44)
    ("C37", "Homeostasis",            "ضبط التوازن الداخلي",       "homeostasis"),
    ("C38", "Adaptation",             "التكيف",                    "adapt"),
    ("C39", "Natural_Selection",      "الانتقاء الطبيعي",         "select_natural"),
    ("C40", "Mutation",               "الطفرة",                    "mutate"),
    ("C41", "Symbiosis",              "التكافل",                   "symbiose"),
    ("C42", "Predator_Prey",          "مفترس ‒ فريسة",            "predator_prey"),
    ("C43", "Immune_Response",        "استجابة مناعية",            "immune_respond"),
    ("C44", "Metabolic_Rate",         "معدل الأيض",                "metabolize"),

    # معلوماتية وحوسبة (45-52)
    ("C45", "Signal_Noise",           "إشارة ‒ ضوضاء",            "signal_noise"),
    ("C46", "Compression",            "الضغط المعلوماتي",          "compress"),
    ("C47", "Encryption",             "التشفير",                   "encrypt"),
    ("C48", "Error_Correction",       "تصحيح الخطأ",               "error_correct"),
    ("C49", "Redundancy",             "التكرار الاحتياطي",         "redundify"),
    ("C50", "Latency",                "الكمون الزمني",             "latency"),
    ("C51", "Throughput",             "معدل النقل",                "throughput"),
    ("C52", "Bottleneck",             "عنق الزجاجة",               "bottleneck"),

    # اجتماعية واقتصادية (53-60)
    ("C53", "Network_Effect",         "تأثير الشبكة",              "network_effect"),
    ("C54", "Supply_Demand",          "العرض والطلب",              "supply_demand"),
    ("C55", "Pareto_Distribution",    "توزيع باريتو",              "pareto"),
    ("C56", "Game_Theory_Nash",       "توازن ناش",                 "nash_equilibrium"),
    ("C57", "Diffusion_Innovation",   "انتشار الابتكار",           "diffuse_innovation"),
    ("C58", "Contagion",              "العدوى",                    "contagion"),
    ("C59", "Tipping_Point",          "نقطة التحول",               "tipping_point"),
    ("C60", "Lock_In_Effect",         "تأثير الإغلاق",             "lock_in"),

    # ظهور وتعقيد (61-63)
    ("C61", "Emergence_Causation",    "السببية الظاهراتية",        "emergence"),
    ("C62", "Self_Organization",      "التنظيم الذاتي",            "self_organize"),
    ("C63", "Complexity_Edge",        "حافة التعقيد",              "edge_complexity"),
]


# ══════════════════════════════════════════════════════════════
# LAYER 3 — COGNITIVE (63 نمط)
# الاستدلال، الإدراك، المعرفة، التعلم، الإبداع
# ══════════════════════════════════════════════════════════════

_LAYER3: List[Tuple] = [
    # استدلال منطقي (1-10)
    ("G01", "Deduction",              "الاستنتاج",                 "deduce"),
    ("G02", "Induction",              "الاستقراء",                 "induce"),
    ("G03", "Abduction",              "التفسير الأفضل",            "abduce"),
    ("G04", "Analogy",                "القياس",                    "analogize"),
    ("G05", "Contradiction",          "التناقض",                   "contradict"),
    ("G06", "Contraposition",         "النقيض المعاكس",            "contrapose"),
    ("G07", "Modus_Ponens",           "الاستلزام التأكيدي",        "modus_ponens"),
    ("G08", "Modus_Tollens",          "الاستلزام النافي",          "modus_tollens"),
    ("G09", "Disjunctive_Syllogism",  "القياس الفصلي",             "disjunct_syllogism"),
    ("G10", "Hypothetical_Syllogism", "القياس الشرطي",             "hypothetical_syllogism"),

    # تحليل وتركيب (11-18)
    ("G11", "Analysis",               "التحليل",                   "analyze"),
    ("G12", "Synthesis",              "التوليف",                   "synthesize"),
    ("G13", "Abstraction",            "التجريد",                   "abstract"),
    ("G14", "Concretization",         "التجسيد",                   "concretize"),
    ("G15", "Generalization",         "التعميم",                   "generalize"),
    ("G16", "Specification",          "التخصيص",                   "specify"),
    ("G17", "Classification",         "التصنيف",                   "classify"),
    ("G18", "Clustering",             "التجميع",                   "cluster"),

    # فرضية وتحقق (19-26)
    ("G19", "Hypothesis_Formation",   "صياغة الفرضية",             "hypothesize"),
    ("G20", "Verification",           "التحقق",                    "verify"),
    ("G21", "Falsification",          "التفنيد",                   "falsify"),
    ("G22", "Confirmation",           "التأكيد",                   "confirm"),
    ("G23", "Bayesian_Update",        "التحديث البايزي",           "bayesian_update"),
    ("G24", "Prior_Formation",        "بناء المسبق",               "form_prior"),
    ("G25", "Posterior_Calculation",  "حساب اللاحق",               "calc_posterior"),
    ("G26", "Likelihood_Assessment",  "تقييم الاحتمالية",          "assess_likelihood"),

    # بحث وحل المشكلة (27-34)
    ("G27", "Problem_Decomposition",  "تفكيك المشكلة",             "decompose_problem"),
    ("G28", "Heuristic_Search",       "البحث الاستدلالي",          "search_heuristic"),
    ("G29", "Constraint_Satisfaction","إرضاء القيود",              "satisfy_constraints"),
    ("G30", "Optimization",           "التحسين",                   "optimize"),
    ("G31", "Backtracking",           "التراجع",                   "backtrack"),
    ("G32", "Branch_And_Bound",       "التفريع والتحديد",          "branch_bound"),
    ("G33", "Divide_And_Conquer",     "فرّق تسد",                  "divide_conquer"),
    ("G34", "Dynamic_Programming",    "البرمجة الديناميكية",       "dynamic_program"),

    # تعلم (35-42)
    ("G35", "Pattern_Recognition",    "التعرف على الأنماط",        "recognize_pattern"),
    ("G36", "Feature_Extraction",     "استخراج الميزات",           "extract_features"),
    ("G37", "Reinforcement",          "التعزيز",                   "reinforce"),
    ("G38", "Transfer_Learning",      "نقل التعلم",                "transfer_learn"),
    ("G39", "Meta_Learning",          "التعلم الذاتي",             "meta_learn"),
    ("G40", "Forgetting_Curve",       "منحنى النسيان",             "forget_curve"),
    ("G41", "Memory_Consolidation",   "توطيد الذاكرة",             "consolidate_memory"),
    ("G42", "Concept_Formation",      "تشكيل المفاهيم",            "form_concept"),

    # وعي وميتا (43-50)
    ("G43", "Meta_Cognition",         "ما وراء المعرفة",           "meta_cognize"),
    ("G44", "Self_Monitoring",        "المراقبة الذاتية",          "self_monitor"),
    ("G45", "Belief_Revision",        "مراجعة المعتقد",            "revise_belief"),
    ("G46", "Uncertainty_Modeling",   "نمذجة عدم اليقين",          "model_uncertainty"),
    ("G47", "Attention_Focus",        "تركيز الانتباه",            "focus_attention"),
    ("G48", "Working_Memory_Load",    "حِمل الذاكرة العاملة",      "load_working_memory"),
    ("G49", "Cognitive_Bias_Detect",  "كشف التحيز المعرفي",        "detect_bias"),
    ("G50", "Epistemic_Humility",     "التواضع المعرفي",           "epistemic_humility"),

    # إبداع وابتكار (51-58)
    ("G51", "Analogical_Reasoning",   "الاستدلال القياسي",         "reason_analogical"),
    ("G52", "Lateral_Thinking",       "التفكير الجانبي",           "think_lateral"),
    ("G53", "Conceptual_Blending",    "مزج المفاهيم",              "blend_concepts"),
    ("G54", "Creative_Constraint",    "القيد الإبداعي",            "constrain_creative"),
    ("G55", "Divergent_Thinking",     "التفكير التشعبي",           "think_divergent"),
    ("G56", "Convergent_Thinking",    "التفكير التقاربي",          "think_convergent"),
    ("G57", "Insight_Formation",      "تكوين الاستبصار",           "form_insight"),
    ("G58", "Prototype_Building",     "بناء النموذج الأولي",       "build_prototype"),

    # قرار وتقييم (59-63)
    ("G59", "Risk_Assessment",        "تقييم المخاطر",             "assess_risk"),
    ("G60", "Trade_Off_Analysis",     "تحليل المقايضات",           "analyze_tradeoff"),
    ("G61", "Satisficing",            "الإرضاء الكافي",            "satisfice"),
    ("G62", "Maximizing",             "التعظيم",                   "maximize"),
    ("G63", "Decision_Under_Uncertainty","القرار في ظل الغموض",    "decide_uncertain"),
]


# ══════════════════════════════════════════════════════════════
# محرك الأنماط الكاملة
# ══════════════════════════════════════════════════════════════

def _build_pattern(row: Tuple, layer: Layer) -> Pattern:
    pid, name_en, name_ar, tag = row
    desc = f"{name_ar} — {name_en}"
    return Pattern(pid, name_en, name_ar, layer, desc, tag)


class SymbolicPatternsExtended:
    """
    المحرك الكامل للـ 158 نمط رمزي.
    يضمّ:
      32  نمط أساسي (Layer 1)
      63  نمط سببي  (Layer 2)
      63  نمط معرفي (Layer 3)
    """

    def __init__(self):
        self._index: Dict[str, Pattern] = {}
        self._by_layer: Dict[Layer, List[Pattern]] = {
            Layer.BASIC: [], Layer.CAUSAL: [], Layer.COGNITIVE: []
        }
        self._build()

    def _build(self):
        for row in _LAYER1:
            p = _build_pattern(row, Layer.BASIC)
            self._index[p.name_en] = p
            self._by_layer[Layer.BASIC].append(p)

        for row in _LAYER2:
            p = _build_pattern(row, Layer.CAUSAL)
            self._index[p.name_en] = p
            self._by_layer[Layer.CAUSAL].append(p)

        for row in _LAYER3:
            p = _build_pattern(row, Layer.COGNITIVE)
            self._index[p.name_en] = p
            self._by_layer[Layer.COGNITIVE].append(p)

    # ──────────────────────────────────────────
    # الواجهة العامة
    # ──────────────────────────────────────────

    def get(self, name_en: str) -> Optional[Pattern]:
        return self._index.get(name_en)

    def apply(self, state: Any, pattern_name: str) -> Dict:
        """
        تطبيق نمط على حالة آحادية.
        في النسخة الحالية: إرجاع وصف التحويل مع الحالة.
        يمكن توصيله بـ UnaryLogicEngine لاحقاً.
        """
        p = self.get(pattern_name)
        if not p:
            return {
                "success": False,
                "error":   f"النمط '{pattern_name}' غير موجود",
                "state":   state
            }
        return {
            "success":     True,
            "pattern_id":  p.pid,
            "pattern":     p.name_en,
            "arabic":      p.name_ar,
            "layer":       p.layer.name,
            "transform":   p.tag,
            "state_in":    str(state),
            "state_out":   f"{p.tag}({state})"
        }

    def search(self, keyword: str) -> List[Pattern]:
        """بحث في الأنماط بالكلمة المفتاحية (عربي أو إنجليزي)"""
        kw = keyword.lower()
        return [
            p for p in self._index.values()
            if kw in p.name_en.lower() or kw in p.name_ar
        ]

    def by_layer(self, layer: Layer) -> List[Pattern]:
        return self._by_layer[layer]

    def stats(self) -> Dict:
        return {
            "total":    len(self._index),
            "basic":    len(self._by_layer[Layer.BASIC]),
            "causal":   len(self._by_layer[Layer.CAUSAL]),
            "cognitive": len(self._by_layer[Layer.COGNITIVE]),
            "target":   158,
            "coverage": f"{len(self._index)/158*100:.1f}%"
        }

    def catalog(self, layer: Optional[Layer] = None) -> str:
        """طباعة فهرس الأنماط"""
        layers = [layer] if layer else list(Layer)
        lines  = []
        for lyr in layers:
            lines.append(f"\n{'═'*50}")
            lines.append(f"  Layer {lyr.value} — {lyr.name}  ({len(self._by_layer[lyr])} نمط)")
            lines.append(f"{'═'*50}")
            for p in self._by_layer[lyr]:
                lines.append(f"  [{p.pid}] {p.name_en:<28} | {p.name_ar:<22} | {p.tag}")
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# اختبار مستقل
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    engine = SymbolicPatternsExtended()

    s = engine.stats()
    print(f"الأنماط المنفذة: {s['total']} / {s['target']}  ({s['coverage']})")
    print(f"  Basic:    {s['basic']}")
    print(f"  Causal:   {s['causal']}")
    print(f"  Cognitive:{s['cognitive']}")

    print("\n── بحث عن 'causation' ──")
    for p in engine.search("causation"):
        print(f"  {p.pid} {p.name_en} → {p.name_ar}")

    print("\n── تطبيق نمط Resonance_Scaling ──")
    result = engine.apply("disk_state_R=0.05", "Resonance_Scaling")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\n── أول 5 أنماط Layer 3 ──")
    for p in engine.by_layer(Layer.COGNITIVE)[:5]:
        print(f"  [{p.pid}] {p.name_en} | {p.name_ar}")
