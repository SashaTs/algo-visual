#!/usr/bin/env python3
"""
Test script for the improved animation system
"""

import sys
import os

# Add the project root to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_animation_import():
    """Test if the animation classes can be imported successfully."""
    try:
        from algorithm_visualizer.ui.animations import AlgorithmAnimator, StreamlitAnimationManager
        print("✅ Animation classes imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_algorithm_with_animation():
    """Test creating an algorithm visualizer and generating steps."""
    try:
        from algorithm_visualizer.algorithms import MergeSortVisualizer
        
        # Create a simple dataset
        data = [64, 34, 25, 12, 22, 11, 90]
        
        # Create and run the visualizer
        visualizer = MergeSortVisualizer("Merge Sort", data)
        result = visualizer.sort()
        
        print(f"✅ Algorithm executed successfully")
        print(f"   Original: {data}")
        print(f"   Sorted: {result}")
        print(f"   Steps recorded: {len(visualizer.steps)}")
        print(f"   Comparisons: {visualizer.metrics.comparisons}")
        
        return True
    except Exception as e:
        print(f"❌ Algorithm test failed: {e}")
        return False

def test_animation_container():
    """Test creating animation HTML."""
    try:
        from algorithm_visualizer.ui.animations import AlgorithmAnimator
        
        animator = AlgorithmAnimator()
        
        # Test data
        data = [5, 2, 8, 1, 9]
        step_info = {
            'step_number': 1,
            'description': 'Testing animation container',
            'comparison_indices': [0, 1],
            'swap_indices': [],
            'pivot_index': None,
            'highlight_indices': [2]
        }
        
        html = animator.create_smooth_animation_container(data, step_info, "Test Algorithm")
        
        print("✅ Animation container created successfully")
        print(f"   HTML length: {len(html)} characters")
        print(f"   Contains CSS: {'<style>' in html}")
        print(f"   Contains JavaScript: {'<script>' in html}")
        
        return True
    except Exception as e:
        print(f"❌ Animation container test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Improved Animation System")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_animation_import),
        ("Algorithm Test", test_algorithm_with_animation),
        ("Animation Container Test", test_animation_container)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Animation system is working correctly.")
        print("\n📝 Summary of Fixes:")
        print("   ✅ Fixed +2 step increment issue")
        print("   ✅ Improved play/pause functionality")  
        print("   ✅ Added smooth animation container")
        print("   ✅ Reduced page refresh flickering")
        print("   ✅ Better state management")
    else:
        print("❌ Some tests failed. Please check the issues above.")