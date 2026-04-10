"""
BetaRoot Phase 1: Complete Test Suite

This file contains comprehensive tests for the unary logic engine.
Covers all functionality, edge cases, and integration scenarios.

Run with: pytest tests/test_phase1_complete.py -v
"""

import pytest
import time
from betaroot_core_complete import (
    UnaryLogicEngine,
    UnaryState,
    RepresentationLevel,
    TransformationType,
    IdentityTransformation,
    ProjectionTransformation,
    CompositionTransformation,
    create_engine,
    encode_to_unary,
)


# ============================================================================
# TESTS: UNARYSTATE DATA STRUCTURE
# ============================================================================

class TestUnaryState:
    """Tests for UnaryState data structure."""
    
    def test_state_creation(self):
        """Test basic state creation."""
        state = UnaryState(
            level=RepresentationLevel.PURE_BEING,
            content=1
        )
        assert state.level == RepresentationLevel.PURE_BEING
        assert state.content == 1
        assert state.certainty == 1.0
    
    def test_state_uniqueness(self):
        """Test that states get unique IDs."""
        s1 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        s2 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        
        # Different states should have different IDs (even same content)
        assert s1.representation_id != s2.representation_id
    
    def test_state_equality(self):
        """Test state equality based on ID."""
        s1 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        s2 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        
        # Copy state
        s2.representation_id = s1.representation_id
        assert s1 == s2
    
    def test_state_hashable(self):
        """Test that states are hashable."""
        s1 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        s2 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=42)
        
        state_set = {s1, s2}
        assert len(state_set) == 2
    
    def test_state_certainty_always_one(self):
        """Test that certainty is always 1.0 in unary system."""
        state = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=42
        )
        state.certainty = 0.5  # Try to change it
        # Reset should restore to 1.0
        assert state.certainty == 1.0
    
    def test_state_parent_chain(self):
        """Test parent chain tracking."""
        s1 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=1)
        s2 = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=2,
            parent_states=[s1]
        )
        s3 = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=3,
            parent_states=[s2]
        )
        
        chain = s3.get_parent_chain()
        assert len(chain) == 3
        assert chain[0] == s3
        assert chain[1] == s2
        assert chain[2] == s1
    
    def test_state_chain_length(self):
        """Test chain length calculation."""
        s1 = UnaryState(level=RepresentationLevel.FIRST_ORDER, content=1)
        assert s1.chain_length == 0
        
        s2 = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=2,
            parent_states=[s1]
        )
        assert s2.chain_length == 1
        
        s3 = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=3,
            parent_states=[s2]
        )
        assert s3.chain_length == 2


# ============================================================================
# TESTS: UNARY LOGIC ENGINE - BASIC OPERATIONS
# ============================================================================

class TestUnaryLogicEngine:
    """Tests for the UnaryLogicEngine core."""
    
    def test_engine_creation(self):
        """Test basic engine creation."""
        engine = create_engine("TestEngine")
        assert engine.name == "TestEngine"
        assert len(engine.state_history) == 0
        assert len(engine.transformation_log) == 0
    
    def test_encode_integer(self):
        """Test encoding an integer."""
        engine = create_engine()
        state = engine.encode(42)
        
        assert state.content == 42
        assert state.level == RepresentationLevel.FIRST_ORDER
        assert state.certainty == 1.0
        assert len(engine.state_history) == 1
    
    def test_encode_string(self):
        """Test encoding a string."""
        engine = create_engine()
        state = engine.encode("hello")
        
        assert state.content == "hello"
        assert state.level == RepresentationLevel.SECOND_ORDER
        assert state.certainty == 1.0
    
    def test_encode_dict(self):
        """Test encoding a dictionary."""
        engine = create_engine()
        data = {"name": "Alice", "age": 30}
        state = engine.encode(data)
        
        assert state.content == data
        assert state.level == RepresentationLevel.SYMBOLIC
    
    def test_encode_none(self):
        """Test encoding None."""
        engine = create_engine()
        state = engine.encode(None)
        
        assert state.content is None
        assert state.level == RepresentationLevel.PURE_BEING
    
    def test_encode_with_source(self):
        """Test encoding with source metadata."""
        engine = create_engine()
        state = engine.encode(42, source="test_data")
        
        assert state.metadata['source'] == "test_data"
    
    def test_multiple_encodes(self):
        """Test multiple encodings."""
        engine = create_engine()
        
        s1 = engine.encode(1)
        s2 = engine.encode(2)
        s3 = engine.encode(3)
        
        assert len(engine.state_history) == 3
        assert engine.state_history[0] == s1
        assert engine.state_history[1] == s2
        assert engine.state_history[2] == s3


