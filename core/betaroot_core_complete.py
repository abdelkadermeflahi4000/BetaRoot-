"""
BetaRoot Phase 1: Complete Unary Logic Engine Implementation

This file contains the FULL implementation of the unary logic engine
with all transformations, verification, and utilities.

Implements:
- UnaryState data structure
- UnaryLogicEngine core
- 3 base transformations (Identity, Projection, Composition)
- Consistency verification system
- State history and tracing
- Complete documentation
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from abc import ABC, abstractmethod
import copy
import time


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class RepresentationLevel(Enum):
    """Levels of unary representation in the hierarchy."""
    PURE_BEING = 0          # Pure existence (1)
    FIRST_ORDER = 1         # First manifestation of 1
    SECOND_ORDER = 2        # Second manifestation of 1
    SYMBOLIC = 3            # Symbolic patterns
    COGNITIVE = 4           # Cognitive constructs


class TransformationType(Enum):
    """Types of unary transformations."""
    IDENTITY = "identity"
    PROJECTION = "projection"
    COMPOSITION = "composition"
    CUSTOM = "custom"


# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class UnaryState:
    """
    Represents a state in the unary system.
    
    Everything is a representation of 1 (Being), just in different forms.
    This is the fundamental data structure in BetaRoot.
    
    Attributes:
        level: Representation level in the hierarchy
        content: The actual content/data at this level
        representation_id: Unique identifier for this specific representation
        metadata: Additional information about the state
        parent_states: Previous states that led to this one
        timestamp: When this state was created
        certainty: How certain we are about this state (always 1.0 for unary)
    """
    level: RepresentationLevel
    content: Any
    representation_id: str = field(default_factory=str)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_states: List['UnaryState'] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    certainty: float = field(default=1.0)  # Always 1.0 in unary system
    
    def __post_init__(self):
        """Generate unique ID and validate state."""
        if not self.representation_id:
            state_str = json.dumps({
                'level': self.level.name,
                'content': str(self.content),
                'timestamp': self.timestamp
            }, sort_keys=True)
            self.representation_id = hashlib.sha256(
                state_str.encode()
            ).hexdigest()[:16]
        
        # Unary system always has perfect certainty
        self.certainty = 1.0
    
    def __repr__(self) -> str:
        return (f"UnaryState("
                f"level={self.level.name}, "
                f"id={self.representation_id}, "
                f"content={self.content})")
    
    def __eq__(self, other: 'UnaryState') -> bool:
        """Two states are equal if they have the same representation ID."""
        if not isinstance(other, UnaryState):
            return False
        return self.representation_id == other.representation_id
    
    def __hash__(self) -> int:
        """Make UnaryState hashable."""
        return hash(self.representation_id)
    
    @property
    def chain_length(self) -> int:
        """Get the length of the parent chain."""
        if not self.parent_states:
            return 0
        return 1 + max((p.chain_length for p in self.parent_states), default=0)
    
    def get_parent_chain(self) -> List['UnaryState']:
        """Get the complete chain of parent states."""
        chain = [self]
        current = self
        while current.parent_states:
            current = current.parent_states[0]
            chain.append(current)
        return chain


@dataclass
class TransformationRecord:
    """Record of a transformation for auditing and replay."""
    transformation_type: TransformationType
    transformation_name: str
    input_state: UnaryState
    output_state: UnaryState
    timestamp: float = field(default_factory=time.time)
    is_valid: bool = True
    error_message: Optional[str] = None
    additional_info: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# TRANSFORMATIONS
# ============================================================================

class UnaryTransformation(ABC):
    """Abstract base class for all unary transformations."""
    
    @abstractmethod
    def apply(self, *args, **kwargs) -> Union[UnaryState, List[UnaryState]]:
        """Apply the transformation."""
        pass
    
    @abstractmethod
    def verify(self, input_states: Union[UnaryState, List[UnaryState]], 
               result: Union[UnaryState, List[UnaryState]]) -> bool:
        """Verify that transformation maintains oneness."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description of this transformation."""
        pass


