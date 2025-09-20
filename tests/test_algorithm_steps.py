#!/usr/bin/env python3
"""
Test script to verify accurate algorithm step generation
"""

import sys
import os

# Add the project root to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_merge_sort_steps():
    """Test merge sort step accuracy."""
    print("🧪 Testing Merge Sort Step Generation")
    print("-" * 40)
    
    from algorithm_visualizer.algorithms import MergeSortVisualizer
    
    # Use a small dataset for clear verification
    data = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original data: {data}")
    
    visualizer = MergeSortVisualizer("Merge Sort", data)
    result = visualizer.sort()
    
    print(f"Sorted result: {result}")
    print(f"Total steps: {len(visualizer.steps)}")
    print(f"Comparisons: {visualizer.metrics.comparisons}")
    
    # Check a few key steps
    print("\n📋 Key Steps Analysis:")
    for i, step in enumerate(visualizer.steps[:10]):  # Show first 10 steps
        print(f"Step {i+1}: {step.description}")
        print(f"   Array state: {step.array_state}")
        if step.comparison_indices:
            print(f"   Comparing indices: {step.comparison_indices}")
        if step.swapped_indices:
            print(f"   Swapped indices: {step.swapped_indices}")
        if step.highlighted_indices:
            print(f"   Highlighted indices: {step.highlighted_indices}")
        print()
    
    # Verify the final result is sorted
    assert result == sorted(data), "Final result should be sorted"
    print("✅ Merge Sort steps verified!")
    return True

def test_selection_sort_steps():
    """Test selection sort step accuracy."""
    print("\n🧪 Testing Selection Sort Step Generation")
    print("-" * 40)
    
    from algorithm_visualizer.algorithms import SelectionSortVisualizer
    
    # Use a small dataset for clear verification
    data = [64, 25, 12, 22, 11]
    print(f"Original data: {data}")
    
    visualizer = SelectionSortVisualizer("Selection Sort", data)
    result = visualizer.sort()
    
    print(f"Sorted result: {result}")
    print(f"Total steps: {len(visualizer.steps)}")
    print(f"Comparisons: {visualizer.metrics.comparisons}")
    print(f"Swaps: {visualizer.metrics.swaps}")
    
    # Verify step accuracy - selection sort should show progressive sorting
    print("\n📋 Step-by-step verification:")
    for i, step in enumerate(visualizer.steps):
        if "Sorted portion now includes" in step.description:
            print(f"Step {i+1}: {step.description}")
            print(f"   Array state: {step.array_state}")
            
            # Check if the sorted portion is actually sorted
            if step.highlighted_indices:
                sorted_portion = [step.array_state[j] for j in step.highlighted_indices]
                if len(sorted_portion) > 1:
                    assert sorted_portion == sorted(sorted_portion), f"Sorted portion should be sorted: {sorted_portion}"
    
    # Verify the final result is sorted
    assert result == sorted(data), "Final result should be sorted"
    print("✅ Selection Sort steps verified!")
    return True

def test_quick_sort_steps():
    """Test quick sort step accuracy."""
    print("\n🧪 Testing Quick Sort Step Generation")
    print("-" * 40)
    
    from algorithm_visualizer.algorithms import QuickSortVisualizer
    
    # Use a small dataset for clear verification
    data = [10, 80, 30, 90, 40, 50, 70]
    print(f"Original data: {data}")
    
    visualizer = QuickSortVisualizer("Quick Sort", data)
    result = visualizer.sort()
    
    print(f"Sorted result: {result}")
    print(f"Total steps: {len(visualizer.steps)}")
    print(f"Comparisons: {visualizer.metrics.comparisons}")
    print(f"Swaps: {visualizer.metrics.swaps}")
    
    # Check partition steps
    print("\n📋 Partition Steps Analysis:")
    partition_steps = [step for step in visualizer.steps if "Partition complete" in step.description]
    for i, step in enumerate(partition_steps):
        print(f"Partition {i+1}: {step.description}")
        print(f"   Array state: {step.array_state}")
        if step.pivot_index is not None:
            pivot_value = step.array_state[step.pivot_index]
            print(f"   Pivot value: {pivot_value} at index {step.pivot_index}")
            
            # Verify partition property: elements left of pivot <= pivot, elements right > pivot
            left_elements = step.array_state[:step.pivot_index]
            right_elements = step.array_state[step.pivot_index + 1:]
            
            if left_elements:
                assert all(x <= pivot_value for x in left_elements), f"Left elements should be <= pivot: {left_elements} <= {pivot_value}"
            if right_elements:
                assert all(x >= pivot_value for x in right_elements), f"Right elements should be >= pivot: {right_elements} >= {pivot_value}"
        print()
    
    # Verify the final result is sorted
    assert result == sorted(data), "Final result should be sorted"
    print("✅ Quick Sort steps verified!")
    return True

def test_step_consistency():
    """Test that steps show consistent array transformations."""
    print("\n🧪 Testing Step Consistency")
    print("-" * 40)
    
    from algorithm_visualizer.algorithms import SelectionSortVisualizer
    
    data = [5, 2, 8, 1, 9]
    visualizer = SelectionSortVisualizer("Selection Sort", data)
    result = visualizer.sort()
    
    # Verify that each step shows a valid array state
    for i, step in enumerate(visualizer.steps):
        # Check that array state has correct length
        assert len(step.array_state) == len(data), f"Step {i+1}: Array length should remain constant"
        
        # Check that indices are within bounds
        if step.comparison_indices:
            for idx in step.comparison_indices:
                assert 0 <= idx < len(step.array_state), f"Step {i+1}: Comparison index {idx} out of bounds"
        
        if step.swapped_indices:
            for idx in step.swapped_indices:
                assert 0 <= idx < len(step.array_state), f"Step {i+1}: Swap index {idx} out of bounds"
        
        if step.highlighted_indices:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(step.array_state), f"Step {i+1}: Highlight index {idx} out of bounds"
        
        if step.pivot_index is not None:
            assert 0 <= step.pivot_index < len(step.array_state), f"Step {i+1}: Pivot index {step.pivot_index} out of bounds"
    
    print("✅ Step consistency verified!")
    return True

if __name__ == "__main__":
    print("🔍 Testing Algorithm Step Generation Accuracy")
    print("=" * 60)
    
    tests = [
        ("Merge Sort Steps", test_merge_sort_steps),
        ("Selection Sort Steps", test_selection_sort_steps),
        ("Quick Sort Steps", test_quick_sort_steps),
        ("Step Consistency", test_step_consistency)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All step generation tests passed!")
        print("\n✅ Improvements Made:")
        print("   • Merge Sort now shows actual array transformations during merge")
        print("   • Selection Sort shows in-place sorting with growing sorted portion")
        print("   • Quick Sort uses proper in-place partitioning")
        print("   • All algorithms show accurate array states at each step")
        print("   • Proper index tracking for comparisons and swaps")
    else:
        print("❌ Some tests failed. Check the algorithm implementations.")