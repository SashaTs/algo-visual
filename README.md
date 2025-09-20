# Algorithm Visualization Framework

A comprehensive, extensible algorithm visualization system designed for educational purposes and algorithm analysis. This framework provides step-by-step visualization, performance metrics, and comparison tools for sorting algorithms with support for future algorithm additions.

## 🌟 Features

### Core Functionality
- **Step-by-Step Visualization**: Track every operation in algorithm execution
- **Performance Metrics**: Measure execution time, comparisons, swaps, and memory usage
- **Algorithm Comparison**: Side-by-side analysis of multiple algorithms
- **Export Capabilities**: JSON metrics export and comprehensive reporting

### Supported Algorithms
- **Merge Sort**: Divide-and-conquer with O(n log n) complexity
- **Quick Sort**: Partition-based sorting with average O(n log n) complexity
- **Selection Sort**: Simple O(n²) algorithm for educational purposes
- **Priority Queue Sort**: Heap-based sorting approach

### Visualization Options
- **Text-Based**: ASCII visualization for terminal environments
- **Matplotlib**: Static and animated visualizations (optional)
- **Streamlit Dashboard**: Interactive web interface (optional)

### Extensibility
- **Modular Architecture**: Easy to add new algorithms
- **Plugin System**: Extensible visualizer framework
- **Custom Metrics**: Add algorithm-specific performance measurements

## 📁 Project Structure

```
algorithm_visualizer/            # Main package
├── __init__.py                 # Package initialization and exports
├── algorithms/                 # Algorithm implementations
│   └── __init__.py            # Sorting algorithm visualizers
├── core/                      # Core framework components
│   ├── base.py               # Abstract base classes and data structures
│   ├── comparator.py         # Algorithm comparison functionality
│   └── text_visualizer.py   # Text-based visualization
├── ui/                       # User interface components
│   ├── cli.py               # Command-line interface
│   ├── dashboard.py         # Streamlit web dashboard
│   └── animations.py        # Animation and visualization helpers
├── visualizers/              # Visualization backends
│   ├── matplotlib_visualizer.py  # Matplotlib plotting
│   └── plotly_visualizer.py     # Plotly interactive plots
├── utils/                    # Utility functions
│   └── data_io.py           # Data input/output operations
├── examples/                 # Usage examples
│   └── basic_usage.py       # Basic example scripts
└── data/                    # Sample data files
    ├── numbers5.txt
    ├── numbers10.txt
    └── numbers100.txt

tests/                       # Test suite
├── __init__.py             # Test package initialization
├── test_algorithm_steps.py # Algorithm step generation tests
├── test_animation_fixes.py # Animation functionality tests
├── test_comprehensive_algorithms.py  # Comprehensive algorithm tests
└── test_visualization.py  # Visualization backend tests

scripts/                     # Legacy standalone scripts (deprecated)
├── README.md               # Scripts documentation
├── legacy_merge_sort.py    # Basic merge sort implementation
├── legacy_quick_sort.py    # Basic quick sort implementation  
├── legacy_selection_sort.py # Basic selection sort implementation
└── legacy_priority_queue_sort.py # Basic priority queue sort

# Root level files
├── README.md               # Project documentation
├── setup.py               # Package installation configuration
├── requirements.txt       # Dependencies list
├── run_tests.py           # Test runner script
├── run_dashboard.py       # Dashboard launcher
├── run_visualization.py   # Visualization demo script
└── demo.py                # Comprehensive demo script
```

### Basic Installation (no dependencies)
```bash
pip install -e .
```

### With Visualization Support
```bash
pip install -e ".[visualization]"
```

### With Web Dashboard
```bash
pip install -e ".[web]"
```

### Full Installation
```bash
pip install -e ".[full]"
```

## Quick Start

### Basic Usage
```python
from algorithm_visualizer import create_algorithm_visualizer

# Create a visualizer
data = [64, 34, 25, 12, 22, 11, 90]
visualizer = create_algorithm_visualizer('merge_sort', data)

# Run the algorithm
visualizer.sort()

# View results
print("Sorted:", visualizer.get_sorted_data())
visualizer.print_steps()

# Performance metrics
metrics = visualizer.get_performance_metrics()
print(f"Comparisons: {metrics.comparisons}")
print(f"Execution time: {metrics.execution_time:.6f}s")
```