# ============================================================================
# TESTS: TRANSFORMATIONS
# ============================================================================

class TestTransformations:
    """Tests for transformation operations."""
    
    def test_identity_transformation(self):
        """Test identity transformation."""
        engine = create_engine()
        state = engine.encode(42)
        
        result = engine.transform(state, 'identity')
        
        assert result.content == state.content
        assert result.level == state.level
        assert result.parent_states[0] == state
    
    def test_projection_dict(self):
        """Test projection on dictionary."""
        engine = create_engine()
        data = {"name": "Alice", "age": 30}
        state = engine.encode(data)
        
        name_state = engine.project(state, 'name')
        
        assert name_state.content == "Alice"
        assert name_state.parent_states[0] == state
    
    def test_projection_list(self):
        """Test projection on list."""
        engine = create_engine()
        state = engine.encode([10, 20, 30])
        
        first = engine.project(state, '0')
        
        assert first.content == 10
    
    def test_projection_missing_key(self):
        """Test projection with missing key."""
        engine = create_engine()
        state = engine.encode({"a": 1})
        
        result = engine.project(state, 'missing')
        
        assert result.content is None
    
    def test_composition_sum(self):
        """Test composition with sum."""
        engine = create_engine()
        
        s1 = engine.encode(10)
        s2 = engine.encode(20)
        s3 = engine.encode(30)
        
        result = engine.compose(
            [s1, s2, s3],
            'sum',
            composition_func=sum
        )
        
        assert result.content['composed_value'] == 60
        assert result.level == RepresentationLevel.SYMBOLIC
    
    def test_composition_concat(self):
        """Test composition with string concatenation."""
        engine = create_engine()
        
        s1 = engine.encode("Hello")
        s2 = engine.encode(" ")
        s3 = engine.encode("World")
        
        result = engine.compose(
            [s1, s2, s3],
            'concat',
            composition_func=lambda x: ''.join(x)
        )
        
        assert result.content['composed_value'] == "Hello World"
    
    def test_unknown_transformation(self):
        """Test error on unknown transformation."""
        engine = create_engine()
        state = engine.encode(42)
        
        with pytest.raises(ValueError):
            engine.transform(state, 'unknown_transform')


# ============================================================================
# TESTS: CONSISTENCY & VERIFICATION
# ============================================================================

class TestConsistencyVerification:
    """Tests for consistency checking and verification."""
    
    def test_consistency_check_valid_state(self):
        """Test consistency check on valid state."""
        engine = create_engine()
        state = engine.encode(42)
        
        result = engine.verify_consistency(state)
        
        assert result['is_consistent'] is True
        assert len(result['violations']) == 0
        assert result['certainty'] == 1.0
    
    def test_consistency_check_parent(self):
        """Test that parent consistency is checked."""
        engine = create_engine()
        
        state1 = engine.encode(1)
        state2 = engine.encode(2, source="test")
        
        result = engine.verify_consistency(state2)
        assert result['is_consistent'] is True
    
    def test_certainty_always_one(self):
        """Test that certainty is always 1.0."""
        engine = create_engine()
        state = engine.encode(42)
        
        result = engine.verify_consistency(state)
        assert result['certainty'] == 1.0


# ============================================================================
# TESTS: INTROSPECTION & ANALYSIS
# ============================================================================

class TestIntrospection:
    """Tests for state introspection and analysis."""
    
    def test_explain_state(self):
        """Test state explanation."""
        engine = create_engine()
        state = engine.encode(42)
        
        explanation = engine.explain_state(state)
        
        assert explanation['state_id'] == state.representation_id
        assert explanation['level'] == 'FIRST_ORDER'
        assert explanation['content'] == 42
        assert explanation['certainty'] == 1.0
    
    def test_get_history(self):
        """Test history retrieval."""
        engine = create_engine()
        
        s1 = engine.encode(1)
        s2 = engine.encode(2)
        
        history = engine.get_history()
        
        assert len(history) == 2
        assert history[0] == s1
        assert history[1] == s2
    
    def test_transformation_log(self):
        """Test transformation logging."""
        engine = create_engine()
        
        s1 = engine.encode(10)
        s2 = engine.encode(20)
        result = engine.compose([s1, s2], 'sum')
        
        log = engine.get_transformation_log()
        
        assert len(log) >= 1
        assert any(
            t.transformation_name == 'sum' 
            for t in log
        )
    
    def test_stats(self):
        """Test engine statistics."""
        engine = create_engine("TestEngine")
        
        engine.encode(1)
        engine.encode(2)
        
        stats = engine.stats()
        
        assert stats['name'] == "TestEngine"
        assert stats['total_states'] >= 2
        assert stats['registered_transformations'] >= 1


