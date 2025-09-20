"""
Algorithm Visualization Demo

Comprehensive demonstration script that showcases the algorithm visualization
framework with text-based output and performance analysis.

Author: Senior Data Visualization Developer
"""

import time
import random
from typing import List, Dict, Any, Optional

# Import our visualization framework
try:
    from algorithm_visualizer.core.comparator import AlgorithmComparator
    from algorithm_visualizer.core.text_visualizer import TextVisualizer
    from algorithm_visualizer.algorithms import (
        MergeSortVisualizer, QuickSortVisualizer,
        SelectionSortVisualizer, PriorityQueueSortVisualizer
    )
    from algorithm_visualizer.utils.data_io import export_metrics
    
    # Define available visualizers
    AVAILABLE_VISUALIZERS = {
        'merge': MergeSortVisualizer,
        'quick': QuickSortVisualizer,
        'selection': SelectionSortVisualizer,
        'priority_queue': PriorityQueueSortVisualizer
    }
    
    VISUALIZER_AVAILABLE = True
except ImportError as e:
    print(f"Error importing visualizer: {e}")
    print("Please ensure the algorithm_visualizer package is properly installed.")
    VISUALIZER_AVAILABLE = False
    AVAILABLE_VISUALIZERS = {}

from algorithm_visualizer.utils.data_io import read_numbers

def main():
    """Main demonstration function."""
    print("🔍 Algorithm Visualization Framework Demo")
    print("=" * 60)
    
    # Initialize text visualizer
    text_viz = TextVisualizer()
    
    # Demo menu
    while True:
        print("\\n📋 Available Demos:")
        print("1. 🎯 Quick Demo (Small Dataset)")
        print("2. 📊 Comprehensive Analysis")
        print("3. 🎮 Interactive Mode")
        print("4. 📈 Performance Benchmarking")
        print("5. 💾 Load Data from File")
        print("6. 🎨 Step-by-Step Visualization")
        print("0. ❌ Exit")
        
        choice = input("\\nSelect demo (0-6): ").strip()
        
        if choice == "0":
            print("Goodbye! 👋")
            break
        elif choice == "1":
            quick_demo()
        elif choice == "2":
            comprehensive_analysis()
        elif choice == "3":
            interactive_mode()
        elif choice == "4":
            performance_benchmarking()
        elif choice == "5":
            load_from_file_demo()
        elif choice == "6":
            step_by_step_demo()
        else:
            print("❌ Invalid choice. Please try again.")

def quick_demo():
    """Quick demonstration with a small dataset."""
    print("\\n🎯 Quick Demo")
    print("-" * 30)
    
    # Generate small random dataset
    data = [random.randint(1, 50) for _ in range(8)]
    print(f"Dataset: {data}")
    
    # Run two algorithms
    comparator = AlgorithmComparator(data)
    
    print("\\n🔄 Running Merge Sort...")
    merge_viz = comparator.add_algorithm(MergeSortVisualizer, "Merge Sort")
    
    print("\\n🔄 Running Quick Sort...")
    quick_viz = comparator.add_algorithm(QuickSortVisualizer, "Quick Sort")
    
    # Show comparison
    print("\\n📊 Performance Comparison:")
    comparator.print_comparison_table()
    
    # Show text report for one algorithm
    text_viz = TextVisualizer()
    print("\\n📄 Detailed Report (Merge Sort):")
    print(text_viz.create_summary_report(merge_viz))