### Algorithm Comparison
```python
from algorithm_visualizer import AlgorithmComparator

# Compare multiple algorithms
comparator = AlgorithmComparator()
algorithms = ['merge_sort', 'quick_sort', 'selection_sort']

for algorithm in algorithms:
    visualizer = create_algorithm_visualizer(algorithm, data.copy())
    visualizer.sort()
    comparator.add_result(algorithm, visualizer)

# View comparison
comparator.print_comparison_table()
best = comparator.get_best_algorithm()
print(f"Best algorithm: {best}")
```

### Command Line Interface
```bash
# Interactive mode
algorithm-visualizer interactive

# Or directly in Python
python -m algorithm_visualizer.ui.cli
```

### Web Dashboard
```bash
# Start the dashboard (if Streamlit is installed)
streamlit run algorithm_visualizer/ui/dashboard.py

# Or using the package entry point (after pip install)
algorithm-dashboard

# Alternative direct invocation
python -m streamlit run algorithm_visualizer/ui/dashboard.py

# Or use the convenient launcher script
python3 run_dashboard.py
```

**Note**: The web dashboard requires Streamlit. If you encounter import errors, set up a virtual environment:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Streamlit
pip install streamlit

# Run the dashboard
streamlit run algorithm_visualizer/ui/dashboard.py
```

## 🎨 Streamlit Web Dashboard

The Streamlit dashboard provides an interactive web interface for exploring sorting algorithms with real-time visualization and comprehensive analysis tools.

### Dashboard Features

#### 📊 **Interactive Algorithm Exploration**
- **Single Algorithm Analysis**: Run individual algorithms with step-by-step visualization
- **Multi-Algorithm Comparison**: Compare multiple algorithms side-by-side
- **Performance Benchmarking**: Test algorithms across different data sizes and types
- **Algorithm Information**: Detailed complexity analysis and descriptions

#### 📋 **Flexible Data Input**
- **Manual Input**: Enter custom datasets via text input
- **Random Generation**: Generate random datasets with configurable size and range
- **File Upload**: Load data from CSV or text files
- **Pattern-Based Data**: Create sorted, reverse-sorted, or nearly-sorted datasets
- **Sample Datasets**: Use pre-loaded example datasets

#### 🎛️ **Visualization Controls**
- **Backend Selection**: Choose between text, matplotlib, or plotly visualizations
- **Step Control**: Show all steps or key steps for large datasets  
- **Interactive Charts**: Plotly-powered interactive performance charts
- **Export Options**: Download results as JSON or images

#### 📈 **Performance Analysis**
- **Real-time Metrics**: Live execution time, comparisons, and swap counts
- **Comparative Tables**: Side-by-side algorithm performance comparison
- **Scaling Analysis**: Performance across different input sizes
- **Algorithm Ranking**: Automatic identification of best-performing algorithms

### Using the Dashboard

1. **Launch the Dashboard**
   ```bash
   cd /path/to/py-test
   streamlit run algorithm_visualizer/ui/dashboard.py
   ```

2. **Configure Your Data**
   - Use the sidebar to select data input method
   - Choose from manual input, random generation, or file upload
   - Adjust data size and range as needed

3. **Explore Algorithms**
   - **Single Algorithm Tab**: Run one algorithm with detailed analysis
   - **Algorithm Comparison Tab**: Compare multiple algorithms
   - **Performance Analysis Tab**: Comprehensive benchmarking
   - **Algorithm Info Tab**: Learn about algorithm characteristics

4. **Customize Visualization**
   - Select visualization backend (text/matplotlib/plotly)
   - Toggle step-by-step visualization
   - Enable performance metrics display

5. **Analyze Results**
   - View real-time performance metrics
   - Compare algorithms in interactive tables
   - Export results for further analysis

### Dashboard Tabs Overview

#### 📈 Single Algorithm
- Choose any available algorithm
- Configure step-by-step visualization
- View detailed performance metrics
- See before/after data comparison
- Interactive algorithm information

#### ⚡ Algorithm Comparison  
- Select multiple algorithms to compare
- Real-time progress tracking
- Comprehensive comparison tables
- Best algorithm identification
- Performance ranking

#### 📊 Performance Analysis
- Test across multiple data sizes
- Different data type patterns (random, sorted, reverse)
- Detailed benchmarking results
- Performance scaling analysis
- Interactive charts and graphs

#### ℹ️ Algorithm Info
- Comprehensive algorithm documentation
- Time and space complexity information
- Stability and in-place characteristics
- Educational descriptions and use cases

### Streamlit Requirements

The dashboard requires Python 3.8+ and the following dependencies:
- `streamlit >= 1.0.0` (required)
- `pandas >= 1.3.0` (for data analysis features)
- `matplotlib >= 3.5.0` (optional, for enhanced visualizations)
- `plotly >= 5.0.0` (optional, for interactive charts)

Install all dashboard dependencies:
```bash
pip install streamlit pandas matplotlib plotly
# Or use the web extra
pip install -e ".[web]"
```

## Available Algorithms

| Algorithm | Time Complexity | Space Complexity | Stable | In-place |
|-----------|----------------|------------------|--------|----------|
| Merge Sort | O(n log n) | O(n) | Yes | No |
| Quick Sort | O(n log n) avg, O(n²) worst | O(log n) | No | Yes |
| Selection Sort | O(n²) | O(1) | No | Yes |
| Priority Queue Sort | O(n log n) | O(n) | No | No |

## Visualization Backends

The package supports multiple visualization backends with automatic fallbacks:

### 📝 **Text Visualization** (Always Available)
- **ASCII-based output**: Works in any terminal environment
- **Step-by-step display**: Clear textual representation of algorithm steps
- **No dependencies**: Uses only Python standard library
- **Cross-platform**: Works on all operating systems
- **Example output**:
  ```
  Step 1: Starting Merge Sort
    Array: [64, 34, 25, 12, 22, 11, 90]
    Highlighted: [0, 1, 2, 3, 4, 5, 6]
  
  Step 2: Dividing array into left and right halves
    Array: [64, 34, 25, 12, 22, 11, 90]
    Highlighted: [0, 1, 2]
  ```

### 📊 **Matplotlib Visualization** (Optional)
- **Static plots**: Bar charts showing array states
- **Animated sequences**: Frame-by-frame algorithm execution
- **Performance charts**: Comparison graphs and timing analysis
- **High-quality output**: Publication-ready figures
- **Installation**: `pip install matplotlib`

### 📈 **Plotly Visualization** (Optional)  
- **Interactive plots**: Zoom, pan, and hover features
- **Web-based output**: Opens in browser automatically
- **Animation controls**: Play/pause/step through algorithm execution
- **3D visualizations**: Advanced visualization options
- **Installation**: `pip install plotly`

### 🌐 **Streamlit Dashboard** (Optional)
- **Full web interface**: Complete interactive application
- **Real-time interaction**: Live algorithm execution and visualization
- **Multi-tab layout**: Organized feature access
- **Data management**: Upload, generate, and manage datasets
- **Export capabilities**: Download results and visualizations
- **Responsive design**: Works on desktop and mobile devices
- **Installation**: `pip install streamlit pandas`

#### Streamlit Dashboard Features:
- **🎯 Interactive Controls**: Sidebar configuration for all parameters
- **📊 Live Metrics**: Real-time performance tracking during execution
- **🔄 Algorithm Switching**: Easy comparison between different algorithms
- **📈 Performance Graphs**: Interactive charts with zooming and filtering
- **💾 Data Persistence**: Session state management for continuous work
- **🎨 Custom Styling**: Modern, educational-focused interface design
- **📱 Mobile Friendly**: Responsive layout that works on all devices

## Package Structure

```
algorithm_visualizer/
├── __init__.py              # Main package with dependency checking
├── algorithms/              # Algorithm implementations
│   └── __init__.py         # All sorting algorithms with visualization
├── core/                   # Core framework
│   ├── base.py            # Base classes and data structures
│   ├── comparator.py      # Algorithm comparison tools
│   └── text_visualizer.py # Text-based visualization
├── visualizers/            # Visualization backends
│   ├── __init__.py        # Backend management
│   ├── matplotlib_visualizer.py
│   └── plotly_visualizer.py
├── ui/                     # User interfaces
│   ├── cli.py             # Command-line interface
│   └── dashboard.py       # Streamlit web dashboard
├── utils/                  # Utility functions
│   └── data_io.py         # Data input/output utilities
├── tests/                  # Test suite
│   └── __init__.py        # Comprehensive tests
├── examples/               # Example scripts
│   └── basic_usage.py     # Usage examples
└── data/                   # Sample data files
    ├── numbers5.txt
    ├── numbers10.txt
    └── numbers100.txt
