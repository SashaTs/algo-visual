"""
Core base classes for algorithm visualization framework.

This module contains the fundamental abstract base classes and data structures
that all algorithm visualizers inherit from.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Union, Dict, Any, Optional, Sequence
import time

Number = Union[int, float]

@dataclass
class AlgorithmStep:
    """Represents a single step in algorithm execution."""
    step_number: int
    description: str
    array_state: List[Number]
    highlighted_indices: List[int] = field(default_factory=list)
    comparison_indices: List[int] = field(default_factory=list)
    swapped_indices: List[int] = field(default_factory=list)
    pivot_index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceMetrics:
    """Tracks algorithm performance metrics."""
    execution_time: float = 0.0
    comparisons: int = 0
    swaps: int = 0
    memory_usage: int = 0
    space_complexity: str = ""
    time_complexity: str = ""
    steps: int = 0  # Added missing steps attribute
    additional_metrics: Dict[str, Any] = field(default_factory=dict)

class AlgorithmVisualizer(ABC):
    """Abstract base class for algorithm visualizers."""
    
    def __init__(self, name: str, data: Optional[Sequence[Number]] = None):
        self.name = name
        self.original_data = list(data or [])  # Convert to list for internal use
        self.current_data = list(data or [])   # Convert to list for internal use
        self.steps: List[AlgorithmStep] = []
        self.metrics = PerformanceMetrics()
        self.step_counter = 0
        self._start_time: float = 0.0
        self._end_time: float = 0.0
        
    @abstractmethod
    def sort(self) -> List[Number]:
        """Execute the sorting algorithm with step tracking."""
        pass
    
    @abstractmethod
    def get_algorithm_info(self) -> Dict[str, str]:
        """Return algorithm complexity and description information."""
        pass
    
    def add_step(self, description: str, array_state: List[Number], 
                 highlighted_indices: Optional[List[int]] = None,
                 comparison_indices: Optional[List[int]] = None,
                 swapped_indices: Optional[List[int]] = None,
                 pivot_index: Optional[int] = None,
                 **metadata):
        """Add a step to the algorithm execution trace."""
        self.step_counter += 1
        step = AlgorithmStep(
            step_number=self.step_counter,
            description=description,
            array_state=array_state.copy(),
            highlighted_indices=highlighted_indices or [],
            comparison_indices=comparison_indices or [],
            swapped_indices=swapped_indices or [],
            pivot_index=pivot_index,
            metadata=metadata
        )
        self.steps.append(step)
    
    def record_comparison(self, i: int, j: int):
        """Record a comparison operation."""
        self.metrics.comparisons += 1
    
    def record_swap(self, i: int, j: int):
        """Record a swap operation."""
        self.metrics.swaps += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            'algorithm': self.name,
            'array_size': len(self.original_data),
            'execution_time': self.metrics.execution_time,
            'comparisons': self.metrics.comparisons,
            'swaps': self.metrics.swaps,
            'total_steps': len(self.steps),
            'memory_usage': self.metrics.memory_usage,
            'complexity_info': self.get_algorithm_info()
        }
    
    def reset(self):
        """Reset the visualizer to initial state."""
        self.current_data = self.original_data.copy()
        self.steps.clear()
        self.metrics = PerformanceMetrics()
        self.step_counter = 0
    
    def get_sorted_data(self) -> List[Number]:
        """Get the sorted data from the last step or by running sort if not yet sorted."""
        if self.steps:
            # Return the array state from the last step
            return self.steps[-1].array_state.copy()
        else:
            # If no steps recorded, run sort and return result
            return self.sort()
    
    def get_steps(self) -> List[AlgorithmStep]:
        """Get the list of recorded algorithm steps."""
        return self.steps.copy()
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get the performance metrics object."""
        # Ensure execution time is calculated
        if hasattr(self, '_start_time') and hasattr(self, '_end_time'):
            self.metrics.execution_time = self._end_time - self._start_time
        return self.metrics
    
    def print_steps(self):
        """Print all algorithm steps in a formatted way."""
        from .text_visualizer import TextVisualizer
        visualizer = TextVisualizer()
        for step in self.steps:
            visualizer.print_step(step)