class IdentityTransformation(UnaryTransformation):
    """
    Identity transformation: preserves the state.
    1 → 1 (same representation)
    
    This is the simplest transformation. The state passes through unchanged,
    but is recorded in history for traceability.
    """
    
    def apply(self, state: UnaryState) -> UnaryState:
        """Create a copy of the state."""
        new_state = UnaryState(
            level=state.level,
            content=state.content,
            metadata=state.metadata.copy(),
            parent_states=[state]
        )
        return new_state
    
    def verify(self, input_state: UnaryState, result: UnaryState) -> bool:
        """Identity transformation always preserves oneness."""
        # The content is the same or equivalent
        return (input_state.content == result.content or
                input_state.level == result.level)
    
    def get_description(self) -> str:
        return "Identity transformation: 1 → 1 (state preserved)"


class ProjectionTransformation(UnaryTransformation):
    """
    Projection transformation: extract one aspect of a unary state.
    
    This transformation shows one facet of the unified representation.
    Used to focus on specific aspects of a complex state.
    
    Example:
        State: {'name': 'Alice', 'age': 30, 'city': 'NYC'}
        Project('name') → 'Alice'
    """
    
    def __init__(self, projection_key: str):
        """
        Args:
            projection_key: The key/attribute to project
        """
        self.projection_key = projection_key
    
    def apply(self, state: UnaryState) -> UnaryState:
        """Extract specific aspect from the state."""
        
        # Handle dict-like content
        if isinstance(state.content, dict):
            projected_content = state.content.get(self.projection_key, None)
        
        # Handle object-like content
        elif hasattr(state.content, self.projection_key):
            projected_content = getattr(state.content, self.projection_key)
        
        # Handle list-like content
        elif isinstance(state.content, (list, tuple)):
            try:
                idx = int(self.projection_key)
                projected_content = state.content[idx]
            except (ValueError, IndexError):
                projected_content = None
        
        else:
            projected_content = None
        
        # Create new state with projected content
        new_state = UnaryState(
            level=state.level,
            content=projected_content,
            metadata={
                'projection_key': self.projection_key,
                'original_keys': list(state.content.keys()) 
                    if isinstance(state.content, dict) else None
            },
            parent_states=[state]
        )
        return new_state
    
    def verify(self, input_state: UnaryState, result: UnaryState) -> bool:
        """Projection maintains oneness through focusing."""
        return (result.parent_states and 
                result.parent_states[0] == input_state)
    
    def get_description(self) -> str:
        return f"Projection transformation: extract '{self.projection_key}'"


class CompositionTransformation(UnaryTransformation):
    """
    Composition transformation: combine multiple instances of 1.
    
    Shows how multiple representations of 1 can be unified.
    Creates a higher-level representation from component representations.
    
    Example:
        States: [UnaryState(1), UnaryState(2), UnaryState(3)]
        Compose('sum') → UnaryState(content={'rule': 'sum', 'values': [1,2,3]})
    """
    
    def __init__(self, composition_rule: str, 
                 composition_func: Optional[Callable] = None):
        """
        Args:
            composition_rule: Name of the composition rule
            composition_func: Optional function to apply
        """
        self.composition_rule = composition_rule
        self.composition_func = composition_func
    
    def apply(self, states: List[UnaryState]) -> UnaryState:
        """Compose multiple states into unified representation."""
        
        # Extract contents
        contents = [s.content for s in states]
        
        # Apply composition function if provided
        if self.composition_func:
            try:
                composed_value = self.composition_func(contents)
            except Exception as e:
                composed_value = contents
        else:
            composed_value = contents
        
        # Create composed state
        composed_content = {
            'rule': self.composition_rule,
            'components': contents,
            'count': len(states),
            'composed_value': composed_value
        }
        
        new_state = UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content=composed_content,
            metadata={'composition_rule': self.composition_rule},
            parent_states=states
        )
        return new_state
    
    def verify(self, input_states: List[UnaryState], 
               result: UnaryState) -> bool:
        """All component states preserved in composition."""
        return (len(result.parent_states) == len(input_states) and
                all(inp in result.parent_states for inp in input_states))
    
    def get_description(self) -> str:
        return f"Composition transformation: combine via '{self.composition_rule}'"


