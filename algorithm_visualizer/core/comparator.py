"""
Algorithm comparison functionality.

This module provides tools for comparing multiple algorithms on the same dataset
and generating performance reports.
"""

import time
from typing import List, Dict, Any, Optional, Type, Union, Sequence
from .base import AlgorithmVisualizer, Number

class AlgorithmComparator:
    """Compare multiple algorithms on the same dataset."""
    
    def __init__(self, data: Sequence[Number]):
        self.data = list(data)  # Convert to list to handle type variance
        self.results: Dict[str, AlgorithmVisualizer] = {}
    
    def add_algorithm(self, visualizer_class: Type[AlgorithmVisualizer], 
                      name: Optional[str] = None) -> AlgorithmVisualizer:
        """Add an algorithm to the comparison."""
        visualizer = visualizer_class(name or visualizer_class.__name__, 
                                      list(self.data))  # Convert to list
        
        start_time = time.time()
        sorted_data = visualizer.sort()
        end_time = time.time()
        
        visualizer.metrics.execution_time = end_time - start_time
        self.results[visualizer.name] = visualizer
        
        return visualizer
    
    def add_result(self, name: str, visualizer: AlgorithmVisualizer) -> None:
        """Add a pre-computed algorithm result to the comparison."""
        self.results[name] = visualizer
    
    def get_comparison_report(self) -> Dict[str, Any]:
        """Generate a comprehensive comparison report."""
        if not self.results:
            return {}
        
        report = {
            'dataset_size': len(self.data),
            'algorithms': {},
            'rankings': {}
        }
        
        # Collect metrics for each algorithm
        for name, visualizer in self.results.items():
            report['algorithms'][name] = visualizer.get_performance_summary()
        
        # Create rankings
        metrics = ['execution_time', 'comparisons', 'swaps', 'total_steps']
        for metric in metrics:
            ranking = sorted(self.results.items(), 
                           key=lambda x: x[1].get_performance_summary()[metric])
            report['rankings'][metric] = [name for name, _ in ranking]
        
        return report
    
    def print_comparison_table(self):
        """Print a comparison table to console."""
        if not self.results:
            print("No algorithms to compare.")
            return
        
        # Prepare data
        names = list(self.results.keys())
        data = []
        for name in names:
            summary = self.results[name].get_performance_summary()
            data.append([
                name,
                f"{summary['execution_time']:.6f}",
                str(summary['comparisons']),
                str(summary['swaps']),
                str(summary['total_steps'])
            ])
        
        # Print table
        headers = ["Algorithm", "Time (s)", "Comparisons", "Swaps", "Steps"]
        col_widths = [max(len(str(row[i])) for row in [headers] + data) + 2 for i in range(len(headers))]
        
        # Print header
        print("\n" + "="*sum(col_widths))
        print("".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))))
        print("="*sum(col_widths))
        
        # Print data rows
        for row in data:
            print("".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))))
        
        print("="*sum(col_widths))
    
    def clear_results(self):
        """Clear all comparison results."""
        self.results.clear()
    
    def get_best_algorithm(self, metric: str = 'execution_time') -> Optional[str]:
        """Get the name of the best performing algorithm for a given metric."""
        if not self.results:
            return None
        
        valid_metrics = ['execution_time', 'comparisons', 'swaps', 'total_steps']
        if metric not in valid_metrics:
            raise ValueError(f"Invalid metric. Must be one of: {valid_metrics}")
        
        best_name = min(self.results.items(), 
                        key=lambda x: x[1].get_performance_summary()[metric])[0]
        return best_name