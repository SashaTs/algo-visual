"""
Basic example of using the algorithm visualizer.

This example demonstrates:
1. Creating algorithm visualizers
2. Running sorting algorithms
3. Viewing results and performance metrics
4. Comparing multiple algorithms
"""

import sys
import os

# Add parent directory to path to import algorithm_visualizer
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from algorithm_visualizer.algorithms import MergeSortVisualizer, QuickSortVisualizer, SelectionSortVisualizer, PriorityQueueSortVisualizer
from algorithm_visualizer.core.comparator import AlgorithmComparator
from algorithm_visualizer.utils.data_io import generate_random_data


def get_available_algorithms():
    """Get available algorithm visualizers."""
    return {
        'merge_sort': MergeSortVisualizer,
        'quick_sort': QuickSortVisualizer,
        'selection_sort': SelectionSortVisualizer,
        'priority_queue_sort': PriorityQueueSortVisualizer
    }


def create_algorithm_visualizer(algorithm_name: str, data):
    """Create an algorithm visualizer instance."""
    algorithms = get_available_algorithms()
    if algorithm_name not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    return algorithms[algorithm_name](algorithm_name, data)


def basic_example():
    """Basic usage example."""
    print("=== Basic Algorithm Visualization Example ===\n")
    
    # Sample data
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original data: {data}")
    
    # Create and run a merge sort visualizer
    print("\n--- Running Merge Sort ---")
    visualizer = create_algorithm_visualizer('merge_sort', data.copy())
    visualizer.sort()
    
    # Show results
    result = visualizer.get_sorted_data()
    print(f"Sorted data: {result}")
    
    # Show performance metrics
    metrics = visualizer.get_performance_metrics()
    print(f"\nPerformance Metrics:")
    print(f"  Steps: {metrics.steps}")
    print(f"  Comparisons: {metrics.comparisons}")
    print(f"  Swaps: {metrics.swaps}")
    print(f"  Execution time: {metrics.execution_time:.6f} seconds")


def comparison_example():
    """Algorithm comparison example."""
    print("\n\n=== Algorithm Comparison Example ===\n")
    
    # Generate test data
    data = generate_random_data(20, 1, 100, seed=42)
    print(f"Test data (20 random numbers): {data}")
    
    # Get available algorithms
    algorithms = get_available_algorithms()
    print(f"\nAvailable algorithms: {', '.join(algorithms)}")
    
    # Create comparator
    comparator = AlgorithmComparator(data)
    
    # Run all algorithms
    print("\nRunning algorithms...")
    for algorithm in algorithms:
        print(f"  Running {algorithm}...")
        visualizer = create_algorithm_visualizer(algorithm, data.copy())
        visualizer.sort()
        comparator.add_result(algorithm, visualizer)
    
    # Show comparison
    print("\n" + "="*80)
    comparator.print_comparison_table()
    
    # Show best algorithm
    best = comparator.get_best_algorithm()
    if best:
        print(f"\nBest algorithm: {best}")


def step_visualization_example():
    """Step-by-step visualization example."""
    print("\n\n=== Step-by-Step Visualization Example ===\n")
    
    # Small dataset for clear visualization
    data = [5, 2, 8, 1, 9]
    print(f"Data to sort: {data}")
    
    # Run selection sort (good for step visualization)
    print("\n--- Selection Sort Steps ---")
    visualizer = create_algorithm_visualizer('selection_sort', data.copy())
    visualizer.sort()
    
    # Print steps
    visualizer.print_steps()


def performance_analysis_example():
    """Performance analysis with different data sizes."""
    print("\n\n=== Performance Analysis Example ===\n")
    
    sizes = [10, 50, 100]
    algorithms = ['merge_sort', 'quick_sort', 'selection_sort']
    
    print("Performance analysis across different data sizes:")
    print("-" * 60)
    
    for size in sizes:
        print(f"\nData size: {size}")
        data = generate_random_data(size, 1, size, seed=42)
        
        for algorithm in algorithms:
            visualizer = create_algorithm_visualizer(algorithm, data.copy())
            visualizer.sort()
            metrics = visualizer.get_performance_metrics()
            
            print(f"  {algorithm:15} - Time: {metrics.execution_time:.6f}s, "
                  f"Comparisons: {metrics.comparisons:4d}, "
                  f"Swaps: {metrics.swaps:4d}")


def main():
    """Run all examples."""
    try:
        basic_example()
        comparison_example()
        step_visualization_example()
        performance_analysis_example()
        
        print("\n\n=== Examples completed successfully! ===")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()