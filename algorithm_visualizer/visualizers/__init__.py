"""Visualization backends for algorithm visualization."""

from typing import Dict, Type, Union, Any, TYPE_CHECKING

from ..core.text_visualizer import TextVisualizer

if TYPE_CHECKING:
    from .matplotlib_visualizer import MatplotlibVisualizer
    from .plotly_visualizer import PlotlyVisualizer

# Optional imports with fallback
try:
    from .matplotlib_visualizer import MatplotlibVisualizer
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MatplotlibVisualizer = None  # type: ignore
    MATPLOTLIB_AVAILABLE = False

try:
    from .plotly_visualizer import PlotlyVisualizer
    PLOTLY_AVAILABLE = True
except ImportError:
    PlotlyVisualizer = None  # type: ignore
    PLOTLY_AVAILABLE = False

# Available visualizers registry with flexible typing to accommodate different visualizer classes
AVAILABLE_VISUALIZERS: Dict[str, Type[Any]] = {
    'text': TextVisualizer,
}

if MATPLOTLIB_AVAILABLE and MatplotlibVisualizer is not None:
    AVAILABLE_VISUALIZERS['matplotlib'] = MatplotlibVisualizer

if PLOTLY_AVAILABLE and PlotlyVisualizer is not None:
    AVAILABLE_VISUALIZERS['plotly'] = PlotlyVisualizer

def get_available_backends() -> list[str]:
    """Get list of available visualization backends."""
    return list(AVAILABLE_VISUALIZERS.keys())

def create_visualizer(backend: str, **kwargs):
    """Create a visualizer with the specified backend."""
    if backend not in AVAILABLE_VISUALIZERS:
        available = list(AVAILABLE_VISUALIZERS.keys())
        raise ValueError(f"Unknown backend: {backend}. Available: {available}")
    
    return AVAILABLE_VISUALIZERS[backend](**kwargs)

__all__ = [
    'TextVisualizer',
    'MATPLOTLIB_AVAILABLE',
    'PLOTLY_AVAILABLE',
    'get_available_backends',
    'create_visualizer',
]

# Add optional visualizers to exports if available
if MATPLOTLIB_AVAILABLE:
    __all__.append('MatplotlibVisualizer')

if PLOTLY_AVAILABLE:
    __all__.append('PlotlyVisualizer')