```

## Development

### Running Tests
```bash
# Run all tests using the test runner
python run_tests.py

# Or run individual test files from the tests directory
python tests/test_algorithm_steps.py
python tests/test_animation_fixes.py
python tests/test_comprehensive_algorithms.py
python tests/test_visualization.py

# Run tests using unittest for detailed output
python -m unittest discover tests/ -v
```

### Development Installation
```bash
pip install -e ".[dev]"
```

### Code Quality
```bash
# Format code
black algorithm_visualizer/

# Lint
flake8 algorithm_visualizer/

# Type checking
mypy algorithm_visualizer/
```

## Examples

### Basic Algorithm Visualization
```python
from algorithm_visualizer import create_algorithm_visualizer

# Quick start with random data
data = [64, 34, 25, 12, 22, 11, 90]
visualizer = create_algorithm_visualizer('merge_sort', data)
visualizer.sort()

# View performance metrics
metrics = visualizer.get_performance_metrics()
print(f"Comparisons: {metrics.comparisons}")
print(f"Swaps: {metrics.swaps}")
print(f"Time: {metrics.execution_time:.6f}s")
```

### Streamlit Dashboard Usage
```python
# Launch the interactive dashboard
import subprocess
subprocess.run(['streamlit', 'run', 'algorithm_visualizer/ui/dashboard.py'])