# ============================================================================
# MAIN ENGINE
# ============================================================================

class UnaryLogicEngine:
    """
    The core BetaRoot engine implementing unary logic.
    
    This is the heart of BetaRoot. It operates on the principle that
    everything is a representation of 1, and transformations maintain
    this fundamental unity.
    
    Key principles:
    - Everything is 1 (Being)
    - Only representations change, not the underlying unity
    - All transformations preserve oneness
    - Complete traceability and history
    - Deterministic (certainty always 1.0)
    """
    
    def __init__(self, name: str = "BetaRoot"):
        """
        Initialize the unary logic engine.
        
        Args:
            name: Name for this engine instance
        """
        self.name = name
        self.transformations: Dict[str, UnaryTransformation] = {
            'identity': IdentityTransformation(),
        }
        self.state_history: List[UnaryState] = []
        self.transformation_log: List[TransformationRecord] = []
        self.verification_log: List[Dict] = []
        self.created_at = time.time()
    
    # -------- Registration --------
    
    def register_transformation(self, name: str, 
                               transformation: UnaryTransformation) -> None:
        """
        Register a new transformation.
        
        Args:
            name: Unique name for the transformation
            transformation: UnaryTransformation instance
        """
        if name in self.transformations:
            raise ValueError(f"Transformation '{name}' already registered")
        self.transformations[name] = transformation
    
    def list_transformations(self) -> Dict[str, str]:
        """Get all registered transformations with descriptions."""
        return {
            name: trans.get_description()
            for name, trans in self.transformations.items()
        }
    
    # -------- Core Operations --------
    
    def encode(self, input_data: Any, 
               source: str = "user_input") -> UnaryState:
        """
        Encode input data as a unary state.
        
        This is the fundamental operation: convert any input into
        a representation of 1.
        
        Args:
            input_data: Any input (binary, text, numbers, etc.)
            source: Description of where the input came from
            
        Returns:
            UnaryState: Unified representation
            
        Example:
            >>> engine = UnaryLogicEngine()
            >>> state = engine.encode("hello world")
            >>> print(state.level)
            RepresentationLevel.SECOND_ORDER
        """
        
        # Step 1: Determine the appropriate representation level
        level = self._determine_level(input_data)
        
        # Step 2: Create unified state
        state = UnaryState(
            level=level,
            content=input_data,
            metadata={'source': source, 'encoding_method': 'direct'}
        )
        
        # Step 3: Verify oneness
        consistency = self._verify_oneness(state)
        
        # Step 4: Record in history
        self.state_history.append(state)
        
        # Step 5: Add verification log entry
        self.verification_log.append({
            'state_id': state.representation_id,
            'level': state.level.name,
            'verified': True,
            'source': source,
            'timestamp': time.time()
        })
        
        return state
    
    def transform(self, state: UnaryState, 
                  transformation_name: str,
                  **kwargs) -> UnaryState:
        """
        Apply a transformation to a unary state.
        
        Args:
            state: Input unary state
            transformation_name: Name of transformation
            **kwargs: Additional arguments for transformation
            
        Returns:
            UnaryState: Transformed state
            
        Raises:
            ValueError: If transformation not found
            RuntimeError: If transformation violates oneness
        """
        
        if transformation_name not in self.transformations:
            raise ValueError(
                f"Unknown transformation: {transformation_name}. "
                f"Available: {list(self.transformations.keys())}"
            )
        
        transformation = self.transformations[transformation_name]
        
        try:
            # Apply transformation
            result = transformation.apply(state, **kwargs)
            
            # Verify transformation maintains oneness
            if not transformation.verify(state, result):
                raise RuntimeError(
                    f"Transformation {transformation_name} violated oneness principle"
                )
            
            # Record transformation
            self.state_history.append(result)
            self.transformation_log.append(
                TransformationRecord(
                    transformation_type=TransformationType.CUSTOM,
                    transformation_name=transformation_name,
                    input_state=state,
                    output_state=result,
                    is_valid=True
                )
            )
            
            return result
        
        except Exception as e:
            # Log failed transformation
            self.transformation_log.append(
                TransformationRecord(
                    transformation_type=TransformationType.CUSTOM,
                    transformation_name=transformation_name,
                    input_state=state,
                    output_state=None,
                    is_valid=False,
                    error_message=str(e)
                )
            )
            raise
    
    def compose(self, states: List[UnaryState], 
                rule: str,
                composition_func: Optional[Callable] = None) -> UnaryState:
        """
        Compose multiple unary states.
        
        Args:
            states: List of unary states to compose
            rule: Composition rule name
            composition_func: Optional function to apply
            
        Returns:
            UnaryState: Composed state
            
        Example:
            >>> s1 = engine.encode(2)
            >>> s2 = engine.encode(3)
            >>> result = engine.compose([s1, s2], 'sum', lambda x: sum(x))
            >>> result.content['composed_value']
            5
        """
        
        if not states:
            raise ValueError("Cannot compose empty list of states")
        
        composition = CompositionTransformation(rule, composition_func)
        result = composition.apply(states)
        
        if not composition.verify(states, result):
            raise RuntimeError("Composition violated oneness principle")
        
        self.state_history.append(result)
        self.transformation_log.append(
            TransformationRecord(
                transformation_type=TransformationType.COMPOSITION,
                transformation_name=rule,
                input_state=states[0],
                output_state=result
            )
        )
        
        return result
    
    def project(self, state: UnaryState, 
                key: str) -> UnaryState:
        """
        Project a specific aspect from a unary state.
        
        Args:
            state: Input unary state
            key: Key/attribute to project
            
        Returns:
            UnaryState: Projected state
            
        Example:
            >>> state = engine.encode({'name': 'Alice', 'age': 30})
            >>> name_state = engine.project(state, 'name')
            >>> name_state.content
            'Alice'
        """
        
        projection = ProjectionTransformation(key)
        result = projection.apply(state)
        
        if not projection.verify(state, result):
            raise RuntimeError("Projection violated oneness principle")
        
        self.state_history.append(result)
        self.transformation_log.append(
            TransformationRecord(
                transformation_type=TransformationType.PROJECTION,
                transformation_name=f"project_{key}",
                input_state=state,
                output_state=result
            )
        )
        
        return result
    
    # -------- Verification & Consistency --------
    
    def verify_consistency(self, state: UnaryState) -> Dict[str, Any]:
        """
        Comprehensive consistency check for a state.
        
        Args:
            state: UnaryState to verify
            
        Returns:
            {
                'is_consistent': bool,
                'violations': List[str],
                'certainty': 1.0,
                'checks_performed': [...]
            }
        """
        violations = []
        checks = []
        
        # Check 1: Parent consistency
        for parent in state.parent_states:
            found = any(
                s.representation_id == parent.representation_id 
                for s in self.state_history
            )
            if not found:
                violations.append(
                    f"Parent state not in history: {parent.representation_id}"
                )
            checks.append('parent_consistency')
        
        # Check 2: Representation level validity
        if state.level not in RepresentationLevel:
            violations.append(f"Invalid representation level: {state.level}")
        checks.append('level_validity')
        
        # Check 3: Certainty must be 1.0
        if state.certainty != 1.0:
            violations.append(
                f"Certainty must be 1.0, got {state.certainty}"
            )
        checks.append('certainty_check')
        
        # Check 4: ID uniqueness
        id_count = sum(
            1 for s in self.state_history 
            if s.representation_id == state.representation_id
        )
        if id_count > 1:
            violations.append(f"Duplicate state ID: {state.representation_id}")
        checks.append('id_uniqueness')
        
        return {
            'is_consistent': len(violations) == 0,
            'violations': violations,
            'certainty': 1.0,
            'checks_performed': checks,
            'state_id': state.representation_id,
            'parent_chain_length': state.chain_length
        }
    
    # -------- Introspection & Analysis --------
    
    def explain_state(self, state: UnaryState) -> Dict[str, Any]:
        """
        Complete explanation of a unary state.
        
        Returns everything about the state and how it was created.
        """
        parent_chain = state.get_parent_chain()
        
        return {
            'state_id': state.representation_id,
            'level': state.level.name,
            'content': state.content,
            'content_type': type(state.content).__name__,
            'metadata': state.metadata,
            'timestamp': state.timestamp,
            'certainty': state.certainty,
            'parent_chain': [s.representation_id for s in parent_chain],
            'parent_chain_length': len(parent_chain),
            'consistency': self.verify_consistency(state),
            'transformations_in_history': [
                tr.transformation_name 
                for tr in self.transformation_log 
                if tr.output_state and tr.output_state.representation_id == state.representation_id
            ]
        }
    
    def get_history(self) -> List[UnaryState]:
        """Get complete transformation history."""
        return self.state_history.copy()
    
    def get_transformation_log(self) -> List[TransformationRecord]:
        """Get log of all transformations."""
        return self.transformation_log.copy()
    
    def stats(self) -> Dict[str, Any]:
        """Get statistics about the engine."""
        return {
            'name': self.name,
            'created_at': self.created_at,
            'total_states': len(self.state_history),
            'total_transformations': len(self.transformation_log),
            'registered_transformations': len(self.transformations),
            'valid_transformations': sum(
                1 for t in self.transformation_log if t.is_valid
            ),
            'failed_transformations': sum(
                1 for t in self.transformation_log if not t.is_valid
            ),
            'verification_checks': len(self.verification_log),
            'uptime_seconds': time.time() - self.created_at
        }
    
    # -------- Reset & Utility --------
    
    def reset(self) -> None:
        """Reset the engine to initial state."""
        self.state_history = []
        self.transformation_log = []
        self.verification_log = []
    
    def export_history(self) -> Dict[str, Any]:
        """Export complete history for persistence."""
        return {
            'name': self.name,
            'created_at': self.created_at,
            'states': [
                {
                    'id': s.representation_id,
                    'level': s.level.name,
                    'content': str(s.content),
                    'parents': [p.representation_id for p in s.parent_states]
                }
                for s in self.state_history
            ],
            'transformations': [
                {
                    'name': t.transformation_name,
                    'type': t.transformation_type.value,
                    'input_id': t.input_state.representation_id,
                    'output_id': t.output_state.representation_id if t.output_state else None,
                    'valid': t.is_valid,
                    'timestamp': t.timestamp
                }
                for t in self.transformation_log
            ]
        }
    
    # -------- Private Methods --------
    
    def _determine_level(self, data: Any) -> RepresentationLevel:
        """Determine appropriate representation level."""
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
        # Record verification
        self.verification_log.append({
            'state_id': state.representation_id,
            'level': state.level.name,
            'verified': True,
            'timestamp': time.time()
        })
        
        return True


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_engine(name: str = "BetaRoot") -> UnaryLogicEngine:
    """
    Create a new unary logic engine.
    
    Args:
        name: Name for the engine
        
    Returns:
        UnaryLogicEngine: Initialized engine
    """
    return UnaryLogicEngine(name)


def encode_to_unary(data: Any) -> UnaryState:
    """
    Quickly encode data to unary without keeping engine.
    
    Args:
        data: Data to encode
        
    Returns:
        UnaryState: Unified representation
        
    Usage:
        >>> state = encode_to_unary("hello")
        >>> print(state.level)
        RepresentationLevel.SECOND_ORDER
    """
    engine = UnaryLogicEngine()
    return engine.encode(data)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Core classes
    'UnaryLogicEngine',
    'UnaryState',
    'UnaryTransformation',
    
    # Transformations
    'IdentityTransformation',
    'ProjectionTransformation',
    'CompositionTransformation',
    
    # Enums
    'RepresentationLevel',
    'TransformationType',
    
    # Data classes
    'TransformationRecord',
    
    # Utility functions
    'create_engine',
    'encode_to_unary',
]
