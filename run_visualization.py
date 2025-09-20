#!/usr/bin/env python3
"""
Algorithm Visualization Quick Start

A simple script to demonstrate the algorithm visualization framework
with the existing algorithms in the project.

Usage:
    python run_visualization.py

Author: Senior Data Visualization Developer
"""

import os
import sys

def main():
    """Main function to run visualization examples."""
    print("🔍 Algorithm Visualization Framework")
    print("=" * 50)
    print("Visualizing existing sorting algorithms from the project")
    print()
    
    # Check if framework files exist
    required_files = [
        "algorithm_visualizer_core.py",
        "sorting_visualizers.py", 
        "reader.py"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        print("Please ensure all framework files are in the current directory.")
        return
    
    try:
        # Import the framework
        from algorithm_visualizer.core.comparator import AlgorithmComparator
        from algorithm_visualizer.core.text_visualizer import TextVisualizer
        from algorithm_visualizer.algorithms import (
            MergeSortVisualizer, QuickSortVisualizer, 
            SelectionSortVisualizer, PriorityQueueSortVisualizer
        )
        from algorithm_visualizer.utils.data_io import read_numbers
        
        print("✅ Framework loaded successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check that the algorithm_visualizer package is properly installed.")
        return
    
    # Load sample data
    sample_files = ["numbers10.txt", "numbers5.txt"]
    data = None
    
    for filename in sample_files:
        if os.path.exists(filename):
            try:
                data = read_numbers(filename)
                print(f"📂 Loaded data from {filename}: {data}")
                break
            except Exception as e:
                print(f"⚠️  Could not load {filename}: {e}")
    
    if data is None:
        # Use default data if no files available
        data = [23, 95, 0, 58, 11, 76, 34, 100, 67, 49]
        print(f"📊 Using default data: {data}")
    
    print()
    
    # Example 1: Quick comparison
    print("🎯 Example 1: Quick Algorithm Comparison")
    print("-" * 40)
    
    try:
        comparator = AlgorithmComparator(data[:8])  # Use smaller subset for demo
        
        print("Running algorithms...")
        merge_viz = comparator.add_algorithm(MergeSortVisualizer, "Merge Sort")
        quick_viz = comparator.add_algorithm(QuickSortVisualizer, "Quick Sort")
        selection_viz = comparator.add_algorithm(SelectionSortVisualizer, "Selection Sort")
        
        print("\\n📊 Performance Comparison:")
        comparator.print_comparison_table()
        
    except Exception as e:
        print(f"❌ Error in comparison: {e}")
    
    print()
    
    # Example 2: Step-by-step visualization
    print("🎨 Example 2: Step-by-Step Visualization")
    print("-" * 45)
    
    try:
        # Use a small dataset for step visualization
        small_data = [64, 34, 25, 12, 22]
        print(f"Dataset: {small_data}")
        
        visualizer = MergeSortVisualizer(data=small_data)
        result = visualizer.sort()
        
        print(f"\\nSorted result: {result}")
        print(f"Total steps recorded: {len(visualizer.steps)}")
        print(f"Comparisons made: {visualizer.metrics.comparisons}")
        
        # Show a few key steps
        text_viz = TextVisualizer()
        print("\\n📋 Sample Steps:")
        
        step_indices = [0, len(visualizer.steps)//3, len(visualizer.steps)//2, -1]
        for idx in step_indices:
            if 0 <= idx < len(visualizer.steps) or idx == -1:
                step = visualizer.steps[idx]
                print()
                text_viz.print_step(step, width=60)
        
    except Exception as e:
        print(f"❌ Error in step visualization: {e}")
    
    print()
    
    # Example 3: Algorithm analysis
    print("📈 Example 3: Detailed Algorithm Analysis")
    print("-" * 45)
    
    try:
        # Analyze Selection Sort (simple algorithm)
        analysis_data = [5, 2, 8, 1, 9, 3]
        print(f"Analyzing Selection Sort with data: {analysis_data}")
        
        visualizer = SelectionSortVisualizer(data=analysis_data)
        result = visualizer.sort()
        
        # Show detailed report
        text_viz = TextVisualizer()
        report = text_viz.create_summary_report(visualizer)
        print()
        print(report)
        
        # Show algorithm complexity info
        info = visualizer.get_algorithm_info()
        print("\\n📚 Algorithm Information:")
        for key, value in info.items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
    except Exception as e:
        print(f"❌ Error in analysis: {e}")
    
    print()
    
    # Example 4: Different data patterns
    print("🔬 Example 4: Testing Different Data Patterns")
    print("-" * 50)
    
    patterns = {
        "Random": [7, 2, 9, 1, 5, 3],
        "Sorted": [1, 2, 3, 4, 5, 6],
        "Reverse": [6, 5, 4, 3, 2, 1],
        "Duplicates": [3, 1, 3, 2, 1, 3]
    }
    
    for pattern_name, pattern_data in patterns.items():
        try:
            print(f"\\n{pattern_name} data: {pattern_data}")
            
            # Test with Quick Sort
            visualizer = QuickSortVisualizer(data=pattern_data)
            result = visualizer.sort()
            
            summary = visualizer.get_performance_summary()
            print(f"  → Comparisons: {summary['comparisons']}, "
                  f"Swaps: {summary['swaps']}, "
                  f"Steps: {summary['total_steps']}")
            
        except Exception as e:
            print(f"  ❌ Error with {pattern_name}: {e}")
    
    print()
    
    # Example 5: Export functionality
    print("💾 Example 5: Export Functionality")
    print("-" * 35)
    
    try:
        from algorithm_visualizer.utils.data_io import export_metrics
        
        # Run algorithm and export results
        export_data = [4, 2, 7, 1, 8, 5, 6, 3]
        visualizer = PriorityQueueSortVisualizer(data=export_data)
        result = visualizer.sort()
        
        # Export to JSON
        export_filename = "sample_algorithm_results.json"
        export_metrics(visualizer, export_filename)
        
        print(f"✅ Exported results to {export_filename}")
        print(f"   Algorithm: {visualizer.name}")
        print(f"   Dataset size: {len(export_data)}")
        print(f"   Total steps: {len(visualizer.steps)}")
        print(f"   File size: {os.path.getsize(export_filename)} bytes")
        
    except Exception as e:
        print(f"❌ Error in export: {e}")
    
    print()
    
    # Conclusion
    print("🎉 Visualization Framework Demo Complete!")
    print("=" * 50)
    print("Next steps:")
    print("• Run 'python demo.py' for interactive exploration")
    print("• Install optional dependencies for advanced features:")
    print("  pip install matplotlib streamlit plotly")
    print("• Run 'streamlit run dashboard.py' for web interface")
    print("• Run 'python test_visualization.py' to run tests")
    print("• See README.md for comprehensive documentation")
    
    # Check for optional dependencies
    optional_deps = ["matplotlib", "streamlit", "plotly", "numpy", "pandas"]
    available_deps = []
    missing_deps = []
    
    for dep in optional_deps:
        try:
            __import__(dep)
            available_deps.append(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if available_deps:
        print(f"\\n✅ Available optional features: {', '.join(available_deps)}")
    if missing_deps:
        print(f"📦 Install for more features: pip install {' '.join(missing_deps)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        print("Please check your Python environment and file permissions.")
        sys.exit(1)