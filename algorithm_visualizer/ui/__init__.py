"""User interface components for algorithm visualization."""

from .cli import CLIInterface
from .dashboard import StreamlitDashboard

# Optional import
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

__all__ = [
    'CLIInterface',
    'STREAMLIT_AVAILABLE'
]

if STREAMLIT_AVAILABLE:
    __all__.append('StreamlitDashboard')