# Or use the CLI shortcut
from algorithm_visualizer.ui.cli import main
main(['--dashboard'])
```

### Performance Analysis
```python
from algorithm_visualizer.utils.data_io import generate_random_data

# Test different data sizes
sizes = [10, 50, 100, 500]
algorithms = ['merge_sort', 'quick_sort', 'selection_sort']

for size in sizes:
    data = generate_random_data(size, 1, size)
    print(f"\nData size: {size}")
    
    for algorithm in algorithms:
        visualizer = create_algorithm_visualizer(algorithm, data.copy())
        visualizer.sort()
        metrics = visualizer.get_performance_metrics()
        print(f"  {algorithm}: {metrics.execution_time:.6f}s, "
              f"{metrics.comparisons} comparisons, {metrics.swaps} swaps")
```

### Custom Data Loading
```python
from algorithm_visualizer.utils.data_io import load_data_from_file

# Load from file
data = load_data_from_file('algorithm_visualizer/data/numbers100.txt')
visualizer = create_algorithm_visualizer('merge_sort', data)
visualizer.sort()

# Export visualization data
export_path = 'merge_sort_analysis.json'
visualizer.export_analysis(export_path)
print(f"Analysis saved to {export_path}")
```

### Advanced Visualization
```python
from algorithm_visualizer.visualizers import create_visualizer, get_available_backends

# Check available backends
backends = get_available_backends()
print(f"Available visualization backends: {backends}")

# Use plotly for interactive visualization
if 'plotly' in backends:
    viz = create_visualizer('plotly')
    viz.visualize_steps(visualizer.get_steps(), data, "Merge Sort")
    
# Use matplotlib for static/animated plots
if 'matplotlib' in backends:
    viz = create_visualizer('matplotlib')
    viz.create_comparison_plot(['merge_sort', 'quick_sort'], [10, 50, 100])
```

## Troubleshooting

### Streamlit Dashboard Issues

#### Dashboard Won't Start
```bash
# Ensure Streamlit is installed
pip install streamlit

# Run with explicit Python module
python -m streamlit run algorithm_visualizer/ui/dashboard.py

# Check Streamlit version
streamlit --version

# Clear Streamlit cache if needed
streamlit cache clear

# If you get "externally-managed-environment" error, use virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install streamlit
streamlit run algorithm_visualizer/ui/dashboard.py
```

#### Port Already in Use
```bash
# Run on a different port
streamlit run algorithm_visualizer/ui/dashboard.py --server.port 8502

