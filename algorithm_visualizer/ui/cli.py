"""Command line interface for algorithm visualization."""

import sys
from typing import List, Optional
from ..core.base import Number, AlgorithmVisualizer  
from ..core.comparator import AlgorithmComparator
from ..utils.data_io import load_data_from_file, generate_random_data

def create_algorithm_visualizer(name: str, data: List[Number]) -> AlgorithmVisualizer:
    """Create a visualizer instance for the given algorithm name."""
    # Import here to avoid circular imports
    from ..algorithms import (
        MergeSortVisualizer, QuickSortVisualizer, 
        SelectionSortVisualizer, PriorityQueueSortVisualizer
    )
    
    visualizers = {
        'merge_sort': MergeSortVisualizer,
        'quick_sort': QuickSortVisualizer,
        'selection_sort': SelectionSortVisualizer,
        'priority_queue_sort': PriorityQueueSortVisualizer
    }
    
    if name.lower() not in visualizers:
        raise ValueError(f"Unknown algorithm: {name}")
    
    return visualizers[name.lower()](data=data)

def get_available_algorithms() -> List[str]:
    """Get list of available algorithm names."""
    return ['merge_sort', 'quick_sort', 'selection_sort', 'priority_queue_sort']


class CLIInterface:
    """Command line interface for running algorithm visualizations."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.comparator = None  # Will be initialized when needed with data
        
    def run_single_algorithm(self, algorithm_name: str, data: List[Number], 
                           show_steps: bool = True) -> None:
        """Run a single algorithm and display results.
        
        Args:
            algorithm_name: Name of the algorithm to run
            data: Data to sort
            show_steps: Whether to show step-by-step visualization
        """
        try:
            visualizer = create_algorithm_visualizer(algorithm_name, data)
            print(f"\n=== Running {algorithm_name} ===")
            print(f"Input data: {data}")
            
            # Run the algorithm
            visualizer.sort()
            
            if show_steps:
                # Show step-by-step visualization
                visualizer.print_steps()
            
            # Show results
            sorted_data = visualizer.current_data if hasattr(visualizer, 'current_data') else visualizer.sort()
            print(f"\nSorted data: {sorted_data}")
            
            # Show performance metrics
            metrics = visualizer.get_performance_metrics()
            print(f"\nPerformance:")
            print(f"  Steps: {metrics.steps}")
            print(f"  Comparisons: {metrics.comparisons}")
            print(f"  Swaps: {metrics.swaps}")
            print(f"  Memory usage: {metrics.memory_usage}")
            print(f"  Execution time: {metrics.execution_time:.6f} seconds")
            
        except Exception as e:
            print(f"Error running algorithm: {e}")
    
    def run_comparison(self, data: List[Number], algorithms: Optional[List[str]] = None) -> None:
        """Run multiple algorithms and compare their performance.
        
        Args:
            data: Data to sort
            algorithms: List of algorithm names to compare (all if None)
        """
        if algorithms is None:
            algorithms = get_available_algorithms()
        
        print(f"\n=== Algorithm Comparison ===")
        print(f"Input data: {data}")
        print(f"Data size: {len(data)}")
        print(f"Algorithms: {', '.join(algorithms)}")
        
        # Initialize comparator with data
        self.comparator = AlgorithmComparator(data)
        
        # Run each algorithm
        for algorithm_name in algorithms:
            try:
                visualizer_class = create_algorithm_visualizer(algorithm_name, data.copy()).__class__
                self.comparator.add_algorithm(visualizer_class, algorithm_name)
                print(f"✓ {algorithm_name} completed")
            except Exception as e:
                print(f"✗ {algorithm_name} failed: {e}")
        
        # Show comparison
        print("\n" + "="*80)
        self.comparator.print_comparison_table()
        
        best = self.comparator.get_best_algorithm()
        if best:
            print(f"\nBest overall algorithm: {best}")
    
    def interactive_mode(self) -> None:
        """Run in interactive mode."""
        print("Algorithm Visualization Tool")
        print("=" * 40)
        
        while True:
            print("\nOptions:")
            print("1. Run single algorithm")
            print("2. Compare multiple algorithms")
            print("3. Load data from file")
            print("4. Generate random data")
            print("5. List available algorithms")
            print("6. Exit")
            
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == "1":
                    self._handle_single_algorithm()
                elif choice == "2":
                    self._handle_comparison()
                elif choice == "3":
                    self._handle_load_file()
                elif choice == "4":
                    self._handle_generate_data()
                elif choice == "5":
                    self._handle_list_algorithms()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _handle_single_algorithm(self) -> None:
        """Handle single algorithm execution."""
        algorithms = get_available_algorithms()
        print(f"\nAvailable algorithms: {', '.join(algorithms)}")
        
        algorithm = input("Enter algorithm name: ").strip()
        if algorithm not in algorithms:
            print(f"Unknown algorithm: {algorithm}")
            return
        
        data = self._get_data_input()
        if data is None:
            return
        
        show_steps = input("Show step-by-step visualization? (y/n): ").strip().lower() == 'y'
        self.run_single_algorithm(algorithm, data, show_steps)
    
    def _handle_comparison(self) -> None:
        """Handle algorithm comparison."""
        data = self._get_data_input()
        if data is None:
            return
        
        algorithms = get_available_algorithms()
        print(f"\nAvailable algorithms: {', '.join(algorithms)}")
        
        choice = input("Select specific algorithms? (y/n): ").strip().lower()
        if choice == 'y':
            selected = input("Enter algorithm names (comma-separated): ").strip()
            selected_algorithms = [alg.strip() for alg in selected.split(',')]
            # Validate algorithms
            invalid = [alg for alg in selected_algorithms if alg not in algorithms]
            if invalid:
                print(f"Unknown algorithms: {', '.join(invalid)}")
                return
            algorithms = selected_algorithms
        
        self.run_comparison(data, algorithms)
    
    def _handle_load_file(self) -> None:
        """Handle loading data from file."""
        filename = input("Enter filename: ").strip()
        try:
            data = load_data_from_file(filename)
            print(f"Loaded {len(data)} numbers from {filename}")
            print(f"Data: {data}")
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def _handle_generate_data(self) -> None:
        """Handle generating random data."""
        try:
            size = int(input("Enter data size: ").strip())
            min_val = int(input("Enter minimum value (default 1): ").strip() or "1")
            max_val = int(input("Enter maximum value (default 100): ").strip() or "100")
            
            data = generate_random_data(size, min_val, max_val)
            print(f"Generated data: {data}")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    def _handle_list_algorithms(self) -> None:
        """Handle listing available algorithms."""
        algorithms = get_available_algorithms()
        print(f"\nAvailable algorithms ({len(algorithms)}):")
        for i, algorithm in enumerate(algorithms, 1):
            print(f"{i}. {algorithm}")
    
    def _get_data_input(self) -> Optional[List[Number]]:
        """Get data input from user."""
        print("\nData input options:")
        print("1. Enter numbers manually")
        print("2. Load from file")
        print("3. Generate random data")
        
        choice = input("Choose option (1-3): ").strip()
        
        try:
            if choice == "1":
                data_str = input("Enter numbers (comma-separated): ").strip()
                return [int(x.strip()) for x in data_str.split(',')]
            
            elif choice == "2":
                filename = input("Enter filename: ").strip()
                return load_data_from_file(filename)
            
            elif choice == "3":
                size = int(input("Enter data size: ").strip())
                min_val = int(input("Enter minimum value (default 1): ").strip() or "1")
                max_val = int(input("Enter maximum value (default 100): ").strip() or "100")
                return generate_random_data(size, min_val, max_val)
            
            else:
                print("Invalid choice")
                return None
                
        except Exception as e:
            print(f"Error getting data: {e}")
            return None


def main():
    """Main entry point for CLI."""
    cli = CLIInterface()
    
    if len(sys.argv) > 1:
        # Command line arguments provided
        if sys.argv[1] == "interactive":
            cli.interactive_mode()
        else:
            print("Usage: python -m algorithm_visualizer.ui.cli [interactive]")
    else:
        # Default to interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()