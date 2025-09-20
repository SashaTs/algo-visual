"""
Data input/output utilities for the algorithm visualization framework.
"""

# Import all functionality from data_io module for convenience
from .data_io import (
    read_numbers,
    export_metrics,
    import_metrics,
    save_dataset,
    generate_test_data,
    validate_data,
    # Backward compatibility aliases
    load_data_from_file,
    generate_random_data
)

# Export everything for convenience
__all__ = [
    'read_numbers',
    'export_metrics', 
    'import_metrics',
    'save_dataset',
    'generate_test_data',
    'validate_data',
    'load_data_from_file',
    'generate_random_data'
]