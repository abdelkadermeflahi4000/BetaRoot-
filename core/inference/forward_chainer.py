# betaroot/core/inference/forward_chainer.py
from typing import List, Dict, Optional
import logging
from ..knowledge.knowledge_base import KnowledgeBase
from ..knowledge.fact_base import FactBase, TruthValue, Fact

logger = logging.getLogger(__name__)

class ForwardChainer:
    """
    Moteur de chaînage avant (Data-Driven Inference)
    Applique itérativement les règles dont les prémisses sont satisfaites
    jusqu'à ce qu'aucune nouvelle conclusion ne puisse être déduite.
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase, max_iterations: int = 50):
        self.kb = kb
        self.fb = fb
        self.max_iterations = max_iterations
        self.inferred_facts: List[Fact] = []
        
    def run(self, initial_facts: Optional[Dict[str, any]] = None) -> List[Fact]:
        """
        Exécute le chaînage avant.
        
        Args:
            initial_facts: Dictionnaire optionnel de faits à ajouter avant de démarrer
                          Format: {"var": (value, truth, confidence, source)}
        Returns:
            Liste des nouveaux faits déduits
        """
        # 1. Injecter les faits initiaux si fournis
        if initial_facts:
            for var, (val, truth, conf, src) in initial_facts.items():
                self.fb.add(var, val, truth, conf, source=src, on_conflict='replace')
                
        logger.info("Starting forward chaining...")
        
        for iteration in range(self.max_iterations):
            # 2. Trouver les règles applicables
            applicable_rules = self.kb.get_applicable_rules(self.fb)
            
            if not applicable_rules:
                logger.info(f"No more applicable rules after {iteration} iterations.")
                break
                
            new_facts_this_iter = []
            
            # 3. Appliquer chaque règle
            for rule in applicable_rules:
                inferred_fact = rule.apply(self.fb)
                if inferred_fact:
                    # Vérifier si le fait est déjà connu avec une confiance égale ou supérieure
                    existing = self.fb.get(inferred_fact.variable)
                    if existing and existing.confidence >= inferred_fact.confidence:
                        continue
                        
                    # Ajouter le fait déduit
                    success, msg = self.fb.add(
                        variable=inferred_fact.variable,
                        value=inferred_fact.value,
                        truth=inferred_fact.truth,
                        confidence=inferred_fact.confidence,
                        source="inference",
                        justification=inferred_fact.justification,
                        on_conflict='merge'
                    )
                    
                    if success:
                        new_facts_this_iter.append(inferred_fact)
                        logger.debug(f"Derived: {inferred_fact}")
            
            self.inferred_facts.extend(new_facts_this_iter)
            
            # 4. Condition d'arrêt : aucune nouvelle déduction
            if not new_facts_this_iter:
                logger.info(f"Forward chaining converged at iteration {iteration}.")
                break
                
        return self.inferred_facts
    
    def get_derivation_chain(self, variable: str) -> List[str]:
        """Retrouve la chaîne de règles qui a conduit à une variable donnée."""
        chain = []
        fact = self.fb.get(variable)
        if fact and fact.justification:
            chain.append(fact.justification)
        return chain