# Find and kill process using port 8501
lsof -ti:8501 | xargs kill -9
```

#### Performance Issues
- **Large datasets**: Use sample sizes < 500 for interactive visualization
- **Slow rendering**: Disable real-time visualization for large sorts
- **Memory usage**: Clear browser cache and restart Streamlit
- **Animation lag**: Reduce animation speed or disable step-by-step view

#### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari (latest versions)
- **Issues with**: Internet Explorer, older browser versions
- **Mobile**: Basic functionality works, desktop recommended for full experience

### General Issues

#### Missing Dependencies
```bash
# Install all optional dependencies
pip install ".[all]"

# Install specific visualization backend
pip install matplotlib plotly streamlit pandas numpy
```

#### Import Errors
```python
# Check package installation
import algorithm_visualizer
print(algorithm_visualizer.__version__)

# Verify backend availability
from algorithm_visualizer.visualizers import get_available_backends
print(get_available_backends())
```

#### Performance Problems
- Use smaller datasets for real-time visualization (< 100 elements)
- Disable animations for large sorts
- Use text-based visualization for very large datasets
- Consider the O(n²) nature of some algorithms with large inputs

## Educational Use

This package is designed for educational purposes:

- **Computer Science Courses**: Demonstrate algorithm behavior and complexity
- **Coding Interviews**: Practice and understand common sorting algorithms
- **Research**: Compare algorithm performance on different data types
- **Self-Learning**: Interactive exploration of algorithm concepts

## Dependencies

### Required
- Python 3.8+
- Standard library only for core functionality

### Optional
- `matplotlib` >= 3.5.0 for static/animated visualizations
- `plotly` >= 5.0.0 for interactive web plots
- `streamlit` >= 1.0.0 for web dashboard
- `pandas` >= 1.3.0 for data analysis features
- `numpy` >= 1.20.0 for enhanced numerical operations

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

- Issues: GitHub Issues
- Documentation: Project Wiki
- Examples: See `examples/` directory

---

**Note**: This package prioritizes educational value and code clarity over raw performance. For production sorting needs, use Python's built-in `sorted()` function.
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd py-test

# Install required dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from algorithm_visualizer_core import AlgorithmComparator, TextVisualizer
from sorting_visualizers import MergeSortVisualizer, QuickSortVisualizer

# Create sample data
data = [64, 34, 25, 12, 22, 11, 90]

# Initialize comparator
comparator = AlgorithmComparator(data)

# Add algorithms to compare
merge_viz = comparator.add_algorithm(MergeSortVisualizer)
quick_viz = comparator.add_algorithm(QuickSortVisualizer)

# Display comparison results
comparator.print_comparison_table()

# Show detailed steps for one algorithm
text_viz = TextVisualizer()
for step in merge_viz.steps[:5]:  # Show first 5 steps
    text_viz.print_step(step)
```

### 3. Interactive Demo

```bash
python demo.py
```

### 4. Web Dashboard (if Streamlit is installed)

```bash
streamlit run dashboard.py
```

## 📊 Usage Examples

### Example 1: Algorithm Comparison

```python
from algorithm_visualizer_core import AlgorithmComparator
from sorting_visualizers import AVAILABLE_VISUALIZERS
from reader import read_numbers

# Load data from file
data = read_numbers("numbers10.txt")

# Compare all available algorithms
comparator = AlgorithmComparator(data)

for name, visualizer_class in AVAILABLE_VISUALIZERS.items():
    comparator.add_algorithm(visualizer_class, name)

# Get detailed comparison report
report = comparator.get_comparison_report()
print(f"Best algorithm by time: {report['rankings']['execution_time'][0]}")
```

### Example 2: Step-by-Step Analysis

```python
from sorting_visualizers import MergeSortVisualizer
from algorithm_visualizer_core import TextVisualizer

# Create visualizer
data = [3, 1, 4, 1, 5, 9, 2, 6]
visualizer = MergeSortVisualizer(data=data)

# Run algorithm
sorted_data = visualizer.sort()

# Analyze steps
text_viz = TextVisualizer()
print(f"Total steps: {len(visualizer.steps)}")
print(f"Comparisons: {visualizer.metrics.comparisons}")
print(f"Algorithm info: {visualizer.get_algorithm_info()}")

# Show specific step
text_viz.print_step(visualizer.steps[5])
```