def comprehensive_analysis():
    """Comprehensive analysis with all algorithms."""
    print("\\n📊 Comprehensive Analysis")
    print("-" * 40)
    
    # Get dataset size from user
    try:
        size = int(input("Enter dataset size (5-50): "))
        size = max(5, min(50, size))
    except ValueError:
        size = 15
        print(f"Using default size: {size}")
    
    # Generate dataset
    data = [random.randint(1, 100) for _ in range(size)]
    print(f"\\nDataset ({size} elements): {data}")
    
    # Run all algorithms
    comparator = AlgorithmComparator(data)
    
    algorithms = [
        (MergeSortVisualizer, "Merge Sort"),
        (QuickSortVisualizer, "Quick Sort"),
        (SelectionSortVisualizer, "Selection Sort"),
        (PriorityQueueSortVisualizer, "Priority Queue Sort")
    ]
    
    visualizers = {}
    for viz_class, name in algorithms:
        print(f"\\n🔄 Running {name}...")
        try:
            viz = comparator.add_algorithm(viz_class, name)
            visualizers[name] = viz
        except Exception as e:
            print(f"❌ Error running {name}: {e}")
    
    # Show comprehensive comparison
    print("\\n📊 Performance Comparison:")
    comparator.print_comparison_table()
    
    # Show detailed metrics for each algorithm
    text_viz = TextVisualizer()
    for name, viz in visualizers.items():
        print(f"\\n📄 Detailed Report ({name}):")
        print(text_viz.create_summary_report(viz))
    
    # Export option
    export_choice = input("\\n💾 Export results to JSON? (y/n): ").strip().lower()
    if export_choice == 'y':
        for name, viz in visualizers.items():
            filename = f"{name.replace(' ', '_').lower()}_results.json"
            export_metrics(viz, filename)
            print(f"✅ Exported {filename}")

