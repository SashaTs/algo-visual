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
                       title: str = "Algorithm Visualization") -> Optional['Figure']:
        """Create static visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the visualization
            
        Returns:
            matplotlib Figure object for Streamlit display, or None if error
        """
        if not steps:
            print("No steps to visualize")
            return None
            
        # Create figure with subplots
        if not MATPLOTLIB_AVAILABLE or plt is None:
            print(f"Cannot create plots: matplotlib not available")
            return None
        
        # Show all steps up to 100, then truncate
        total_steps = len(steps)
        max_steps = 100
        is_truncated = total_steps > max_steps
        
        if is_truncated:
            # Show first 100 steps
            steps_to_show = steps[:max_steps]
            step_indices = list(range(max_steps))
            num_steps = max_steps
        else:
            # Show all steps
            steps_to_show = steps
            step_indices = list(range(total_steps))
            num_steps = total_steps
        
        # Calculate optimal grid layout
        cols = min(4, num_steps)  # Max 4 columns
        rows = (num_steps + cols - 1) // cols
        
        # Adjust figure size based on number of steps
        fig_width = max(self.width, cols * 3)
        fig_height = max(self.height, rows * 2.5)
        
        self.fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
            
        # Create title with truncation info
        title_text = f"{title} - {num_steps} of {total_steps} steps"
        if is_truncated:
            title_text += " (truncated - showing first 100)"
        
        self.fig.suptitle(title_text, fontsize=16)
        
        for i, step_idx in enumerate(step_indices):
            if i < len(axes):  # Safety check
                ax = axes[i] if len(axes) > 1 else axes[0]
                step = steps_to_show[step_idx]
                
                self._plot_array_state(ax, step.array_state, step.highlighted_indices,
                                     f"Step {step_idx + 1}: {step.description[:50]}{'...' if len(step.description) > 50 else ''}")
        
        # Hide unused subplots
        for i in range(len(step_indices), len(axes)):
            axes[i].set_visible(False)
            
        # Only use tight_layout for smaller numbers of subplots to avoid performance issues
        if plt is not None and num_steps <= 50:
            plt.tight_layout()
        
        return self.fig
    
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
                                  title: str = "Performance Comparison") -> Optional['Figure']:
        """Create performance comparison charts showing all algorithms on the same chart.
        
        Args:
            algorithms: List of algorithm names
            times: Execution times for each algorithm
            comparisons: Number of comparisons for each algorithm
            title: Title for the charts
            
        Returns:
            matplotlib Figure object for Streamlit display, or None if error
        """
        if not MATPLOTLIB_AVAILABLE or plt is None:
            print(f"Cannot create charts: matplotlib not available")
            return None
            
        # Create figure with single subplot and dual y-axes
        self.fig, ax1 = plt.subplots(figsize=(self.width, self.height))
        self.fig.suptitle(title, fontsize=16)
        
        # Create second y-axis
        ax2 = ax1.twinx()
        
        # Set up bar positions
        x_pos = range(len(algorithms))
        width = 0.35
        
        # Execution time bars (left y-axis)
        bars1 = ax1.bar([x - width/2 for x in x_pos], times, width, 
                       label='Execution Time (s)', color='skyblue', alpha=0.8)
        
        # Comparisons bars (right y-axis)
        bars2 = ax2.bar([x + width/2 for x in x_pos], comparisons, width,
                       label='Comparisons', color='lightcoral', alpha=0.8)
        
        # Configure left y-axis (execution time)
        ax1.set_xlabel('Algorithms', fontsize=12)
        ax1.set_ylabel('Execution Time (seconds)', color='steelblue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='steelblue')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(algorithms, rotation=45, ha='right')
        
        # Configure right y-axis (comparisons)
        ax2.set_ylabel('Number of Comparisons', color='darkred', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='darkred')
        
        # Add value labels on bars
        for bar, time in zip(bars1, times):
            height = bar.get_height()
            ax1.annotate(f'{time:.4f}s',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, color='steelblue')
        
        for bar, comp in zip(bars2, comparisons):
            height = bar.get_height()
            ax2.annotate(f'{int(comp)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, color='darkred')
        
        # Add legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        # Add grid for better readability
        ax1.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.fig
    
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
        
        # For better distribution, use more sophisticated selection
        if num_steps > 2:
            # Distribute remaining steps evenly across the timeline
            remaining_slots = num_steps - 2  # Excluding first and last
            step_size = (len(steps) - 2) / remaining_slots
            
            for i in range(remaining_slots):
                idx = int(1 + i * step_size)
                # Avoid duplicates
                if idx not in indices and idx < len(steps) - 1:
                    indices.append(idx)
        
        # Always include the last step
        if len(steps) - 1 not in indices:
            indices.append(len(steps) - 1)
        
        return sorted(indices)
    
    def plot_performance_analysis(self, df) -> Optional['Figure']:
        """Create unified performance analysis charts.
        
        Args:
            df: DataFrame with performance analysis results
            
        Returns:
            Matplotlib figure or None if creation fails
        """
        if not MATPLOTLIB_AVAILABLE or plt is None:
            return None
            
        try:
            import pandas as pd
            
            # Create figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Performance Analysis - All Algorithms', fontsize=16, fontweight='bold')
            
            # 1. Execution Time by Data Size
            pivot_time = df.pivot_table(values='Execution Time', index='Data Size', columns='Algorithm')
            for algorithm in pivot_time.columns:
                ax1.plot(pivot_time.index, pivot_time[algorithm], marker='o', label=algorithm)
            ax1.set_xlabel('Data Size')
            ax1.set_ylabel('Execution Time (s)')
            ax1.set_title('Execution Time by Data Size')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. Comparisons by Data Size
            pivot_comparisons = df.pivot_table(values='Comparisons', index='Data Size', columns='Algorithm')
            for algorithm in pivot_comparisons.columns:
                ax2.plot(pivot_comparisons.index, pivot_comparisons[algorithm], marker='s', label=algorithm)
            ax2.set_xlabel('Data Size')
            ax2.set_ylabel('Number of Comparisons')
            ax2.set_title('Comparisons by Data Size')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 3. Swaps by Data Size
            pivot_swaps = df.pivot_table(values='Swaps', index='Data Size', columns='Algorithm')
            for algorithm in pivot_swaps.columns:
                ax3.plot(pivot_swaps.index, pivot_swaps[algorithm], marker='^', label=algorithm)
            ax3.set_xlabel('Data Size')
            ax3.set_ylabel('Number of Swaps')
            ax3.set_title('Swaps by Data Size')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # 4. Performance by Data Type (average across all sizes)
            avg_by_type = df.groupby(['Algorithm', 'Data Type'])['Execution Time'].mean().unstack()
            avg_by_type.plot(kind='bar', ax=ax4)
            ax4.set_xlabel('Algorithm')
            ax4.set_ylabel('Average Execution Time (s)')
            ax4.set_title('Performance by Data Type')
            ax4.legend(title='Data Type')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating performance analysis charts: {e}")
            return None