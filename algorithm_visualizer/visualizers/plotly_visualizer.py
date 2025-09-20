"""Plotly-based visualization backend."""

from typing import List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from ..core.base import AlgorithmStep, Number


class PlotlyVisualizer:
    """Plotly-based visualizer for sorting algorithms."""
    
    def __init__(self, width: int = 800, height: int = 600):
        """Initialize the plotly visualizer.
        
        Args:
            width: Figure width in pixels
            height: Figure height in pixels
        """
        self.width = width
        self.height = height
        
    def visualize_steps(self, steps: List[AlgorithmStep], data: List[Number], 
                       title: str = "Algorithm Visualization") -> Optional[go.Figure]:
        """Create static visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the visualization
            
        Returns:
            Plotly Figure object for Streamlit display, or None if error
        """
        if not steps:
            print("No steps to visualize")
            return None
        
        # Detect algorithm type and use specialized visualization if needed
        algorithm_type = self._detect_algorithm_type(steps, title)
        
        if algorithm_type == 'binary_search':
            return self._visualize_binary_search(steps, data, title)
        elif algorithm_type == 'breadth_first_search':
            return self._visualize_bfs(steps, data, title)
        else:
            # Use standard array-based visualization for sorting algorithms
            return self._visualize_sorting_algorithm(steps, data, title)
    
    def _detect_algorithm_type(self, steps: List[AlgorithmStep], title: str) -> str:
        """Detect the algorithm type from steps and title."""
        title_lower = title.lower()
        
        if 'binary search' in title_lower or any('binary search' in step.description.lower() for step in steps):
            return 'binary_search'
        elif 'bfs' in title_lower or 'breadth' in title_lower or any('bfs' in step.description.lower() for step in steps):
            return 'breadth_first_search'
        else:
            return 'sorting'
    
    def _visualize_binary_search(self, steps: List[AlgorithmStep], data: List[Number], title: str) -> Optional[go.Figure]:
        """Create specialized visualization for binary search."""
        try:
            from .specialized_visualizers import BinarySearchVisualizer
            visualizer = BinarySearchVisualizer()
            return visualizer.create_plotly_visualization(steps, data, title)
        except ImportError as e:
            print(f"Could not import specialized visualizer: {e}")
            return self._visualize_sorting_algorithm(steps, data, title)
    
    def _visualize_bfs(self, steps: List[AlgorithmStep], data: List[Number], title: str) -> Optional[go.Figure]:
        """Create specialized visualization for BFS."""
        try:
            from .specialized_visualizers import BFSGraphVisualizer
            visualizer = BFSGraphVisualizer()
            return visualizer.create_plotly_visualization(steps, data, title)
        except ImportError as e:
            print(f"Could not import specialized visualizer: {e}")
            return self._visualize_sorting_algorithm(steps, data, title)
    
    def _visualize_sorting_algorithm(self, steps: List[AlgorithmStep], data: List[Number], title: str) -> Optional[go.Figure]:
        """Create standard array-based visualization for sorting algorithms."""
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
        
        # Adjust spacing based on number of rows to prevent plotly errors
        if rows > 10:
            vertical_spacing = max(0.02, 1.0 / (rows * 2))  # Smaller spacing for many rows
            horizontal_spacing = 0.02
        else:
            vertical_spacing = 0.08
            horizontal_spacing = 0.05
        
        # Create subplots
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"Step {i+1}: {steps_to_show[i].description[:40]}{'...' if len(steps_to_show[i].description) > 40 else ''}" 
                          for i in step_indices],
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing
        )
        
        for idx, step_idx in enumerate(step_indices):
            row = idx // cols + 1
            col = idx % cols + 1
            step = steps_to_show[step_idx]
            
            # Create bar chart for this step
            colors = ['red' if i in step.highlighted_indices else 'lightblue' 
                     for i in range(len(step.array_state))]
            
            fig.add_trace(
                go.Bar(
                    x=list(range(len(step.array_state))),
                    y=step.array_state,
                    marker_color=colors,
                    showlegend=False,
                    text=step.array_state,
                    textposition='outside'
                ),
                row=row, col=col
            )
        
        # Create title with truncation info
        title_text = f"{title} - {num_steps} of {total_steps} steps"
        if is_truncated:
            title_text += " (truncated - showing first 100)"
        
        fig.update_layout(
            title=title_text,
            height=max(self.height, rows * 200),  # Adjust height based on rows
            width=max(self.width, cols * 200),    # Adjust width based on columns
            showlegend=False
        )
        
        return fig
    
    def animate_algorithm(self, steps: List[AlgorithmStep], data: List[Number],
                         title: str = "Algorithm Animation") -> None:
        """Create animated visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the animation
        """
        if not steps:
            print("No steps to animate")
            return
            
        # Create frames for animation
        frames = []
        for i, step in enumerate(steps):
            colors = ['red' if j in step.highlighted_indices else 'lightblue' 
                     for j in range(len(step.array_state))]
            
            frame = go.Frame(
                data=[go.Bar(
                    x=list(range(len(step.array_state))),
                    y=step.array_state,
                    marker_color=colors,
                    text=step.array_state,
                    textposition='outside'
                )],
                name=f"Step {i+1}",
                layout=go.Layout(
                    title=f"Step {i+1}: {step.description}"
                )
            )
            frames.append(frame)
        
        # Create initial figure
        initial_step = steps[0]
        colors = ['red' if i in initial_step.highlighted_indices else 'lightblue' 
                 for i in range(len(initial_step.array_state))]
        
        fig = go.Figure(
            data=[go.Bar(
                x=list(range(len(initial_step.array_state))),
                y=initial_step.array_state,
                marker_color=colors,
                text=initial_step.array_state,
                textposition='outside'
            )],
            frames=frames
        )
        
        # Add animation controls
        fig.update_layout(
            title=title,
            width=self.width,
            height=self.height,
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 1000, "redraw": True},
                                      "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Step:",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f"Step {i+1}"],
                               {"frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300}}],
                        "label": f"Step {i+1}",
                        "method": "animate"
                    }
                    for i in range(len(steps))
                ]
            }]
        )
        
        fig.show()
    
    def plot_performance_comparison(self, algorithms: List[str], 
                                  times: List[float], comparisons: List[int],
                                  title: str = "Performance Comparison") -> go.Figure:
        """Create performance comparison charts showing all algorithms on the same chart.
        
        Args:
            algorithms: List of algorithm names
            times: Execution times for each algorithm
            comparisons: Number of comparisons for each algorithm
            title: Title for the charts
            
        Returns:
            Plotly Figure object for Streamlit display
        """
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add execution time bars (primary y-axis)
        fig.add_trace(
            go.Bar(
                x=algorithms,
                y=times,
                name="Execution Time (s)",
                marker_color='skyblue',
                text=[f'{t:.4f}s' for t in times],
                textposition='outside',
                yaxis='y',
                offsetgroup=1
            ),
            secondary_y=False,
        )
        
        # Add comparisons bars (secondary y-axis)
        fig.add_trace(
            go.Bar(
                x=algorithms,
                y=comparisons,
                name="Comparisons",
                marker_color='lightcoral',
                text=[str(c) for c in comparisons],
                textposition='outside',
                yaxis='y2',
                offsetgroup=2
            ),
            secondary_y=True,
        )
        
        # Set x-axis title
        fig.update_xaxes(title_text="Algorithms")
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Execution Time (seconds)", title_font_color="steelblue", secondary_y=False)
        fig.update_yaxes(title_text="Number of Comparisons", title_font_color="darkred", secondary_y=True)
        
        # Update layout
        fig.update_layout(
            title=title,
            height=self.height,
            width=self.width,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            barmode='group'
        )
        
        return fig
    
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
    
    def plot_performance_analysis(self, df) -> Optional[go.Figure]:
        """Create unified performance analysis charts.
        
        Args:
            df: DataFrame with performance analysis results
            
        Returns:
            Plotly Figure object for Streamlit display, or None if error
        """
        try:
            import pandas as pd
            
            # Create subplots with 2x2 layout
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Execution Time by Data Size',
                    'Comparisons by Data Size', 
                    'Swaps by Data Size',
                    'Performance by Data Type'
                ),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Define colors for algorithms
            colors = px.colors.qualitative.Set1
            
            # 1. Execution Time by Data Size
            pivot_time = df.pivot_table(values='Execution Time', index='Data Size', columns='Algorithm')
            for i, algorithm in enumerate(pivot_time.columns):
                fig.add_trace(
                    go.Scatter(
                        x=pivot_time.index,
                        y=pivot_time[algorithm],
                        mode='lines+markers',
                        name=f'{algorithm} (Time)',
                        line=dict(color=colors[i % len(colors)]),
                        marker=dict(symbol='circle'),
                        showlegend=(i == 0)  # Only show legend for first algorithm group
                    ),
                    row=1, col=1
                )
            
            # 2. Comparisons by Data Size
            pivot_comparisons = df.pivot_table(values='Comparisons', index='Data Size', columns='Algorithm')
            for i, algorithm in enumerate(pivot_comparisons.columns):
                fig.add_trace(
                    go.Scatter(
                        x=pivot_comparisons.index,
                        y=pivot_comparisons[algorithm],
                        mode='lines+markers',
                        name=f'{algorithm} (Comparisons)',
                        line=dict(color=colors[i % len(colors)]),
                        marker=dict(symbol='square'),
                        showlegend=False
                    ),
                    row=1, col=2
                )
            
            # 3. Swaps by Data Size
            pivot_swaps = df.pivot_table(values='Swaps', index='Data Size', columns='Algorithm')
            for i, algorithm in enumerate(pivot_swaps.columns):
                fig.add_trace(
                    go.Scatter(
                        x=pivot_swaps.index,
                        y=pivot_swaps[algorithm],
                        mode='lines+markers',
                        name=f'{algorithm} (Swaps)',
                        line=dict(color=colors[i % len(colors)]),
                        marker=dict(symbol='triangle-up'),
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            # 4. Performance by Data Type (average across all sizes)
            avg_by_type = df.groupby(['Algorithm', 'Data Type'])['Execution Time'].mean().unstack()
            
            # Create grouped bar chart for data types
            for i, data_type in enumerate(avg_by_type.columns):
                fig.add_trace(
                    go.Bar(
                        x=avg_by_type.index,
                        y=avg_by_type[data_type],
                        name=data_type,
                        showlegend=True
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title_text="Performance Analysis - All Algorithms",
                title_font_size=16,
                height=800,
                showlegend=True
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Data Size", row=1, col=1)
            fig.update_yaxes(title_text="Execution Time (s)", row=1, col=1)
            
            fig.update_xaxes(title_text="Data Size", row=1, col=2)
            fig.update_yaxes(title_text="Comparisons", row=1, col=2)
            
            fig.update_xaxes(title_text="Data Size", row=2, col=1)
            fig.update_yaxes(title_text="Swaps", row=2, col=1)
            
            fig.update_xaxes(title_text="Algorithm", row=2, col=2)
            fig.update_yaxes(title_text="Avg Execution Time (s)", row=2, col=2)
            
            return fig
            
        except Exception as e:
            print(f"Error creating performance analysis charts: {e}")
            return None