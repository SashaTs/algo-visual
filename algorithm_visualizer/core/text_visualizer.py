"""
Text-based visualization for algorithm steps.

This module provides ASCII-based visualization that works in any terminal
without requiring graphics libraries.
"""

from typing import Dict
from .base import AlgorithmStep, AlgorithmVisualizer

class TextVisualizer:
    """Text-based visualization for environments without graphics libraries."""
    
    def __init__(self):
        self.color_symbols = {
            'default': '█',
            'comparing': '▓',
            'highlighted': '▒',
            'swapped': '░',
            'pivot': '▀'
        }
    
    def print_step(self, step: AlgorithmStep, width: int = 80):
        """Print a text representation of the algorithm step."""
        print(f"\nStep {step.step_number}: {step.description}")
        print("-" * width)
        
        # Create visual representation
        array_str = "["
        for i, value in enumerate(step.array_state):
            symbol = self._get_symbol(i, step)
            array_str += f"{symbol} {value:3} "
        array_str = array_str.rstrip() + "]"
        
        print(f"Array: {array_str}")
        
        # Add legend
        legend = []
        if step.comparison_indices:
            legend.append(f"{self.color_symbols['comparing']} = Comparing")
        if step.highlighted_indices:
            legend.append(f"{self.color_symbols['highlighted']} = Highlighted")
        if step.swapped_indices:
            legend.append(f"{self.color_symbols['swapped']} = Swapped")
        if step.pivot_index is not None:
            legend.append(f"{self.color_symbols['pivot']} = Pivot")
        
        if legend:
            print("Legend: " + " | ".join(legend))
    
    def _get_symbol(self, index: int, step: AlgorithmStep) -> str:
        """Get the symbol for an array element based on its role."""
        if step.pivot_index == index:
            return self.color_symbols['pivot']
        elif index in step.swapped_indices:
            return self.color_symbols['swapped']
        elif index in step.comparison_indices:
            return self.color_symbols['comparing']
        elif index in step.highlighted_indices:
            return self.color_symbols['highlighted']
        else:
            return self.color_symbols['default']
    
    def create_summary_report(self, visualizer: AlgorithmVisualizer) -> str:
        """Create a text summary report."""
        summary = visualizer.get_performance_summary()
        info = visualizer.get_algorithm_info()
        
        # Format execution time properly
        exec_time = summary['execution_time']
        if exec_time == 0:
            time_str = "0.000000s"
        else:
            time_str = f"{exec_time:.6f}s"
        
        report = f"""
╔══════════════════════════════════════════╗
║           ALGORITHM ANALYSIS REPORT       ║
╠══════════════════════════════════════════╣
║ Algorithm: {summary['algorithm']:<25} ║
║ Array Size: {summary['array_size']:<24} ║
║ Execution Time: {time_str:<19} ║
║ Total Steps: {summary['total_steps']:<23} ║
║ Comparisons: {summary['comparisons']:<23} ║
║ Swaps: {summary['swaps']:<29} ║
╠══════════════════════════════════════════╣
║ Time Complexity: {info.get('time_complexity', 'N/A'):<19} ║
║ Space Complexity: {info.get('space_complexity', 'N/A'):<18} ║
╚══════════════════════════════════════════╝
        """.strip()
        
        return report
    
    def print_all_steps(self, visualizer: AlgorithmVisualizer, max_steps: int = 20):
        """Print all steps of an algorithm execution."""
        if not visualizer.steps:
            print("No steps recorded for this algorithm.")
            return
        
        print(f"\n🎬 All Steps for {visualizer.name}")
        print("=" * 60)
        
        steps_to_show = visualizer.steps[:max_steps]
        for step in steps_to_show:
            self.print_step(step)
            if len(visualizer.steps) > max_steps:
                input("Press Enter to continue...")
        
        if len(visualizer.steps) > max_steps:
            print(f"\n... and {len(visualizer.steps) - max_steps} more steps")
        
        print(f"\n📊 Final Summary:")
        print(self.create_summary_report(visualizer))