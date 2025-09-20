"""
Data input/output utilities for the algorithm visualization framework.
"""

import json
import os
from typing import List, Union, Dict, Any, Optional, cast
from ..core.base import AlgorithmVisualizer, Number

def read_numbers(file_path: str) -> List[Number]:
    """Read a text file and return a list of numbers (ints or floats).

    Each non-empty line should contain a single numeric literal. Lines that
    cannot be parsed as int or float will raise ValueError.
    """
    numbers: List[Number] = []
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, raw in enumerate(f, 1):
            s = raw.strip()
            if not s:
                continue
            try:
                numbers.append(int(s))
            except ValueError:
                try:
                    numbers.append(float(s))
                except ValueError:
                    raise ValueError(f"Invalid number in {file_path} at line {line_num}: {s}")
    
    return numbers

def export_metrics(visualizer: AlgorithmVisualizer, filename: str):
    """Export performance metrics to JSON."""
    data = {
        'summary': visualizer.get_performance_summary(),
        'algorithm_info': visualizer.get_algorithm_info(),
        'steps': [
            {
                'step_number': step.step_number,
                'description': step.description,
                'array_state': step.array_state,
                'highlighted_indices': step.highlighted_indices,
                'comparison_indices': step.comparison_indices,
                'swapped_indices': step.swapped_indices,
                'pivot_index': step.pivot_index,
                'metadata': step.metadata
            }
            for step in visualizer.steps
        ]
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to export metrics to {filename}: {e}")

def import_metrics(filename: str) -> Dict[str, Any]:
    """Import performance metrics from JSON."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filename}: {e}")
    except Exception as e:
        raise IOError(f"Failed to import metrics from {filename}: {e}")

def save_dataset(data: List[Number], filename: str):
    """Save a dataset to a text file."""
    try:
        with open(filename, 'w') as f:
            for number in data:
                f.write(f"{number}\n")
    except Exception as e:
        raise IOError(f"Failed to save dataset to {filename}: {e}")

def generate_test_data(size: int, min_val: int = 0, max_val: int = 100, 
                       pattern: str = 'random', seed: Optional[int] = None) -> List[Number]:
    """Generate test data with different patterns."""
    import random
    
    if seed is not None:
        random.seed(seed)
    
    if pattern == 'random':
        return cast(List[Number], [random.randint(min_val, max_val) for _ in range(size)])
    elif pattern == 'sorted':
        step = (max_val - min_val) // max(size - 1, 1)
        return cast(List[Number], [min_val + i * step for i in range(size)])
    elif pattern == 'reverse':
        step = (max_val - min_val) // max(size - 1, 1)
        return cast(List[Number], [max_val - i * step for i in range(size)])
    elif pattern == 'nearly_sorted':
        data: List[Number] = [min_val + i * ((max_val - min_val) // max(size - 1, 1)) for i in range(size)]
        # Swap a few random elements
        for _ in range(size // 10):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            data[i], data[j] = data[j], data[i]
        return data
    elif pattern == 'duplicates':
        unique_values = [random.randint(min_val, max_val) for _ in range(size // 3 + 1)]
        return cast(List[Number], [random.choice(unique_values) for _ in range(size)])
    else:
        raise ValueError(f"Unknown pattern: {pattern}")

def validate_data(data: List[Number]) -> bool:
    """Validate that data is a proper list of numbers."""
    if not isinstance(data, list):
        return False
    
    for item in data:
        if not isinstance(item, (int, float)):
            return False
    
    return True

# Aliases for backward compatibility
load_data_from_file = read_numbers
def generate_random_data(size: int, min_val: int = 0, max_val: int = 100, seed: Optional[int] = None) -> List[Number]:
    """Generate random test data with optional seed for reproducibility."""
    return generate_test_data(size, min_val, max_val, 'random', seed)