### Example 3: Performance Benchmarking

```python
import time
from algorithm_visualizer_core import AlgorithmComparator
from sorting_visualizers import MergeSortVisualizer, QuickSortVisualizer

# Test different data sizes
sizes = [10, 50, 100, 500]
results = {}

for size in sizes:
    data = list(range(size, 0, -1))  # Worst case: reverse sorted
    
    comparator = AlgorithmComparator(data)
    merge_viz = comparator.add_algorithm(MergeSortVisualizer)
    quick_viz = comparator.add_algorithm(QuickSortVisualizer)
    
    results[size] = {
        'merge_sort': merge_viz.metrics.execution_time,
        'quick_sort': quick_viz.metrics.execution_time
    }

# Analyze scaling behavior
for size, timings in results.items():
    print(f"Size {size}: Merge={timings['merge_sort']:.4f}s, Quick={timings['quick_sort']:.4f}s")
```

### Example 4: Custom Data Patterns

```python
import random
from sorting_visualizers import SelectionSortVisualizer

# Test different data patterns
patterns = {
    'random': [random.randint(1, 100) for _ in range(20)],
    'sorted': list(range(1, 21)),
    'reverse': list(range(20, 0, -1)),
    'nearly_sorted': list(range(1, 21))
}

# Mess up nearly sorted
patterns['nearly_sorted'][5], patterns['nearly_sorted'][15] = patterns['nearly_sorted'][15], patterns['nearly_sorted'][5]

for pattern_name, data in patterns.items():
    visualizer = SelectionSortVisualizer(data=data)
    result = visualizer.sort()
    
    print(f"{pattern_name}: {visualizer.metrics.comparisons} comparisons, "
          f"{visualizer.metrics.execution_time:.4f}s")
```

### Example 5: Export and Analysis

```python
from algorithm_visualizer_core import export_metrics, import_metrics
from sorting_visualizers import QuickSortVisualizer

# Run algorithm
data = [random.randint(1, 100) for _ in range(30)]
visualizer = QuickSortVisualizer(data=data)
result = visualizer.sort()

# Export detailed metrics
export_metrics(visualizer, "quick_sort_analysis.json")

# Later, import and analyze
imported_data = import_metrics("quick_sort_analysis.json")
print(f"Algorithm: {imported_data['summary']['algorithm']}")
print(f"Total steps: {len(imported_data['steps'])}")

# Analyze step patterns
step_types = {}
for step in imported_data['steps']:
    desc = step['description'].split(':')[0]
    step_types[desc] = step_types.get(desc, 0) + 1

print("Step distribution:", step_types)
```

## 🔧 Advanced Features

### Adding New Algorithms

To add a new sorting algorithm:

1. **Create a new visualizer class**:

```python
from algorithm_visualizer_core import AlgorithmVisualizer

class BubbleSortVisualizer(AlgorithmVisualizer):
    def sort(self):
        arr = self.current_data.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                self.record_comparison(j, j + 1)
                self.add_step(f"Comparing {arr[j]} and {arr[j+1]}", 
                             arr, comparison_indices=[j, j+1])
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.record_swap(j, j + 1)
                    self.add_step(f"Swapped {arr[j+1]} and {arr[j]}", 
                                 arr, swapped_indices=[j, j+1])
        
        return arr
    
    def get_algorithm_info(self):
        return {
            'time_complexity': 'O(n²)',
            'space_complexity': 'O(1)',
            'stability': 'Stable',
            'description': 'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order'
        }
```

2. **Register the new algorithm**:

```python
from sorting_visualizers import AVAILABLE_VISUALIZERS
AVAILABLE_VISUALIZERS['bubble_sort'] = BubbleSortVisualizer
```

### Custom Metrics

Add custom performance metrics:

```python
class CustomMergeSortVisualizer(MergeSortVisualizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recursion_depth = 0
        self.max_recursion_depth = 0
    
    def _merge_sort_recursive(self, arr, left, right):
        self.recursion_depth += 1
        self.max_recursion_depth = max(self.max_recursion_depth, self.recursion_depth)
        
        result = super()._merge_sort_recursive(arr, left, right)
        
        self.recursion_depth -= 1
        return result
    
    def get_performance_summary(self):
        summary = super().get_performance_summary()
        summary['max_recursion_depth'] = self.max_recursion_depth
        return summary
```

