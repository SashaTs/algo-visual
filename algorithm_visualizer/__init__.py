"""
Algorithm Visualizer Package

A comprehensive tool for visualizing and analyzing sorting algorithms.
Designed to work with minimal dependencies while providing enhanced features
when optional visualization libraries are available.
"""

import sys
from typing import List

# Dependency checking
def _check_dependencies():
    """Check for optional dependencies and return availability status."""
    deps = {}
    
    try:
        import matplotlib
        deps['matplotlib'] = True
    except ImportError:
        deps['matplotlib'] = False
    
    try:
        import plotly
        deps['plotly'] = True
    except ImportError:
        deps['plotly'] = False
    
    try:
        import streamlit
        deps['streamlit'] = True
    except ImportError:
        deps['streamlit'] = False
    
    return deps

# Check dependencies once at import time
_DEPENDENCIES = _check_dependencies()

# Export dependency status
MATPLOTLIB_AVAILABLE = _DEPENDENCIES['matplotlib']
PLOTLY_AVAILABLE = _DEPENDENCIES['plotly']
STREAMLIT_AVAILABLE = _DEPENDENCIES['streamlit']

def require_dependency(name: str):
    """Require a specific dependency and provide helpful error message."""
    if not _DEPENDENCIES.get(name, False):
        install_commands = {
            'matplotlib': 'pip install matplotlib',
            'plotly': 'pip install plotly',
            'streamlit': 'pip install streamlit'
        }
        cmd = install_commands.get(name, f'pip install {name}')
        raise ImportError(f"Missing optional dependency '{name}'. Install with: {cmd}")

# Core imports (always available)
try:
    from .algorithms import (
        create_algorithm_visualizer,
        get_available_algorithms,
        get_algorithm_info
    )
    from .core.comparator import AlgorithmComparator
    from .core.base import AlgorithmVisualizer, AlgorithmStep, PerformanceMetrics
    from .core.text_visualizer import TextVisualizer
    
except ImportError as e:
    print(f"Error importing core components: {e}")
    print("Make sure all core modules are properly installed")
    raise

# Conditional imports with fallback
try:
    from .visualizers import get_available_backends, create_visualizer
except ImportError:
    def get_available_backends():
        return ['text']
    
    def create_visualizer(backend='text', **kwargs):
        if backend != 'text':
            raise ValueError(f"Backend '{backend}' not available. Only 'text' backend is available.")
        return TextVisualizer(**kwargs)

# Package metadata
__version__ = "1.0.0"
__author__ = "Alex"
__description__ = "A comprehensive tool for visualizing and analyzing sorting algorithms"

# Main exports
__all__ = [
    # Core functionality
    'create_algorithm_visualizer',
    'get_available_algorithms',
    'get_algorithm_info',
    'AlgorithmComparator',
    'AlgorithmVisualizer',
    'AlgorithmStep',
    'PerformanceMetrics',
    'TextVisualizer',
    
    # Visualization
    'get_available_backends',
    'create_visualizer',
    
    # Dependency status
    'MATPLOTLIB_AVAILABLE',
    'PLOTLY_AVAILABLE', 
    'STREAMLIT_AVAILABLE',
    'require_dependency',
    
    # Metadata
    '__version__',
    '__author__',
    '__description__'
]

def print_system_info():
    """Print system and dependency information."""
    print(f"Algorithm Visualizer v{__version__}")
    print(f"Python {sys.version}")
    print("\nOptional Dependencies:")
    for name, available in _DEPENDENCIES.items():
        status = "✅ Available" if available else "❌ Not installed"
        print(f"  {name}: {status}")
    
    print(f"\nAvailable algorithms: {', '.join(get_available_algorithms())}")
    print(f"Available backends: {', '.join(get_available_backends())}")

# Add convenience function to exports
__all__.append('print_system_info')