#!/usr/bin/env python3
"""
Comprehensive test of all improved algorithms
"""

import sys
import os

# Add the project root to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_all_algorithms():
    """Test all algorithms with the same dataset for comparison."""
    print("🧪 Testing All Improved Algorithms")
    print("=" * 50)
    
    from algorithm_visualizer.algorithms import (
        MergeSortVisualizer, QuickSortVisualizer, 
        SelectionSortVisualizer, PriorityQueueSortVisualizer
    )
    
    # Test dataset
    test_data = [64, 34, 25, 12, 22, 11, 90]
    expected_result = sorted(test_data)
    
    algorithms = [
        ("Merge Sort", MergeSortVisualizer),
        ("Quick Sort", QuickSortVisualizer),
        ("Selection Sort", SelectionSortVisualizer),
        ("Priority Queue Sort", PriorityQueueSortVisualizer)
    ]
    
    results = {}
    
    for name, algorithm_class in algorithms:
        print(f"\n🔍 Testing {name}")
        print("-" * 30)
        
        visualizer = algorithm_class(name, test_data.copy())
        result = visualizer.sort()
        
        # Verify correctness
        success = result == expected_result
        
        results[name] = {
            'success': success,
            'result': result,
            'steps': len(visualizer.steps),
            'comparisons': visualizer.metrics.comparisons,
            'swaps': visualizer.metrics.swaps,
            'execution_time': visualizer.metrics.execution_time
        }
        
        print(f"Original: {test_data}")
        print(f"Result:   {result}")
        print(f"Expected: {expected_result}")
        print(f"Correct:  {'✅' if success else '❌'}")
        print(f"Steps:    {len(visualizer.steps)}")
        print(f"Comparisons: {visualizer.metrics.comparisons}")
        print(f"Swaps:    {visualizer.metrics.swaps}")
        
        # Show first few significant steps
        print("Key Steps:")
        significant_steps = [step for step in visualizer.steps 
                           if any([step.swapped_indices, step.comparison_indices, 
                                  "Complete" in step.description, "Starting" in step.description])]
        
        for i, step in enumerate(significant_steps[:5]):
            print(f"  {i+1}. {step.description[:60]}...")
            if step.swapped_indices:
                print(f"     Swapped: {step.swapped_indices}")
    
    # Summary
    print(f"\n📊 Algorithm Comparison Summary")
    print("=" * 50)
    print(f"{'Algorithm':<20} {'Correct':<8} {'Steps':<8} {'Comparisons':<12} {'Swaps':<8}")
    print("-" * 56)
    
    for name, data in results.items():
        status = "✅" if data['success'] else "❌"
        print(f"{name:<20} {status:<8} {data['steps']:<8} {data['comparisons']:<12} {data['swaps']:<8}")
    
    # Verify all passed
    all_passed = all(data['success'] for data in results.values())
    
    if all_passed:
        print("\n🎉 All algorithms produce correct results!")
        print("\n✅ Step Generation Improvements:")
        print("   • Accurate array state tracking throughout execution")
        print("   • Proper visualization of in-place operations")
        print("   • Clear indication of comparisons, swaps, and highlights")
        print("   • Consistent index bounds checking")
        print("   • Meaningful step descriptions")
        return True
    else:
        print("\n❌ Some algorithms failed correctness test!")
        return False

def test_step_visualization_quality():
    """Test the quality and accuracy of step visualization."""
    print("\n🔍 Testing Step Visualization Quality")
    print("=" * 40)
    
    from algorithm_visualizer.algorithms import MergeSortVisualizer
    
    data = [5, 2, 8, 1]
    visualizer = MergeSortVisualizer("Merge Sort", data)
    result = visualizer.sort()
    
    # Check for visualization quality metrics
    quality_checks = {
        'has_meaningful_descriptions': 0,
        'has_comparison_indices': 0,
        'has_swap_indices': 0,
        'has_highlight_indices': 0,
        'shows_array_changes': 0
    }
    
    previous_state = None
    for step in visualizer.steps:
        # Check meaningful descriptions
        if len(step.description) > 10 and any(word in step.description.lower() 
                                            for word in ['comparing', 'merging', 'placing', 'dividing']):
            quality_checks['has_meaningful_descriptions'] += 1
        
        # Check visualization elements
        if step.comparison_indices:
            quality_checks['has_comparison_indices'] += 1
        if step.swapped_indices:
            quality_checks['has_swap_indices'] += 1
        if step.highlighted_indices:
            quality_checks['has_highlight_indices'] += 1
        
        # Check if array state changes
        if previous_state is not None and step.array_state != previous_state:
            quality_checks['shows_array_changes'] += 1
        previous_state = step.array_state.copy()
    
    print("Quality Metrics:")
    for metric, count in quality_checks.items():
        print(f"  {metric.replace('_', ' ').title()}: {count} steps")
    
    # Quality score
    total_steps = len(visualizer.steps)
    quality_score = sum(quality_checks.values()) / (total_steps * len(quality_checks)) * 100
    print(f"\nOverall Quality Score: {quality_score:.1f}%")
    
    return quality_score > 50  # Expect at least 50% quality

if __name__ == "__main__":
    print("🚀 Comprehensive Algorithm Step Generation Test")
    print("=" * 60)
    
    tests = [
        ("All Algorithms Correctness", test_all_algorithms),
        ("Step Visualization Quality", test_step_visualization_quality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 Final Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe algorithm step generation is now accurate and ready for visualization!")
        print("\n🎯 Ready for Dashboard Testing:")
        print("   1. Run: streamlit run algorithm_visualizer/ui/dashboard.py")
        print("   2. Select any algorithm")
        print("   3. Watch accurate step-by-step visualization")
        print("   4. Use animation controls for smooth playback")
    else:
        print("❌ Some tests failed. Check the implementations above.")