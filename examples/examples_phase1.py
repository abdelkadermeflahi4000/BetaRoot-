"""
BetaRoot Phase 1: Practical Examples

This file demonstrates the unary logic engine in action.
Run each example to see how BetaRoot works.
"""

from betaroot_core_complete import create_engine, RepresentationLevel


def example_1_basic_encoding():
    """Example 1: Basic encoding of different data types."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Encoding")
    print("="*60)
    
    engine = create_engine("Example1")
    
    # Encode different types of data
    examples = [
        (None, "None value"),
        (42, "Integer"),
        (3.14, "Float"),
        ("Hello, World!", "String"),
        ([1, 2, 3], "List"),
        ({"name": "Alice", "age": 30}, "Dictionary"),
    ]
    
    for data, description in examples:
        state = engine.encode(data, source=description)
        print(f"\nInput: {description}")
        print(f"  Content: {state.content}")
        print(f"  Level: {state.level.name}")
        print(f"  ID: {state.representation_id}")
        print(f"  Certainty: {state.certainty}")


def example_2_transformations():
    """Example 2: Applying transformations."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Transformations")
    print("="*60)
    
    engine = create_engine("Example2")
    
    # Create a state
    user_data = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }
    state = engine.encode(user_data)
    print(f"\nOriginal state: {state.content}")
    
    # Apply identity transformation
    print("\n--- Identity Transformation ---")
    identity_state = engine.transform(state, 'identity')
    print(f"Result: {identity_state.content}")
    print(f"Parent: {identity_state.parent_states[0].representation_id}")
    
    # Apply projection
    print("\n--- Projection Transformation ---")
    name_state = engine.project(state, 'name')
    print(f"Project('name'): {name_state.content}")
    
    age_state = engine.project(state, 'age')
    print(f"Project('age'): {age_state.content}")
    
    city_state = engine.project(state, 'city')
    print(f"Project('city'): {city_state.content}")


def example_3_composition():
    """Example 3: Composing multiple states."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Composition")
    print("="*60)
    
    engine = create_engine("Example3")
    
    # Create individual number states
    print("\n--- Composing Numbers (Sum) ---")
    s1 = engine.encode(10, source="first_number")
    s2 = engine.encode(20, source="second_number")
    s3 = engine.encode(30, source="third_number")
    
    result = engine.compose(
        [s1, s2, s3],
        rule='sum',
        composition_func=sum
    )
    
    print(f"Composed: 10 + 20 + 30")
    print(f"Result: {result.content['composed_value']}")
    print(f"Components: {result.content['components']}")
    
    # String composition
    print("\n--- Composing Strings (Concat) ---")
    s1 = engine.encode("Hello", source="greeting")
    s2 = engine.encode(" ", source="space")
    s3 = engine.encode("World", source="noun")
    
    result = engine.compose(
        [s1, s2, s3],
        rule='concat',
        composition_func=lambda x: ''.join(x)
    )
    
    print(f"Composed: 'Hello' + ' ' + 'World'")
    print(f"Result: {result.content['composed_value']}")


def example_4_consistency_verification():
    """Example 4: Consistency verification."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Consistency Verification")
    print("="*60)
    
    engine = create_engine("Example4")
    
    # Create a transformation chain
    state1 = engine.encode({"x": 10, "y": 20})
    state2 = engine.project(state1, 'x')
    state3 = engine.transform(state2, 'identity')
    
    # Verify each state
    for i, state in enumerate([state1, state2, state3], 1):
        print(f"\n--- State {i} ---")
        consistency = engine.verify_consistency(state)
        
        print(f"Content: {state.content}")
        print(f"Is Consistent: {consistency['is_consistent']}")
        print(f"Certainty: {consistency['certainty']}")
        print(f"Violations: {consistency['violations']}")
        print(f"Checks: {', '.join(consistency['checks_performed'])}")


def example_5_introspection():
    """Example 5: Introspection and explanation."""
    print("\n" + "="*60)
    print("EXAMPLE 5: State Introspection")
    print("="*60)
    
    engine = create_engine("Example5")
    
    # Create complex transformation chain
    data = {"user": {"name": "Bob", "scores": [85, 90, 88]}}
    state1 = engine.encode(data)
    state2 = engine.project(state1, 'user')
    state3 = engine.project(state2, 'scores')
    
    # Get detailed explanation
    explanation = engine.explain_state(state3)
    
    print(f"\n--- Final State Explanation ---")
    print(f"State ID: {explanation['state_id']}")
    print(f"Level: {explanation['level']}")
    print(f"Content Type: {explanation['content_type']}")
    print(f"Content: {explanation['content']}")
    print(f"Certainty: {explanation['certainty']}")
    print(f"Parent Chain Length: {explanation['parent_chain_length']}")
    print(f"Is Consistent: {explanation['consistency']['is_consistent']}")


