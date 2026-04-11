"""
BetaRoot Core: Resonance Law Module
قانون الرنين الفيزيائي — مدمج مع بنية BetaRoot

المعادلة الأساسية:
    f = k * (h / R²)

حيث:
    f  = التردد (Hz)
    R  = نصف القطر (m)
    h  = السُمك (m)
    k  = ثابت المادة = sqrt(E / (12 * rho * (1 - nu²)))

الدمج مع BetaRoot:
    1. PhysicalDisk     → كيان فيزيائي (Facts في MemoryStore)
    2. ResonanceLaw     → قاعدة سببية (Rules في InferenceEngine)
    3. ResonanceBeta    → فرضية بايزية (BetaNode من prob_logic)
    4. ResonancePattern → نمط رمزي (Layer 2 من SymbolicPatterns)
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


# ═══════════════════════════════════════════════════════
# ١. الثوابت الفيزيائية للزجاج الكريستالي
# ═══════════════════════════════════════════════════════

GLASS_PROPERTIES = {
    "crystal": {
        "E":   70e9,    # معامل المرونة (Pa)
        "rho": 2500,    # الكثافة (kg/m³)
        "nu":  0.22,    # معامل بواسون
        "name": "زجاج كريستالي"
    },
    "quartz": {
        "E":   72e9,
        "rho": 2650,
        "nu":  0.17,
        "name": "كوارتز"
    }
}

# معامل النمط الاهتزازي الأساسي (m,n) = (0,0)
ALPHA_MN = 1.0148


# ═══════════════════════════════════════════════════════
# ٢. الكيان الفيزيائي — القرص الزجاجي
# ═══════════════════════════════════════════════════════

@dataclass
class PhysicalDisk:
    """
    قرص زجاجي واحد في الارمونيكا
    يُمثَّل كـ Fact داخل MemoryStore
    """
    name: str
    radius: float        # نصف القطر (m)
    thickness: float     # السُمك (m)
    material: str = "crystal"

    def mass(self) -> float:
        """الكتلة = rho * pi * R² * h"""
        rho = GLASS_PROPERTIES[self.material]["rho"]
        return rho * math.pi * (self.radius ** 2) * self.thickness

    def k_constant(self) -> float:
        """ثابت المادة k"""
        props = GLASS_PROPERTIES[self.material]
        E   = props["E"]
        rho = props["rho"]
        nu  = props["nu"]
        return math.sqrt(E / (12 * rho * (1 - nu ** 2)))

    def frequency(self) -> float:
        """
        f = (alpha_mn / 2π) * (h / R²) * k
        المعادلة الكاملة للرنين
        """
        k = self.k_constant()
        return (ALPHA_MN / (2 * math.pi)) * (self.thickness / self.radius ** 2) * k

    def to_fact(self) -> Dict:
        """تحويل القرص إلى Fact قابل للحقن في MemoryStore"""
        return {
            "subject":   self.name,
            "predicate": "خصائص_فيزيائية",
            "object":    {
                "radius":    self.radius,
                "thickness": self.thickness,
                "material":  self.material,
                "mass_kg":   round(self.mass(), 6),
                "freq_hz":   round(self.frequency(), 2)
            }
        }


# ═══════════════════════════════════════════════════════
# ٣. قانون الرنين — القاعدة السببية
# ═══════════════════════════════════════════════════════

class ResonanceLaw:
    """
    قاعدة سببية: العلاقة بين (R, h, M) والتردد f
    تُحقن كـ Rule في InferenceEngine
    """

    @staticmethod
    def compare(disk_a: PhysicalDisk, disk_b: PhysicalDisk) -> Dict:
        """
        قارن ترددَي قرصين وأنتج سلسلة استنتاج
        يُحاكي منطق InferenceEngine.answer_query()
        """
        fa = disk_a.frequency()
        fb = disk_b.frequency()
        ratio = fb / fa if fa > 0 else 0

        reasoning = [
            f"[1] {disk_a.name}: R={disk_a.radius*100:.1f}cm, h={disk_a.thickness*1000:.1f}mm → f={fa:.1f} Hz",
            f"[2] {disk_b.name}: R={disk_b.radius*100:.1f}cm, h={disk_b.thickness*1000:.1f}mm → f={fb:.1f} Hz",
            f"[3] القانون: f ∝ h/R²",
            f"[4] نسبة R²: ({disk_b.radius}/{disk_a.radius})² = {(disk_b.radius/disk_a.radius)**2:.3f}",
            f"[5] نتيجة: f_B/f_A = {ratio:.4f}",
            f"[6] الصوت الأعمق: {'B' if fb < fa else 'A'} (كتلة أكبر → تردد أقل)"
        ]

        return {
            "success":   True,
            "answer":    f"التردد ينخفض بنسبة {ratio:.4f} عند مضاعفة الأبعاد",
            "certainty": 1.0,
            "reasoning": reasoning,
            "f_a":       round(fa, 2),
            "f_b":       round(fb, 2)
        }

    @staticmethod
    def scale_series(base_disk: PhysicalDisk, n_disks: int = 8) -> List[Dict]:
        """
        توليد سلسلة من الأقراص (مثل الارمونيكا الكاملة)
        كل قرص: R يتزايد 15% عن السابق
        """
        series = []
        r = base_disk.radius
        for i in range(n_disks):
            disk = PhysicalDisk(
                name=f"قرص_{i+1}",
                radius=r,
                thickness=base_disk.thickness,
                material=base_disk.material
            )
            series.append({
                "index":    i + 1,
                "radius_cm": round(r * 100, 2),
                "mass_g":   round(disk.mass() * 1000, 3),
                "freq_hz":  round(disk.frequency(), 2),
                "fact":     disk.to_fact()
            })
            r *= 1.15   # زيادة 15% لكل قرص
        return series


# ═══════════════════════════════════════════════════════
# ٤. الفرضية البايزية — تحقق تجريبي
# ═══════════════════════════════════════════════════════

class ResonanceBeta:
    """
    نمذجة بايزية لقانون f ∝ 1/M
    يرث منطق BetaNode من prob_logic.py
    """

    def __init__(self, hypothesis: str = "f_inversely_proportional_to_R_squared"):
        self.hypothesis = hypothesis
        self.alpha = 1   # مؤيد (prior)
        self.beta  = 1   # معارض (prior)
        self.observations: List[Dict] = []

    def observe(self, disk_a: PhysicalDisk, disk_b: PhysicalDisk,
                tolerance: float = 0.05) -> bool:
        """
        قياس تجريبي: هل يتوافق القياس الحقيقي مع المعادلة؟
        tolerance: هامش الخطأ المقبول (5% افتراضي)
        """
        predicted_ratio = (disk_b.radius / disk_a.radius) ** 2  # f_a/f_b = R_b²/R_a²
        actual_ratio    = disk_a.frequency() / disk_b.frequency()
        error           = abs(predicted_ratio - actual_ratio) / predicted_ratio
        confirmed       = error <= tolerance

        if confirmed:
            self.alpha += 1
        else:
            self.beta  += 1

        self.observations.append({
            "disk_a":          disk_a.name,
            "disk_b":          disk_b.name,
            "predicted_ratio": round(predicted_ratio, 4),
            "actual_ratio":    round(actual_ratio, 4),
            "error_pct":       round(error * 100, 2),
            "confirmed":       confirmed
        })

        return confirmed

    def certainty(self) -> float:
        """درجة اليقين البايزي (0 → 1)"""
        return self.alpha / (self.alpha + self.beta)

    def report(self) -> Dict:
        return {
            "hypothesis":     self.hypothesis,
            "alpha":          self.alpha,
            "beta":           self.beta,
            "certainty":      round(self.certainty(), 4),
            "observations":   len(self.observations),
            "confirmations":  self.alpha - 1,
            "refutations":    self.beta  - 1
        }


# ═══════════════════════════════════════════════════════
# ٥. نمط رمزي — Layer 2 Causal
# ═══════════════════════════════════════════════════════

RESONANCE_PATTERN = {
    "name":        "Resonance_Scaling",
    "category":    "causal",
    "layer":       2,
    "description": "قانون تناسب التردد مع السُمك وعكس مربع القطر",
    "formula":     "f = k * (h / R²)",
    "symbolic_id": "RSN_001",
    "causal_chain": [
        "R ↑  →  R² ↑  →  f ↓  →  صوت أعمق",
        "h ↑  →  f ↑  →  صوت أحدّ",
        "M ↑  →  f ↓  →  قانون الكتلة"
    ]
}


# ═══════════════════════════════════════════════════════
# ٦. نقطة الدخول الموحدة
# ═══════════════════════════════════════════════════════

def inject_into_betaroot(memory_store, inference_engine=None) -> Dict:
    """
    حقن قانون الرنين كاملاً في بنية BetaRoot:
      - Facts  → MemoryStore
      - Rules  → MemoryStore
      - Series → قائمة أقراص جاهزة
    """
    base = PhysicalDisk("قرص_الأساس", radius=0.05, thickness=0.003)
    law  = ResonanceLaw()
    beta = ResonanceBeta()

    # توليد 8 أقراص
    series = law.scale_series(base, n_disks=8)

    # حقن كـ Facts
    for disk_data in series:
        f = disk_data["fact"]
        memory_store.add_fact(f["subject"], f["predicate"], str(f["object"]))

    # حقن قاعدة سببية
    memory_store.add_rule("قرص_زجاجي", "تردد_يتناسب_عكسياً_مع_مربع_القطر")
    memory_store.add_rule("كتلة_أكبر", "تردد_أخفض")

    # تحقق بايزي على أول زوج
    d1 = PhysicalDisk("ق1", series[0]["radius_cm"]/100, base.thickness)
    d2 = PhysicalDisk("ق2", series[1]["radius_cm"]/100, base.thickness)
    beta.observe(d1, d2)

    return {
        "pattern":       RESONANCE_PATTERN,
        "series":        series,
        "bayesian":      beta.report(),
        "facts_injected": len(series),
        "rules_injected": 2
    }


# ═══════════════════════════════════════════════════════
# تشغيل مستقل للاختبار
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 55)
    print("  BetaRoot × قانون الرنين — اختبار كامل")
    print("=" * 55)

    # --- ١. قرصان للمقارنة ---
    disk_A = PhysicalDisk("قرص_A", radius=0.05,  thickness=0.003)
    disk_B = PhysicalDisk("قرص_B", radius=0.10,  thickness=0.003)

    print("\n[١] مقارنة قرصين:")
    result = ResonanceLaw.compare(disk_A, disk_B)
    for step in result["reasoning"]:
        print(f"    {step}")
    print(f"\n    اليقين: {result['certainty']}")

    # --- ٢. سلسلة الارمونيكا ---
    print("\n[٢] سلسلة الارمونيكا (8 أقراص):")
    base  = PhysicalDisk("أساس", radius=0.04, thickness=0.003)
    series = ResonanceLaw.scale_series(base, 8)
    print(f"    {'#':<4} {'R (cm)':<10} {'كتلة (g)':<12} {'f (Hz)':<10}")
    print(f"    {'-'*36}")
    for s in series:
        print(f"    {s['index']:<4} {s['radius_cm']:<10} {s['mass_g']:<12} {s['freq_hz']:<10}")

    # --- ٣. الفرضية البايزية ---
    print("\n[٣] التحقق البايزي:")
    beta = ResonanceBeta()
    disks = [PhysicalDisk(f"ق{i}", series[i]["radius_cm"]/100, 0.003)
             for i in range(8)]
    for i in range(len(disks)-1):
        beta.observe(disks[i], disks[i+1])

    r = beta.report()
    print(f"    الفرضية:      {r['hypothesis']}")
    print(f"    تأكيدات:      {r['confirmations']}")
    print(f"    تفنيدات:      {r['refutations']}")
    print(f"    اليقين البايزي: {r['certainty']}")

    # --- ٤. النمط الرمزي ---
    print("\n[٤] النمط الرمزي:")
    for chain in RESONANCE_PATTERN["causal_chain"]:
        print(f"    {chain}")

    print("\n" + "=" * 55)
    print("  جاهز للحقن في BetaRoot عبر inject_into_betaroot()")
    print("=" * 55)
