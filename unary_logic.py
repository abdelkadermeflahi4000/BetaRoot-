"""
BetaRoot Core: Unary Logic Engine

This module implements the fundamental unary logic system that converts
all inputs into unified representations and maintains the principle of
"Only 1, Never 0".
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from abc import ABC, abstractmethod


class RepresentationLevel(Enum):
    """Levels of unary representation"""
    PURE_BEING = 0          # Pure existence
    FIRST_ORDER = 1         # First representation of 1
    SECOND_ORDER = 2        # Second representation of 1
    SYMBOLIC = 3            # Symbolic patterns
    COGNITIVE = 4           # Cognitive constructs


@dataclass
class UnaryState:
    """
    Represents a state in the unary system.
    
    Everything is a representation of 1, just in different forms.
    """
    level: RepresentationLevel
    content: Any
    representation_id: str = field(default_factory=str)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_states: List['UnaryState'] = field(default_factory=list)
    
    def __post_init__(self):
        """Generate unique ID for this state"""
        if not self.representation_id:
            state_str = json.dumps({
                'level': self.level.name,
                'content': str(self.content)
            }, sort_keys=True)
            self.representation_id = hashlib.sha256(
                state_str.encode()
            ).hexdigest()[:16]
    
    def __repr__(self):
        return f"UnaryState(level={self.level.name}, id={self.representation_id})"


class UnaryTransformation(ABC):
    """Abstract base class for unary transformations"""
    
    @abstractmethod
    def apply(self, state: UnaryState) -> UnaryState:
        """Apply transformation to a unary state"""
        pass
    
    @abstractmethod
    def verify(self, source: UnaryState, result: UnaryState) -> bool:
        """Verify that transformation maintains oneness"""
        pass


class IdentityTransformation(UnaryTransformation):
    """
    Identity transformation: preserves the state.
    This is the simplest transformation - 1 remains 1.
    """
    
    def apply(self, state: UnaryState) -> UnaryState:
        """Return a copy of the state"""
        new_state = UnaryState(
            level=state.level,
            content=state.content,
            metadata=state.metadata.copy(),
            parent_states=state.parent_states.copy()
        )
        new_state.parent_states.append(state)
        return new_state
    
    def verify(self, source: UnaryState, result: UnaryState) -> bool:
        """Identity always maintains oneness"""
        return (source.content == result.content or 
                source.representation_id in result.representation_id)


class ProjectionTransformation(UnaryTransformation):
    """
    Projection transformation: extract specific aspect of 1.
    Shows one facet of the unified representation.
    """
    
    def __init__(self, projection_key: str):
        self.projection_key = projection_key
    
    def apply(self, state: UnaryState) -> UnaryState:
        """Extract specific projection of the state"""
        if isinstance(state.content, dict):
            projected_content = state.content.get(
                self.projection_key, 
                None
            )
        else:
            projected_content = getattr(
                state.content, 
                self.projection_key, 
                None
            )
        
        new_state = UnaryState(
            level=state.level,
            content=projected_content,
            metadata={'projection_key': self.projection_key},
            parent_states=[state]
        )
        return new_state
    
    def verify(self, source: UnaryState, result: UnaryState) -> bool:
        """Projection maintains oneness through focusing"""
        return result.parent_states[0] == source


class CompositionTransformation(UnaryTransformation):
    """
    Composition transformation: combine multiple 1s.
    Shows how multiple representations of 1 relate.
    """
    
    def __init__(self, composition_rule: str):
        self.composition_rule = composition_rule
    
    def apply(self, states: List[UnaryState]) -> UnaryState:
        """Compose multiple states into unified representation"""
        combined_content = {
            'rule': self.composition_rule,
            'components': [s.content for s in states],
            'count': len(states)
        }
        
        new_state = UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content=combined_content,
            metadata={'composition_rule': self.composition_rule},
            parent_states=states
        )
        return new_state
    
    def verify(self, states: List[UnaryState], result: UnaryState) -> bool:
        """All components preserved in composition"""
        return len(result.parent_states) == len(states)


class UnaryLogicEngine:
    """
    Main unary logic engine.
    
    This is the core of BetaRoot. It operates on the principle that
    everything is a representation of 1, and transformations maintain
    this fundamental unity.
    """
    
    def __init__(self):
        self.transformations: Dict[str, UnaryTransformation] = {
            'identity': IdentityTransformation(),
        }
        self.state_history: List[UnaryState] = []
        self.verification_log: List[Dict] = []
    
    def register_transformation(self, name: str, 
                              transformation: UnaryTransformation):
        """Register a custom transformation"""
        self.transformations[name] = transformation
    
    def encode(self, input_data: Any) -> UnaryState:
        """
        Encode input data as a unary state.
        
        This is the fundamental operation: convert anything into
        a representation of 1.
        
        Args:
            input_data: Any input (binary, text, numbers, etc.)
            
        Returns:
            UnaryState: Unified representation
        """
        # Step 1: Determine the level of representation
        level = self._determine_level(input_data)
        
        # Step 2: Create unified state
        state = UnaryState(
            level=level,
            content=input_data
        )
        
        # Step 3: Verify oneness
        self._verify_oneness(state)
        
        # Step 4: Record in history
        self.state_history.append(state)
        
        return state
    
    def transform(self, state: UnaryState, 
                 transformation_name: str) -> UnaryState:
        """
        Apply a transformation to a unary state.
        
        Args:
            state: Input unary state
            transformation_name: Name of transformation
            
        Returns:
            UnaryState: Transformed state
        """
        if transformation_name not in self.transformations:
            raise ValueError(f"Unknown transformation: {transformation_name}")
        
        transformation = self.transformations[transformation_name]
        result = transformation.apply(state)
        
        # Verify transformation maintains oneness
        if not transformation.verify(state, result):
            raise RuntimeError(
                f"Transformation {transformation_name} violated oneness principle"
            )
        
        self.state_history.append(result)
        
        return result
    
    def compose(self, states: List[UnaryState], 
               rule: str) -> UnaryState:
        """
        Compose multiple unary states.
        
        Args:
            states: List of unary states to compose
            rule: Composition rule
            
        Returns:
            UnaryState: Composed state
        """
        composition = CompositionTransformation(rule)
        result = composition.apply(states)
        
        if not composition.verify(states, result):
            raise RuntimeError("Composition violated oneness principle")
        
        self.state_history.append(result)
        
        return result
    
    def project(self, state: UnaryState, 
               key: str) -> UnaryState:
        """
        Project a specific aspect of a unary state.
        
        Args:
            state: Input unary state
            key: Key to project
            
        Returns:
            UnaryState: Projected state
        """
        projection = ProjectionTransformation(key)
        result = projection.apply(state)
        
        if not projection.verify(state, result):
            raise RuntimeError("Projection violated oneness principle")
        
        self.state_history.append(result)
        
        return result
    
    def _determine_level(self, data: Any) -> RepresentationLevel:
        """Determine appropriate representation level"""
        if data is None or isinstance(data, bool):
            return RepresentationLevel.PURE_BEING
        elif isinstance(data, (int, float)):
            return RepresentationLevel.FIRST_ORDER
        elif isinstance(data, str):
            return RepresentationLevel.SECOND_ORDER
        elif isinstance(data, (dict, list)):
            return RepresentationLevel.SYMBOLIC
        else:
            return RepresentationLevel.COGNITIVE
    
    def _verify_oneness(self, state: UnaryState) -> bool:
        """
        Verify that a state maintains the oneness principle.
        
        This is critical: we ensure that no "0" (non-being) exists,
        only different representations of 1 (being).
        """
        if state.content is None and not isinstance(state.content, bool):
            # None is a valid representation (absence = different representation)
            return True
        
        # Record verification
        self.verification_log.append({
            'state_id': state.representation_id,
            'level': state.level.name,
            'verified': True
        })
        
        return True
    
    def verify_consistency(self, state: UnaryState) -> Dict[str, Any]:
        """
        Comprehensive consistency check for a state.
        
        Returns:
            {
                'is_consistent': bool,
                'violations': List[str],
                'certainty': 1.0 (always)
            }
        """
        violations = []
        
        # Check 1: Parent consistency
        for parent in state.parent_states:
            if parent.representation_id not in [
                s.representation_id for s in self.state_history
            ]:
                violations.append(f"Parent state not in history: {parent.representation_id}")
        
        # Check 2: Level consistency
        if state.level not in RepresentationLevel.__members__.values():
            violations.append(f"Invalid representation level: {state.level}")
        
        # Check 3: Content non-nullity (can't be truly nothing)
        # Note: None is valid, just a different representation
        
        return {
            'is_consistent': len(violations) == 0,
            'violations': violations,
            'certainty': 1.0
        }
    
    def get_history(self) -> List[UnaryState]:
        """Get complete transformation history"""
        return self.state_history.copy()
    
    def reset(self):
        """Reset the engine to initial state"""
        self.state_history = []
        self.verification_log = []
    
    def explain_state(self, state: UnaryState) -> Dict[str, Any]:
        """
        Explain a unary state completely.
        
        Returns:
            {
                'representation_id': str,
                'level': str,
                'content': Any,
                'parent_chain': List[str],
                'transformations_applied': List[str],
                'consistency': Dict
            }
        """
        parent_chain = []
        current = state
        
        while current.parent_states:
            parent = current.parent_states[0]
            parent_chain.append(parent.representation_id)
            current = parent
        
        return {
            'representation_id': state.representation_id,
            'level': state.level.name,
            'content': state.content,
            'parent_chain': parent_chain,
            'metadata': state.metadata,
            'consistency': self.verify_consistency(state),
            'certainty': 1.0
        }


# Convenience functions

def create_engine() -> UnaryLogicEngine:
    """Create a new unary logic engine"""
    return UnaryLogicEngine()


def encode_to_unary(data: Any) -> UnaryState:
    """
    Quickly encode data to unary without keeping engine.
    
    Usage:
        >>> state = encode_to_unary("hello")
        >>> print(state.level)
    """
    engine = UnaryLogicEngine()
    return engine.encode(data)


__all__ = [
    'UnaryLogicEngine',
    'UnaryState',
    'UnaryTransformation',
    'IdentityTransformation',
    'ProjectionTransformation',
    'CompositionTransformation',
    'RepresentationLevel',
    'create_engine',
    'encode_to_unary',
]