def interactive_mode():
    """Interactive mode for custom analysis."""
    print("\\n🎮 Interactive Mode")
    print("-" * 25)
    
    # Get custom dataset
    print("\\n📝 Dataset Configuration:")
    print("1. Random dataset")
    print("2. Manual input")
    print("3. Specific pattern")
    
    data_choice = input("Choose option (1-3): ").strip()
    
    if data_choice == "1":
        size = int(input("Size: "))
        min_val = int(input("Min value: "))
        max_val = int(input("Max value: "))
        data = [random.randint(min_val, max_val) for _ in range(size)]
    elif data_choice == "2":
        data_str = input("Enter numbers separated by spaces: ")
        data = [int(x) for x in data_str.split()]
    elif data_choice == "3":
        pattern = input("Pattern (sorted/reverse/nearly): ").strip().lower()
        size = int(input("Size: "))
        if pattern == "sorted":
            data = list(range(1, size + 1))
        elif pattern == "reverse":
            data = list(range(size, 0, -1))
        elif pattern == "nearly":
            data = list(range(1, size + 1))
            # Swap a few elements
            for _ in range(size // 10):
                i, j = random.randint(0, size-1), random.randint(0, size-1)
                data[i], data[j] = data[j], data[i]
        else:
            data = [random.randint(1, 100) for _ in range(size)]
    else:
        data = [random.randint(1, 50) for _ in range(10)]
    
    print(f"\\nDataset: {data}")
    
    # Algorithm selection
    print("\\n🎯 Algorithm Selection:")
    available = list(AVAILABLE_VISUALIZERS.keys())
    for i, alg in enumerate(available, 1):
        print(f"{i}. {alg}")
    
    selected_indices = input("Select algorithms (comma-separated numbers): ").split(",")
    selected_algorithms = []
    
    for idx_str in selected_indices:
        try:
            idx = int(idx_str.strip()) - 1
            if 0 <= idx < len(available):
                selected_algorithms.append(available[idx])
        except ValueError:
            continue
    
    if not selected_algorithms:
        selected_algorithms = ['merge_sort']
    
    # Run selected algorithms
    comparator = AlgorithmComparator(data)
    results = {}
    
    for alg_name in selected_algorithms:
        print(f"\\n🔄 Running {alg_name}...")
        viz_class = AVAILABLE_VISUALIZERS[alg_name]
        viz = comparator.add_algorithm(viz_class)
        results[alg_name] = viz
    
    # Show results
    print("\\n📊 Results:")
    comparator.print_comparison_table()

def performance_benchmarking():
    """Performance benchmarking across different data sizes."""
    print("\\n📈 Performance Benchmarking")
    print("-" * 35)
    
    # Different dataset sizes
    sizes = [10, 20, 30, 50]
    results = {}
    
    for size in sizes:
        print(f"\\n📊 Testing with {size} elements...")
        data = [random.randint(1, 100) for _ in range(size)]
        
        comparator = AlgorithmComparator(data)
        
        # Test each algorithm
        for alg_name, viz_class in AVAILABLE_VISUALIZERS.items():
            print(f"  🔄 Running {alg_name}...")
            try:
                viz = comparator.add_algorithm(viz_class)
                
                if size not in results:
                    results[size] = {}
                results[size][alg_name] = viz.get_performance_summary()
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    # Display benchmark results
    print("\\n📈 Benchmark Results:")
    print("=" * 80)
    
    headers = ["Size"] + list(next(iter(results.values())).keys())
    print(f"{'Size':<6} {'Algorithm':<20} {'Time (s)':<12} {'Comparisons':<12} {'Swaps':<8}")
    print("-" * 80)
    
    for size in sorted(results.keys()):
        for alg_name, summary in results[size].items():
            print(f"{size:<6} {alg_name:<20} {summary['execution_time']:<12.6f} "
                  f"{summary['comparisons']:<12} {summary['swaps']:<8}")

def load_from_file_demo():
    """Demonstrate loading data from files."""
    print("\\n💾 Load Data from File Demo")
    print("-" * 35)
    
    # List available files
    sample_files = ["numbers5.txt", "numbers10.txt", "numbers100.txt"]
    
    print("Available sample files:")
    for i, filename in enumerate(sample_files, 1):
        print(f"{i}. {filename}")
    
    choice = input("\\nSelect file (1-3) or enter custom filename: ").strip()
    
    try:
        if choice in ['1', '2', '3']:
            filename = sample_files[int(choice) - 1]
        else:
            filename = choice
        
        print(f"\\n📂 Loading data from {filename}...")
        data = read_numbers(filename)
        print(f"✅ Loaded {len(data)} numbers: {data[:10]}{'...' if len(data) > 10 else ''}")
        
        # Run analysis
        comparator = AlgorithmComparator(data)
        
        # Run a couple of algorithms
        merge_viz = comparator.add_algorithm(MergeSortVisualizer, "Merge Sort")
        quick_viz = comparator.add_algorithm(QuickSortVisualizer, "Quick Sort")
        
        print("\\n📊 Results:")
        comparator.print_comparison_table()
        
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
    except Exception as e:
        print(f"❌ Error loading file: {e}")

def step_by_step_demo():
    """Step-by-step visualization demo."""
    print("\\n🎨 Step-by-Step Visualization Demo")
    print("-" * 45)
    
    # Small dataset for clear visualization
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Dataset: {data}")
    
    # Choose algorithm
    print("\\nChoose algorithm:")
    algorithms = list(AVAILABLE_VISUALIZERS.keys())
    for i, alg in enumerate(algorithms, 1):
        print(f"{i}. {alg}")
    
    try:
        choice = int(input("Select (1-4): ")) - 1
        if 0 <= choice < len(algorithms):
            alg_name = algorithms[choice]
            viz_class = AVAILABLE_VISUALIZERS[alg_name]
        else:
            alg_name = "merge_sort"
            viz_class = MergeSortVisualizer
    except ValueError:
        alg_name = "merge_sort"
        viz_class = MergeSortVisualizer
    
    print(f"\\n🔄 Running {alg_name} with step tracking...")
    visualizer = viz_class(data=data)
    result = visualizer.sort()
    
    print(f"\\n✅ Sorted result: {result}")
    print(f"📊 Total steps recorded: {len(visualizer.steps)}")
    
    # Show steps interactively
    text_viz = TextVisualizer()
    
    show_all = input("\\n🎬 Show all steps? (y/n): ").strip().lower() == 'y'
    
    if show_all:
        for step in visualizer.steps:
            text_viz.print_step(step)
            if len(visualizer.steps) > 20:  # Pause for long algorithms
                input("Press Enter to continue...")
    else:
        # Show specific steps
        while True:
            try:
                step_num = input(f"\\nEnter step number (1-{len(visualizer.steps)}, 0 to exit): ")
                step_num = int(step_num)
                
                if step_num == 0:
                    break
                elif 1 <= step_num <= len(visualizer.steps):
                    step = visualizer.steps[step_num - 1]
                    text_viz.print_step(step)
                else:
                    print("❌ Invalid step number")
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                break
    
    # Show summary report
    print("\\n📄 Final Report:")
    print(text_viz.create_summary_report(visualizer))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        print("Please check your Python environment and dependencies.")