"""Setup configuration for the algorithm visualizer package."""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    """Read a file and return its contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as f:
        return f.read()

# Version
VERSION = "1.0.0"

# Required dependencies
REQUIRED = [
    # No required dependencies - the package is designed to work with Python standard library only
]

# Optional dependencies
EXTRAS = {
    'visualization': [
        'matplotlib>=3.5.0',
        'plotly>=5.0.0',
    ],
    'web': [
        'streamlit>=1.0.0',
        'pandas>=1.3.0',
    ],
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.10.0',
        'black>=21.0.0',
        'flake8>=3.8.0',
        'mypy>=0.900',
    ],
    'full': [
        'matplotlib>=3.5.0',
        'plotly>=5.0.0',
        'streamlit>=1.0.0',
        'pandas>=1.3.0',
        'numpy>=1.20.0',
    ]
}

setup(
    name="algorithm-visualizer",
    version=VERSION,
    author="Alex",
    author_email="alex@example.com",
    description="A comprehensive tool for visualizing and analyzing sorting algorithms",
    long_description="""
Algorithm Visualizer
===================

A comprehensive Python package for visualizing and analyzing sorting algorithms.

Features:
- Multiple sorting algorithm implementations (merge sort, quick sort, selection sort, priority queue sort)
- Step-by-step visualization with text, matplotlib, and plotly backends
- Performance analysis and algorithm comparison
- Interactive web dashboard using Streamlit
- Command-line interface for batch operations
- Comprehensive test suite
- Educational examples and documentation

The package is designed to work without any external dependencies for basic functionality,
with optional enhancements available through visualization libraries.

Usage:
    from algorithm_visualizer import create_algorithm_visualizer
    
    visualizer = create_algorithm_visualizer('merge_sort', [64, 34, 25, 12, 22, 11, 90])
    visualizer.sort()
    visualizer.print_steps()
""",
    long_description_content_type="text/plain",
    url="https://github.com/example/algorithm-visualizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    package_data={
        'algorithm_visualizer': [
            'data/*.txt',
            'examples/*.py',
        ],
    },
    entry_points={
        'console_scripts': [
            'algorithm-visualizer=algorithm_visualizer.ui.cli:main',
            'algorithm-dashboard=algorithm_visualizer.ui.dashboard:main',
        ],
    },
    keywords=['algorithms', 'sorting', 'visualization', 'education', 'analysis'],
    project_urls={
        'Bug Reports': 'https://github.com/example/algorithm-visualizer/issues',
        'Source': 'https://github.com/example/algorithm-visualizer',
        'Documentation': 'https://github.com/example/algorithm-visualizer/wiki',
    },
)