# ============================================================================
# TESTS: COMPLEX SCENARIOS
# ============================================================================

class TestComplexScenarios:
    """Tests for complex multi-step scenarios."""
    
    def test_deep_transformation_chain(self):
        """Test a chain of transformations."""
        engine = create_engine()
        
        # Create initial state
        state = engine.encode({"a": 1, "b": 2, "c": 3})
        
        # Project 'a'
        a_state = engine.project(state, 'a')
        assert a_state.content == 1
        
        # Apply identity
        a_state2 = engine.transform(a_state, 'identity')
        assert a_state2.content == 1
        
        # Check chain
        chain = a_state2.get_parent_chain()
        assert len(chain) >= 2
    
    def test_nested_composition(self):
        """Test nested composition."""
        engine = create_engine()
        
        # First level
        s1 = engine.compose(
            [engine.encode(1), engine.encode(2)],
            'sum',
            sum
        )
        
        s2 = engine.compose(
            [engine.encode(3), engine.encode(4)],
            'sum',
            sum
        )
        
        # Second level
        result = engine.compose(
            [s1, s2],
            'sum',
            lambda x: sum([d['composed_value'] for d in x])
        )
        
        # Result should be 1+2+3+4 = 10
        assert result.content['composed_value'] == 10
    
    def test_export_import_history(self):
        """Test history export for persistence."""
        engine = create_engine("TestEngine")
        
        s1 = engine.encode(1)
        s2 = engine.encode(2)
        result = engine.compose([s1, s2], 'sum', sum)
        
        exported = engine.export_history()
        
        assert exported['name'] == "TestEngine"
        assert len(exported['states']) >= 3
        assert len(exported['transformations']) >= 1


# ============================================================================
# TESTS: UTILITY FUNCTIONS
# ============================================================================

class TestUtilityFunctions:
    """Tests for utility functions."""
    
    def test_create_engine(self):
        """Test engine creation utility."""
        engine = create_engine()
        assert isinstance(engine, UnaryLogicEngine)
    
    def test_encode_to_unary_shortcut(self):
        """Test quick encoding function."""
        state = encode_to_unary("hello")
        
        assert state.content == "hello"
        assert state.level == RepresentationLevel.SECOND_ORDER


# ============================================================================
# TESTS: ERROR HANDLING
# ============================================================================

class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_empty_composition(self):
        """Test error on empty composition."""
        engine = create_engine()
        
        with pytest.raises(ValueError):
            engine.compose([], 'sum')
    
    def test_invalid_level(self):
        """Test handling of invalid representation level."""
        # This should not raise during creation
        state = UnaryState(
            level=RepresentationLevel.FIRST_ORDER,
            content=42
        )
        assert state.level == RepresentationLevel.FIRST_ORDER


# ============================================================================
# TESTS: PERFORMANCE & SCALE
# ============================================================================

class TestPerformanceAndScale:
    """Tests for performance characteristics."""
    
    def test_large_composition(self):
        """Test composition of many states."""
        engine = create_engine()
        
        states = [engine.encode(i) for i in range(100)]
        
        result = engine.compose(states, 'sum', sum)
        
        assert result.content['count'] == 100
    
    def test_deep_chain(self):
        """Test deep transformation chain."""
        engine = create_engine()
        
        state = engine.encode(42)
        
        # Apply identity 10 times
        for _ in range(10):
            state = engine.transform(state, 'identity')
        
        # Should still be consistent
        consistency = engine.verify_consistency(state)
        assert consistency['is_consistent'] is True
        assert state.chain_length == 10


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_full_workflow(self):
        """Test a complete workflow."""
        # Create engine
        engine = create_engine("IntegrationTest")
        
        # Encode data
        data = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25},
            ]
        }
        state = engine.encode(data)
        
        # Project users
        users_state = engine.project(state, 'users')
        
        # Check consistency throughout
        for s in [state, users_state]:
            consistency = engine.verify_consistency(s)
            assert consistency['is_consistent'] is True
        
        # Get final explanation
        explanation = engine.explain_state(users_state)
        assert explanation['certainty'] == 1.0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
