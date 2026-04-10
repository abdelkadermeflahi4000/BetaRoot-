# betaroot/core/inference/backward_chainer.py
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from ..knowledge.knowledge_base import KnowledgeBase
from ..knowledge.fact_base import FactBase, TruthValue

logger = logging.getLogger(__name__)

class ProofStatus(Enum):
    PROVEN = "proven"
    DISPROVEN = "disproven"
    UNKNOWN = "unknown"
    PARTIAL = "partial"

@dataclass
class ProofNode:
    """Arbre de preuve pour le chaînage arrière"""
    variable: str
    status: ProofStatus
    confidence: float = 0.0
    children: List['ProofNode'] = field(default_factory=list)
    rule_used: Optional[str] = None
    depth: int = 0
    
    def __repr__(self):
        return f"ProofNode({self.variable}, {self.status.value}, conf={self.confidence:.2f})"

class BackwardChainer:
    """
    Moteur de chaînage arrière (Goal-Driven Inference)
    Vérifie récursivement si une hypothèse peut être prouvée
    à partir des faits observés et des règles disponibles.
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase, max_depth: int = 10):
        self.kb = kb
        self.fb = fb
        self.max_depth = max_depth
        self._visited: Set[str] = set()  # Protection contre les cycles
        
    def prove(self, hypothesis: str, depth: int = 0) -> ProofNode:
        """
        Tente de prouver une hypothèse.
        
        Returns:
            ProofNode représentant l'arbre de preuve
        """
        if depth > self.max_depth:
            return ProofNode(hypothesis, ProofStatus.UNKNOWN, 0.0, depth=depth)
            
        if hypothesis in self._visited:
            return ProofNode(hypothesis, ProofStatus.UNKNOWN, 0.0, depth=depth)
            
        self._visited.add(hypothesis)
        
        # 1. Vérifier si le fait est déjà dans la base
        fact = self.fb.get(hypothesis)
        if fact:
            status = (ProofStatus.PROVEN if fact.truth == TruthValue.TRUE else 
                     ProofStatus.DISPROVEN if fact.truth == TruthValue.FALSE else 
                     ProofStatus.UNKNOWN)
            self._visited.discard(hypothesis)
            return ProofNode(hypothesis, status, fact.confidence, depth=depth)
            
        # 2. Chercher les règles qui concluent cette hypothèse
        supporting_rules = self.kb.get_rules_for_conclusion(hypothesis)
        
        if not supporting_rules:
            self._visited.discard(hypothesis)
            return ProofNode(hypothesis, ProofStatus.UNKNOWN, 0.0, depth=depth)
            
        # 3. Évaluer chaque règle support
        best_proof = ProofNode(hypothesis, ProofStatus.UNKNOWN, 0.0, depth=depth)
        
        for rule in supporting_rules:
            rule_node = ProofNode(hypothesis, ProofStatus.UNKNOWN, 0.0, 
                                 rule_used=rule.id, depth=depth)
            
            # Vérifier récursivement chaque prémisse
            all_premises_met = True
            min_confidence = 1.0
            
            for premise in rule.antecedents:
                premise_proof = self.prove(premise, depth + 1)
                rule_node.children.append(premise_proof)
                
                if premise_proof.status == ProofStatus.DISPROVEN:
                    all_premises_met = False
                    break
                    
                if premise_proof.status == ProofStatus.UNKNOWN:
                    all_premises_met = False
                    
                min_confidence = min(min_confidence, premise_confidence := premise_proof.confidence)
            
            if all_premises_met:
                rule_confidence = min_confidence * rule.confidence
                rule_node.status = ProofStatus.PROVEN
                rule_node.confidence = rule_confidence
                
                # Garder la preuve avec la plus haute confiance
                if rule_confidence > best_proof.confidence:
                    best_proof = rule_node
                    
        self._visited.discard(hypothesis)
        return best_proof
    
    def explain_proof(self, node: ProofNode, indent: int = 0) -> str:
        """Génère une explication textuelle de l'arbre de preuve."""
        prefix = "  " * indent
        status_emoji = {"proven": "✅", "disproven": "❌", "unknown": "❓", "partial": "⚠️"}
        line = f"{prefix}{status_emoji.get(node.status.value, '•')} {node.variable} ({node.status.value}) [conf={node.confidence:.2f}]"
        if node.rule_used:
            line += f" ← {node.rule_used}"
            
        explanation = [line]
        for child in node.children:
            explanation.extend(self.explain_proof(child, indent + 1).split('\n'))
        return '\n'.join(explanation)