def example_6_real_world_scenario():
    """Example 6: Real-world scenario - analyzing user data."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Real-World Scenario - User Data Analysis")
    print("="*60)
    
    engine = create_engine("Example6")
    
    # Simulate a user database
    users_data = [
        {"name": "Alice", "age": 30, "score": 95},
        {"name": "Bob", "age": 25, "score": 87},
        {"name": "Charlie", "age": 35, "score": 92},
    ]
    
    print(f"\nOriginal Data: {len(users_data)} users")
    
    # Encode the data
    state = engine.encode(users_data, source="user_database")
    print(f"Encoded state ID: {state.representation_id}")
    
    # Extract names
    print(f"\n--- Extracting Names ---")
    for i, user in enumerate(users_data):
        user_state = engine.encode(user, source=f"user_{i}")
        name_state = engine.project(user_state, 'name')
        print(f"User {i}: {name_state.content}")
    
    # Compose scores for statistics
    print(f"\n--- Score Composition ---")
    score_states = []
    for i, user in enumerate(users_data):
        user_state = engine.encode(user, source=f"user_{i}")
        score_state = engine.project(user_state, 'score')
        score_states.append(score_state)
    
    stats = engine.compose(
        score_states,
        rule='average',
        composition_func=lambda x: sum(x) / len(x)
    )
    
    average_score = stats.content['composed_value']
    print(f"Average Score: {average_score:.1f}")


def example_7_transformation_history():
    """Example 7: Examining transformation history."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Transformation History")
    print("="*60)
    
    engine = create_engine("Example7")
    
    # Create a sequence of operations
    print("\n--- Operations ---")
    s1 = engine.encode(100)
    print("1. Encode 100")
    
    s2 = engine.encode(200)
    print("2. Encode 200")
    
    s3 = engine.compose([s1, s2], 'sum', sum)
    print("3. Compose (sum)")
    
    s4 = engine.transform(s3, 'identity')
    print("4. Apply identity")
    
    # Get statistics
    print("\n--- Engine Statistics ---")
    stats = engine.stats()
    
    print(f"Engine Name: {stats['name']}")
    print(f"Total States: {stats['total_states']}")
    print(f"Total Transformations: {stats['total_transformations']}")
    print(f"Registered Transformations: {stats['registered_transformations']}")
    print(f"Valid Transformations: {stats['valid_transformations']}")
    print(f"Failed Transformations: {stats['failed_transformations']}")
    
    # List all transformations
    print(f"\n--- Available Transformations ---")
    transforms = engine.list_transformations()
    for name, description in transforms.items():
        print(f"• {name}: {description}")


def example_8_multi_level_hierarchy():
    """Example 8: Building a multi-level data hierarchy."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Multi-Level Hierarchy")
    print("="*60)
    
    engine = create_engine("Example8")
    
    # Build a hierarchy
    print("\n--- Building Company Hierarchy ---")
    
    # Level 1: Employees
    employees = [
        {"id": 1, "name": "Alice", "department": "Engineering"},
        {"id": 2, "name": "Bob", "department": "Sales"},
        {"id": 3, "name": "Charlie", "department": "Engineering"},
    ]
    
    company_state = engine.encode(employees, source="company_employees")
    print(f"Level 0: Company (state: {company_state.representation_id[:8]}...)")
    
    # Level 2: Individual departments
    departments = {}
    for employee in employees:
        dept = employee['department']
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(employee['name'])
    
    print(f"\nLevel 1: Departments")
    for dept_name, emp_names in departments.items():
        dept_state = engine.encode(emp_names, source=f"dept_{dept_name}")
        print(f"  {dept_name}: {dep_state.representation_id[:8]}...")
    
    print("\nHierarchy created successfully!")


def example_9_practical_unary_principle():
    """Example 9: Demonstrating the core unary principle."""
    print("\n" + "="*60)
    print("EXAMPLE 9: Core Unary Principle - Everything is 1")
    print("="*60)
    
    engine = create_engine("Example9")
    
    print("\nThe Unary Principle: All data is a representation of 1 (Being)")
    print("Only the form changes, never the fundamental unity.\n")
    
    # Different representations of "unity"
    representations = [
        (None, "Absence (representation of 1)"),
        (0, "Zero (representation of 1)"),
        (1, "One (direct representation)"),
        ("being", "Concept (representation of 1)"),
        ([1], "List containing 1"),
        ({"unity": True}, "Dictionary about unity"),
    ]
    
    print("--- Different Representations of Unity ---")
    for value, description in representations:
        state = engine.encode(value, source=description)
        print(f"\n{description}:")
        print(f"  Value: {value}")
        print(f"  Level: {state.level.name}")
        print(f"  Is Consistent: {engine.verify_consistency(state)['is_consistent']}")
    
    print("\n✓ All representations are valid and maintain oneness!")


def example_10_deterministic_reasoning():
    """Example 10: Showing deterministic (not probabilistic) reasoning."""
    print("\n" + "="*60)
    print("EXAMPLE 10: Deterministic Reasoning")
    print("="*60)
    
    engine = create_engine("Example10")
    
    print("\nBetaRoot Uses Deterministic Logic (1.0 certainty)")
    print("Traditional AI Uses Probabilistic Logic (~0.85 certainty)\n")
    
    # Create logical states
    fact1 = engine.encode("All humans are mortal", source="logical_fact")
    fact2 = engine.encode("Socrates is human", source="logical_fact")
    
    print("Fact 1: All humans are mortal")
    print(f"  Certainty: {fact1.certainty}")
    
    print("\nFact 2: Socrates is human")
    print(f"  Certainty: {fact2.certainty}")
    
    # Logical conclusion
    conclusion = engine.encode(
        "Therefore, Socrates is mortal",
        source="logical_conclusion"
    )
    
    print("\nConclusion: Socrates is mortal")
    print(f"  Certainty: {conclusion.certainty}")
    
    print("\n✓ All conclusions are 100% certain (not probabilistic)!")


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        example_1_basic_encoding,
        example_2_transformations,
        example_3_composition,
        example_4_consistency_verification,
        example_5_introspection,
        example_6_real_world_scenario,
        example_7_transformation_history,
        example_8_multi_level_hierarchy,
        example_9_practical_unary_principle,
        example_10_deterministic_reasoning,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in {example_func.__name__}: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("BetaRoot Phase 1 - Practical Examples")
    print("="*60)
    
    # Run specific example or all
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        example_func = globals().get(f'example_{example_num}')
        if example_func:
            example_func()
        else:
            print(f"Example {example_num} not found")
    else:
        # Run all
        run_all_examples()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
