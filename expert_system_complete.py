#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BetaRoot Expert System - Complete Integrated Package
يجمع: قاعدة المعرفة، الحقائق، السلسلة الأمامية/الخلفية، المحرك البيزي، 
المحلل التشخيصي، مولد الشرح، وواجهة المستخدم التفاعلية.
الاستخدام: python expert_system_complete.py
"""
import sys, os, json, time, uuid, copy, hashlib, logging
from typing import Dict, List, Optional, Any, Tuple, Callable, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from pathlib import Path

# ==========================================
# 📦 External Dependencies
# ==========================================
import networkx as nx
try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
    PGMPY_AVAILABLE = True
except ImportError:
    PGMPY_AVAILABLE = False
    print("⚠️  تحذير: مكتبة pgmpy غير مثبتة. سيتم تعطيل الاستدلال البيزي.")
    print("   للتثبيت: pip install pgmpy")

# ==========================================
# 🔧 Logging & Config
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("BetaRootExpert")

# ==========================================
# 📚 1. KNOWLEDGE & FACT BASE
# ==========================================
class RuleType(Enum):
    IMPLICATION = auto()
    BICONDITIONAL = auto()
    CAUSAL = auto()
    CONSTRAINT = auto()

@dataclass
class Rule:
    id: str
    antecedents: List[str]
    consequent: str
    rule_type: RuleType
    confidence: float = 1.0
    enabled: bool = True

    def is_satisfied(self, fb: 'FactBase', threshold: float = 0.5) -> bool:
        if not self.enabled: return False
        return all(fb.is_true(ant, threshold) for ant in self.antecedents)

    def apply(self, fb: 'FactBase') -> Optional['Fact']:
        if not self.is_satisfied(fb): return None
        conf = self.confidence
        for ant in self.antecedents:
            f = fb.get(ant)
            if f: conf *= f.confidence
        return Fact(self.consequent, True, TruthValue.TRUE, min(conf, 1.0), source="inference", justification=self.id)

class KnowledgeBase:
    def __init__(self, name="default"):
        self.name = name
        self.rules: Dict[str, Rule] = {}
        self.causal_graph: nx.DiGraph = nx.DiGraph()
        self._ant_idx: Dict[str, Set[str]] = {}
        self._cons_idx: Dict[str, Set[str]] = {}

    def add_rule(self, rule: Rule):
        self.rules[rule.id] = rule
        if rule.rule_type == RuleType.CAUSAL:
            for ant in rule.antecedents:
                self.causal_graph.add_edge(ant, rule.consequent, rule_id=rule.id)
        for ant in rule.antecedents:
            self._ant_idx.setdefault(ant, set()).add(rule.id)
        self._cons_idx.setdefault(rule.consequent, set()).add(rule.id)

    def get_applicable(self, fb: 'FactBase', threshold=0.5) -> List[Rule]:
        return [r for r in self.rules.values() if r.is_satisfied(fb, threshold)]

    def get_rules_for(self, conclusion: str) -> List[Rule]:
        return [self.rules[rid] for rid in self._cons_idx.get(conclusion, set()) if rid in self.rules]

    def get_rules_triggered_by(self, var: str) -> List[Rule]:
        return [self.rules[rid] for rid in self._ant_idx.get(var, set()) if rid in self.rules]

    def find_affected(self, var: str) -> Set[str]:
        return nx.descendants(self.causal_graph, var) if var in self.causal_graph else set()

class TruthValue(Enum):
    TRUE = auto()
    FALSE = auto()
    UNKNOWN = auto()
    CONTRADICTED = auto()

@dataclass
class Fact:
    variable: str
    value: Any
    truth: TruthValue
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "user"
    justification: Optional[str] = None
    version: int = 1

@dataclass
class HistoryEntry:
    variable: str
    action: str
    old_fact: Optional[Fact]
    new_fact: Optional[Fact]
    timestamp: datetime = field(default_factory=datetime.now)

class FactBase:
    def __init__(self, name="default", max_history=1000):
        self.name = name
        self.facts: Dict[str, Fact] = {}
        self.history: List[HistoryEntry] = []
        self.max_history = max_history

    def add(self, var: str, val: Any, truth: TruthValue, conf=1.0, source="user", justification=None, on_conflict="reject") -> Tuple[bool, str]:
        old = self.facts.get(var)
        new = Fact(var, val, truth, conf, source=source, justification=justification, version=(old.version+1 if old else 1))
        
        if old and old.contradicts(new):
            if on_conflict == "reject": return False, "conflict"
            elif on_conflict == "replace": pass
            elif on_conflict == "flag": new.truth = TruthValue.CONTRADICTED
            
        self.facts[var] = new
        self.history.append(HistoryEntry(var, "add" if not old else "update", old, new))
        if len(self.history) > self.max_history: self.history.pop(0)
        return True, "ok"

    def get(self, var: str) -> Optional[Fact]: return self.facts.get(var)
    def is_true(self, var: str, threshold=0.5) -> bool:
        f = self.facts.get(var)
        return f and f.truth == TruthValue.TRUE and f.confidence >= threshold
    def get_history(self, var=None, limit=20):
        entries = [e for e in self.history if var is None or e.variable == var]
        return entries[-limit:]
    def export(self) -> dict:
        return {k: {"v": f.value, "t": f.truth.name, "c": f.confidence, "s": f.source} for k,f in self.facts.items()}
    @classmethod
    def import_from(cls, data: dict):
        fb = cls(name="imported")
        for k,v in data.items():
            fb.add(k, v["v"], TruthValue[v["t"]], v["c"], v["s"], on_conflict="replace")
        return fb

    def contradicts(self, a: Fact, b: Fact) -> bool:
        return a.variable == b.variable and a.truth != b.truth and a.truth != TruthValue.UNKNOWN and b.truth != TruthValue.UNKNOWN
    Fact.contradicts = contradicts

# ==========================================
# ⚙️ 2. INFERENCE ENGINES
# ==========================================
class ForwardChainer:
    def __init__(self, kb: KnowledgeBase, fb: FactBase, max_iter=50):
        self.kb, self.fb, self.max_iter = kb, fb, max_iter
        self.inferred = []
    def run(self) -> List[Fact]:
        for i in range(self.max_iter):
            rules = self.kb.get_applicable(self.fb)
            if not rules: break
            new = []
            for r in rules:
                f = r.apply(self.fb)
                if f:
                    ok, _ = self.fb.add(f.variable, f.value, f.truth, f.confidence, "inference", f.justification, on_conflict="merge")
                    if ok: new.append(f)
            self.inferred.extend(new)
            if not new: break
        return self.inferred

class ProofStatus(Enum): PROVEN = "proven"; DISPROVEN = "disproven"; UNKNOWN = "unknown"

@dataclass
class ProofNode:
    variable: str
    status: ProofStatus
    confidence: float = 0.0
    children: List['ProofNode'] = field(default_factory=list)
    rule_used: Optional[str] = None

class BackwardChainer:
    def __init__(self, kb: KnowledgeBase, fb: FactBase, max_depth=10):
        self.kb, self.fb, self.max_depth = kb, fb, max_depth
        self.visited = set()
        self.ask_user_fn = None  # للتفاعل مع المستخدم عند نقص البيانات

    def prove(self, hyp: str, depth=0) -> ProofNode:
        if depth > self.max_depth or hyp in self.visited:
            return ProofNode(hyp, ProofStatus.UNKNOWN, 0.0)
        self.visited.add(hyp)
        
        fact = self.fb.get(hyp)
        if fact:
            self.visited.discard(hyp)
            return ProofNode(hyp, ProofStatus.PROVEN if fact.truth==TruthValue.TRUE else ProofStatus.DISPROVEN, fact.confidence)
        
        if self.ask_user_fn:
            user_val = self.ask_user_fn(hyp)
            if user_val is not None:
                self.fb.add(hyp, user_val, TruthValue.TRUE if user_val else TruthValue.FALSE, 0.95, "user_query")
                fact = self.fb.get(hyp)
                if fact: return ProofNode(hyp, ProofStatus.PROVEN if fact.truth==TruthValue.TRUE else ProofStatus.DISPROVEN, fact.confidence)

        rules = self.kb.get_rules_for(hyp)
        if not rules:
            self.visited.discard(hyp)
            return ProofNode(hyp, ProofStatus.UNKNOWN, 0.0)

        best = ProofNode(hyp, ProofStatus.UNKNOWN, 0.0)
        for r in rules:
            node = ProofNode(hyp, ProofStatus.UNKNOWN, 0.0, rule_used=r.id)
            ok, min_conf = True, 1.0
            for ant in r.antecedents:
                child = self.prove(ant, depth+1)
                node.children.append(child)
                if child.status == ProofStatus.DISPROVEN: ok = False; break
                if child.status == ProofStatus.UNKNOWN: ok = False
                min_conf = min(min_conf, child.confidence)
            if ok:
                node.status, node.confidence = ProofStatus.PROVEN, min_conf * r.confidence
                if node.confidence > best.confidence: best = node
        self.visited.discard(hyp)
        return best

    def explain(self, node: ProofNode, indent=0) -> str:
        pre = "  "*indent
        s = "✅" if node.status==ProofStatus.PROVEN else "❌" if node.status==ProofStatus.DISPROVEN else "❓"
        line = f"{pre}{s} {node.variable} [{node.status.value}] (conf={node.confidence:.2f})"
        if node.rule_used: line += f" ← {node.rule_used}"
        res = [line]
        for c in node.children: res.append(self.explain(c, indent+1))
        return "\n".join(res)

# ==========================================
# 🎲 3. BAYESIAN & HYBRID SOLVER
# ==========================================
class BayesianEngine:
    def __init__(self, G: nx.DiGraph):
        self.G = G
        self.model = None
        self.inference = None
        if not PGMPY_AVAILABLE: raise RuntimeError("pgmpy not available")
        self.model = BayesianNetwork(list(G.edges()))

    def build(self, cpds: dict):
        for node, cfg in cpds.items():
            evidence = cfg.get("evidence", [])
            vals = cfg.get("values_given_parents", [])
            card = len(cfg.get("values", [0,1]))
            self.model.add_cpds(TabularCPD(node, card, vals, evidence, [2]*len(evidence)))
        if self.model.check_model():
            self.inference = VariableElimination(self.model)
        else:
            raise ValueError("Invalid Bayesian Network structure")

    def query(self, vars: List[str], evidence: dict=None) -> dict:
        if not self.inference: return {}
        res = self.inference.query(variables=vars, evidence=evidence or {})
        out = {}
        for f in ([res] if not isinstance(res, list) else res):
            v = f.variables[0]
            for i, val in enumerate(f.values):
                out[f"{v}={i}"] = float(val)
        return out

class HybridSolver:
    def __init__(self, kb: KnowledgeBase, fb: FactBase, forward: ForwardChainer, backward: BackwardChainer, bayes: Optional[BayesianEngine]=None):
        self.kb, self.fb, self.forward, self.backward, self.bayes = kb, fb, forward, backward, bayes

    def solve(self, hypothesis: str, evidence: dict=None) -> dict:
        if evidence:
            for k,v in evidence.items():
                self.fb.add(k, bool(v), TruthValue.TRUE, 0.99, "evidence", on_conflict="replace")
        self.forward.run()
        proof = self.backward.prove(hypothesis)
        if proof.status == ProofStatus.PROVEN and proof.confidence >= 0.95:
            return {"method": "symbolic", "confidence": proof.confidence, "result": True, "trace": proof}
        
        if self.bayes and self.bayes.inference:
            ev = {k:1 if v else 0 for k,v in {**evidence, **{f.variable:f.value for f in self.fb.facts.values() if f.truth==TruthValue.TRUE}}.items()}
            res = self.bayes.query([hypothesis], evidence=ev)
            best = max(res, key=res.get) if res else ("0", 0.0)
            val = int(best.split("=")[1]) == 1
            conf = res[best]
            return {"method": "bayesian", "confidence": conf, "result": val, "trace": res}
        return {"method": "unknown", "confidence": 0.0, "result": None, "trace": proof}

# ==========================================
# 🔍 4. DIAGNOSTIC & EXPLANATION
# ==========================================
class DiagnosticAnalyzer:
    def __init__(self, kb, fb, solver):
        self.kb, self.fb, self.solver = kb, fb, solver
    def root_cause(self, symptom: str, top_k=3) -> str:
        causes = self.kb.find_affected(symptom)
        if not causes: return f"⚠️ لا توجد علاقات سببية مسجلة لـ {symptom}"
        res = []
        for c in causes:
            r = self.solver.solve(c)
            res.append((c, r["confidence"]))
        res.sort(key=lambda x: x[1], reverse=True)
        return "\n".join([f"  {i+1}. {c} ({conf:.2%})" for i,(c,conf) in enumerate(res[:top_k])])
    
    def what_if(self, hypothetical: dict) -> str:
        temp_fb = copy.deepcopy(self.fb)
        for k,v in hypothetical.items():
            temp_fb.add(k, v, TruthValue.TRUE, 0.9, "simulation", on_conflict="replace")
        affected = set()
        for k in hypothetical: affected.update(self.kb.find_affected(k))
        return f"🔮 المتغيرات المتأثرة: {', '.join(affected) if affected else 'لا شيء'}"

class ExplanationGenerator:
    @staticmethod
    def generate(hypothesis: str, result: dict, fb: FactBase, kb: KnowledgeBase) -> str:
        lines = [f"📊 تقرير الاستدلال: {hypothesis}", f"✅ النتيجة: {result['result']} ({result['confidence']:.2%})", f"🛠️ الطريقة: {result['method']}"]
        if isinstance(result["trace"], ProofNode):
            lines.append("\n🌳 شجرة الإثبات:")
            bc = BackwardChainer(kb, fb)
            lines.append(bc.explain(result["trace"]))
        lines.append("\n📜 سجل الحقائق المؤثرة:")
        for e in fb.get_history(limit=5):
            lines.append(f"  • {e.variable} ← {e.action}")
        return "\n".join(lines)

# ==========================================
# 💾 5. SESSION & CACHE
# ==========================================
class SessionManager:
    def __init__(self, dir="sessions"):
        self.dir = Path(dir); self.dir.mkdir(exist_ok=True)
    def save(self, fb: FactBase, meta: dict=None):
        p = self.dir / f"{meta.get('id', uuid.uuid4())}.json"
        p.write_text(json.dumps({"facts": fb.export(), "meta": meta or {}}))
        return str(p)
    def load(self, session_id: str):
        p = self.dir / f"{session_id}.json"
        if not p.exists(): raise FileNotFoundError
        d = json.loads(p.read_text())
        return FactBase.import_from(d["facts"]), d["meta"]

# ==========================================
# 🖥️ 6. CLI INTERFACE
# ==========================================
class ExpertCLI:
    def __init__(self, kb, fb, solver, analyzer, session_mgr):
        self.kb, self.fb, self.solver, self.analyzer, self.sess = kb, fb, solver, analyzer, session_mgr
        self.last_result = {}

    def run(self):
        print("🤖 مرحباً بك في نظام BetaRoot الخبير | اكتب 'help' أو 'مساعدة'")
        while True:
            try: cmd = input("\n👤 المستخدم> ").strip().lower()
            except: break
            
            if cmd in ("exit", "خروج", "quit"): break
            elif cmd in ("help", "مساعدة"): self._help()
            elif cmd.startswith(("add ", "أضف ")): self._add(cmd)
            elif cmd.startswith(("ask ", "اسأل ")): self._ask(cmd)
            elif cmd.startswith(("diagnose ", "شخّص ")): self._diagnose(cmd)
            elif cmd.startswith(("whatif ", "ماذا_لو ")): self._whatif(cmd)
            elif cmd in ("explain", "شرح"): self._explain()
            elif cmd in ("status", "حالة"): self._status()
            elif cmd.startswith("save "): self._save(cmd)
            else: print("⚠️ أمر غير معروف. اكتب 'help'")

    def _help(self):
        print("الأوامر: add <var> <val> | ask <hypo> | diagnose <sym> | whatif var1=val1 | explain | status | save <id>")

    def _add(self, cmd):
        parts = cmd.split()
        if len(parts)>=3:
            ok, msg = self.fb.add(parts[1], parts[2].lower()=="true", TruthValue.TRUE, source="user", on_conflict="replace")
            print(f"{'✅' if ok else '❌'} {msg}")
            self.solver.forward.run()
            
    def _ask(self, cmd):
        hypo = cmd.split(maxsplit=1)[1] if " " in cmd else ""
        if not hypo: return
        self.last_result = self.solver.solve(hypo)
        print(f"📈 {hypo} = {self.last_result['result']} (يقين: {self.last_result['confidence']:.2%}, طريقة: {self.last_result['method']})")

    def _diagnose(self, cmd):
        sym = cmd.split(maxsplit=1)[1] if " " in cmd else ""
        if sym: print(self.analyzer.root_cause(sym))

    def _whatif(self, cmd):
        raw = cmd.split(maxsplit=1)[1] if " " in cmd else ""
        try:
            hypo = {k: v.lower()=="true" for k,v in (i.split("=") for i in raw.split(","))}
            print(self.analyzer.what_if(hypo))
        except: print("❌ صيغة خاطئة. مثال: whatif Fever=true,Cough=true")

    def _explain(self):
        if self.last_result:
            print(ExplanationGenerator.generate("", self.last_result, self.fb, self.kb))
        else: print("⚠️ لا يوجد استنتاج حديث لشرحه.")

    def _status(self):
        print(f"📊 القواعد: {len(self.kb.rules)} | الحقائق: {len(self.fb.facts)} | السجل: {len(self.fb.history)}")

    def _save(self, cmd):
        sid = cmd.split(maxsplit=1)[1] if " " in cmd else uuid.uuid4().hex
        p = self.sess.save(self.fb, {"id": sid})
        print(f"💾 تم حفظ الجلسة: {p}")

# ==========================================
# 🚀 7. MAIN & DEMO CONFIG
# ==========================================
def main():
    print("🚀 جاري تحميل نظام BetaRoot الخبير...")
    kb = KnowledgeBase("medical_demo")
    kb.add_rule(Rule("R1", ["Fever", "Cough"], "PossibleInfection", RuleType.IMPLICATION, 0.9))
    kb.add_rule(Rule("R2", ["PossibleInfection", "HighWBC"], "BacterialInfection", RuleType.CAUSAL, 0.85))
    
    fb = FactBase("patient_session")
    fb.add("Fever", True, TruthValue.TRUE, 0.95, "observation")
    fb.add("Cough", True, TruthValue.TRUE, 0.90, "observation")
    
    forward = ForwardChainer(kb, fb)
    backward = BackwardChainer(kb, fb)
    # دالة تفاعلية لطرح الأسئلة عند نقص البيانات
    backward.ask_user_fn = lambda q: input(f"❓ النظام: هل {q} صحيح؟ (true/false): ").strip().lower() == "true"
    
    bayes = None
    cpd_config = {
        "Fever": {"values":[0,1], "evidence":[], "values_given_parents":[[0.9],[0.1]]},
        "Cough": {"values":[0,1], "evidence":[], "values_given_parents":[[0.8],[0.2]]},
        "PossibleInfection": {"values":[0,1], "evidence":["Fever","Cough"], "values_given_parents":[[1.0,0.3,0.3,0.05],[0.0,0.7,0.7,0.95]]},
        "HighWBC": {"values":[0,1], "evidence":[], "values_given_parents":[[0.85],[0.15]]},
        "BacterialInfection": {"values":[0,1], "evidence":["PossibleInfection","HighWBC"], "values_given_parents":[[1.0,0.4,0.3,0.01],[0.0,0.6,0.7,0.99]]}
    }
    if PGMPY_AVAILABLE:
        try:
            bayes = BayesianEngine(kb.causal_graph)
            bayes.build(cpd_config)
        except Exception as e:
            print(f"⚠️ فشل تحميل المحرك البيزي: {e}")
            
    solver = HybridSolver(kb, fb, forward, backward, bayes)
    analyzer = DiagnosticAnalyzer(kb, fb, solver)
    sess_mgr = SessionManager()
    
    # تشغيل تلقائي سريع للاستدلال الأمامي
    forward.run()
    
    cli = ExpertCLI(kb, fb, solver, analyzer, sess_mgr)
    cli.run()

if __name__ == "__main__":
    main()
