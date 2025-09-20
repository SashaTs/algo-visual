# Scripts Directory

This directory contains legacy standalone sorting algorithm implementations that were moved from the root directory during refactoring.

## Files

- **legacy_merge_sort.py** - Basic merge sort implementation
- **legacy_quick_sort.py** - Basic quick sort implementation  
- **legacy_selection_sort.py** - Basic selection sort implementation
- **legacy_priority_queue_sort.py** - Basic priority queue sort implementation

## Usage

These scripts are kept for backward compatibility and educational purposes. For new development, use the comprehensive `algorithm_visualizer` package instead.

```python
# Old approach (legacy scripts)
python scripts/legacy_merge_sort.py

# New approach (recommended)
from algorithm_visualizer import create_algorithm_visualizer
visualizer = create_algorithm_visualizer('merge_sort', data)
```

## Migration

If you were using these files directly, consider migrating to the main package which provides:
- Better error handling
- Step-by-step visualization
- Performance metrics
- Multiple visualization backends
- Algorithm comparison tools