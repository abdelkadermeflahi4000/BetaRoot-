# betaroot/core/__init__.py
from .unary_logic import UnaryLogicEngine, create_engine
from .symbolic_patterns import SymbolicPatternEngine

class BetaRoot:
    def __init__(self):
        self.unary = create_engine()
        self.symbolic = SymbolicPatternEngine()
        # ... باقي الطبقات

    def process(self, input_data: Any, patterns: List[str] = None) -> dict:
        state = self.unary.encode(input_data)
        
        if patterns:
            state = self.symbolic.apply_multiple(state, patterns)
        
        return {
            "result": state.content,
            "representation_id": state.representation_id,
            "level": state.level.name,
            "applied_patterns": [p for p in patterns] if patterns else [],
            "certainty": 1.0
        }
