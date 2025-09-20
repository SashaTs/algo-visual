"""Matplotlib-based visualization backend."""

from typing import List, Optional, Tuple, TYPE_CHECKING

# Optional matplotlib imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    plt = None
    animation = None
    MATPLOTLIB_AVAILABLE = False

# Type hints only during type checking
if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from matplotlib.animation import FuncAnimation

from ..core.base import AlgorithmStep, Number


class MatplotlibVisualizer:
    """Matplotlib-based visualizer for sorting algorithms."""
    
    def __init__(self, width: int = 12, height: int = 6):
        """Initialize the matplotlib visualizer.
        
        Args:
            width: Figure width in inches
            height: Figure height in inches
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is not available. Install with: pip install matplotlib")
        
        self.width = width
        self.height = height
        self.fig = None
        self.ax = None
        
    def visualize_steps(self, steps: List[AlgorithmStep], data: List[Number], 
                       title: str = "Algorithm Visualization") -> None:
        """Create static visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the visualization
        """
        if not steps:
            print("No steps to visualize")
            return
            
        # Create figure with subplots
        if not MATPLOTLIB_AVAILABLE or plt is None:
            print(f"Cannot create plots: matplotlib not available")
            return
            
        num_steps = min(len(steps), 6)  # Limit to 6 steps for readability
        cols = 3
        rows = (num_steps + cols - 1) // cols
        
        self.fig, axes = plt.subplots(rows, cols, figsize=(self.width, self.height))
        if rows == 1:
            axes = [axes] if cols == 1 else axes
        else:
            axes = axes.flatten()
            
        self.fig.suptitle(title, fontsize=16)
        
        # Show key steps
        step_indices = self._select_key_steps(steps, num_steps)
        
        for i, step_idx in enumerate(step_indices):
            ax = axes[i] if len(axes) > 1 else axes
            step = steps[step_idx]
            
            self._plot_array_state(ax, step.array_state, step.highlighted_indices,
                                 f"Step {step_idx + 1}: {step.description}")
        
        # Hide unused subplots
        for i in range(len(step_indices), len(axes)):
            axes[i].set_visible(False)
            
        if plt is not None:
            plt.tight_layout()
            plt.show()
    
    def create_animation(self, steps: List[AlgorithmStep], interval: int = 500):
        """Create an animated visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps to animate
            interval: Time between frames in milliseconds
            
        Returns:
            Animation object if matplotlib is available, None otherwise
        """
        if not MATPLOTLIB_AVAILABLE or not steps or plt is None or animation is None:
            return None
            
        self.fig, self.ax = plt.subplots(figsize=(self.width, self.height))
        
        def animate(frame):
            if self.ax is not None:
                self.ax.clear()
                step = steps[frame]
                artists = self._draw_enhanced_array_state(self.ax, step.array_state, step, 
                                             f"Step {step.step_number}: {step.description}")
                return artists if artists else []
            return []
        
        anim = animation.FuncAnimation(
            self.fig, animate, frames=len(steps), 
            interval=interval, repeat=True, blit=False
        )
        
        if plt is not None:
            plt.tight_layout()
            plt.show()
        return anim

    def _draw_enhanced_array_state(self, ax, array_state, step, title):
        """Draw array state with enhanced visual effects."""
        if not MATPLOTLIB_AVAILABLE or ax is None:
            return []
            
        positions = range(len(array_state))
        colors = []
        
        # Color mapping for enhanced visualization
        color_map = {
            'default': '#64B5F6',
            'comparing': '#FFB74D', 
            'swapping': '#E57373',
            'sorted': '#81C784',
            'pivot': '#BA68C8',
            'highlight': '#FFD54F'
        }
        
        for i, value in enumerate(array_state):
            color = color_map['default']
            
            if i in step.comparison_indices:
                color = color_map['comparing']
            elif i in step.swapped_indices:
                color = color_map['swapping'] 
            elif i == step.pivot_index:
                color = color_map['pivot']
            elif i in step.highlighted_indices:
                color = color_map['highlight']
                
            colors.append(color)
        
        # Create bars with enhanced styling
        bars = ax.bar(positions, array_state, color=colors, alpha=0.8, 
                     edgecolor='white', linewidth=1)
        
        # Add value labels on bars
        text_artists = []
        for i, (bar, value) in enumerate(zip(bars, array_state)):
            height = bar.get_height()
            text = ax.text(bar.get_x() + bar.get_width()/2., height + max(array_state) * 0.01,
                          f'{value}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            text_artists.append(text)
        
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        ax.set_xlabel('Index', fontsize=10)
        ax.set_ylabel('Value', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, max(array_state) * 1.1 if array_state else 1)
        
        # Return all artist objects for animation
        return list(bars) + text_artists
    
    def plot_performance_comparison(self, algorithms: List[str], 
                                  times: List[float], comparisons: List[int],
                                  title: str = "Performance Comparison") -> None:
        """Create performance comparison charts.
        
        Args:
            algorithms: List of algorithm names
            times: Execution times for each algorithm
            comparisons: Number of comparisons for each algorithm
            title: Title for the charts
        """
        if not MATPLOTLIB_AVAILABLE or plt is None:
            print(f"Cannot create charts: matplotlib not available")
            return
            
        self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.width, self.height))
        self.fig.suptitle(title, fontsize=16)
        
        # Execution time chart
        bars1 = ax1.bar(algorithms, times, color='skyblue')
        ax1.set_title('Execution Time')
        ax1.set_ylabel('Time (seconds)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{height:.4f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Comparisons chart
        bars2 = ax2.bar(algorithms, comparisons, color='lightcoral')
        ax2.set_title('Number of Comparisons')
        ax2.set_ylabel('Comparisons')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def _plot_array_state(self, ax, array_state: List[Number], 
                         highlighted_indices: List[int], title: str) -> None:
        """Plot the current state of the array.
        
        Args:
            ax: Matplotlib axis
            array_state: Current array state
            highlighted_indices: Indices to highlight
            title: Title for the plot
        """
        positions = range(len(array_state))
        colors = ['red' if i in highlighted_indices else 'lightblue' 
                 for i in positions]
        
        bars = ax.bar(positions, array_state, color=colors)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, array_state)):
            height = bar.get_height()
            ax.annotate(f'{value}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    def _select_key_steps(self, steps: List[AlgorithmStep], num_steps: int) -> List[int]:
        """Select key steps to display from all steps.
        
        Args:
            steps: All algorithm steps
            num_steps: Number of steps to select
            
        Returns:
            List of step indices to display
        """
        if len(steps) <= num_steps:
            return list(range(len(steps)))
        
        # Always include first and last steps
        if num_steps < 2:
            return [0]
        
        indices = [0]
        
        # Select evenly spaced steps in between
        if num_steps > 2:
            step_size = (len(steps) - 2) / (num_steps - 2)
            for i in range(1, num_steps - 1):
                idx = int(1 + (i - 1) * step_size)
                indices.append(idx)
        
        # Always include the last step
        indices.append(len(steps) - 1)
        
        return indices