### Custom Visualization

Create custom visualization backends:

```python
class CustomTextVisualizer(TextVisualizer):
    def print_step(self, step, width=100):
        # Custom visualization logic
        print(f"🔢 Step {step.step_number}: {step.description}")
        
        # ASCII bar chart
        max_val = max(step.array_state) if step.array_state else 1
        for i, val in enumerate(step.array_state):
            bar_length = int((val / max_val) * 20)
            symbol = self._get_symbol(i, step)
            bar = symbol * bar_length
            print(f"{i:2d}: {bar} ({val})")
```

## 📋 Dependencies

### Required
- Python 3.7+
- Standard library modules (json, time, collections, abc, dataclasses)

### Optional (for enhanced features)
- **matplotlib**: Static and animated visualizations
- **numpy**: Enhanced mathematical operations
- **streamlit**: Web dashboard interface
- **plotly**: Interactive web visualizations
- **pandas**: Data analysis and export

Install optional dependencies:
```bash
pip install matplotlib numpy streamlit plotly pandas
```

## 🎯 Performance Considerations

### Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Stability |
|-----------|----------------|------------------|-----------|
| Merge Sort | O(n log n) | O(n) | Stable |
| Quick Sort | O(n²) worst, O(n log n) avg | O(log n) | Unstable |
| Selection Sort | O(n²) | O(1) | Unstable |
| Priority Queue Sort | O(n log n) | O(n) | Depends |

### Visualization Overhead

- **Step tracking** adds ~10-20% overhead to algorithm execution
- **Text visualization** is lightweight and suitable for large datasets
- **Matplotlib visualization** may be memory-intensive for large step counts
- **Web dashboard** recommended for datasets under 100 elements for responsiveness

### Memory Usage

- Each step stores a copy of the array state
- For large datasets, consider:
  - Limiting step recording frequency
  - Using delta compression for step storage
  - Streaming visualization instead of storing all steps

## 🔬 Educational Use Cases

### Algorithm Teaching
- **Step-by-step breakdown** helps students understand algorithm logic
- **Visual comparison** demonstrates efficiency differences
- **Performance metrics** illustrate Big O complexity in practice

### Research Applications
- **Algorithm behavior analysis** under different data patterns
- **Performance profiling** for optimization research
- **Comparative studies** across multiple implementations

### Development and Debugging
- **Algorithm verification** through step validation
- **Performance regression testing** with metrics tracking
- **Optimization impact measurement** before/after comparisons

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```python
ImportError: No module named 'matplotlib'
```
Solution: Install optional dependencies or use text-only mode.

**2. Memory Issues with Large Datasets**
```python
MemoryError: Unable to allocate array
```
Solution: Reduce dataset size or disable step recording for large data.

**3. Performance Issues**
```python
# For large datasets, disable detailed step tracking
visualizer = MergeSortVisualizer(data=large_data)
visualizer.step_counter = float('inf')  # Disable step recording
result = visualizer.sort()
```

**4. File Loading Errors**
```python
FileNotFoundError: [Errno 2] No such file or directory: 'numbers10.txt'
```
Solution: Ensure data files are in the current working directory.

### Debug Mode

Enable verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed algorithm execution information
```

## 🤝 Contributing

### Adding New Algorithms
1. Extend `AlgorithmVisualizer` base class
2. Implement `sort()` and `get_algorithm_info()` methods
3. Add appropriate `add_step()` calls for visualization
4. Register in `AVAILABLE_VISUALIZERS` dictionary
5. Add tests and documentation

### Reporting Issues
- Include Python version and OS
- Provide minimal reproducing example
- Include error messages and stack traces

### Feature Requests
- Describe the use case and benefit
- Provide implementation suggestions if possible
- Consider backward compatibility

## 📄 License

This project is designed for educational and research purposes. Feel free to use and modify according to your needs.

## 🙏 Acknowledgments

- Built on top of existing sorting algorithm implementations
- Inspired by algorithm visualization tools like VisuAlgo and Algorithm Visualizer
- Thanks to the Python community for excellent libraries (matplotlib, streamlit, plotly)

---

**Created by:** Senior Data Visualization Developer  
**Version:** 1.0.0  
**Last Updated:** September 2025